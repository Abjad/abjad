def transpose_chromatic_pitch_number_by_octave_transposition_mapping(chromatic_pitch_number, mapping):
    '''.. versionadded:: 1.1

    Transpose `chromatic_pitch_number` by the some number of octaves up or down.
    Derive correct number of octaves from `mapping` where
    `mapping` is a list of ``(range_spec, octave)`` pairs
    and ``range_spec`` is, in turn, a ``(start, stop)`` pair
    suitable to pass to the built-in Python ``range()`` function::

        abjad> mapping = [((-39, -13), 0), ((-12, 23), 12), ((24, 48), 24)]

    The mapping given here comprises three ``(range_spec, octave)`` pairs.
    The first such pair is ``((-39, -13), 0)`` and can be read as follows:
    "any pitches between ``-39`` and ``-13`` should be transposed into the
    octave rooted at pitch ``0``." The octave rooted at pitch ``0``
    equals the twelve pitches ``range(0, 0 + 12)`` or
    ``[0, 1, ..., 10, 11]``.

    The second ``(range_spec, octave)`` pair is ``((-12, 23), 12)`` and
    can be read as "any pitches between ``-12`` and ``23`` should be
    transposed into the octave rooted at pitch ``12``," with the octave
    rooted at pitch ``12`` equal to the twelve pitches
    ``range(12, 12 + 12)`` or ``[12, 13, ..., 22, 23]``.

    The third and last ``(range_spec, octave)`` pair is ``((24, 48), 24)``
    and can be read as "any pitches between ``24`` and ``48`` should
    be transposed to the octave rooted at ``24``," with the octave
    rooted at ``24`` equal to the twelve pitches ``range(24, 24, + 12)``
    or ``[24, 25, ..., 34, 35]``.

    The mapping given here divides
    the compass of the piano, from ``-39`` to ``48``, into three
    disjunct subranges and then explains how to transpose pitches
    found in any of those three disjunct subranges. This means that,
    for example, all the f-sharps within the range of the piano now
    undergo a known transposition under `mapping` as defined here::

        abjad> pitchtools.transpose_chromatic_pitch_number_by_octave_transposition_mapping(-30, mapping)
        6

    We verify that pitch ``-30`` should map to pitch ``6`` by noticing
    that pitch ``-30`` falls in the first of the three subranges
    defined by `mapping` from ``-39`` to ``-13`` and then noting
    that `mapping` sends pitches with that subrange to the octave
    rooted at pitch ``0``. The octave transposition of ``-30`` that
    falls within the octave rooted at ``0`` is ``6``::

        abjad> pitchtools.transpose_chromatic_pitch_number_by_octave_transposition_mapping(-18, mapping)
        6

    Likewise, `mapping` sends pitch ``-18`` to pitch ``6`` because
    pitch ``-18`` falls in the same subrange from ``-39`` to ``-13``
    as did pitch ``-39`` and so undergoes the same transposition to
    the octave rooted at ``0``.

    In this way we can map all f-sharps from ``-39`` to ``48`` according
    to `mapping`::

        abjad> pitch_numbers = [-30, -18, -6, 6, 18, 30, 42]
        abjad> for n in pitch_numbers:
        ...   n, pitchtools.transpose_chromatic_pitch_number_by_octave_transposition_mapping(n, mapping)
        (-30, 6)
        (-18, 6)
        (-6, 18)
        (6, 18)
        (18, 18)
        (30, 30)
        (42, 30)

    And so on.

    Return chromatic pitch number.

    .. versionchanged:: 2.0
        renamed ``pitchtools.send_pitch_number_to_octave()`` to
        ``pitchtools.transpose_chromatic_pitch_number_by_octave_transposition_mapping()``.
    '''

    target_pitch_class = chromatic_pitch_number % 12

    for ((start, stop), octave_root) in mapping:
        source_range = range(start, stop + 1)
        if chromatic_pitch_number in source_range:
            target_octave = range(octave_root, octave_root + 12)
            for candidate_pitch in target_octave:
                candidate_pitch_class = candidate_pitch % 12
                if candidate_pitch_class == target_pitch_class:
                    return candidate_pitch
