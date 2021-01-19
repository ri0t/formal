Formal User's Manual
====================

Welcome to the Formal Users Manual!
This part of the documentation explains how to work with Formal.


Usage
-----

1) Build your schema

::

        >>> schema = {
            'name': 'Country',
            'id': '#country',
            'properties': {
                'name': {'type': 'string'},
                'abbreviation': {'type': 'string'},
            },
            'additionalProperties': False,
        }

2) Connect to your database

::

        >>> import formal
        >>> formal.connect("test")

3) Create a model

::

        >>> Country = formal.model_factory(schema)

4) Create an object using your model

::

        >>> sweden = Country({"name": 'Sweden', "abbreviation": 'SE'})
        >>> sweden.save()
        >>> sweden._id
        ObjectId('50b506916ee7d81d42ca2190')

5) Let the object validate itself!

::

        >>> sweden = Country.find_one({"name" : "Sweden"})
        >>> sweden.name = 5
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "formal/model.py", line 254, in __setattr__
            self.validate_field(attr, self._schema["properties"][attr], value)
          File "formal/model.py", line 189, in validate_field
            self.validate_simple(key, value_schema, value)
          File "formal/model.py", line 236, in validate_simple
            (key, value_type, str(value), type(value)))
        formal.exceptions.ValidationError: Field 'name' is of type 'string', received '5' (<type 'int'>)

        >>> sweden.overlord = 'Bears'
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "formal/model.py", line 257, in __setattr__
            raise ValidationError("Additional property '%s' not allowed!" % attr)
        formal.exceptions.ValidationError: Additional property 'overlord' not allowed!

.. note:: Notice the use of find_one, which is a standard pymongo operation
          passed through. You can use this as described in
          the `PyMongo documentation <https://api.mongodb.com/python/current/>`_

6) You can also update objects from dictionaries:

::

        >>> sweden.update({"name": "Sverige"})
        >>> sweden.save()

7) To get them to a browser or other similar things, serialize them:

::

        >>> sweden.serializablefields()
        {'_id': '50b506916ee7d81d42ca2190', 'name': 'Sverige', 'abbreviation': 'SE', 'id': '#country'}

Choosing a collection
---------------------

.. note:: By default Formal will use the pluralized version of the model's name.

If you want to use something else, put it in the JSON-schema:

::

        {
            "name": "MyModel",
            ...
            "collectionName": "some_collection",
            ...
        }

Multiple Databases
------------------

To use multiple databases, simply call ``connect()`` multiple times:

::

        >>> import formal
        >>> formal.connect("test")
        >>> formal.connect("other_db")

.. note:: By default all models will use the first database specified.

If you want to use a different one, put it in the JSON-schema:

::

        {
            "name": "MyModel",
            ...
            "databaseName": "other_db",
            ...
        }


.. toctree::
    :maxdepth: 2

