:orphan:

Interval cycle intersection
===========================

Derived tone rows from inversionally related interval cycles in Milton Babbitt's
`Partitions for Piano` (1957).

----

::

    >>> def perle_cyclic_set(starting_pitch, interval):
    ...     returned_list = [starting_pitch]
    ...     for _ in range(10):
    ...         val = returned_list[-1] + interval
    ...         val %= 12
    ...         returned_list.append(val)
    ...     return returned_list

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

::

    >>> def make_row(
    ...     cyclic_interval,
    ...     transposed_interval,
    ...     hexachord_pattern,
    ...     second_hex_transposition,
    ... ):
    ...     first_cycle = perle_cyclic_set(
    ...         starting_pitch=0,
    ...         interval=cyclic_interval,
    ...     )
    ...     second_cycle = perle_cyclic_set(
    ...         starting_pitch=transposed_interval,
    ...         interval=cyclic_interval,
    ...     )
    ...     p1 = abjad.Pattern(
    ...         hexachord_pattern,
    ...         period=6,
    ...     )
    ...     p2 = abjad.Pattern(
    ...         hexachord_pattern,
    ...         period=6,
    ...         inverted=True,
    ...     )
    ...     intersection_1 = intersect_sequences(
    ...         first_cycle,
    ...         second_cycle,
    ...         p1,
    ...         p2,
    ...         6,
    ...     )
    ...     third_cycle = perle_cyclic_set(
    ...         starting_pitch=(second_hex_transposition % 12),
    ...         interval=((12 - cyclic_interval) % 12),
    ...     )
    ...     fourth_cycle = perle_cyclic_set(
    ...         starting_pitch=((second_hex_transposition - transposed_interval) % 12),
    ...         interval=((12 - cyclic_interval) % 12),
    ...     )
    ...     p3 = abjad.Pattern(
    ...         hexachord_pattern,
    ...         period=6,
    ...     )
    ...     p4 = abjad.Pattern(
    ...         hexachord_pattern,
    ...         period=6,
    ...         inverted=True,
    ...     )
    ...     intersection_2 = intersect_sequences(
    ...         third_cycle,
    ...         fourth_cycle,
    ...         p3,
    ...         p4,
    ...         6,
    ...     )
    ...     row = abjad.TwelveToneRow(intersection_1 + intersection_2)
    ...     return row

----

Examples
--------

**Example 1.** What is this?

::

    >>> row = make_row(1, 9, [0, 2, 4], 5)
    >>> abjad.show(row)

----

**Example 2.** What is this?

::

    >>> row = make_row(1, 3, [0, 1, 3], -1)
    >>> abjad.show(row)

:author:`[Evans (3.2). From Milton Babbit's Partitions for Piano (1957).]`
