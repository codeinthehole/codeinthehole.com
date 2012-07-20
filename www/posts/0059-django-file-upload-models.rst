======================
Use models for uploads
======================
----------------------------------------------------
Using models for audit and clarity :: django, python
----------------------------------------------------

All Django developers will deal with file uploads at some point.  I contend
that it's a good practice to use models to capture the upload metadata and to
track processing status.  This article explains how and why.

An e-commerce example
=====================

Suppose your e-commerce application allows admins to upload CSV files to update
product stock levels (a common requirement).  A typical file may
comprise a SKU and a stock level::

    9781231231999,0
    9781231231999,4
    9781231231999,2
    ...

`Django's docs`_ detail a common pattern for dealing with file uploads such as
this.  The steps are generally:

1.  Validate the form submission;
2.  Write upload data to permanent storage;
3.  Process the file;
4.  Delete the file (optional)

For example:

.. _`Django's docs`: https://docs.djangoproject.com/en/dev/topics/http/file-uploads/?from=olddocs

.. sourcecode:: python

    def handle_upload(request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'])
                return HttpResponseRedirect('/success/url/')
        else:
            form = UploadFileForm()
        return render_to_response('upload.html', {'form': form})

    def handle_uploaded_file(f):
        filepath = '/tmp/somefile.txt'
        with open(filepath, 'wb+') as dest:
            for chunk in f.chunks:
                dest.write(chunk)
        process_file(filepath)

    def process_file(filepath):
        ...

This works fine.  

However, it's often desirable to collect audit information
about which files have been processed, how long processing took and who uploaded
them.  Of course, this can be addressed by logging but a more elegant solution
to use a simple audit model as well.  Consider an alternative implementation of
``handle_uploaded_file``:

.. sourcecode:: python

    def handle_uploaded_file(user, f):
        filepath = '/tmp/somefile.txt'
        with open(filepath, 'wb+') as dest:
            for chunk in f.chunks:
                dest.write(chunk)
        upload = StockUpload.objects.create(
            filepath=filepath,
            uploaded_by=user
        )
        upload.process()

where we're now passing the logged-in user too.

The model definition for ``StockUpload`` may look like:

.. sourcecode:: python

    import datetime
    from django.db import models

    class StockUpload(models.Model):
        filepath = models.CharField(max_length=255)
        
        # Upload audit information
        uploaded_by = model.ForeignKey('auth.User')
        date_uploaded = model.DateTimeField(auto_now_add=True)

        # Processing audit information
        PENDING, PROCESSED, FAILED = 'Pending', 'Processed', 'Failed'
        STATUSES = (
            (PENDING, _(PENDING)),
            (PROCESSED, _(PROCESSED)),
            (FAILED, _(FAILED)),
        )
        status = model.CharField(max_length=64, choices=STATUSES, default=PENDING)
        processing_description = model.TextField(blank=True, null=True)
        num_records = models.PositiveIntegerField()
        date_start_processing = models.DateTimeField(null=True)
        date_end_processing = models.DateTimeField(null=True)

        def process(self):
            self.date_start_processing = datetime.datetime.now()
            try:
                # process upload data, 
                ...
            except Exception, e:
                self._mark_failed(unicode(e))
            else:
                self._mark_processed(num_records)

        def _mark_processed(self, num_records, description=None):
            self.status = self.PROCESSED
            self.date_end_processing = datetime.datetime.now()
            self.num_records = num_records
            self.processing_description = description
            self.save()

        def _mark_failed(self, description):
            self.status = self.FAILED
            self.processing_description = description
            self.save()

        @property
        def filename(self):
            return os.path.basename(self.filename)

        def was_processing_successful(self):
            return self.status == self.PROCESSED

You can go further and push the file creation into a manager method so the
filepath generation is removed from the view:

.. sourcecode:: python

    def handle_uploaded_file(f):
        upload = StockUpload.objects.create_from_stream(user, f)
        upload.process()

where ``create_from_stream`` could be implemented as:

.. sourcecode:: python

    class StockUploadManager(models.Manager):

        def create_from_stream(self, user, f):
            filepath = self.generate_filename()
            with open(filepath, 'wb+') as dest:
                for chunk in f.chunks:
                    dest.write(chunk)
            return self.create(
                filepath=filepath,
                uploaded_by=user
            )

and, if processing takes a while, push the work into Celery:

.. sourcecode:: python

    @task()
    def process_upload(upload_id):
        upload = StockUpload.objects.get(id=upload_id)
        upload.process()

    def handle_uploaded_file(user, f):
        upload = StockUpload.create_from_stream(user, f)
        process_upload.delay(upload.id)

Here's a more complete implementation that uses a library of mine,
`django-async-messages`_, to send a message back to the user who uploaded the file:

.. _`django-async-messages`: https://github.com/codeinthehole/django-async-messages/

.. sourcecode:: python

    # tasks.py

    @task()
    def process_upload(upload_id):
        upload = StockUpload.objects.get(id=upload_id)
        upload.process()
        if upload.was_processing_successful():
            message_user(
                upload.uploaded_by, 
                "Your upload %s was processed successfully, %d records imported" % (
                    upload.filename,
                    upload.num_records))
        else:
            message_user(
                upload.uploaded_by, 
                "Your upload %s could not be processed, error message: %s" % (
                    upload.filename,
                    upload.processing_description,))

    # views.py

    def handle_upload(request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                upload = StockUpload.create_from_stream(request.user, 
                                                        request.FILES['file'])
                process_upload.delay(upload.id)
                return HttpResponseRedirect('/success/url/')
        else:
            form = UploadFileForm()
        return render_to_response('upload.html', {'form': form})


Discussion
==========

The advantages of using a model are:

* It keeps your view simple - all processing logic is extracted away.

* The file processing logic is re-usable.  You could use a management command to 
  process files specified at the commandline.

* It's easy to defer processing to a Celery worker.

* You can gather metrics on processing speed and keep audit information on who
  is uploading what.

* You can write a simple ``ListView`` to show the audit information of uploaded
  files to admins.  

The above is just a toy example - there are lots of variations that can be used.
For instance, you may not want to keep the processing logic on the model itself,
it may make sense to have a separate function for this.  However the general
notion of using a model to represent an uploaded file and to track its state is
a useful one.
