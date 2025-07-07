:orphan:

..  todo:: Include under discussion of score structure.

Parentage
=========

Many score objects contain other score objects:

::

    >>> string = r"\tuplet 3/2 { c'4 d' e' } \tuplet 3/2 { c'4 d' e' }"
    >>> staff = abjad.Staff(string)
    >>> score = abjad.Score([staff])
    >>> abjad.show(score)

Abjad uses the idea of parentage to model the way objects contain each other:

::

    >>> note = abjad.get.leaf(score, 0)
    >>> parentage = abjad.get.parentage(note)
    >>> parentage

Use parentage to find the immediate parent of a component:

::

    >>> parentage.parent

Or the root of the score in the which the component resides:

::

    >>> parentage.root

Or to find the depth at which the component is embedded in its score:

::

    >>> parentage.count(abjad.Tuplet)
