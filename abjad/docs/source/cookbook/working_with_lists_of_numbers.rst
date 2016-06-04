Working with lists of numbers
=============================

Python provides a built-in ``list`` type that you can use to carry around
almost anything.

Creating lists
--------------

Create a list with square brackets:

::

    >>> my_list = [23, 7, 10, 18, 13, 20, 3, 2, 18, 9, 14, 3]
    >>> my_list
    [23, 7, 10, 18, 13, 20, 3, 2, 18, 9, 14, 3]


Inspecting list attributes
--------------------------

Use ``len()`` to find the number of elements in any list

::

    >>> len(my_list)
    12


Adding and removing elements
----------------------------

Use ``append()`` to add one element to a list:

::

    >>> my_list.append(5)
    >>> my_list
    [23, 7, 10, 18, 13, 20, 3, 2, 18, 9, 14, 3, 5]

Use ``extend()`` to extend one list with the contents of another:

::

    >>> my_other_list = [19, 11, 4, 10, 12]
    >>> my_list.extend(my_other_list)
    >>> my_list
    [23, 7, 10, 18, 13, 20, 3, 2, 18, 9, 14, 3, 5, 19, 11, 4, 10, 12]


Indexing and slicing lists
--------------------------

You can return a single value from a list with a numeric index:

::

    >>> my_list[0]
    12
    >>> my_list[1]
    10
    >>> my_list[2]
    4

You can return many values from a list with slice notation:

::

    >>> my_list[:4]
    [12, 10, 4, 11]


Reversing the order of elements
-------------------------------

Use ``reverse()`` to reverse the elements in a list:

::

    >>> my_list.reverse()
    >>> my_list
    [12, 10, 4, 11, 19, 5, 3, 14, 9, 18, 2, 3, 20, 13, 18, 10, 7, 23]

More information on these and all other operations defined on the built-in
Python ``list`` is available in the `Python tutorial
<http://docs.python.org/tutorial/introduction.html#lists>`__.
