:orphan:

What's the difference between duration and written duration?
============================================================

Abjad uses the term "written duration" to refer to the face value of notes, rests and
chords prior to time-scaling effects of tuplets or measures with unusual time signatures.
Abjad's written duration corresponds to the informal names most frequently used when
talking about note duration.

Consider the measure below:

::

    >>> staff = abjad.Staff(r"\time 5/15 c16 [ c c c c ]", lilypond_type="RhythmicStaff")
    >>> leaves = abjad.select(staff).leaves()

::

    >>> abjad.show(staff)

Every note in the measure equals one sixteenth of a whole note:

::

    >>> note = staff[0]
    >>> abjad.get.duration(note)

But now consider this measure:

::

    >>> tuplet = abjad.Tuplet((4, 5), r"\time 4/16 c16 [ c c c c ]")
    >>> staff = abjad.Staff([tuplet], lilypond_type="RhythmicStaff")
    >>> leaves = abjad.select(staff).leaves()

::

    >>> abjad.show(staff)

The notes in this measure are equal to only one twentieth of a whole note:

::

    >>> note = tuplet[0]
    >>> abjad.get.duration(note)

The notes in this measure are "sixteenth notes" with a duration equal to a value other
than ``1/16``. Abjad formalizes this distinction in the difference between the duration
of these notes (``1/20``) and written duration of these notes (``1/16``).

Written duration is a user-assignable value. Users can assign and reassign the written
duration of notes, rests and chords at initialization or any time thereafter. But the
(unqualified) duration of a note, rest or chord is a derived property Abjad calculates
based on the rhythmic context governing the note, rest or chord.
