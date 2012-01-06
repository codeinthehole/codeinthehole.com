==================================================
Javascript cookie objects using Prototype and JSON
==================================================
--------------------------------------------------------------------
Simple class-based wrapper to using cookies :: javascript, prototype
--------------------------------------------------------------------

It's sometime useful to interact with cookies directly on the client-side using
javascript. This can be useful for a variety of situations, such as persisting
display settings between page requests without storing anything on the server.
I've also used them to display a simple welcome message to new visitors. It can
make your controller code simpler if this kind of simple display logic is
contained entirely on the client side.

To this end, I use the following simple Cookies object, build on top of the
Prototype Javascript library (version > 1.5):

.. sourcecode:: javascript

    var Cookies = Class.create({
        initialize: function(path, domain) {
            this.path = path || '/';
            this.domain = domain || null;
        },
        // Sets a cookie
        set: function(key, value, days) {
            if (typeof key != 'string') {
                throw "Invalid key";
            }
            if (typeof value != 'string' && typeof value != 'number') {
                throw "Invalid value";
            }
            if (days && typeof days != 'number') {
                throw "Invalid expiration time";
            }
            var setValue = key+'='+escape(new String(value));
            if (days) {
                var date = new Date();
                date.setTime(date.getTime()+(days*24*60*60*1000));
                var setExpiration = "; expires="+date.toGMTString();
            } else var setExpiration = "";
            var setPath = '; path='+escape(this.path);
            var setDomain = (this.domain) ? '; domain='+escape(this.domain) : '';
            var cookieString = setValue+setExpiration+setPath+setDomain;
            document.cookie = cookieString;
        },
        // Returns a cookie value or false
        get: function(key) {
            var keyEquals = key+"=";
            var value = false;
            document.cookie.split(';').invoke('strip').each(function(s){
                if (s.startsWith(keyEquals)) {
                    value = unescape(s.substring(keyEquals.length, s.length));
                    throw $break;
                }
            });
            return value;
        },
        // Clears a cookie
        clear: function(key) {
            this.set(key,'',-1);
        },
        // Clears all cookies
        clearAll: function() {
            document.cookie.split(';').collect(function(s){
                return s.split('=').first().strip();
            }).each(function(key){
                this.clear(key);
            }.bind(this));
        }
    });

The API is simple: cookie objects are created with optional path and domain
arguments to the constructor. The set(), get() and clear() methods are then
used to define the name=value pairs that cookies comprise. In addition, the
get() method takes an optional third parameter for setting the expiry time in
days if you want the data persisted longer than the current session.

Cookies can now be interacted with in the following manner:

.. sourcecode:: javascript

    var biscuits = new Cookies();
    biscuits.set('show_nav', 'yes');
    if (biscuits.get('show_nav') {
        // Show the navigation...
    }

The above object is useful for storing simple string data, but we can easily
extend the above to allow arrays and objects to be persisted in the cookie by
using JSON.

.. sourcecode:: javascript

    var JsonCookies = Class.create(Cookies, {});
    JsonCookies.addMethods({
        // Overridden set method to JSON-encode value
        set: function($super, key, value, days) {
            switch (typeof value) {
                case 'undefined':
                case 'function':
                case 'unknown': 
                    throw "Invalid value type";
                    break;
                case 'boolean': 
                case 'string': 
                case 'number': 
                    value = String(value.toString());
                break;
            }
            $super(key, Object.toJSON(value), days);
        },
        // Overriden get method to JSON-decode the value
        get: function($super, key) {
            var value = $super(key);
            return (value) ? value.evalJSON() : false;
        }
    });

As we're overriding the set and get methods, the API remains the same:

.. sourcecode:: javascript

    // Persist some array data
    var hobnobs = new JsonCookies();
    hobnobs.set('selectedIds', [12,46,32], 7)

    // On a different request, use the data
    var hobnobs = new JsonCookies();
    var selectedIds = hobnobs.get('selectedIds');
    if (selectedIds) {
    // Do something with the selected ids
    }

As this object does not rely on the DOM in any way, it is easily testable as it
requires little in the way of fixtures. What follows is set of unit tests that
work with the JSUnit testing suite. You can run the unit tests directly, using
the JSUnit test runner.

.. sourcecode:: javascript

    var myKey    = 'hereismykey';
    var myValue  = 'hereismyvalue';
    var myCookies;
    function setUp() {
        myCookies = new Cookies();
        myCookies.set(myKey, myValue);
    }
    function testSet() {
        var cookieString = myKey+'='+myValue;
        assertTrue('Cookies set', document.cookie.indexOf(cookieString) != -1);
    }
    function testGet() {
        assertEquals('Cookies get', myValue, myCookies.get(myKey));
    }
    function testClear() {
        myCookies.clear(myKey);
        assertFalse('Cookies clear', myCookies.get(myKey));
    }
    function testClearAll() {
        var myNewKey   = 'hereismynewkey';
        var myNewValue = 'hereismynewvalue';
        myCookies.set(myNewKey, myNewValue);
        myCookies.clearAll();
        assertFalse('Check cookie has been cleared for myKey', myCookies.get(myKey));
        assertFalse('Check cookie has been cleared for myNewKey', myCookies.get(myNewValue));
    }
    function testArrayInJsonCookies() {
        var testKey   = 'test';
        var testValue = [1,2,3];
        var jar = new JsonCookies();
        jar.set(testKey, testValue);
        var testReturn = jar.get(testKey);
        assertTrue('Check length of array is the same', testValue.length == testReturn.length);
        assertEquals('Checking arrays are the same', $A(testValue).toJSON(), $A(testReturn).toJSON());
    }
    function testObjectInJsonCookies() {
        var testKey   = 'test';
        var testValue = {'name':'barry', 'age': 29};
        var jar = new JsonCookies();
        jar.set(testKey, testValue);
        var testReturn = jar.get(testKey);
        assertTrue('Check length of array is the same', testValue.length == testReturn.length);
        assertEquals('Checking objects are the same', $A(testValue).toJSON(), $A(testReturn).toJSON());
    }

One minor shortcoming of the present version of JSUnit is that it is difficult
to test equality of arrays and objects. The simple work-around used above is to
test equality of their JSON encodings, which acheives the same end without
resorting to looping through comparing property by property.

It should be noted that I am far from the first person to create Javascript
cookie objects in this way - here are a few others doing similar things:

JSON javascript cookies
Cookie Jar: Yummy JSON encoded cookies with Prototype
The main difference is that my objects use an inheritance structure to add the
JSON-encoding facilities and throw errors when invalid arguments are passed.
Also, I have another post in the pipeline which builds on these cookie objects
to do something cool. Watch this space.
