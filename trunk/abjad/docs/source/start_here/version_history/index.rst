:tocdepth: 2

Version history
===============


Abjad 2.13
----------

Released 2013-10-23. Built from r12,499.  Implements 485 public classes and 465
functions totaling 198,812 lines.


API refactoring
^^^^^^^^^^^^^^^

More than half the functionality of the Abjad API has migrated from functions
to class methods. This means that the total number of functions in the API has
decreased from 1045 in Abjad 2.12 to only 465 in Abjad 2.13. This also means
that many classes now provide additional functionality in the form of public
methods. Check the API entries of the Abjad classes you work with the most
often for new features. And note that essentially all functionality
available in Abjad 2.12 has been ported to Abjad 2.13, usually with an
interface that is easier to use and better documented.

For example, the predicates previously implemented as ``pitchtools`` functions
are now implemented as methods bound to the Abjad ``NamedPitch`` class:

- ``NamedPitch.is_diatonic_pitch_name()``
- ``NamedPitch.is_diatonic_pitch_number()``
- ``NamedPitch.is_pitch_carrier()``
- ``NamedPitch.is_pitch_class_octave_number_string()``
- ``NamedPitch.is_pitch_name()``
- ``NamedPitch.is_pitch_number()``



Introducing ``inspect()``
^^^^^^^^^^^^^^^^^^^^^^^^^

A new ``inspect()`` function is now available when you start Abjad.
``inspect()`` is a factory function that returns an instance of the new
``AttributeInspectionAgent`` ("the inspector") when called on any score
component. Use the inspector to examine component attributes determined by
score structure.  Here's how to use ``inspect()`` to get the duration of a
tupletted note:

::

    >>> tuplet = Tuplet(Multiplier(2, 3), "c'4 d'4 e'4")
    >>> note = tuplet[0]
    >>> note.written_duration
    Duration(1, 4)
    >>> inspect(note).get_duration()
    Duration(1, 6)

These are the methods available as part of the new inspection interface:

- ``AttributeInspectionAgent.get_annotation()``
- ``AttributeInspectionAgent.get_badly_formed_components()``
- ``AttributeInspectionAgent.get_components()``
- ``AttributeInspectionAgent.get_contents()``
- ``AttributeInspectionAgent.get_descendants()``
- ``AttributeInspectionAgent.get_duration()``
- ``AttributeInspectionAgent.get_effective_context_mark()``
- ``AttributeInspectionAgent.get_effective_staff()``
- ``AttributeInspectionAgent.get_grace_containers()``
- ``AttributeInspectionAgent.get_leaf()``
- ``AttributeInspectionAgent.get_lineage()``
- ``AttributeInspectionAgent.get_mark()``
- ``AttributeInspectionAgent.get_marks()``
- ``AttributeInspectionAgent.get_markup()``
- ``AttributeInspectionAgent.get_parentage()``
- ``AttributeInspectionAgent.get_spanner()``
- ``AttributeInspectionAgent.get_spanners()``
- ``AttributeInspectionAgent.get_tie_chain()``
- ``AttributeInspectionAgent.get_timespan()``
- ``AttributeInspectionAgent.get_vertical_moment()``
- ``AttributeInspectionAgent.get_vertical_moment_at()``
- ``AttributeInspectionAgent.is_bar_line_crossing()``
- ``AttributeInspectionAgent.is_well_formed()``
- ``AttributeInspectionAgent.report_modifications()``
- ``AttributeInspectionAgent.tabulate_well_formedness_violations()``


Introducing  ``mutate()``
^^^^^^^^^^^^^^^^^^^^^^^^^

A new ``mutate()`` function is now availble when you start Abjad.
``mutate()`` is a factory function that returns an instance of the
new ``ScoreMutationAgent`` class when called on any score component. Use
the ``ScoreMutationAgent`` to make structural changes to the component
or components on which it was called. Here's how to use ``mutate()``
to split the notes in a staff:

::

    >>> staff = Staff("c'4 d'4 e'4 f'4")
    >>> mutate(staff).split([Duration(3, 8)])
    >>> show(staff)

These are the methods available as part of the new mutation interface:

- ``ScoreMutationAgent.copy()``
- ``ScoreMutationAgent.extract()``
- ``ScoreMutationAgent.fuse()``
- ``ScoreMutationAgent.replace()``
- ``ScoreMutationAgent.scale()``
- ``ScoreMutationAgent.splice()``
- ``ScoreMutationAgent.split()``

``mutate()`` cleans up previously complex parts of the system.
There are now only a single copy function, a single split
function and a single fuse function implemented in Abjad.


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
