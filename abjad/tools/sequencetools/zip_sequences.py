# -*- coding: utf-8 -*_
import collections


def zip_sequences(iterables, cyclic=False, truncate=True):
    r'''Zips `iterables`.

    ..  container:: example

        **Example 1.** Zips two `iterables` cyclically:

        ::

            >>> iterables = [[1, 2, 3], ['a', 'b']]
            >>> sequencetools.zip_sequences(iterables, cyclic=True)
            [(1, 'a'), (2, 'b'), (3, 'a')]

    ..  container:: example

        **Example 2.** Zips three `iterables` cyclically:

        ::

            >>> iterables = [[10, 11, 12], [20, 21], [30, 31, 32, 33]]
            >>> sequencetools.zip_sequences(iterables, cyclic=True)
            [(10, 20, 30), (11, 21, 31), (12, 20, 32), (10, 21, 33)]

    ..  container:: example

        **Example 3.** Zips iterables without truncation:

        ::

            >>> iterables = ([1, 2, 3, 4], [11, 12, 13], [21, 22, 23])
            >>> sequencetools.zip_sequences(iterables, truncate=False)
            ((1, 11, 21), (2, 12, 22), (3, 13, 23), (4,))

    ..  container:: example

        ** Example 4.** Zips iterables noncyclically and with truncation.
        Equivalent to built-in ``zip()``:

        ::

            >>> iterables = ([1, 2, 3, 4], [11, 12, 13], [21, 22, 23])
            >>> sequencetools.zip_sequences(iterables)
            ((1, 11, 21), (2, 12, 22), (3, 13, 23))

    Returns new object of `iterables` type.
    '''

    for iterable in iterables:
        if not isinstance(iterable, collections.Iterable):
            message = 'must by iterable {!r}.'
            message = message.format(iterable)
            raise Exception(message)

    sequences_type = type(iterables)

    if cyclic:
        result = []
        if not min(len(x) for x in iterables):
            return result
        max_length = max([len(x) for x in iterables])
        for i in range(max_length):
            part = []
            for iterable in iterables:
                index = i % len(iterable)
                element = iterable[index]
                part.append(element)
            part = tuple(part)
            result.append(part)
    elif not truncate:
        result = []
        max_length = max([len(x) for x in iterables])
        for i in range(max_length):
            part = []
            for iterable in iterables:
                try:
                    part.append(iterable[i])
                except IndexError:
                    pass
            result.append(tuple(part))
    elif truncate:
        result = list(zip(*iterables))

    result = sequences_type(result)
    return result
