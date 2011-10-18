=============================
Inspecting Javascript objects
=============================
------------------------------------------
Simple introspection methods :: javascript
------------------------------------------

Learning Ruby or Python from the command-line prompt is greatly enhanced by the
built-in inspection methods these languages provide. These allow the methods
and properties of an object to be interrogated via a simple method call which
returns an array of all property or method names.

For instance, in IRB (the interactive Ruby command-line) we can interrogate the
integer object:

.. sourcecode:: ruby

    irb(main):001:0>my_int = 1
    irb(main):002:0>my_int.methods

This returns an array of all method names for integer objects:

.. sourcecode:: ruby

    ["%", "odd?", "inspect", "prec_i", "<<", "tap", "div", "&", "clone", ">>", "public_methods", "_send_", "object_id", "instance_variable_defined?", "equal?", "freeze", "to_sym", "*", "ord", "+", "extend", "next", "send", "round", "methods", "prec_f", "-", "even?", "singleton_method_added", "divmod", "hash", "/", "integer?", "downto", "dup", "to_enum", "instance_variables", "|", "eql?", "size", "instance_eval", "truncate", "~", "id", "to_i", "singleton_methods", "modulo", "taint", "zero?", "times", "instance_variable_get", "frozen?", "enum_for", "display", "instance_of?", "^", "method", "to_a", "+@", "-@", "quo", "instance_exec", "type", "**", "upto", "to_f", "<", "step", "protected_methods", "<=>", "between?", "==", "remainder", ">", "===", "to_int", "nonzero?", "pred", "instance_variable_set", "coerce", "respond_to?", "kind_of?", "floor", "succ", ">=", "prec", "to_s", "<=", "fdiv", "class", "private_methods", "=~", "tainted?", "_id_", "abs", "untaint", "nil?", "chr", "id2name", "is_a?", "ceil", "[]"]

Meanwhile, in Python we use the build-in function ``dir()``:

.. sourcecode:: python

    >>> my_dict = {}
    >>> dir(my_dict)

to get a list of attributes (including methods) for a dictionary variable:

.. sourcecode:: python

    ['_class_', '_cmp_', '_contains_', '_delattr_', '_delitem_', '_doc_', '_eq_', '_ge_', '_getattribute_', '_getitem_', '_gt_', '_hash_', '_init_', '_iter_', '_le_', '_len_', '_lt_', '_ne_', '_new_', '_reduce_', '_reduce_ex_', '_repr_', '_setattr_', '_setitem_', '_str_', 'clear', 'copy', 'fromkeys', 'get', 'has_key', 'items', 'iteritems', 'iterkeys', 'itervalues', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']

Javascript doesn't provide such a feature as standard but it's straightforward
to implement a simple inspection object:

.. sourcecode:: javascript

    var Inspect = {
        TYPE_FUNCTION: 'function',
        // Returns an array of (the names of) all methods
        methods: function(obj) {
            var testObj = obj || self;
            var methods = [];
            for (prop in testObj) {
                if (typeof testObj[prop] == Inspect.TYPE_FUNCTION && typeof Inspect[prop] != Inspect.TYPE_FUNCTION) {
                    methods.push(prop);
                }
            }
            return methods;
        },
        // Returns an array of (the names of) all properties
        properties: function(obj) {
            var testObj = obj || self;
            var properties = [];
            for (prop in testObj) {
                if (typeof testObj[prop] != Inspect.TYPE_FUNCTION && typeof Inspect[prop] != Inspect.TYPE_FUNCTION) {
                    properties.push(prop);
                }
            }
            return properties;
        }
    }

Now we can simply pass in any object (or call without an argument to test the
window object) to retrieve an array or properties or methods. For example,
working at the Firebug console, we can examine the hash object of the Prototype
Javascript library, and the native ``document.location`` object:

.. image:: /static/images/screenshots/firebug-screenshot.jpg

Moreover, it can sometimes be useful to have a debug mode for an application
where these methods are added to the supertype "object" which provides the
prototype for all others. In this instance, debug mode is switched on by added
a 'debug_mode' parameter to the GET parameters. For convenience, I'm also using
the methodize function provided by Prototype:

.. sourcecode:: javascript

    if (/[?&]debug_mode(&.*)?$/.test(document.location.search)) {
        Object.prototype.properties = Inspect.properties.methodize();
        Object.prototype.methods = Inspect.methods.methodize();
    }

Then you can inspect an object without refering to the Inspect object
(namespace really):

.. sourcecode:: javascript

    var my_hash = new Hash();
    my_hash.methods();
    my_hash.properties()

Code and associated JSunit test suite available at `my github repo`_.

.. _`my github repo`: http://github.com/codeinthehole/js-nuggets/

Further reading: `Ruby Tip - Cleaner Object Inspection - YodaYid's WackyWorld`_

.. _`Ruby Tip - Cleaner Object Inspection - YodaYid's WackyWorld`: http://yodayid.blogspot.com/2007/05/ruby-tip-cleaner-object-inspection.html
