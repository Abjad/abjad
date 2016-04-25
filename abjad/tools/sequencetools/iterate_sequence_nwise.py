# -*- coding: utf-8 -*-
import collections


def iterate_sequence_nwise(iterable, n=2, cyclic=False, wrapped=False):
    '''Iterates elements in `iterable` `n` at a time.

    ..  container:: example

        Iterates iterable by pairs:

        ::

            >>> for x in sequencetools.iterate_sequence_nwise(range(10)):
            ...     x
            ...
            (0, 1)
            (1, 2)
            (2, 3)
            (3, 4)
            (4, 5)
            (5, 6)
            (6, 7)
            (7, 8)
            (8, 9)

    ..  container:: example

        Iterates iterable by triples:

        ::

            >>> for x in sequencetools.iterate_sequence_nwise(range(10), n=3):
            ...     x
            ...
            (0, 1, 2)
            (1, 2, 3)
            (2, 3, 4)
            (3, 4, 5)
            (4, 5, 6)
            (5, 6, 7)
            (6, 7, 8)
            (7, 8, 9)


    ..  container:: example

        Iterates iterable by pairs. Wraps around at end:

        ::

            >>> for x in sequencetools.iterate_sequence_nwise(
            ...     range(10), n=2, wrapped=True):
            ...     x
            ...
            (0, 1)
            (1, 2)
            (2, 3)
            (3, 4)
            (4, 5)
            (5, 6)
            (6, 7)
            (7, 8)
            (8, 9)
            (9, 0)

    ..  container:: example

        Iterates iterable by triples. Wraps around at end:

        ::

            >>> for x in sequencetools.iterate_sequence_nwise(
            ...     range(10), n=3, wrapped=True):
            ...     x
            ...
            (0, 1, 2)
            (1, 2, 3)
            (2, 3, 4)
            (3, 4, 5)
            (4, 5, 6)
            (5, 6, 7)
            (6, 7, 8)
            (7, 8, 9)
            (8, 9, 0)
            (9, 0, 1)

    ..  container:: example

        Iterates iterable by pairs. Cycles indefinitely:

        ::

            >>> pairs = sequencetools.iterate_sequence_nwise(
            ...     range(10), n=2, cyclic=True)
            >>> for _ in range(15):
            ...     next(pairs)
            (0, 1)
            (1, 2)
            (2, 3)
            (3, 4)
            (4, 5)
            (5, 6)
            (6, 7)
            (7, 8)
            (8, 9)
            (9, 0)
            (0, 1)
            (1, 2)
            (2, 3)
            (3, 4)
            (4, 5)

        Returns infinite generator.

    ..  container:: example

        Iterates iterable by triples. Cycles indefinitely:

        ::

            >>> triples = sequencetools.iterate_sequence_nwise(
            ...     range(10), n=3, cyclic=True)
            ...
            >>> for _ in range(15):
            ...     next(triples)
            (0, 1, 2)
            (1, 2, 3)
            (2, 3, 4)
            (3, 4, 5)
            (4, 5, 6)
            (5, 6, 7)
            (6, 7, 8)
            (7, 8, 9)
            (8, 9, 0)
            (9, 0, 1)
            (0, 1, 2)
            (1, 2, 3)
            (2, 3, 4)
            (3, 4, 5)
            (4, 5, 6)

        Returns infinite generator.

    Ignores ``wrapped`` when ``cyclic=True``.

    Returns generator.
    '''

    if not isinstance(iterable, collections.Iterable):
        message = 'must be iterable: {!r}.'
        message = message.format(iterable)
        raise Exception(message)

    if cyclic:
        element_buffer = []
        long_enough = False
        for element in iterable:
            element_buffer.append(element)
            if not long_enough:
                if n <= len(element_buffer):
                    long_enough = True
            if long_enough:
                yield tuple(element_buffer[-n:])
        len_sequence = len(element_buffer)
        current = len_sequence - n + 1
        while True:
            output = []
            for local_offset in range(n):
                index = (current + local_offset) % len_sequence
                output.append(element_buffer[index])
            yield tuple(output)
            current += 1
            current %= len_sequence
    elif wrapped:
        first_n_minus_1 = []
        element_buffer = []
        for element in iterable:
            element_buffer.append(element)
            if len(element_buffer) == n:
                yield tuple(element_buffer)
                element_buffer.pop(0)
            if len(first_n_minus_1) < n - 1:
                first_n_minus_1.append(element)
        element_buffer = element_buffer + first_n_minus_1
        if element_buffer:
            for x in range(n - 1):
                yield tuple(element_buffer[x:x+n])
    else:
        element_buffer = []
        for element in iterable:
            element_buffer.append(element)
            if len(element_buffer) == n:
                yield tuple(element_buffer)
                element_buffer.pop(0)
