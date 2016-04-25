# -*- coding: utf-8 -*-
import collections


def iterate_sequence_boustrophedon(iterable, duplicates=False):
    '''Iterates `iterable` boustrophedon.

    ..  container:: example

        Iterates `iterable` first forward and then backward.
        Duplicates neither first nor last elements:

        ::

            >>> iterable = [1, 2, 3, 4, 5]
            >>> generator = sequencetools.iterate_sequence_boustrophedon(
            ...     iterable, duplicates=False)
            >>> list(generator)
            [1, 2, 3, 4, 5, 4, 3, 2]

    ..  container:: example

        Iterates `iterable` first forward and then backward.
        Duplicates both first and last elements:

        ::

            >>> iterable = [1, 2, 3, 4, 5]
            >>> generator = sequencetools.iterate_sequence_boustrophedon(
            ...     iterable, duplicates=True)
            >>> list(generator)
            [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]

    Returns generator.
    '''

    if not isinstance(iterable, collections.Iterable):
        message = 'must be iterable: {!r}.'
        message = message.format(iterable)
        raise Exception(message)

    if duplicates:
        sequence_copy = []
        for x in iterable:
            yield x
            sequence_copy.append(x)
        for x in reversed(sequence_copy):
            yield x
    else:
        sequence_copy = []
        for x in iterable:
            yield x
            sequence_copy.append(x)
        for x in reversed(sequence_copy[1:-1]):
            yield x
