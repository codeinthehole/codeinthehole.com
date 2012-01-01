======================================================
Domain-model-mapper - A PHP Data Mapper implementation
======================================================
-----------------------------------------------------------------------------------
A lightweight implementation of the Data Mapper for PHP 5.3 :: php, design_patterns
-----------------------------------------------------------------------------------

At various PHP conferences and meetups over the last few weeks, I've seen
attention drawn to the `Data Mapper design pattern`_. This is an elegant pattern
that splits the responsibilities of business logic and persistence. In the
words of pattern supremo Martin Fowler:

.. _`Data Mapper design pattern`: http://martinfowler.com/eaaCatalog/dataMapper.html

    The Data Mapper is a layer of software that separates the in-memory objects
    from the database. Its responsibility is to transfer data between the two and
    also to isolate them from each other. With Data Mapper the in-memory objects
    needn't know even that there's a database present; they need no SQL interface
    code, and certainly no knowledge of the database schema 

This is a cleaner separation of concerns than that found in the ubiquitous
Active Record pattern which, while a useful construct, conflates business logic
with persistence. This can make a big difference in terms of testability as
using a Data Mapper decouples the database from your domain models, making it
easy to write unit tests. This has been something I've found slightly difficult
with Django where the emphasis is more on writing integration tests that use
fixtures to set up the test environmentl; writing unit tests without using a
database is hard when foreign key constraints are involved.

Anyhow, it's a favourite pattern of mine and I've recently pushed to Github a
small library for PHP 5.3 which provides data mapper functionality. The
extended details are in the `README`_ but the essential idea is: Create your
domain models as subclasses of BaseDomainModel. This superclass provides
methods for identifying a model, loading a model with data and implements a set
of magic methods to allow easy access to field values. You can create a
collection object too using ModelCollection as your superclass. This is useful
if you want to implement methods that act on a collection of models, such as
getTotalPrice() or similar. Create a corresponding mapper object as a subclass
of Mapper. This class provides the usual persistence methods such as save(),
insert(), update(), delete() as well as some helper methods to make writing
"finder" methods easier. Sample usage is as follows. First set up your classes
to model your domain.

.. _`README`: https://github.com/codeinthehole/domain-model-mapper

.. sourcecode:: php

    // Create model class
    class Person extends \DMM\BaseDomainModel
    {
        public function __construct()
        {
            // Specify field(s) that identify a model
            parent::__construct('person_id');

            // Optionally specify field names
            $this->__setFieldNames(array('first_name', 'last_name', 'age'));
        }

        public function getName()
        {
            return trim(sprintf("%s %s", $this->first_name, $this->last_name));
        }
    }

    // Create model collection class
    class PersonCollection extends \DMM\ModelCollection
    {
        public function getTotalAge()
        {
            return array_sum($this->pluckField('age'));
        }
    }

    // Create mapper class
    class PersonMapper extends \DMM\Mapper
    {
        private $tableName = 'people';
        private $tablePrimaryKey = 'person_id';

        protected $modelClass = 'Person';
        protected $modelCollectionClass = 'PersonCollection';

        public function __construct(PDO $pdo)
        {
            parent::__construct($pdo, $this->tableName, $this->tablePrimaryKey);
        }

        public function findByAge($age)
        {
            $sql =
                "SELECT * 
                FROM `{$this->tableName}`
                WHERE age = :age";
            $bindings = array(
                'age' => $age
            );
            return $this->fetchCollection($sql, $bindings);
        }
    }

These can then used as follows:

.. sourcecode:: php

    // Create a new model
    $person = new Person;
    $person->first_name = 'Alan';
    $person->last_name = 'Smith';
    $person->age = 56;

    // or
    $otherPerson = new Person;
    $otherPerson->__load(array(
        'first_name' => 'Barry',
        'last_name' => 'Smith',
        'age' => 34
    ));

    $mapper = new PersonMapper($pdo);
    $mapper->save($person);
    echo $person->person_id; // 1

    // Load a collection
    $twentyYearOlds = $mapper->findByAge(20);

Unit testing is now trivial as you can simply instantiate your model and use
the ``__load`` method to populate it with data for testing.

.. sourcecode:: php

    $model = new Person;
    $model->first_name = '  terry';
    $model->last_name = 'jones     ';
    $this->assertSame('terry jones', $model->getName());

Relationships between models are not a feature of the package at the moment.
The best way to handle this is to use a "repository" object which composes
several mappers.

The `code is on github`_ if you are interested.

.. _`code is on github`: https://github.com/codeinthehole/domain-model-mapper
