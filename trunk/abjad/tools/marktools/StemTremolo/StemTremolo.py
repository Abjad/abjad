# -*- encoding: utf-8 -*-
from abjad.tools.componenttools.Component import Component
from abjad.tools import mathtools
from abjad.tools.marktools.Mark import Mark


class StemTremolo(Mark):
    '''A stem tremolo.

    ::

        >>> note = Note("c'4")

    ::

        >>> marktools.StemTremolo(16)(note)
        StemTremolo(16)(c'4)

    ..  doctest::

        >>> f(note)
        c'4 :16

    ::

        >>> show(note) # doctest: +SKIP

    Stem tremolos implement ``__slots__``.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_format_slot', 
        '_tremolo_flags',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        Mark.__init__(self)
        self._format_slot = 'right'
        if len(args) == 1 and isinstance(args[0], type(self)):
            self.tremolo_flags = args[0].tremolo_flags
        elif len(args) == 1 and not isinstance(args[0], type(self)):
            self.tremolo_flags = args[0]
        else:
            raise ValueError('can not initialize stem tremolo.')

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copy stem tremolo:

        ::

            >>> import copy
            >>> stem_tremolo_1 = marktools.StemTremolo(16)
            >>> stem_tremolo_2 = copy.copy(stem_tremolo_1)

        ::

            >>> stem_tremolo_1 == stem_tremolo_2
            True

        ::

            >>> stem_tremolo_1 is not stem_tremolo_2
            True

        Returns new stem tremolo.
        '''
        new = type(self)(self.tremolo_flags)
        new._format_slot = self._format_slot
        return new

    def __eq__(self, expr):
        r'''True when `expr` is a stem tremolo with equal tremolo flags:
        Otherwise false:

        ::

            >>> stem_tremolo_1 = marktools.StemTremolo(16)
            >>> stem_tremolo_2 = marktools.StemTremolo(16)
            >>> stem_tremolo_3 = marktools.StemTremolo(32)

        ::

            >>> stem_tremolo_1 == stem_tremolo_1
            True
            >>> stem_tremolo_1 == stem_tremolo_2
            True
            >>> stem_tremolo_1 == stem_tremolo_3
            False
            >>> stem_tremolo_2 == stem_tremolo_1
            True
            >>> stem_tremolo_2 == stem_tremolo_2
            True
            >>> stem_tremolo_2 == stem_tremolo_3
            False
            >>> stem_tremolo_3 == stem_tremolo_1
            False
            >>> stem_tremolo_3 == stem_tremolo_2
            False
            >>> stem_tremolo_3 == stem_tremolo_3
            True

        Returns boolean.
        '''
        assert isinstance(expr, type(self))
        if self.tremolo_flags == expr.tremolo_flags:
            return True
        return False

    def __str__(self):
        return ':%s' % str(self.tremolo_flags)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return '%s' % self.tremolo_flags

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        r'''LilyPond format string:

        ::

            >>> stem_tremolo = marktools.StemTremolo(16)
            >>> stem_tremolo.lilypond_format
            ':16'

        Returns string.
        '''
        return str(self)

    @apply
    def tremolo_flags():
        def fget(self):
            r'''Get tremolo flags:

            ::

                >>> stem_tremolo = marktools.StemTremolo(16)
                >>> stem_tremolo.tremolo_flags
                16

            Set tremolo flags:

            ::

                >>> stem_tremolo.tremolo_flags = 32
                >>> stem_tremolo.tremolo_flags
                32

            Set integer.
            '''
            return self._tremolo_flags
        def fset(self, tremolo_flags):
            if not mathtools.is_nonnegative_integer_power_of_two(
                tremolo_flags):
                message ='tremolo flags must be'
                message += ' nonnegative integer power of 2.'
                raise ValueError(message)
            self._tremolo_flags = tremolo_flags
        return property(**locals())
