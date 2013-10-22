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
``inspect()`` is a factory function that returns an instance of the new
AttributeInspectionAgent (or just "the inspector"). The inspector allows you
to get a large number of different score component attributes determined by
score structure. Here's an example of using ``inspect()`` to get the duration
of a tupletted note:

::

    >>> tuplet = Tuplet(Multiplier(2, 3), "c'4 d'4 e'4")
    >>> note = tuplet[0]
    >>> note.written_duration
    Duration(1, 4)
    >>> inspect(note).get_duration()
    Duration(1, 6)

It now makes sense to speak of an "inspection interface" availabe in the
system:

::

    AttributeInspectionAgent.get_annotation()
    AttributeInspectionAgent.get_badly_formed_components()
    AttributeInspectionAgent.get_components()
    AttributeInspectionAgent.get_contents()
    AttributeInspectionAgent.get_descendants()
    AttributeInspectionAgent.get_duration()
    AttributeInspectionAgent.get_effective_context_mark()
    AttributeInspectionAgent.get_effective_staff()
    AttributeInspectionAgent.get_grace_containers()
    AttributeInspectionAgent.get_leaf()
    AttributeInspectionAgent.get_lineage()
    AttributeInspectionAgent.get_mark()
    AttributeInspectionAgent.get_marks()
    AttributeInspectionAgent.get_markup()
    AttributeInspectionAgent.get_parentage()
    AttributeInspectionAgent.get_spanner()
    AttributeInspectionAgent.get_spanners()
    AttributeInspectionAgent.get_tie_chain()
    AttributeInspectionAgent.get_timespan()
    AttributeInspectionAgent.get_vertical_moment()
    AttributeInspectionAgent.get_vertical_moment_at()
    AttributeInspectionAgent.is_bar_line_crossing()
    AttributeInspectionAgent.is_well_formed()
    AttributeInspectionAgent.report_modifications()
    AttributeInspectionAgent.tabulate_well_formedness_violations()


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

    ScoreMutationAgent.copy()
    ScoreMutationAgent.extract()
    ScoreMutationAgent.fuse()
    ScoreMutationAgent.replace()
    ScoreMutationAgent.scale()
    ScoreMutationAgent.splice()
    ScoreMutationAgent.split()

``mutate()`` cleans up a number of previously complex parts of the system.
There are, for example, now only a single copy function, a single split
function and a single fuse function implemented in all of Abjad.


Selection objects
^^^^^^^^^^^^^^^^^

Slicing now returns a selection. Tie chains are now implemented as selections.
And you may use the newly added ``select()`` function to create selections by
hand.


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

A new ``StringOrchestraScoreTemplate`` is now available in the
``scoretemplatetools`` package.







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
