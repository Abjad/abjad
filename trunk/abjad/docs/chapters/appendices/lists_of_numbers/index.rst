Working with lists of numbers
-----------------------------

Python provides a built-in ``list`` class that you can use to carry
around almost anything. The examples here show how to create a list of
numbers and then do things with the numbers in the list.

Create a list with square brackets. ::

    abjad> my_list = [23, 7, 10, 18, 13, 20, 3, 2, 18, 9, 14, 3]
    abjad> my_list
    [23, 7, 10, 18, 13, 20, 3, 2, 18, 9, 14, 3]

Use ``len()`` to find the number of elements in any list. ::

    abjad> len(my_list)
    12

Use ``append()`` to add one element to a list. ::

    abjad> my_list.append(5)
    abjad> my_list
    [23, 7, 10, 18, 13, 20, 3, 2, 18, 9, 14, 3, 5]

Use ``extend()`` to extend one list with the contents of another. ::

    abjad> my_other_list = [19, 11, 4, 10, 12]
    abjad> my_list.extend(my_other_list)
    abjad> my_list
    [23, 7, 10, 18, 13, 20, 3, 2, 18, 9, 14, 3, 5, 19, 11, 4, 10, 12]

Use ``reverse()`` to reverse the elements in a list. ::

    abjad> my_list.reverse()
    abjad> my_list
    [12, 10, 4, 11, 19, 5, 3, 14, 9, 18, 2, 3, 20, 13, 18, 10, 7, 23]

You can return a single value from a list with a numeric index. ::

    abjad> my_list[0]
    12
    abjad> my_list[1]
    10
    abjad> my_list[2]
    4

You can return many values from a list with slice notation. ::

    abjad> my_list[:4]
    [12, 10, 4, 11]

More information on these and all other operations defined on the
built-in Python ``list`` is available in the `Python tutorial <http://docs.python.org/tutorial/introduction.html#lists>`__.
