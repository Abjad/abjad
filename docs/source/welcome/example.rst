As a first example, start Python, import Abjad, make some notes:

::

    >>> import abjad
    >>> string = "c'16 f' g' a' d' g' a' b' e' a' b' c'' f' b' c'' d''16"
    >>> staff_1 = abjad.Staff(string, name="Staff_1")
    >>> abjad.show(staff_1)

Use Python's list operations to split, reverse, join the input string. Then extend
staff 1:

::

    >>> pitches = string.split()
    >>> pitches = reversed(pitches)
    >>> retrograde = " ".join(pitches)
    >>> staff_1.extend(retrograde)
    >>> abjad.show(staff_1)

Create a second staff:

::

    >>> string = string + " " + retrograde
    >>> staff_2 = abjad.Staff(string, name="Staff_2")

Enclose both staves in a staff group and a score:

::

    >>> staff_group = abjad.StaffGroup(
    ...     [staff_1, staff_2],
    ...     lilypond_type="PianoStaff",
    ...     name="PianoStaff",
    ... )
    >>> score = abjad.Score([staff_group], name="Score")
    >>> abjad.show(score)

Invert the pitches in staff 2:

::

    >>> for note in abjad.select(staff_2).notes():
    ...     note.written_pitch = note.written_pitch.invert(axis="G4")
    ... 
    >>> abjad.show(score)

Define a function to partition notes, loop over parts, attach slurs, attach articulations:

::

    >>> def slur_parts(staff, counts):
    ...     notes = abjad.select(staff).notes()
    ...     parts = notes.partition_by_counts(counts, cyclic=True)
    ...     for part in parts:
    ...         first_note, last_note = part[0], part[-1]
    ...         accent = abjad.Articulation("accent")
    ...         start_slur = abjad.StartSlur()
    ...         abjad.attach(accent, first_note)
    ...         abjad.attach(start_slur, first_note)
    ...         staccato = abjad.Articulation("staccato")
    ...         stop_slur = abjad.StopSlur()
    ...         abjad.attach(staccato, last_note)
    ...         abjad.attach(stop_slur, last_note)

Slur staff 1:

::

    >>> slur_parts(staff_1, [2, 4, 4])
    >>> abjad.show(score)

Slur staff 2:

::

    >>> slur_parts(staff_2, [4])
    >>> abjad.show(score)

Define a function to tupletize alternating groups of notes:

::

    >>> def tupletize_notes(staff, counts, modulus):
    ...     notes = abjad.select(staff).notes()
    ...     parts = notes.partition_by_counts(counts, cyclic=True)
    ...     for i, part in enumerate(parts):
    ...         if i % len(counts) == modulus:
    ...             abjad.mutate.wrap(part, abjad.Tuplet("3:2"))

Tupletize staff 1:

::

    >>> tupletize_notes(staff_1, [6, 4], 0)
    >>> abjad.show(score)

Tupletize staff 2:

::

    >>> tupletize_notes(staff_2, [4, 6], 1)
    >>> abjad.show(score)

Trim both staves:

::

    >>> del(staff_1[-6:])
    >>> del(staff_2[-3:])
    >>> abjad.show(score)

Attach a time signature, attach a doule bar line, clean up tuplet brackets:

::

    >>> first_note = abjad.select(staff_1).note(0)
    >>> time_signature = abjad.TimeSignature((2, 8))
    >>> abjad.attach(time_signature, first_note)
    >>> last_note = abjad.select(staff_2).note(-1)
    >>> bar_line = abjad.BarLine("|.")
    >>> abjad.attach(bar_line, last_note)
    >>> abjad.override(score).tuplet_bracket.staff_padding = 2
    >>> abjad.show(score)
