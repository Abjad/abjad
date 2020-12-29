Hexchordal recombination, by dyad
---------------------------------

Double-stop creation from hexachord pairs in Luigi Nono's `Fragmente -- Stille, an
Diotima`:

----

First we define functions to illustrate the examples that follow:

::

    >>> def illustrate_collection(sequence, reversed_indices, transpositions, moment_denominator):
    ...     center = int(len(sequence) / 2)
    ...     hexachord_1 = [_ for _ in sequence[:center]]
    ...     hexachord_2 = [_ for _ in sequence[center:]]
    ...     diads = [list(_) for _ in zip(hexachord_1, hexachord_2)]
    ...     for index in reversed_indices:
    ...        diads[index] = (diads[index][1], diads[index][0])
    ...     notes = []
    ...     for diad in diads:
    ...         lower = diad[0]
    ...         higher = diad[1]
    ...         while higher < lower:
    ...             higher = abjad.NamedInterval("+P8").transpose(higher)
    ...         chord = abjad.Chord([lower, higher], (1, 8))
    ...         notes.append(chord)
    ...     for pair in transpositions:
    ...         written_pitches = notes[pair[0]].written_pitches
    ...         interval = abjad.NumberedInterval(pair[1])
    ...         notes[pair[0]].written_pitches = interval.transpose(written_pitches)
    ...     containers = abjad.illustrators.make_piano_score(notes)
    ...     score, treble_staff, bass_staff = containers
    ...     abjad.override(score).BarLine.stencil = False
    ...     abjad.override(score).Beam.stencil = False
    ...     abjad.override(score).Flag.stencil = False
    ...     abjad.override(score).Rest.stencil = False
    ...     abjad.override(score).SpacingSpanner.strict_note_spacing = True
    ...     abjad.override(score).SpanBar.stencil = False
    ...     abjad.override(score).Stem.stencil = False
    ...     abjad.override(score).TimeSignature.stencil = False
    ...     moment = abjad.SchemeMoment((1, moment_denominator))
    ...     abjad.setting(score).proportional_notation_duration = moment
    ...     lilypond_file = abjad.LilyPondFile(items=[score], global_staff_size=16)
    ...     return lilypond_file

----

Show Nono dyads:

::

    >>> scale = abjad.PitchSegment(
    ...     [
    ...         "cs''",
    ...         "d''",
    ...         "ef''",
    ...         "e''",
    ...         "f''",
    ...         "fs''",
    ...         "g''",
    ...         "gs''",
    ...         "a''",
    ...         "bf''",
    ...         "b''",
    ...         "c'''",
    ...     ],
    ... )
    ...
    >>> file = illustrate_collection(
    ...     scale,
    ...     [1, 2, 4, 5],
    ...     [(2, "+12"), (3, "+12"), (4, "-12"), (5, "-24")],
    ...     25,
    ... )
    ...
    >>> abjad.show(file)

Show alternate dyads:

::

    >>> scale = abjad.PitchSegment(
    ...     [
    ...         0,
    ...         1,
    ...         4,
    ...         6,
    ...         2,
    ...         3,
    ...         5,
    ...         9,
    ...     ],
    ... )
    ...
    >>> file = illustrate_collection(
    ...     scale,
    ...     [2, 3],
    ...     [(0, "-12"), (2, "-24"), (3, "+12")],
    ...     25,
    ... )
    ...
    >>> abjad.show(file)
