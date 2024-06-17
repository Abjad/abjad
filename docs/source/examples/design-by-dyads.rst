Design, by dyads
================

..

----

The function below pairs pitches at corresponding positions in a segment partitioned into
halves. A sequence of two-note chords results. A first optional parameter flips the
pitches in chords specified by index. A second optional parameter transposes chords,
specified again by index. Two examples follow. The first operates on the regular
structure of an ascending chromatic scale. The second successively tranforms a segment
with greater intervallic variety. The implementation given here generalizes a process due
to Luigi Nono:

::

    >>> def partition(string, flip=None, transpositions=None):
    ...     strings = string.split()
    ...     assert len(strings) % 2 == 0, repr(string)
    ...     segment = [abjad.NamedPitch(_) for _ in strings]
    ...     flip = flip or []
    ...     transpositions = dict(transpositions or [])
    ...     center = int(len(segment) / 2)
    ...     left = segment[:center]
    ...     right = segment[center:]
    ...     pairs = zip(left, right)
    ...     chords = []
    ...     for i, pair in enumerate(pairs):
    ...         chord = abjad.Chord(pair, (1, 4))
    ...         if i in flip:
    ...             pitches = chord.written_pitches
    ...             lower, higher = pitches
    ...             while lower < higher:
    ...                 lower = lower + "+P8" 
    ...             chord.written_pitches = [lower, higher]
    ...         interval = transpositions.get(i, "P1")
    ...         pitches = tuple(_.transpose(interval) for _ in chord.written_pitches)
    ...         chord.written_pitches = pitches
    ...         chords.append(chord)
    ...     return chords

LilyPond settings to format examples:

::

    >>> preamble = r"""#(set-global-staff-size 16)
    ...
    ... \layout {
    ...     \context {
    ...         \Score
    ...         \override BarLine.stencil = ##f
    ...         \override BarNumber.stencil = ##f
    ...         \override Beam.stencil = ##f
    ...         \override Flag.stencil = ##f
    ...         \override Rest.stencil = ##f
    ...         \override SpacingSpanner.strict-note-spacing = ##t
    ...         \override SpanBar.stencil = ##f
    ...         \override Stem.stencil = ##f
    ...         \override TimeSignature.transparent = ##t
    ...         proportionalNotationDuration = \musicLength 16
    ...     }
    ... }
    ... """

----

Examples
--------

**Example 1a.** Ascending chromatic scale:

    >>> string = "cs'' d'' ef'' e'' f'' fs'' g'' gs'' a'' bf'' b'' c'''"
    >>> notes = [abjad.Note(_, (1, 4)) for _ in string.split()]
    >>> score = abjad.illustrators.make_piano_score(notes)
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

**Example 1b.** Starting segment; partitioned:

    >>> string = "cs'' d'' ef'' e'' f'' fs'' g'' gs'' a'' bf'' b'' c'''"
    >>> chords = partition(string)
    >>> score = abjad.illustrators.make_piano_score(chords)
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

**Example 1c.** Starting segment; partitioned; chords at indexes 1, 2, 4, 5 flipped:

    >>> string = "cs'' d'' ef'' e'' f'' fs'' g'' gs'' a'' bf'' b'' c'''"
    >>> chords = partition(string, flip=[1, 2, 4, 5])
    >>> score = abjad.illustrators.make_piano_score(chords)
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

**Example 1d.** Starting segment; partitioned; chords 1, 2, 4, 5 flipped; chords at
indexes 2, 3, 4, 5 selectively transposed:

    >>> string = "cs'' d'' ef'' e'' f'' fs'' g'' gs'' a'' bf'' b'' c'''"
    >>> transpositions = [(2, "+12"), (3, "+12"), (4, "-12"), (5, "-24")]
    >>> chords = partition(string, flip=[1, 2, 4, 5], transpositions=transpositions)
    >>> score = abjad.illustrators.make_piano_score(chords)
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

This example reproduces violin double stops in Luigi Nono's *Fragment --- Stille, an
Diotima* (1980).

----

**Example 2a.** Starting segment written by hand:

    >>> string = "d, b af c'' a' fs'' g'' gs'' as'' b'' d'' f' g' ef' e df c bf,"
    >>> notes = [abjad.Note(_, (1, 4)) for _ in string.split()]
    >>> score = abjad.illustrators.make_piano_score(notes)
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

**Example 2b.** Starting segment; partitioned:

    >>> string = "d, b af c'' a' fs'' g'' gs'' as'' b'' d'' f' g' ef' e df c bf,"
    >>> chords = partition(string)
    >>> score = abjad.illustrators.make_piano_score(chords)
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

**Example 2c.** Starting segment; partitioned; chords at indexes 0, 1, 2, 4 flipped:

    >>> string = "d, b af c'' a' fs'' g'' gs'' as'' b'' d'' f' g' ef' e df c bf,"
    >>> chords = partition(string, flip=[0, 1, 2, 4])
    >>> score = abjad.illustrators.make_piano_score(chords)
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

**Example 2d.** Starting segment; partitioned; chords 0, 1, 2, 4 flipped; chords at
indexes 0, 1 selectively transposed:

    >>> string = "d, b af c'' a' fs'' g'' gs'' as'' b'' d'' f' g' ef' e df c bf,"
    >>> transpositions = [(0, "-36"), (1, "-24")]
    >>> chords = partition(string, flip=[0, 1, 2, 4], transpositions=transpositions)
    >>> score = abjad.illustrators.make_piano_score(chords)
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

:author:`[Evans (3.2), Bača (3.2, 3.7); generalized from Luigi Nono, example 1d, above.]`
