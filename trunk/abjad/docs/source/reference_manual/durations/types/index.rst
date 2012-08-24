Duration types
==============

Abjad publishes duration information about all score components.


Written duration
----------------

Abjad uses written duration to refer to the face value of
notes, rests and chords prior to prolation.
Abjad written duration corresponds to the informal names most frequently used
when talking about note duration.

These sixteenth notes are worth a sixteenth of a whole note:

::

   >>> measure = Measure((5, 16), "c16 c c c c")
   >>> beam = beamtools.BeamSpanner(measure)
   >>> staff = stafftools.RhythmicStaff([measure])


::

   >>> show(staff, docs=True)

.. image:: images/index-1.png


::

   >>> note = measure[0]
   >>> note.written_duration
   Duration(1, 16)


These sixteenth notes are worth more than a sixteenth of a whole note:

::

   >>> tuplet = tuplettools.FixedDurationTuplet(Duration(5, 16), "c8 c c c c")
   >>> beam = beamtools.BeamSpanner(tuplet)
   >>> measure = Measure((5, 16), [tuplet])
   >>> staff = stafftools.RhythmicStaff([measure])


::

   >>> show(staff, docs=True)

.. image:: images/index-2.png


::

   >>> note = tuplet[0]
   >>> note.written_duration
   Duration(1, 8)


The notes in these examples are 'sixteenth notes' that carry different prolated durations.
Abjad written duration captures the fact that the note heads and flag counts of the two
examples match.

Written duration is a user-assignable rational number.
Users can assign and reassign the written duration of notes, rests and chords
at initialization and at any time during the life of the note, rest or chord.
Written durations must be assignable;
see the chapter on :doc:`assignability <../assignability/index>` for details.
Note that Abjad containers do not carry written duration.


Prolated duration
-----------------

:doc:`Prolation <../prolation/index>` refers to the duration-scaling
effects of tuplets and special types of time signature.
Prolation is a way of thinking about the contribution that musical structure makes to
the duration of score objects.
All durated Abjad objects carry a prolated duration.
Prolated duration is an emergent property of notes, tuplets and other durated objects.
The prolated duration of notes, rests and chords equals the product
of the written duration and prolation of those objects.
The prolated duration of tuplets, measures and other containers equals the
the container's duration interface multiplied by the container's prolation.


Contents duration
-----------------

Abjad defines the contents duration of tuplets, measures, voices, staves
and other containers equal to the sum of the preprolated duration of each
of the elements in the container.

The measure here contains two eighth notes and tuplet.
These elements carry preprolated durations equal to ``1/8``, ``1/8`` and ``2/8``, respectively:

::

   >>> notes = 2 * Note("c'8")
   >>> beam = beamtools.BeamSpanner(notes)
   >>> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 c c") 
   >>> beam = beamtools.BeamSpanner(tuplet)
   >>> measure = Measure((4, 8), notes + [tuplet])
   >>> staff = stafftools.RhythmicStaff([measure])


::

   >>> show(staff, docs=True)

.. image:: images/index-3.png


::

   >>> measure.contents_duration
   Duration(1, 2)


The contents duration of the measure here equals ``1/8 + 1/8 + 2/8 = 4/8``.


Target duration
---------------

Abjad defines the target duration of fixed-duration tuplets equal to
composer-settable duration to which the tuplet prolates its contents.

This fixed-duration tuplet carries a target duration equal to ``4/8``:

::

   >>> tuplet = tuplettools.FixedDurationTuplet(Duration(4, 8), "c'8 c c c c") 
   >>> beam = beamtools.BeamSpanner(tuplet)
   >>> measure = Measure((4, 8), [tuplet])
   >>> staff = stafftools.RhythmicStaff([measure])


::

   >>> show(staff, docs=True)

.. image:: images/index-4.png


::

   >>> tuplet.target_duration
   Duration(1, 2)


The tuplet contents sum to ``5/8``. But tuplet target duration always equals ``4/8``.


Multiplied duration
-------------------

Abjad defines the multiplied duration of notes, rests and chords equal to
the product of written duration and leaf multiplier.

The first two notes below carry leaf mulitipliers equal to ``2/1``:

::

   >>> notes = 4 * Note("c'16")
   >>> notes[0].duration_multiplier = Fraction(2, 1)
   >>> notes[1].duration_multiplier = Fraction(2, 1)
   >>> measure = Measure((3, 8), notes)
   >>> beam = beamtools.BeamSpanner(measure)
   >>> staff = stafftools.RhythmicStaff([measure])


::

   >>> show(staff, docs=True)

.. image:: images/index-5.png


::

   >>> note = measure[0]
   >>> note.written_duration
   Duration(1, 16)


::

   >>> note.duration_multiplier
   Fraction(2, 1)


::

   >>> note.written_duration * note.duration_multiplier
   Duration(1, 8)
   >>> note.multiplied_duration
   Duration(1, 8)


The written duration of these first two notes equals ``1/16`` and so
the multiplied duration of these first two notes equals ``1/16 * 2/1 = 1/8``.
