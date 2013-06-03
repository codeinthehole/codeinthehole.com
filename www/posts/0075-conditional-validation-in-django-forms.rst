=================================
Conditional logic in Django forms
=================================
--------------------------------------------
Radio buttons can be tamed :: django, python
--------------------------------------------

The problem
-----------

It's common for UX professionals to design forms like the following:

.. image:: /static/images/screenshots/radio-form-wire.png
    :class: screenshot

where radio buttons are employed to split the form into sections, each of which
can have it's own fields which are only mandatory if the parent radio button
is checked.  Thus the validation logic is conditional on the submitted form
data.

Such requirements are slightly tricky to capture in Django as they tread
slightly outside the normal path of form validation.  Specifically:

* It's not documented how to render radio buttons separately.  The default
  behaviour is to render an unordered list.  The `guidance on fine-grained
  template control`_ only covers looping over the choices.

* It's not obvious how to change the validation properties of a form field
  dynamically, depending on the submitted data.

.. _`guidance on fine-grained template control`: https://docs.djangoproject.com/en/dev/ref/forms/widgets/#radioselect

A solution
----------

Start with this form class:

.. sourcecode:: python

    from django import forms

    class ScheduleForm(forms.Form):
        NOW, LATER = 'now', 'later'
        SCHEDULE_CHOICES = (
            (NOW, 'Send immediately'),
            (LATER, 'Send later'),
        )
        schedule = forms.ChoiceField(
            choices=SCHEDULE_CHOICES, widget=forms.RadioSelect)
        send_date = forms.DateTimeField(
            label="", required=False)

Note the ``send_date`` field has ``required=False`` as it is only mandatory
if the 'Send later' radio button is selected.  For simplicity, we are are only using a single
datetime field for the send date rather than the split-widget field of the wire.

We can render this as follows:

.. sourcecode:: html

    <form action="." method='post'>
        {% csrf_token %}
        {{ form.non_field_errors }}

        <h3>Send schedule</h3>
        {{ form.schedule.errors }}

        <div class="span4">
            {{ form.schedule.0 }}<br/>
            <span class="help-text">(Once you've checked out)</span>
        </div>

        <div class="span4">
            {{ form.schedule.1 }}<br/>
            {{ form.send_date }}
            {{ form.send_date.errors }}
        </div>

        <button type="submit">Save</button>
    </form>

Observe that:

* the radio buttons are rendered individually individually by referring to
  the index of each option (this works in Django 1.4+).

* we don't render the errors for the ``schedule`` next to one particular
  radio button, but above the container elements.

Next we add conditional validation to the form class:

.. sourcecode:: python

    from django import forms

    class ScheduleForm(forms.Form):
        NOW, LATER = 'now', 'later'
        SCHEDULE_CHOICES = (
            (NOW, 'Send immediately'),
            (LATER, 'Send later'),
        )
        schedule = forms.ChoiceField(
            choices=SCHEDULE_CHOICES, widget=forms.RadioSelect)
        send_date = forms.DateTimeField(
            label="", required=False)

        def __init__(self, data=None, *args, **kwargs):
            super(ScheduleForm, self).__init__(data, *args, **kwargs)
            
            # If 'later' is chosen, set send_date as required
            if data and data.get('schedule', None) == self.LATER:
                self.fields['send_date'].required = True

Here, we override ``__init__`` and inspect the raw submitted data so that we
can set ``required=True`` on the ``send_date`` field appropriately.  This is
the conventional way of adding conditional logic to form validation, although
it's more commmon to use an additional argument to ``__init__`` to determine the
field adjustments.

Discussion
----------

This solution is not perfect.  It's a little odd to use the raw form data to
change validation rules.  However, I'm not aware of a cleaner alternative.

Related links:

* `Advanced Django Form Usage`_ - A decent overview of various issues around forms from DjangoCon 2011.
  
.. _`Advanced Django Form Usage`: http://www.slideshare.net/pydanny/advanced-django-forms-usage
