As a first example, start Python, import Abjad, make some notes:

::

    >>> import abjad
    >>> string = "c'16 f' g' a' d' g' a' b' e' a' b' c'' f' b' c'' d''16"
    >>> voice_1 = abjad.Voice(string, name="Voice_1")
    >>> staff_1 = abjad.Staff([voice_1], name="Staff_1")
    >>> abjad.show(staff_1)

Use Python's list operations to split, reverse, join the input string. Then extend
voice 1:

::

    >>> pitches = string.split()
    >>> pitches = reversed(pitches)
    >>> retrograde = " ".join(pitches)
    >>> voice_1.extend(retrograde)
    >>> abjad.show(staff_1)

Create a second voice in a second staff:

::

    >>> string = string + " " + retrograde
    >>> voice_2 = abjad.Voice(string, name="Voice_2")
    >>> staff_2 = abjad.Staff([voice_2], name="Staff_2")

Enclose both staves in a staff group and a score:

::

    >>> piano_staff = abjad.StaffGroup(
    ...     [staff_1, staff_2],
    ...     lilypond_type="PianoStaff",
    ...     name="PianoStaff",
    ... )
    >>> score = abjad.Score([piano_staff], name="Score")
    >>> abjad.show(score)

Invert the pitches in voice 2:

::

    >>> for note in abjad.Selection(voice_2).notes():
    ...     note.written_pitch = note.written_pitch.invert(axis="G4")
    ... 
    >>> abjad.show(score)

Define a function to partition notes, loop over parts, attach slurs, attach articulations:

::

    >>> def slur_parts(voice, counts):
    ...     notes = abjad.Selection(voice).notes()
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

Slur voice 1:

::

    >>> slur_parts(voice_1, [2, 4, 4])
    >>> abjad.show(score)

Slur voice 2:

::

    >>> slur_parts(voice_2, [4])
    >>> abjad.show(score)

Define a function to tupletize alternating groups of notes:

::

    >>> def tupletize_notes(voice, counts, modulus):
    ...     notes = abjad.Selection(voice).notes()
    ...     parts = notes.partition_by_counts(counts, cyclic=True)
    ...     for i, part in enumerate(parts):
    ...         if i % len(counts) == modulus:
    ...             abjad.mutate.wrap(part, abjad.Tuplet("3:2"))

Tupletize voice 1:

::

    >>> tupletize_notes(voice_1, [6, 4], 0)
    >>> abjad.show(score)

Tupletize voice 2:

::

    >>> tupletize_notes(voice_2, [4, 6], 1)
    >>> abjad.show(score)

Trim both voices:

::

    >>> del(voice_1[-6:])
    >>> del(voice_2[-3:])
    >>> abjad.show(score)

Attach a time signature, attach a doule bar line, clean up tuplet brackets:

::

    >>> first_note = abjad.Selection(voice_1).note(0)
    >>> time_signature = abjad.TimeSignature((2, 8))
    >>> abjad.attach(time_signature, first_note)
    >>> last_note = abjad.Selection(voice_2).note(-1)
    >>> bar_line = abjad.BarLine("|.")
    >>> abjad.attach(bar_line, last_note)
    >>> abjad.override(score).tuplet_bracket.staff_padding = 2
    >>> abjad.show(score)
