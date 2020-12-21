Hexachordal recombination, all-interval
---------------------------------------

Elliott Carter's parallel-inverted all-interval collections:

Define appropriately invertible hexachords:

::

    >>> import abjad
    ...
    >>> score = abjad.Score()
    >>> group = abjad.StaffGroup()
    >>> source_hex = abjad.PitchClassSegment([0, 4, 9, 10, 8, 5])
    >>> source_hexachords = [
    ...     source_hex,
    ...     source_hex.invert(),
    ...     source_hex.retrograde().transpose((0 - source_hex[-1].number)),
    ...     source_hex.retrograde().transpose((0 - source_hex[-1].number)).invert(),
    ... ]
    ...

Iterate over hexachords, combining with hexachord inversion transposed six semitones above the final hexachord pitch, stacking each pitch as an interval above the previous pitch:

::

    >>> for hexachord in source_hexachords:
    ...     s1 = hexachord
    ...     s2 = s1.invert().transpose(s1[-1].number + 6)
    ...     full_sequence = abjad.PitchSegment(s1 + s2)
    ...     transposed_sequence = full_sequence.transpose(-24)
    ...     vertical_sequence = [-24]
    ...     for pitch in transposed_sequence[1:]:
    ...         pitch_number = pitch.number
    ...         while pitch_number < vertical_sequence[-1]:
    ...             pitch_number += 12
    ...         vertical_sequence.append(pitch_number)
    ...     staff = abjad.Staff([abjad.Note(_, (1, 16)) for _ in vertical_sequence])
    ...     abjad.attach(abjad.Clef("bass"), staff[0])
    ...     abjad.attach(abjad.Clef("treble"), staff[4])
    ...     abjad.ottava(staff[8:])
    ...     abjad.label(staff).with_intervals(prototype=abjad.NumberedIntervalClass)
    ...     abjad.override(staff).text_script.staff_padding = 7
    ...     group.append(staff)
    ...

Add staff group to score and override settings:

::

    >>> score.append(group)
    >>> abjad.override(score).Beam.stencil = "##f"
    >>> abjad.override(score).Flag.stencil = "##f"
    >>> abjad.override(score).Stem.stencil = "##f"
    >>> abjad.override(score).TimeSignature.stencil = "##f"
    >>> abjad.override(score).StaffGrouper.staff_staff_spacing = "#'((basic-distance . 20) (minimum-distance . 20) (padding . 2))"
    >>> abjad.setting(score).proportional_notation_duration = abjad.SchemeMoment((1, 45))
    >>> abjad.label(group[0][:6]).color_leaves("red")
    >>> abjad.label(group[0][6:]).color_leaves("blue")
    >>> abjad.label(group[1][:6]).color_leaves("blue")
    >>> abjad.label(group[1][6:]).color_leaves("red")
    >>> abjad.label(group[2][:6]).color_leaves("blue")
    >>> abjad.label(group[2][6:]).color_leaves("red")
    >>> abjad.label(group[3][:6]).color_leaves("red")
    >>> abjad.label(group[3][6:]).color_leaves("blue")
    >>> file = abjad.LilyPondFile.new(
    ...     score,
    ...     includes=["abjad.ily"],
    ... )
    ...

Show file:

::

    >>> abjad.show(file)
