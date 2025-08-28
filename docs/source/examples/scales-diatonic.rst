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
    >>> note = abjad.select.note(staff, 0)
    >>> key_signature = abjad.KeySignature(
    ...     abjad.NamedPitchClass("a"), abjad.Mode("major")
    ... ) 
    >>> abjad.attach(key_signature, note)
    >>> abjad.show(staff)

----

A function to generate one octave of a scale
--------------------------------------------

Use a list of intervals to model the structure of any scale. Here's the interval
structure of C major, G major, D major and every other scale in the major mode:

::

    >>> intervals = "M2 M2 m2 M2 M2 M2 m2".split()
    >>> intervals = [abjad.NamedInterval(_) for _ in intervals]

This function makes one octave of any scale:

::

    >>> def make_scale(tonic, intervals):
    ...     pitches = []
    ...     pitch = abjad.NamedPitch(tonic)
    ...     pitches.append(pitch)
    ...     for interval in intervals:
    ...         pitch = pitch + interval
    ...         pitches.append(pitch)
    ...     return pitches

Here's one octave of a major scale, rooted on C:

::

    >>> make_scale("c'", intervals)

Here's one octave of a natural minor scale, rooted on C:

::

    >>> intervals = "M2 m2 M2 M2 m2 M2 M2".split()
    >>> intervals = [abjad.NamedInterval(_) for _ in intervals]
    >>> make_scale("c'", intervals)

Here's one octave of a Dorian scale, rooted on C:

::

    >>> intervals = "M2 m2 M2 M2 M2 m2 M2".split()
    >>> intervals = [abjad.NamedInterval(_) for _ in intervals]
    >>> make_scale("c'", intervals)

----

Illustrating one scale at a time
--------------------------------

Change pitches to notes like this:

::

    >>> intervals = "M2 M2 m2 M2 M2 M2 m2".split()
    >>> intervals = [abjad.NamedInterval(_) for _ in intervals]
    >>> pitches = make_scale("a'", intervals)
    >>> duration = abjad.Duration(1, 4)
    >>> notes = [abjad.Note.from_duration_and_pitch(duration, _) for _ in pitches]

::

    >>> voice = abjad.Voice(notes, name="Example_Voice")
    >>> staff = abjad.Staff([voice], name="Example_Staff")
    >>> note = abjad.select.note(staff, 0)
    >>> key_signature = abjad.KeySignature(
    ...     abjad.NamedPitchClass("a"), abjad.Mode("major")
    ... ) 
    >>> abjad.attach(key_signature, note)
    >>> abjad.show(staff)

Reverse scale direction like this:

::

    >>> duration = abjad.Duration(1, 4)
    >>> retrograde = reversed(pitches)
    >>> notes = [abjad.Note.from_duration_and_pitch(duration, _) for _ in retrograde]

::

    >>> voice = abjad.Voice(notes, name="Example_Voice")
    >>> staff = abjad.Staff([voice], name="Example_Staff")
    >>> note = abjad.select.note(staff, 0)
    >>> key_signature = abjad.KeySignature(
    ...     abjad.NamedPitchClass("a"), abjad.Mode("major")
    ... ) 
    >>> abjad.attach(key_signature, note)
    >>> abjad.show(staff)

Join ascending and descending segments like this:

::

    >>> duration = abjad.Duration(1, 4)
    >>> notes = [abjad.Note.from_duration_and_pitch(duration, _) for _ in pitches]
    >>> retrograde = reversed(pitches)
    >>> descending = [abjad.Note.from_duration_and_pitch(duration, _) for _ in retrograde]
    >>> descending = descending[1:]
    >>> notes.extend(descending)

::

    >>> voice = abjad.Voice(notes, name="Example_Voice")
    >>> staff = abjad.Staff([voice], name="Example_Staff")
    >>> note = abjad.select.note(staff, 0)
    >>> key_signature = abjad.KeySignature(
    ...     abjad.NamedPitchClass("a"), abjad.Mode("major")
    ... ) 
    >>> abjad.attach(key_signature, note)
    >>> abjad.show(staff)


----

A function to enumerate many scales
-----------------------------------

This dictionary changes mode to intervals:

::

    >>> mode_to_intervals = {
    ...     "major": "M2 M2 m2 M2 M2 M2 m2",
    ...     "minor": "M2 m2 M2 M2 m2 M2 M2",
    ...     "dorian": "M2 m2 M2 M2 M2 m2 M2",
    ... }

This function enumerates scales in any mode:

::

    >>> def make_score(tonics, mode_name):
    ...     voice = abjad.Voice(name="Example_Voice")
    ...     staff = abjad.Staff([voice], name="Example_Staff")
    ...     score = abjad.Score([staff], name="Score")
    ...     intervals = mode_to_intervals[mode_name]
    ...     intervals = intervals.split()
    ...     intervals = [abjad.NamedInterval(_) for _ in intervals]
    ...     duration = abjad.Duration(1, 4)
    ...     for tonic in tonics:
    ...         pitch_class = abjad.NamedPitchClass(tonic)
    ...         mode = abjad.Mode(mode_name)
    ...         key_signature = abjad.KeySignature(pitch_class, mode)
    ...         pitches = []
    ...         ascending = make_scale(tonic, intervals)
    ...         pitches.extend(ascending)
    ...         descending = make_scale(tonic, intervals)
    ...         descending = list(reversed(descending))[1:]
    ...         pitches.extend(descending)
    ...         notes = [abjad.Note.from_duration_and_pitch(duration, _) for _ in pitches]
    ...         name = notes[0].written_pitch().get_name_in_locale(locale="us")
    ...         name = name[:-1]
    ...         string = fr'\markup {{ "{name} {mode_name}" }}'
    ...         markup = abjad.Markup(string)
    ...         abjad.attach(markup, notes[0], direction=abjad.UP)
    ...         bar_line = abjad.BarLine("||")
    ...         abjad.attach(bar_line, notes[-1])
    ...         string = r"\markup \transparent A"
    ...         strut = abjad.Markup(string)
    ...         bundle = abjad.bundle(strut, r"- \tweak staff-padding 8")
    ...         abjad.attach(bundle, notes[-1], direction=abjad.UP)
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

:author:`[Bača (3.3, 3.7, 3.29)]`
