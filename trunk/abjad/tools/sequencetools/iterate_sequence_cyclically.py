import itertools


# TODO: merge with sequencetools.repeat_to_length() #

def iterate_sequence_cyclically(sequence, step=1, start=0, length='inf'):
    '''.. versionadded:: 1.1

    Iterate `sequence` cyclically according to `step`, `start` and `length`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequence = [1, 2, 3, 4, 5, 6, 7]

    ::

        abjad> list(sequencetools.iterate_sequence_cyclically(sequence, length = 20))
        [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6]

    ::

        abjad> list(sequencetools.iterate_sequence_cyclically(sequence, 2, length = 20))
        [1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4]

    ::

        abjad> list(sequencetools.iterate_sequence_cyclically(sequence, 2, 3, length = 20))
        [4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7]

    ::

        abjad> list(sequencetools.iterate_sequence_cyclically(sequence, -2, 5, length = 20))
        [6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3]

    .. versionchanged:: 2.0
        allows generator input.

    ::

        abjad> list(sequencetools.iterate_sequence_cyclically(xrange(1, 8), -2, 5, length = 20))
        [6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3]

    Set `step` to jump size and direction across sequence.

    Set `start` to the index of `sequence` where the function begins iterating.

    Set `length` to number of elements to return. Set to ``'inf'`` to return infinitely.

    Return generator.

    .. versionchanged:: 2.0
        renamed ``sequencetools.phasor()`` to
        ``sequencetools.iterate_sequence_cyclically()``.
    '''

    #assert isinstance(iterable, list)
    assert isinstance(step, int)
    assert isinstance(start, int)
    if isinstance(length, str):
        assert length == 'inf'
    else:
        assert isinstance(length, int)

    # itertools.islice() does not handle negative step.
    # so we divided iterable into two halves from start index.
    # then we reverse those two halves.
    # then we recombined the halves and pass positive step.
    if step < 0:
        step = abs(step)
        list_iterable = list(sequence)
        left, right = reversed(list_iterable[:start-1]), reversed(list_iterable[start-1:])
        sequence = itertools.chain(left, right)

    # iterate and yield
    total = 0
    for x in itertools.islice(itertools.cycle(sequence), start, None, step):
        yield x
        total += 1
        if not length == 'inf':
            if total == length:
                raise StopIteration
