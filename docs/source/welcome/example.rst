**An example.** Start Python, import Abjad, make some notes:

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

    >>> for note in abjad.select(score["Staff_2"]).notes():
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

Call the function one way on staff 1 and another way on staff 2:

::

    >>> slur_parts(score["Staff_1"], [2, 4, 4])
    >>> slur_parts(score["Staff_2"], [4])
    >>> abjad.show(score)

Tupletize notes in staff 1:

::

    >>> notes = abjad.select(score["Staff_1"]).notes()
    >>> abjad.mutate.wrap(notes[:6], abjad.Tuplet("3:2"))
    >>> abjad.mutate.wrap(notes[10:16], abjad.Tuplet("3:2"))
    >>> abjad.mutate.wrap(notes[20:26], abjad.Tuplet("3:2"))
    >>> abjad.show(score)

Tupletize notes in staff 2:

::

    >>> notes = abjad.select(score["Staff_2"]).notes()
    >>> abjad.mutate.wrap(notes[4:10], abjad.Tuplet("3:2"))
    >>> abjad.mutate.wrap(notes[14:20], abjad.Tuplet("3:2"))
    >>> abjad.mutate.wrap(notes[24:30], abjad.Tuplet("3:2"))
    >>> abjad.show(score)

Trim both staves, attach a time signature, attach a doule bar line, clean up tuplet
brackets:

::

    >>> del(score["Staff_1"][-6:])
    >>> del(score["Staff_2"][-3:])
    >>> first_note = abjad.select(score["Staff_1"]).note(0)
    >>> abjad.attach(abjad.TimeSignature((2, 8)), first_note)
    >>> last_note = abjad.select(score["Staff_2"]).note(-1)
    >>> abjad.attach(abjad.BarLine("|."), last_note)
    >>> abjad.override(score).tuplet_bracket.staff_padding = 2
    >>> abjad.show(score)

