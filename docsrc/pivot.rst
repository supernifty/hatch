.. _pivot:

pivot
=====

Reshape data from `narrow format <https://en.wikipedia.org/wiki/Wide_and_narrow_data#Narrow>`_ to `wide format <https://en.wikipedia.org/wiki/Wide_and_narrow_data#Wide>`_.

Sometimes wide format is called *stacked* and narrow format is called *unstacked* or *long*.

For example here is a small table in *narrow format* representing working hours for two employees on each weekday, where employees are also associated with a level:

.. code-block:: text

   person,feature,val
   Alice,level,A1
   Bob,level,B3
   Alice,mon,8
   Bob,mon,0
   Alice,tue,8
   Bob,tue,0
   Alice,wed,4
   Bob,wed,4
   Alice,thu,1
   Bob,thu,6
   Alice,fri,4
   Bob,fri,0

And here is the same data in *wide format*: 

.. code-block:: text

   person,level,mon,tue,wed,thu,fri
   Alice,A1,8,8,4,1,4
   Bob,B3,0,0,4,6,0

In this particular example the ``person`` column has been used as an index for the output rows, and the values in the ``feature`` 
column have been unstacked into column headings, with values from the ``val`` column populating the rows. 

An alternative wide representation of the same dataset is shown below, where the ``feature`` column
has been used as an index of the output rows, and the values in the ``person`` column have been
unstacked into new column headings. As before the values from the ``val`` column populate the rows.

.. code-block:: text

   feature,Alice,Bob
   fri,4,0
   level,A1,B3
   mon,8,0
   thu,1,6
   tue,8,0
   wed,4,4

Usage
-----

.. code-block:: text

   gurita pivot [-h] -c COLUMN [COLUMN ...] -i COLUMN [COLUMN ...]
                [-v COLUMN [COLUMN ...]] [-f FUNCTION [FUNCTION ...]] 

Arguments
---------

.. list-table::
   :widths: 25 20 10
   :header-rows: 1
   :class: tight-table

   * - Argument
     - Description
     - Reference
   * - * ``-h``
       * ``--help``
     - display help for this command
     - :ref:`help <pivot_help>`
   * - * ``-i COLUMN [COLUMN...]``
       * ``--index COLUMN [COLUMN...]``
     - use these columns as the index (required) 
     - :ref:`index columns <pivot_index_columns>`
   * - * ``-c COLUMN [COLUMN ...]``
       * ``--cols COLUMN [COLUMN ...]``
     - unstack these columns (required)
     - :ref:`pivot columns <pivot_columns>`
   * - * ``-v COLUMN [COLUMN...]``
       * ``--vals COLUMN [COLUMN...]``
     - populate the rows from these columns 
     - :ref:`value columns <pivot_value_columns>`
   * - * ``-f FUNCTION [FUNCTION ...]``
       * ``--fun FUNCTION [FUNCTION ...]``
     - Aggregation function 
     - :ref:`aggregating function <pivot_fun>`

See also
--------

* :doc:`melt <melt/>` is the inverse of ``pivot``.
* :doc:`groupby <groupby/>` also provides a way to aggregate rows based on a key.

.. _pivot_help:

Getting help
------------

The full set of command line arguments for ``pivot`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita pivot -h

Example
-------

Suppose the following data is stored in a file called ``example.csv``:

.. code-block:: text

   person,feature,val
   Alice,level,A1
   Bob,level,B3
   Alice,mon,8
   Bob,mon,0
   Alice,tue,8
   Bob,tue,0
   Alice,wed,4
   Bob,wed,4
   Alice,thu,1
   Bob,thu,6
   Alice,fri,4
   Bob,fri,0


This is an example of data in "narrow format" (or "unstacked" or "long").

The ``pivot`` command can convert the data into "wide format", as demonstrated in the following example:

.. code-block:: text

    gurita pivot -i person -c feature -v val < example.csv

The output of the above command is as follows:

.. code-block:: text

   person,fri,level,mon,thu,tue,wed
   Alice,4,A1,8,1,8,4
   Bob,0,B3,0,6,0,4

In this example the ``person`` column is used as the index of the output data; it acts like a key for the new rows. There are two distinct values for ``person`` (``Alice`` and ``Bob``), so there are two rows in the output data.

The remaining new columns in the output data are derived from the values in the ``feature`` column (``fri``, ``level``, ``mon``, ``thu``, ``tue``, ``wed``). You'll note that the new columns have been generated in an arbitrary order, however, 
usually this is not important because the order of the columns in the data rarely matters.

The values in the corresponding rows are determined from the ``val`` column. For instance, in the original data set, given ``Alice`` as a key, ``level`` is associated uniqely with the value ``A1``. Therefore, in the output data, the row for ``Alice`` in the ``level`` column contains ``A1``. 

As an alternative example, we could pivot the data in a different way, by using the ``feature`` column as the index, and unstacking the ``person`` column:

.. code-block:: text

    gurita pivot -i feature -c person -v val < example.csv

The output of the above command is as follows:

.. code-block:: text

    feature,Alice,Bob
    fri,4,0
    level,A1,B3
    mon,8,0
    thu,1,6
    tue,8,0
    wed,4,4

In this example there are six values in the ``feature`` column, so there are correspondingly six rows in the output. Also, the two unique values in the ``person`` column have been unstacked into two new columns in the output. 

These two examples show that ``pivot`` provides a mechanism to structure and view the same dataset in multiple ways.

The inverse of ``pivot`` is ``melt``. For example the following commands show how to invert the 
pivoted data in wide format back to an equivalent of the input long format:

.. code-block:: text

    gurita pivot -i person -c feature -v val + melt -i person -v mon tue wed thu fri level --varname feature --valname val < example.csv

The output of the above command is as follows:

.. code-block:: text

    person,feature,val
    Alice,mon,8
    Bob,mon,0
    Alice,tue,8
    Bob,tue,0
    Alice,wed,4
    Bob,wed,4
    Alice,thu,1
    Bob,thu,6
    Alice,fri,4
    Bob,fri,0
    Alice,level,A1
    Bob,level,B3

.. code-block:: text

   gurita pivot -i feature -c person -v val + melt -i feature -v Alice Bob --varname person --valname val < example.csv

The output of the above command is as follows:

.. code-block:: text

   feature,person,val
   fri,Alice,4
   level,Alice,A1
   mon,Alice,8
   thu,Alice,1
   tue,Alice,8
   wed,Alice,4
   fri,Bob,0
   level,Bob,B3
   mon,Bob,0
   thu,Bob,6
   tue,Bob,0
   wed,Bob,4

Note that in both examples using ``pivot`` followed by ``melt`` the output data is not in 
*exactly* the same order as the origial input data. Some of the rows and columns have been 
reordered. However, the data is semantically equivalent to the original data because row and column
ordering does not normally matter. Regardless of structure, the data represents the same information.

.. _pivot_missing_data:

Missing data 
------------

Consider the following modified version of the data set from above, where the row ``Alice,level,A1`` has been removed. In this new dataset ``Bob`` has an associated ``level`` by ``Alice`` does not.

.. code-block:: text

   person,feature,val
   Bob,level,B3
   Alice,mon,8
   Bob,mon,0
   Alice,tue,8
   Bob,tue,0
   Alice,wed,4
   Bob,wed,4
   Alice,thu,1
   Bob,thu,6
   Alice,fri,4
   Bob,fri,0

We can pivot the data as before with the following command:

.. code-block:: text

    gurita pivot -i person -c feature -v val < example.csv

The output of the above command is as follows:

.. code-block:: text

   person,fri,level,mon,thu,tue,wed
   Alice,4,,8,1,8,4
   Bob,0,B3,0,6,0,4

The ``level`` column exists, as before, in the output. This is because ``level`` appears in the input ``feature`` column.

Even though ``level`` is only defined for ``Bob``, all output rows must have this column. Since ``level`` is not defined for ``Alice`` in the input data, the only
reasonable thing to do is make this cell empty in the output. 

There are many other ways that the dataset could have a missing ``level`` value for ``Alice``.
For example, the data could contain the following row:

.. code-block:: text

   Alice,level,

In all such cases the output of the ``pivot`` command would be the same thing, to account for
the missing ``level`` associated with ``Alice``. Similarly for other missing data.

Missing data can be removed from the dataset using the :doc:`dropna <dropna>` command.

.. _pivot_index_columns:

Specifying columns to act as an index 
-------------------------------------

.. code-block:: text

    -i COLUMN [COLUMN ...]
    --index COLUMN [COLUMN ...]

When unstacking a dataset the ``pivot`` command groups data together into output rows 
using an *index* (or a key), computed from one or more input columns. This is a required
argument.

Suppose we have the following dataset in long format stored in a file called ``example.csv``:

.. code-block:: text

    person,level,variable,value
    Alice,A1,sun,0
    Bob,B3,sun,4
    Wei,B1,sun,0
    Imani,A2,sun,0
    Diego,C2,sun,3
    Alice,A1,mon,8
    Bob,B3,mon,0
    Wei,B1,mon,0
    Imani,A2,mon,8
    Diego,C2,mon,7
    Alice,A1,tue,8
    Bob,B3,tue,0
    Wei,B1,tue,8
    Imani,A2,tue,8
    Diego,C2,tue,7

One way to convert the data into wide format is to group data into output rows based on an index from the ``person`` and ``level`` columns, with the ``variable`` column unstacked into new output columns, and the output rows populated by the ``value`` column:

.. code-block:: text

    gurita pivot -i person level -c variable -v value < example.csv

The output of the above command is as follows:

.. code-block:: text

    person,level,mon,sun,tue
    Alice,A1,8,0,8
    Bob,B3,0,4,0
    Diego,C2,7,3,7
    Imani,A2,8,0,8
    Wei,B1,0,0,8

In this case we can see that the output rows are indexed by a key formed from the ``person`` and ``level`` input columns. For instance all entries for ``Alice`` and ``A1`` are grouped together.

In a more contrived example, we could form an index from the ``level`` and ``variable`` input columns and unstack the ``person`` column, like so:

.. code-block:: text

    gurita pivot -i level variable -c person -v value < example.csv

The output of the above command is shown below:

.. code-block:: text

    level,variable,Alice,Bob,Diego,Imani,Wei
    A1,mon,8.0,,,,
    A1,sun,0.0,,,,
    A1,tue,8.0,,,,
    A2,mon,,,,8.0,
    A2,sun,,,,0.0,
    A2,tue,,,,8.0,
    B1,mon,,,,,0.0
    B1,sun,,,,,0.0
    B1,tue,,,,,8.0
    B3,mon,,0.0,,,
    B3,sun,,4.0,,,
    B3,tue,,0.0,,,
    C2,mon,,,7.0,,
    C2,sun,,,3.0,,
    C2,tue,,,7.0,,

.. _pivot_columns:

Specifying columns to pivot
---------------------------

.. _pivot_value_columns:

Specifying columns to pivot
---------------------------

.. code-block:: text

    -v COLUMN [COLUMN ...]
    --vals COLUMN [COLUMN ...]

.. _pivot_fun:

Aggregating multiple values
---------------------------

Suppose ``Alice`` has *two* values associated with ``level`` (``B2`` and ``A1``), where previously
there was only one:

.. code-block:: text

    person,feature,val
    Alice,level,B2
    Alice,level,A1
    Bob,level,B3
    Alice,mon,8
    Bob,mon,0
    Alice,tue,8
    Bob,tue,0
    Alice,wed,4
    Bob,wed,4
    Alice,thu,1
    Bob,thu,6
    Alice,fri,4
    Bob,fri,0

We can try to pivot the data as before:

.. code-block:: text

    gurita pivot -i person -c feature -v val < example.csv

However, this generates an error:

.. code-block:: text

    gurita ERROR: Error: Index contains duplicate entries, cannot reshape; exiting

The problem is that the output data must have a single cell corresponding to the ``level`` associated with ``Alice``. However, in this data set there are *two* ``level`` values for ``Alice``, and ``pivot`` 
does not know how to resolve this multiplicity.

This situation can be resolved by specifying an :ref:`aggregating function <pivot_fun>` to map multiple values into a single result.

For example, we could use ``-f sample`` to pick a random value from the collection of possibilities:

.. code-block:: text

    gurita pivot -i person -c feature -v val -f sample < example.csv

The output of the above command is as follows:

.. code-block:: text

    person,fri,level,mon,thu,tue,wed
    Alice,4,A1,8,1,8,4
    Bob,0,B3,0,6,0,4

Note that the output may differ each time the command is run because it chooses a ``level`` value for ``Alice`` at random.

The behaviour of the aggregating function for ``pivot`` is similar to that of the :doc:`groupby <groupby>` command.

Allowed aggregation functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following aggregating functions can be used with ``-f/--fun``:

* sample (randomly choose one of the possible values)
* size (size of the group)
* sum
* mean
* mad (mean absolute deviation)
* median
* min
* max
* prod
* std (standard deviation)
* var (variance)
* sem (standard error of the mean)
* skew
* quantile (50% quantile)
