# -*- encoding: utf-8 -*-
#from abjad.tools.marktools.LilyPondCommand import LilyPondCommand
from abjad.tools.marktools.Mark import Mark


class BarLine(Mark):
    r'''A bar line.

    ::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> bar_line = marktools.BarLine('|.')
        >>> attach(bar_line, staff[-1])
        >>> show(staff) # doctest: +SKIP

    ::

        >>> bar_line
        BarLine('|.')(f'4)

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
            \bar "|."
        }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_abbreviation',
        '_format_slot',
        )

    _format_slot = 'after'

    ### INITIALIZER ##

    def __init__(self, abbreviation='|'):
        Mark.__init__(self)
        self.abbreviation = abbreviation

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies bar line.

        Returns new bar line.
        '''
        return type(self)(self.abbreviation)

    def __eq__(self, arg):
        r'''True when `arg` is a bar line with equal abbreviation.
        Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            return self.abbreviation == arg.abbreviation
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.abbreviation)

    @property
    def _lilypond_format(self):
        return r'\bar "{}"'.format(self.abbreviation)

    ## PUBLIC PROPERTIES ##

    @apply
    def abbreviation():
        def fget(self):
            r'''Gets and sets abbreviation.

            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> bar_line = marktools.BarLine()
                >>> attach(bar_line, staff[-1])
                >>> bar_line.abbreviation
                '|'

            Sets abbreviation.

            ::

                >>> bar_line.abbreviation = '|.'
                >>> bar_line.abbreviation
                '|.'

            ..  doctest::

                >>> print format(staff)
                \new Staff {
                    c'4
                    d'4
                    e'4
                    f'4
                    \bar "|."
                }

            Returns string.
            '''
            return self._abbreviation
        def fset(self, abbreviation):
            assert isinstance(abbreviation, str)
            self._abbreviation = abbreviation
        return property(**locals())
