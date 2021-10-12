:orphan:

Pitch conventions
=================

Pitch numbers
-------------

Abjad numbers pitches like this:

::

    >>> score = abjad.illustrators.make_piano_score()
    >>> treble_staff, bass_staff = score["Treble_Staff"], score["Bass_Staff"]
    >>> duration = abjad.Duration(1, 32)
    >>> pitches = range(-12, 12 + 1)
    >>> for pitch in pitches:
    ...     note = abjad.Note(pitch, duration)
    ...     rest = abjad.Rest(duration)
    ...     if 0 <= note.written_pitch.number:
    ...         treble_staff.append(note)
    ...         bass_staff.append(rest)
    ...     else:
    ...         treble_staff.append(rest)
    ...         bass_staff.append(note)
    ...     number = note.written_pitch.number
    ...     string = rf"\markup {number}"
    ...     markup = abjad.Markup(string, direction=abjad.Down)
    ...     abjad.attach(markup, bass_staff[-1])
    ...
    >>> clef = abjad.Clef("bass")
    >>> note = abjad.select(bass_staff).note(0)
    >>> abjad.attach(clef, note)

::

    >>> preamble =r"""#(set-global-staff-size 15)
    ...
    ... \layout {
    ...     \context {
    ...         \Score
    ...         \override Beam.transparent = ##t
    ...         \override Flag.transparent = ##t
    ...         \override Rest.transparent = ##t
    ...         \override Stem.stencil = ##f
    ...         \override TextScript.staff-padding = #6
    ...         \override TimeSignature.stencil = ##f
    ...         proportionalNotationDuration = #(ly:make-moment 1 56)
    ...     }
    ... }"""

    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

Diatonic pitch numbers
----------------------

Abjad numbers diatonic pitches like this:

::

    >>> score = abjad.illustrators.make_piano_score()
    >>> treble_staff, bass_staff = score["Treble_Staff"], score["Bass_Staff"]
    >>> duration = abjad.Duration(1, 32)
    >>> pitches = []
    >>> diatonic_pitches = [0, 2, 4, 5, 7, 9, 11]
    >>> pitches.extend([-24 + x for x in diatonic_pitches])
    >>> pitches.extend([-12 + x for x in diatonic_pitches])
    >>> pitches.extend([0 + x for x in diatonic_pitches])
    >>> pitches.extend([12 + x for x in diatonic_pitches])
    >>> pitches.append(24)
    >>> for pitch in pitches:
    ...     note = abjad.Note(pitch, duration)
    ...     rest = abjad.Rest(duration)
    ...     if 0 <= note.written_pitch.number:
    ...         treble_staff.append(note)
    ...         bass_staff.append(rest)
    ...     else:
    ...         treble_staff.append(rest)
    ...         bass_staff.append(note)
    ...     number = note.written_pitch._get_diatonic_pitch_number()
    ...     string = rf"\markup {number}"
    ...     markup = abjad.Markup(string, direction=abjad.Down)
    ...     abjad.attach(markup, bass_staff[-1])
    ...
    >>> clef = abjad.Clef("bass")
    >>> note = abjad.select(bass_staff).note(0)
    >>> abjad.attach(clef, note)

    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

Accidental abbreviations
------------------------

Abjad abbreviates accidentals like this:

    ======================         ============================
    accidental name                abbreviation
    ======================         ============================
    quarter sharp                  "qs"
    quarter flat                   "qf"
    sharp                          "s"
    flat                           "f"
    three-quarters sharp           "tqs"
    three-quarters flat            "tqf"
    double sharp                   "ss"
    double flat                    "ff"
    ======================         ============================

Octave designation
------------------

Abjad designates octaves with both numbers and ticks:

    ===============        =============
    octave notation        tick notation
    ===============        =============
    C7                     c''''
    C6                     c'''
    C5                     c''
    C4                     c'
    C3                     c
    C2                     c,
    C1                     c,,
    ===============        =============

Default accidental spelling
---------------------------

Abjad picks between enharmonic equivalents according to the following table:

    ============================        ====================================
    pitch-class number                  pitch-class name
    ============================        ====================================
    0                                   C
    1                                   C#
    2                                   D
    3                                   Eb
    4                                   E
    5                                   F
    6                                   F#
    7                                   G
    8                                   Gb
    9                                   A
    10                                  Bb
    11                                  B
    ============================        ====================================
