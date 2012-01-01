================================================
A dashboard pattern for Django class-based views
================================================

---------------------------------------------------------------------------------------
A brief discussion of a pattern which enables dashboard pages to be easily constructed.
---------------------------------------------------------------------------------------

A common pattern in django class-based views is to have a `DetailView <http://www.google.com>`_ which also
has a series for very simple forms that are perhaps no more than a button.  An
example might be a page within an order management dashboard that displays
details of the order but also provides buttons to cancel, refund, re-order,
print a shipping note.

I find myself doing this one quite frequently.

.. sourcecode:: python

    class OrderView(DetailView):
        model_class = Order
        context_object_name = 'order'
        permitted_actions = ('cancel_order', 'refund_order')

        def post(self, request, *args, **kwargs):
            if 'action' in request.POST and 'action' in self.permitted_actions:
                order = self.get_object()
                try:
                    return getattr(self, request.POST['action'])(request, order)
                except AttributeError:
                    raise '
            return super()

        def cancel_order(self, order):
            # ...do some stuff
            pass

        def refund_order(self, order):
            # ...do some stuff
            pass
            
            

This handles the situation where
