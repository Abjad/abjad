from abjad.tools import mathtools
from numbers import Number


def _repeat_sequence_to_weight(sequence, weight, remainder = 'chop'):
    '''Repeat sequence to weight exactly::

        abjad> from abjad.tools.sequencetools._repeat_sequence_to_weight import _repeat_sequence_to_weight

        abjad> _repeat_sequence_to_weight([5, 5, 5], 23)
        [5, 5, 5, 5, 3]

    Repeat sequence to weight at most::

        abjad> _repeat_sequence_to_weight([5, 5, 5], 23, remainder = 'less')
        [5, 5, 5, 5]

    Repeat sequence to weight at least::

        abjad> _repeat_sequence_to_weight([5, 5, 5], 23, remainder = 'more')
        [5, 5, 5, 5, 5]

    .. versionchanged:: 2.0
        renamed ``listtools.repeat_list_to_weight()`` to
        ``sequencetools.repeat_sequence_to_weight()``.
    '''

    assert isinstance(weight, Number)
    assert 0 <= weight

    result = []
    result.append(sequence[0])
    i = 1
    while mathtools.weight(result) < weight:
        result.append(sequence[i % len(sequence)])
        i += 1
    if weight < mathtools.weight(result):
        if remainder == 'less':
            result = result[:-1]
        elif remainder == 'chop':
            last_sign = mathtools.sign(result[-1])
            needed_weight = weight - mathtools.weight(result[:-1])
            result = result[:-1] + [last_sign * needed_weight]
        elif remainder == 'more':
            pass
    return type(sequence)(result)
