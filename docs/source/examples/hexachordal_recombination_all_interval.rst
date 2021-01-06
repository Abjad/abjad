Hexachordal recombination, all-interval
---------------------------------------

Elliott Carter's parallel-inverted all-interval collections.

----

First we define functions to illustrate the examples that follow:

::

    >>> def illustrate_collection(hexachord, starting_pitch, moment_denominator):
    ...     notes = []
    ...     s1 = hexachord
    ...     s2 = s1.invert().transpose(s1[-1].number + 6)
    ...     full_sequence = abjad.PitchSegment(s1 + s2)
    ...     transposed_sequence = full_sequence.transpose(starting_pitch)
    ...     vertical_sequence = [full_sequence[0] + starting_pitch]
    ...     for pitch in transposed_sequence[1:]:
    ...         pitch_number = pitch.number
    ...         while pitch_number < vertical_sequence[-1]:
    ...             pitch_number += 12
    ...         vertical_sequence.append(pitch_number)
    ...     notes = [abjad.Note(_, (1, 16)) for _ in vertical_sequence]
    ...     containers = abjad.illustrators.make_piano_score(notes)
    ...     score, treble_staff, bass_staff = containers
    ...     abjad.override(score).BarLine.stencil = False
    ...     abjad.override(score).BarNumber.stencil = False
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

Define appropriately invertible hexachords:

::

    >>> source_hex = abjad.PitchClassSegment([0, 4, 9, 10, 8, 5])
    >>> hexachord_permutations = [
    ...     source_hex,
    ...     source_hex.invert(),
    ...     source_hex.retrograde().transpose((0 - source_hex[-1].number)),
    ...     source_hex.retrograde().transpose((0 - source_hex[-1].number)).invert(),
    ... ]
    ...

Illustrate parallel-inverted collection from first hexachord permutation:

::

    >>> file = illustrate_collection(hexachord_permutations[0], -24, 25)
    >>> abjad.show(file)

Illustrate parallel-inverted collection from second hexachord permutation:

::

    >>> file = illustrate_collection(hexachord_permutations[1], -24, 25)
    >>> abjad.show(file)

Illustrate parallel-inverted collection from third hexachord permutation:

::

    >>> file = illustrate_collection(hexachord_permutations[2], -24, 25)
    >>> abjad.show(file)

Illustrate parallel-inverted collection from fourth hexachord permutation:

::

    >>> file = illustrate_collection(hexachord_permutations[3], -24, 25)
    >>> abjad.show(file)

:author:`[Authored: Bača/Evans (3.2).]`
