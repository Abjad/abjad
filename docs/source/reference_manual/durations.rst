:tocdepth: 2

Durations
=========

::

    >>> import abjad


Breves, longas and other long durations
---------------------------------------

A breve is a duration equal to two whole notes. Abjad supports breve-durated
notes, rests and chords with and without dots.

You can create breves with a LilyPond input string:

::

    >>> note_1 = abjad.Note(r"c'\breve")
    >>> note_2 = abjad.Note(r"d'\breve.")

Or with an explicit duration:

::

    >>> note_3 = abjad.Note("e'", abjad.Duration(2, 1))
    >>> note_4 = abjad.Note("f'", abjad.Duration(3, 1))

The written duration of a breve always returns an Abjad duration object:

::

    >>> notes = [note_1, note_2, note_3, note_4]
    >>> for note in notes:
    ...     note, note.written_duration
    ...

LilyPond renders breves like this:

::

    >>> staff = abjad.Staff(notes)
    >>> abjad.show(staff)

Abjad also supports longas. A longa equals two breves:

::

    >>> note_1 = abjad.Note(r"c'\longa")
    >>> note_2 = abjad.Note("d'", abjad.Duration(6, 1))

    ::

    >>> notes = [note_1, note_2]
    >>> for note in notes:
    ...     note, note.written_duration
    ...

 ::

    >>> staff = abjad.Staff(notes)
    >>> abjad.show(staff)

A maxima is a duration equal to two longas:

::

    >>> note_1 = abjad.Note(r"c'\maxima")
    >>> note_2 = abjad.Note("d'", abjad.Duration(12, 1))

    ::

    >>> notes = [note_1, note_2]
    >>> for note in notes:
    ...     note, note.written_duration
    ...

Abjad supports maximas and LilyPond supplies a ``\maxima`` command. But you can
not use Abjad to render maxima-valued notes, rests and chords because LilyPond
supplies no glyphs for these durations.

The same is true for all durations greater than or equal to eight whole notes:
you can initialize and work with all such durations in Abjad but you will only
be able to use LilyPond to render as notation those values equal to less than
eight whole notes.


LilyPond multipliers
--------------------

LilyPond provides an asterisk `*` operator to scale the durations of notes,
rests and chords by arbitrarily positive rational values. LilyPond multipliers
are indivisible and generate no typographic output of their own. However, while
independent from the typographic output, LilyPond multipliers do factor into
calculations of duration.

Abjad implements LilyPond multpliers as multiplier objects.

::

    >>> note = abjad.Note("c'4", multiplier=(1, 2))

::

    >>> string = abjad.lilypond(note)
    >>> print(string)

::

    >>> note.written_duration
    >>> abjad.get.duration(note)

::

    >>> abjad.show(note)

LilyPond multipliers scale the durations of the half notes below to that of
quarter notes:

::

    >>> half_notes = [
    ...     abjad.Note("c'2", multiplier=(1, 2)),
    ...     abjad.Note("c'2", multiplier=(1, 2)),
    ...     abjad.Note("c'2", multiplier=(1, 2)),
    ...     abjad.Note("c'2", multiplier=(1, 2)),
    ... ]
    >>> top_staff = abjad.Staff("c'4 c'4 c'4 c'4", lilypond_type="RhythmicStaff")
    >>> bottom_staff = abjad.Staff(half_notes, lilypond_type="RhythmicStaff")
    >>> staff_group = abjad.StaffGroup([top_staff, bottom_staff])

::

    >>> abjad.show(staff_group)

Note that the LilyPond multiplication `*` operator differs from the Abjad
multiplication `*` operator. LilyPond multiplication scales duration of
LilyPond notes, rests and chords. Abjad multiplication copies Abjad containers
and leaves.


What's the difference between duration and written duration?
------------------------------------------------------------

Abjad uses the term "written duration" to refer to the face value of notes,
rests and chords prior to time-scaling effects of tuplets or measures with
unusual time signatures. Abjad's written duration corresponds to the informal
names most frequently used when talking about note duration.

Consider the measure below:

::

    >>> staff = abjad.Staff(r"\time 5/15 c16 [ c c c c ]", lilypond_type='RhythmicStaff')
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
    >>> staff = abjad.Staff([tuplet], lilypond_type='RhythmicStaff')
    >>> leaves = abjad.select(staff).leaves()

::

    >>> abjad.show(staff)

The notes in this measure are equal to only one twentieth of a whole note:
Every note in this measures 

::

    >>> note = tuplet[0]
    >>> abjad.get.duration(note)

The notes in this measure are "sixteenth notes" with a duration equal to a
value other than ``1/16``. Abjad formalizes this distinction in the difference
between the duration of these notes (``1/20``) and written duration of these
notes (``1/16``).

Written duration is a user-assignable value. Users can assign and
reassign the written duration of notes, rests and chords at initialization or
any time thereafter. But the (unqualified) duration of a note, rest or chord is
a derived property Abjad calculates based on the rhythmic context governing the
note, rest or chord.


What does it mean for a duration to be "assignable"?
----------------------------------------------------

Western notation makes it easy to notate notes, rests and chords with durations
like ``1/4`` and ``3/16``. But notating notes, rests and chords with durations
like ``1/3`` can only be done with recourse to tuplets or ties.

Abjad formalizes the difference between durations like ``1/4`` and ``1/5`` in
the concept of **assignability**: a duration ``n/d`` is assignable when and
only when numerator ``n`` is of the form ``2**i-2**j`` with ``i>j`` and
denominator ``d`` is of the form ``2**v``.  In this definition ``i`` must be a
positive integer, and ``j`` and ``v`` must be nonnegative integers.

Assignability is important because it explains why you can set the duration
of any note, rest or chord to ``1/4`` or ``7/4`` but never to ``1/5`` or
``7/5``.
