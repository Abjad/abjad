LilyPond multipliers
====================

LilyPond provides an asterisk `*` operator to scale the durations of
notes, rests and chords by arbitrarily positive rational
values. LilyPond multipliers are inivisible and generate no
typographic output of their own. However, while independent from the
typographic output, LilyPond multipliers do factor in in calculations
of duration and time.

Abjad implements LilyPond multpliers as the settable `duration.multiplier`
attribute of notes, rests and chords.

::

   >>> note = Note("c'4")
   >>> note.duration_multiplier = Fraction(1, 2)
   >>> note.duration_multiplier
   Multiplier(1, 2)


::

   >>> f(note)
   c'4 * 1/2


Abjad also implements a `duration.multiplied` attribute to examine the
duration of a note, rest or chord as affected by the multiplier.

::

   >>> note.multiplied_duration
   Duration(1, 8)


LilyPond multipliers give the half notes here multiplied durations equal to a quarter note.

::

   >>> notes = Note("c'4") * 4
   >>> multiplied_note = Note(0, (1, 2))
   >>> multiplied_note.duration_multiplier = Fraction(1, 2)
   >>> multiplied_notes = multiplied_note * 4
   >>> top = stafftools.RhythmicStaff(notes)
   >>> bottom = stafftools.RhythmicStaff(multiplied_notes)
   >>> staves = scoretools.StaffGroup([top, bottom])


::

   >>> show(staves)

.. image:: images/index-1.png


.. note::

    Abjad models multiplication fundamentally differently than prolation .
    See the chapter on :doc:`../prolation/index` for more
    information.

.. note::

    The LilyPond multiplication `*` operator differs from the Abjad
    multiplication `*` operator. LilyPond multiplication scales duration
    of LilyPond notes, rests and chords. Abjad multiplication
    copies Abjad containers and leaves.
