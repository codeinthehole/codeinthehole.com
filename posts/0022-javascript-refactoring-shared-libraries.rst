=======================================================
Javascript refactoring for customising shared libraries
=======================================================
-------------------------------------------------------------------------------
Structuring a javascript file for repeating use and customisation :: javascript
-------------------------------------------------------------------------------

One difficulty working with a shared in-house framework is it is difficult to
maintain a common javascript file that is valid across multiple applications.
This is currently an issue we face at Tangent, where we run a generic
e-commerce platform which we customise to the needs of each client. Most of
these e-commerce applications have a javascript-rich checkout page whose
functionality differs in small yet significant ways such as the required and
optional fields within a delivery address, or the range of delivery options
available. Ideally, you would have a single javascript file to work for all
these checkouts, but these differences make such a file impracticle due to the
changes in DOM structure and business logic between applications.

For instance, one problem that arose recently was a requirement to remove the
javascript messaging from within certain parts of the checkout for one
appliation. The shared checkout.js file features a method which reloads the
order totals within the page after a new delivery option has been chosen and
displays a message to notify the user:

.. sourcecode:: javascript

    // [checkout.js]
    var shop = {
        checkout: {
            reloadOrderTotals: function() {
                // Do the reloading...
                shop.display.notify("Order totals recalculating...");
            }
    }

Unfortunately, another client required the same functionality to reload the
order totals but without the notification call. One option would have been to
create a local version of the checkout.js file and remove the offending line,
but this would have created a larger maintenance overhead going forward due to
the large amount of duplicate code.

A neater option would have been to dynamically override the
shop.checkout.reloadOrderTotals method in an application-specific file:

.. sourcecode:: javascript

    // [application.js]
    shop.checkout.reloadOrderTotals = function() {
        // Reload order totals but without a notification call
    }

However, again this leads to most of the the body of the
``shop.checkout.reloadOrderTotals`` method being duplicated just to remove one
line.

Instead, drawing inspiration from the excellent Working with Legacy Code by
Michael Flowers, a neater solution is to perform a dynamic-language version of
the Extract method refactoring to isolate the functionality that we wanted to
override into it's own method. Hence, we alter checkout.js to split the
reloading and notification functionality into two methods:

.. sourcecode:: javascript

    // [checkout.js]
    var shop = {
        checkout: {
            reloadOrderTotals: function() {
                // Do the reloading...
                shop.checkout.displayOrderTotalNotification("Order totals recalculating...");
            },
            displayOrderTotalNotification(message) {
                shop.display.notify(message);
            } 
    }

Now in the local project javascript file, we can null out the messaging behaviour:

.. sourcecode:: javascript

    // [application.js]
    shop.checkout.displayOrderTotalNotification = function(){}

This neat trick allows us to customise our core javascript functionality in a
way that does not lead to code duplication. The only thing required to make
this work is to ensure that the shared checkout file is loaded before the
application-specific one.
