Hexchordal recombination, by dyad
---------------------------------

Double-stop creation from hexachord pairs in Luigi Nono's `Fragmente -- Stille, an
Diotima`:

Define tone row and divide into hexachords:

::

    >>> scale = abjad.PitchSegment(["cs''", "d''", "ef''", "e''", "f''", "fs''", "g''", "gs''", "a''", "bf''", "b''", "c'''"])
    >>> hexachord_1 = [_ for _ in scale[:6]]
    >>> hexachord_2 = [_ for _ in scale[6:]]

Isolate diads from paired hexachords:

::

    >>> diads = [list(_) for _ in zip(hexachord_1, hexachord_2)]
    >>> reversed_indices = [1, 2, 4, 5]
    >>> for index in reversed_indices:
    ...     diads[index] = (diads[index][1], diads[index][0])
    ...
    >>> staff = abjad.Staff()
    >>> for diad in diads:
    ...     lower = diad[0]
    ...     higher = diad[1]
    ...     while higher < lower:
    ...         higher = abjad.NamedInterval("+P8").transpose(higher)
    ...     chord = abjad.Chord([lower, higher], (1, 8))
    ...     staff.append(chord)
    ...

Change octaves:

::

    >>> staff[2].written_pitches = abjad.NamedInterval("+P8").transpose(staff[2].written_pitches)
    >>> staff[3].written_pitches = abjad.NamedInterval("+P8").transpose(staff[3].written_pitches)
    >>> staff[4].written_pitches = abjad.NamedInterval("-P8").transpose(staff[4].written_pitches)
    >>> staff[5].written_pitches = abjad.NumberedInterval("-24").transpose(staff[5].written_pitches)

Override staff settings:

::

    >>> abjad.override(staff).Beam.stencil = "##f"
    >>> abjad.override(staff).Flag.stencil = "##f"
    >>> abjad.override(staff).Stem.stencil = "##f"
    >>> abjad.override(staff).text_script.staff_padding = 4
    >>> abjad.override(staff).TimeSignature.stencil = "##f"
    >>> score = abjad.Score([staff])
    >>> abjad.setting(score).proportional_notation_duration = abjad.SchemeMoment(
    ...     (1, 20)
    ... )

Show score:

::

    >>> abjad.show(score)
