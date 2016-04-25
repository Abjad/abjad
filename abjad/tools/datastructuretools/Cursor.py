# -*- coding: utf-8 -*-
import collections
from abjad.tools.abctools import AbjadObject


class Cursor(AbjadObject):
    r'''A cursor.

    ..  container:: example

        **Example 1.** Gets elements one at a time:

        ::

            >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
            >>> source = datastructuretools.CyclicTuple(source)
            >>> cursor = datastructuretools.Cursor(source=source)

        ::

                >>> cursor.next()
                (13,)
                >>> cursor.next()
                ('da capo',)
                >>> cursor.next()
                (Note("cs'8."),)
                >>> cursor.next()
                ('rit.',)
                >>> cursor.next()
                (13,)
                >>> cursor.next()
                ('da capo',)

    ..  container:: example

        **Example 2.** Gets different numbers of elements at a time:

        ::

            >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
            >>> source = datastructuretools.CyclicTuple(source)
            >>> cursor = datastructuretools.Cursor(source=source)

        ::

            >>> cursor.next(count=2)
            (13, 'da capo')
            >>> cursor.next(count=-1)
            ('da capo',)
            >>> cursor.next(count=2)
            ('da capo', Note("cs'8."))
            >>> cursor.next(count=-1)
            (Note("cs'8."),)
            >>> cursor.next(count=2)
            (Note("cs'8."), 'rit.')
            >>> cursor.next(count=-1)
            ('rit.',)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_position',
        '_source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        source=(),
        position=None,
        ):
        assert isinstance(source, collections.Iterable), repr(source)
        self._source = source
        assert isinstance(position, (int, type(None))), repr(position)
        self._position = position

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a cursor with keyword
        arguments equal to this cursor. Otherwise false.

        Returns true or false.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __hash__(self):
        r'''Hashes cursor.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(Cursor, self).__hash__()

    ### PUBLIC PROPERTIES ###

    @property
    def position(self):
        r'''Gets position.

        ..  container:: example

            **Example 1.** Position starting at none:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = datastructuretools.Cursor(source=source)

            ::

                >>> cursor.position is None
                True

            ::

                >>> cursor.next()
                (13,)
                >>> cursor.next()
                ('da capo',)
                >>> cursor.next()
                (Note("cs'8."),)
                >>> cursor.next()
                ('rit.',)

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = datastructuretools.Cursor(
                ...     source=source,
                ...     position=None,
                ...     )

            ::

                >>> cursor.position is None
                True

            ::

                >>> cursor.next(count=-1)
                ('rit.',)
                >>> cursor.next(count=-1)
                (Note("cs'8."),)
                >>> cursor.next(count=-1)
                ('da capo',)
                >>> cursor.next(count=-1)
                (13,)

            This is default behavior.

        ..  container:: example

            **Example 1.** Position starting at 0:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = datastructuretools.Cursor(
                ...     source=source,
                ...     position=0,
                ...     )

            ::

                >>> cursor.position
                0

            ::

                >>> cursor.next()
                (13,)
                >>> cursor.next()
                ('da capo',)
                >>> cursor.next()
                (Note("cs'8."),)
                >>> cursor.next()
                ('rit.',)

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = datastructuretools.Cursor(
                ...     source=source,
                ...     position=0,
                ...     )

            ::

                >>> cursor.position
                0

            ::

                >>> cursor.next(count=-1)
                ('rit.',)
                >>> cursor.next(count=-1)
                (Note("cs'8."),)
                >>> cursor.next(count=-1)
                ('da capo',)
                >>> cursor.next(count=-1)
                (13,)

            This is default behavior.

        ..  container:: example

            **Example 3.** Position starting at -1:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = datastructuretools.Cursor(
                ...     source=source,
                ...     position=-1,
                ...     )

            ::

                >>> cursor.position
                -1

            ::

                >>> cursor.next()
                ('rit.',)
                >>> cursor.next()
                (13,)
                >>> cursor.next()
                ('da capo',)
                >>> cursor.next()
                (Note("cs'8."),)

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = datastructuretools.Cursor(
                ...     source=source,
                ...     position=-1,
                ...     )

            ::

                >>> cursor.position
                -1

            ::

                >>> cursor.next(count=-1)
                (Note("cs'8."),)
                >>> cursor.next(count=-1)
                ('da capo',)
                >>> cursor.next(count=-1)
                (13,)
                >>> cursor.next(count=-1)
                ('rit.',)

        Returns tuple.
        '''
        return self._position

    @property
    def source(self):
        r'''Gets source.

        ..  container:: example

            **Example 1.** List source:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> cursor = datastructuretools.Cursor(source=source)

            ::

                >>> cursor.source
                [13, 'da capo', Note("cs'8."), 'rit.']

        ..  container:: example

            **Example 2.** Cyclic tuple source:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = datastructuretools.Cursor(source=source)

            ::

                >>> cursor.source
                CyclicTuple([13, 'da capo', Note("cs'8."), 'rit.'])

        Returns source.
        '''
        return self._source

    ### PUBLIC METHODS ###

    def next(self, count=1):
        r'''Gets next `count` elements in source.

        ..  container:: example

            **Example 1.** Gets elements one at a time:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = datastructuretools.Cursor(source=source)

            ::

                >>> cursor.next()
                (13,)
                >>> cursor.next()
                ('da capo',)
                >>> cursor.next()
                (Note("cs'8."),)
                >>> cursor.next()
                ('rit.',)
                >>> cursor.next()
                (13,)
                >>> cursor.next()
                ('da capo',)

        ..  container:: example

            **Example 2.** Gets elements one at a time in reverse:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = datastructuretools.Cursor(source=source)

            ::

                >>> cursor.next(count=-1)
                ('rit.',)
                >>> cursor.next(count=-1)
                (Note("cs'8."),)
                >>> cursor.next(count=-1)
                ('da capo',)
                >>> cursor.next(count=-1)
                (13,)

        ..  container:: example

            **Example 3.** Gets same two elements forward and back:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = datastructuretools.Cursor(source=source)

            ::

                >>> cursor.next(count=2)
                (13, 'da capo')
                >>> cursor.next(count=-2)
                ('da capo', 13)
                >>> cursor.next(count=2)
                (13, 'da capo')
                >>> cursor.next(count=-2)
                ('da capo', 13)

        ..  container:: example

            **Example 4.** Gets different numbers of elements at a time:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = datastructuretools.Cursor(source=source)

            ::

                >>> cursor.next(count=2)
                (13, 'da capo')
                >>> cursor.next(count=-1)
                ('da capo',)
                >>> cursor.next(count=2)
                ('da capo', Note("cs'8."))
                >>> cursor.next(count=-1)
                (Note("cs'8."),)
                >>> cursor.next(count=2)
                (Note("cs'8."), 'rit.')
                >>> cursor.next(count=-1)
                ('rit.',)

        ..  container:: example

            **Example 5.** Gets different numbers of elements at a time:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = datastructuretools.Cursor(source=source)

            ::

                >>> cursor.next(count=2)
                (13, 'da capo')
                >>> cursor.next(count=-3)
                ('da capo', 13, 'rit.')
                >>> cursor.next(count=2)
                ('rit.', 13)
                >>> cursor.next(count=-3)
                (13, 'rit.', Note("cs'8."))
                >>> cursor.next(count=2)
                (Note("cs'8."), 'rit.')
                >>> cursor.next(count=-3)
                ('rit.', Note("cs'8."), 'da capo')

        Raises an index error if no (more) elements exist.

        Returns tuple.
        '''
        result = []
        if self.position is None:
            self._position = 0
        if 0 < count:
            for i in range(count):
                element = self.source[self.position]
                result.append(element)
                self._position += 1
        elif count < 0:
            for i in range(abs(count)):
                self._position -= 1
                element = self.source[self.position]
                result.append(element)
        result = tuple(result)
        return result
