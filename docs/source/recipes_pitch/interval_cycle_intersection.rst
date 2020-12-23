Interval cycle intersection
---------------------------

Derived tone rows from inversionally related interval cycles in Milton Babbitt's
`Partitions for Piano`:

Define helper function for creating interval cycles:

::

    >>> def perle_cyclic_set(starting_pitch, interval):
    ...     returned_list = [starting_pitch]
    ...     for _ in range(10):
    ...         val = returned_list[-1] + interval
    ...         val %= 12
    ...         returned_list.append(val)
    ...     return returned_list

Define helper function to intersect cycles:

::

    >>> def intersect_sequences(seq_1, seq_2, pattern_1, pattern_2, length):
    ...     returned_list = []
    ...     for index in range(length):
    ...         match_1 = pattern_1.matches_index(index, length)
    ...         match_2 = pattern_2.matches_index(index, length)
    ...         if match_1:
    ...             value = seq_1.pop(0)
    ...             returned_list.append(value)
    ...         elif match_2:
    ...             value = seq_2.pop(0)
    ...             returned_list.append(value)
    ...         else:
    ...             returned_list.append(None)
    ...     return returned_list

Create first intersection:

::

    >>> ic1_p5 = perle_cyclic_set(starting_pitch=5, interval=1)
    >>> ic1_p2 = perle_cyclic_set(starting_pitch=2, interval=1)
    >>> ic1_p5_pattern = abjad.Pattern(
    ...     indices=[0, 2, 4],
    ...     period=6,
    ... )
    >>> ic1_p2_pattern = abjad.Pattern(
    ...     indices=[1, 3, 5],
    ...     period=6,
    ... )
    >>> intersection_1 = intersect_sequences(ic1_p5, ic1_p2, ic1_p5_pattern, ic1_p2_pattern, 6)

Create second intersection:

::

    >>> ic11_p10 = perle_cyclic_set(starting_pitch=10, interval=11)
    >>> ic11_p1 = perle_cyclic_set(starting_pitch=1, interval=11)
    >>> ic11_p10_pattern = abjad.Pattern(
    ...     indices=[0, 2, 4],
    ...     period=6,
    ... )
    >>> ic11_p1_pattern = abjad.Pattern(
    ...     indices=[1, 3, 5],
    ...     period=6,
    ... )
    >>> intersection_2 = intersect_sequences(ic11_p10, ic11_p1, ic11_p10_pattern, ic11_p1_pattern, 6)

Create and override staff:

::

    >>> row = abjad.TwelveToneRow(intersection_1 + intersection_2)
    >>> staff = abjad.Staff([abjad.Note(_, (1, 8)) for _ in row])
    >>> abjad.attach(abjad.TimeSignature((6, 8)), staff[0])
    >>> abjad.label(staff).with_intervals(prototype=abjad.NumberedIntervalClass)
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


