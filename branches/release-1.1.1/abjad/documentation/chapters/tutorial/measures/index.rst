Working with measures
=====================


Rigid, dynamic and anonymous
----------------------------

The easiest way to build an Abjad measure full of music is with
:class:`~abjad.measure.rigid.measure.RigidMeasure`. ::

   abjad> measure = RigidMeasure((3, 8), construct.scale(3))
   abjad> print measure.format
   \time 3/8
   c'8
   d'8
   e'8

To use a rigid measure, you need to
know the duration of measure you want to make before you make it.

If you want a measure that grows and shinks as you add music
to it and take music out, you can use a 
:class:`~abjad.measure.dynamic.measure.DynamicMeasure`. ::

   abjad> measure = DynamicMeasure(construct.scale(4))
   abjad> print measure.format
   \time 1/2
   c'8
   d'8
   e'8
   f'8

::

   abjad> measure.pop(-1)
   Note(f', 8)
   abjad> print measure.format
   \time 3/8
   c'8
   d'8
   e'8

If you want this same dynamic behavior in a measure that hides 
its time signature, use an
:class:`~abjad.measure.anonymous.measure.AnonymousMeasure`. ::

   abjad> measure = AnonymousMeasure(construct.scale(4))
   abjad> print measure.format
   \override Staff.TimeSignature #'stencil = ##f
   \time 1/2
   c'8
   d'8
   e'8
   f'8
   \revert Staff.TimeSignature #'stencil

::

   abjad> measure.pop(-1)
   Note(f', 8)
   abjad> print measure.format
   \override Staff.TimeSignature #'stencil = ##f
   \time 3/8
   c'8
   d'8
   e'8
   \revert Staff.TimeSignature #'stencil


Showing where measures start and stop
-------------------------------------

By default Abjad prints the contents of a measure with no
start and stop delimiters.
But you can tell individual measures to number their start
and stop points in the output code sent to LilyPond. ::

   abjad> staff = Staff(RigidMeasure((2, 8), construct.scale(2)) * 3)
   abjad> measure = staff[-1]
   abjad> measure.formatter.number.self = 'comment'
   \new Staff {
         \time 2/8
         c'8
         d'8
         \time 2/8
         c'8
         d'8
      % start measure 3
         \time 2/8
         c'8
         d'8
      % stop measure 3
   }

.. note:: Abjad measures numbers from 1 as we would expect in 
   the musical score (rather than from 0 as we might expect
   for the index of a list).

You can also turn on format-level measure numbering for all the
measures in a staff, voice or other container. ::

   abjad> staff = Staff(RigidMeasure((2, 8), construct.scale(2)) * 3)
   abjad> staff.formatter.number.measures = 'comment'
   abjad> print staff.format
   \new Staff {
      % start measure 1
         \time 2/8
         c'8
         d'8
      % stop measure 1
      % start measure 2
         \time 2/8
         c'8
         d'8
      % stop measure 2
      % start measure 3
         \time 2/8
         c'8
         d'8
      % stop measure 3
   }
