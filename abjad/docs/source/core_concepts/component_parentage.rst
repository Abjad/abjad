Component parentage
===================

Many score objects contain other score objects.

..  abjad::

    tuplet = Tuplet(Multiplier(2, 3), "c'4 d'4 e'4")
    staff = Staff(2 * tuplet)
    score = Score([staff])
    show(score)

Abjad uses the idea of parentage to model the way objects contain each other.


Getting the parentage of a component
------------------------------------

Use the inspector to get the parentage of any component:

..  abjad::

    note = next(iterate(score).by_leaf())
    parentage = inspect_(note).get_parentage()

..  abjad::

    parentage

Abjad returns a special type of selection.


Parentage attributes
--------------------

Use parentage to find the immediate parent of a component:

..  abjad::

    parentage.parent

Or the root of the score in the which the component resides:

..  abjad::

    parentage.root

Or to find the depth at which the component is embedded in its score:

..  abjad::

    parentage.depth

Or the number of tuplets in which the component is nested:

..  abjad::

    parentage.tuplet_depth
