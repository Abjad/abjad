.. _abjad--tools--scoretools--Selection:

Selection
=========

.. automodule:: abjad.tools.scoretools.Selection

.. currentmodule:: abjad.tools.scoretools.Selection

.. container:: svg-container

   .. inheritance-diagram:: abjad
      :lineage: abjad.tools.scoretools.Selection

.. autoclass:: Selection

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Selection.__add__

   .. automethod:: Selection.__contains__

   .. automethod:: Selection.__copy__

   .. automethod:: Selection.__eq__

   .. automethod:: Selection.__format__

   .. automethod:: Selection.__getitem__

   .. automethod:: Selection.__hash__

   .. automethod:: Selection.__illustrate__

   .. automethod:: Selection.__iter__

   .. automethod:: Selection.__len__

   .. automethod:: Selection.__radd__

   .. automethod:: Selection.__repr__

   .. automethod:: Selection.__reversed__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: Selection.are_contiguous_logical_voice

   .. automethod:: Selection.are_contiguous_same_parent

   .. automethod:: Selection.are_leaves

   .. automethod:: Selection.are_logical_voice

   .. automethod:: Selection.chord

   .. automethod:: Selection.chords

   .. automethod:: Selection.components

   .. automethod:: Selection.count

   .. automethod:: Selection.filter

   .. automethod:: Selection.filter_duration

   .. automethod:: Selection.filter_length

   .. automethod:: Selection.filter_pitches

   .. automethod:: Selection.filter_preprolated

   .. automethod:: Selection.flatten

   .. automethod:: Selection.group_by

   .. automethod:: Selection.group_by_contiguity

   .. automethod:: Selection.group_by_duration

   .. automethod:: Selection.group_by_length

   .. automethod:: Selection.group_by_measure

   .. automethod:: Selection.group_by_pitch

   .. automethod:: Selection.index

   .. automethod:: Selection.leaf

   .. automethod:: Selection.leaves

   .. automethod:: Selection.logical_ties

   .. automethod:: Selection.map

   .. automethod:: Selection.nontrivial

   .. automethod:: Selection.note

   .. automethod:: Selection.notes

   .. automethod:: Selection.partition_by_counts

   .. automethod:: Selection.partition_by_durations

   .. automethod:: Selection.partition_by_ratio

   .. automethod:: Selection.rest

   .. automethod:: Selection.rests

   .. automethod:: Selection.run

   .. automethod:: Selection.runs

   .. automethod:: Selection.top

   .. automethod:: Selection.tuplet

   .. automethod:: Selection.tuplets

   .. automethod:: Selection.with_next_leaf

   .. automethod:: Selection.with_previous_leaf

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Selection.items