Parentage
=========

::

    >>> import abjad

Many score objects contain other score objects.

::

    >>> staff = abjad.Staff([
    ...     abjad.Tuplet((2, 3), "c'4 d'4 e'4"),
    ...     abjad.Tuplet((2, 3), "c'4 d'4 e'4"),
    ... ])
    >>> score = abjad.Score([staff])
    >>> abjad.show(score)

Abjad uses the idea of parentage to model the way objects contain each other.


Getting the parentage of a component
------------------------------------

Get the parentage of any component:

::

    >>> note = abjad.get.leaf(score, 0)
    >>> parentage = abjad.get.parentage(note)

::

    >>> parentage

Abjad returns a special type of selection.


Parentage attributes
--------------------

Use parentage to find the immediate parent of a component:

::

    >>> parentage.parent

Or the root of the score in the which the component resides:

::

    >>> parentage.root

Or to find the depth at which the component is embedded in its score:

::

    >>> parentage.count(abjad.Tuplet)
