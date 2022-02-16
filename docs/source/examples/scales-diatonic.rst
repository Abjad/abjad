Scales, diatonic
================

..

----

Scale literals
--------------

Use string input to "write" a scale directly:

::

    >>> voice = abjad.Voice("a'4 b' cs'' d'' e'' fs'' gs'' a''", name="Example_Voice")
    >>> staff = abjad.Staff([voice], name="Example_Staff")
    >>> note = abjad.Selection(staff).note(0)
    >>> key_signature = abjad.KeySignature("a", "major") 
    >>> abjad.attach(key_signature, note)
    >>> abjad.show(staff)

----

A function to generate one octave of a scale
--------------------------------------------

Use an interval segment to model the structure of any scale. Here's the interval
structure of C major, G major, D major and every other scale in the major mode:

::

    >>> string = "M2 M2 m2 M2 M2 M2 m2"
    >>> major_mode = abjad.IntervalSegment(string)
    >>> major_mode

This function makes one octave of any scale:

::

    >>> def make_scale(tonic, interval_segment):
    ...     pitches = []
    ...     pitch = abjad.NamedPitch(tonic)
    ...     pitches.append(pitch)
    ...     for interval in interval_segment:
    ...         pitch = pitch + interval
    ...         pitches.append(pitch)
    ...     pitch_segment = abjad.PitchSegment(pitches)
    ...     return pitch_segment

Here's one octave of a major scale, rooted on C:

::

    >>> make_scale("c'", major_mode)

Here's one octave of a natural minor scale, rooted on C:

::

    >>> string = "M2 m2 M2 M2 m2 M2 M2"
    >>> minor_mode = abjad.IntervalSegment(string)
    >>> make_scale("c'", minor_mode)

Here's one octave of a Dorian scale, rooted on C:

::

    >>> string = "M2 m2 M2 M2 M2 m2 M2"
    >>> dorian_mode = abjad.IntervalSegment(string)
    >>> make_scale("c'", dorian_mode)

----

Illustrating one scale at a time
--------------------------------

Change pitches to notes like this:

::

    >>> pitch_segment = make_scale("a'", major_mode)
    >>> notes = [abjad.Note(_, (1, 4)) for _ in pitch_segment]

::

    >>> voice = abjad.Voice(notes, name="Example_Voice")
    >>> staff = abjad.Staff([voice], name="Example_Staff")
    >>> note = abjad.Selection(staff).note(0)
    >>> key_signature = abjad.KeySignature("a", "major") 
    >>> abjad.attach(key_signature, note)
    >>> abjad.show(staff)

Reverse scale direction like this:

::

    >>> notes = [abjad.Note(_, (1, 4)) for _ in reversed(pitch_segment)]

::

    >>> voice = abjad.Voice(notes, name="Example_Voice")
    >>> staff = abjad.Staff([voice], name="Example_Staff")
    >>> note = abjad.Selection(staff).note(0)
    >>> key_signature = abjad.KeySignature("a", "major") 
    >>> abjad.attach(key_signature, note)
    >>> abjad.show(staff)

Join ascending and descending segments like this:

::

    >>> notes = [abjad.Note(_, (1, 4)) for _ in pitch_segment]
    >>> descending = [abjad.Note(_, (1, 4)) for _ in reversed(pitch_segment)]
    >>> descending = descending[1:]
    >>> notes.extend(descending)

::

    >>> voice = abjad.Voice(notes, name="Example_Voice")
    >>> staff = abjad.Staff([voice], name="Example_Staff")
    >>> note = abjad.Selection(staff).note(0)
    >>> key_signature = abjad.KeySignature("a", "major") 
    >>> abjad.attach(key_signature, note)
    >>> abjad.show(staff)


----

A function to enumerate many scales
-----------------------------------

This dictionary changes mode name to interval segment:

::

    >>> mode_name_to_interval_segment = {
    ...     "major": abjad.IntervalSegment("M2 M2 m2 M2 M2 M2 m2"),
    ...     "minor": abjad.IntervalSegment("M2 m2 M2 M2 m2 M2 M2"),
    ...     "dorian": abjad.IntervalSegment("M2 m2 M2 M2 M2 m2 M2"),
    ... }

This function enumerates scales in any mode:

::

    >>> def make_score(tonics, mode_name):
    ...     voice = abjad.Voice(name="Example_Voice")
    ...     staff = abjad.Staff([voice], name="Example_Staff")
    ...     score = abjad.Score([staff], name="Score")
    ...     interval_segment = mode_name_to_interval_segment[mode_name]
    ...     for tonic in tonics:
    ...         key_signature = abjad.KeySignature(tonic, mode_name)
    ...         pitches = []
    ...         ascending = make_scale(tonic, interval_segment)
    ...         pitches.extend(ascending)
    ...         descending = make_scale(tonic, interval_segment)
    ...         descending = list(reversed(descending))[1:]
    ...         pitches.extend(descending)
    ...         notes = [abjad.Note(_, (1, 4)) for _ in pitches]
    ...         name = notes[0].written_pitch.get_name(locale="us")
    ...         name = name[:-1]
    ...         string = fr'\markup {{ "{name} {mode_name}" }}'
    ...         markup = abjad.Markup(string, direction=abjad.Up)
    ...         abjad.attach(markup, notes[0])
    ...         bar_line = abjad.BarLine("||")
    ...         abjad.attach(bar_line, notes[-1])
    ...         string = r"\markup \transparent A"
    ...         strut = abjad.Markup(string, direction=abjad.Up)
    ...         abjad.tweak(strut).staff_padding = 8 
    ...         abjad.attach(strut, notes[-1])
    ...         voice.extend(notes)
    ...     time_signature = abjad.TimeSignature((15, 4))
    ...     abjad.attach(time_signature, voice[0])
    ...     return score

This LilyPond code styles output:

::

    >>> preamble = r"""#(set-global-staff-size 14)
    ... 
    ... \layout {
    ...     \context {
    ...         \Score
    ...         \override BarNumber.stencil = ##f
    ...         \override TextScript.staff-padding = 3
    ...         \override TimeSignature.stencil = ##f
    ...     }
    ...     indent = 0
    ... }
    ... """

----

Twelve major scales
-------------------

    >>> string = "C4 G4 D4 A4 E4 B4 F4 Bb4 Eb4 Ab4 Db4 Gb4"
    >>> tonics = string.split()
    >>> score = make_score(tonics, "major")
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

----

Twelve minor scales
-------------------

    >>> string = "C4 G4 D4 A4 E4 B4 F4 Bb4 Eb4 Ab4 Db4 Gb4"
    >>> tonics = string.split()
    >>> score = make_score(tonics, "minor")
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

----

Twelve Dorian scales
--------------------

    >>> string = "C4 G4 D4 A4 E4 B4 F4 Bb4 Eb4 Ab4 Db4 Gb4"
    >>> tonics = string.split()
    >>> score = make_score(tonics, "dorian")
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

:author:`[Bača (3.3)]`
