Component parentage
===================

::

    >>> import abjad

Many score objects contain other score objects.

::

    >>> tuplet = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
    >>> staff = abjad.Staff(2 * tuplet)
    >>> score = abjad.Score([staff])
    >>> show(score)

Abjad uses the idea of parentage to model the way objects contain each other.


Getting the parentage of a component
------------------------------------

Use the inspector to get the parentage of any component:

::

    >>> note = abjad.inspect(score).leaf(0)
    >>> parentage = abjad.inspect(note).parentage()

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
