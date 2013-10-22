:tocdepth: 2

Version history
===============


Abjad 2.13
----------

Released 2013-10-18. Built from r12,311.
Implements 500 public classes and 526 functions totaling 199,255.

API refactoring
^^^^^^^^^^^^^^^

We're moved half of the API functionality from functions to class methods.
This is true for almost every package in the system.

Introducing ``inspect()``
^^^^^^^^^^^^^^^^^^^^^^^^^

A new top-level ``inspect()`` function is now available when you start Abjad.
Use the function to inspect a large number of derived attributes that
pertain to score components. Example:

::

    >>> tuplet = Tuplet(Multiplier(2, 3), "c'4 d'4 e'4")
    >>> note = tuplet[0]
    >>> note.written_duration
    Duration(1, 4)

    >>> inspect(note).get_duration()
    Duration(1, 6)

Introducing ``select()``
^^^^^^^^^^^^^^^^^^^^^^^^

Slicing now returns a selection. Tie chains are now implemented as selections.
And you may use the newly added ``select()`` function to create selections by
hand.

Introducing  ``mutate()``
^^^^^^^^^^^^^^^^^^^^^^^^^

Abjad now ships with a top-level ``mutate()`` function availble when you start
the system. ``mutate()`` is a factory function that returns an instance of the
new ScoreMutationAgent class when called on any score component. The
ScoreMutationAgent then allows you to make structural changes to the component
or components on which it was called. Here's an example of using ``mutate()``
to split the notes in a staff:

::

    >>> staff = Staff("c'4 d'4 e'4 f'4")
    >>> mutate(staff).split([Duration(3, 8)])
    >>> show(staff)

It now makes sense to speak of a "mutatation interface" available in the
system:

::

    ScoreMutationAgent.copy([n, include_enclosing_containers])
    ScoreMutationAgent.extract([scale_contents])
    ScoreMutationAgent.fuse()
    ScoreMutationAgent.replace(recipients)
    ScoreMutationAgent.scale(multiplier)
    ScoreMutationAgent.splice(components[, direction, grow_spanners])
    ScoreMutationAgent.split(durations[, fracture_spanners, ...])

``mutate()`` cleans up a number of previously complex parts of the system.
There are, for example, now only a single copy function, a single split
function and a single fuse function implemented in all of Abjad.


Collections
^^^^^^^^^^^

ObjectInventory has been generalized by a collected of five new type collection
classes: ``TypedCollection``, ``TypedCounter``, ``TypedSet``, ``TypedTuple``,
``TypedList``.



``pitchtools`` refactoring
^^^^^^^^^^^^^^^^^^^^^^^^^^



Improvements to the docs
^^^^^^^^^^^^^^^^^^^^^^^^



Other features
^^^^^^^^^^^^^^

ClefMark now understands octavation suffixes such as _8, _15, ^8 and ^15.
It takes these suffixes into account when determining its middle-C position.











Older versions
--------------

..  toctree::
    :maxdepth: 1

    version_2_12
    version_2_11
    version_2_10
    version_2_9
    version_2_8
    version_2_7
    version_2_6
    version_2_5
    version_2_4
    version_2_3
    version_2_2
    version_2_1
    version_2_0
