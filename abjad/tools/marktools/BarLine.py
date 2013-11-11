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
        '_bar_line_string',
        '_format_slot',
        )

    _format_slot = 'after'

    ### INITIALIZER ##

    def __init__(self, bar_line_string='|'):
        Mark.__init__(self)
        self.bar_line_string = bar_line_string

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies bar line.

        Returns new bar line.
        '''
        return type(self)(self.bar_line_string)

    def __eq__(self, arg):
        r'''True when `arg` is a bar line with equal bar line string.
        Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            return self.bar_line_string == arg.bar_line_string
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.bar_line_string)

    @property
    def _lilypond_format(self):
        return r'\bar "{}"'.format(self.bar_line_string)

    ## PUBLIC PROPERTIES ##

    @apply
    def bar_line_string():
        def fget(self):
            r'''Gets and sets bar line string.

            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> bar_line = marktools.BarLine()
                >>> attach(bar_line, staff[-1])
                >>> bar_line.bar_line_string
                '|'

            Sets bar line string:

            ::

                >>> bar_line.bar_line_string = '|.'
                >>> bar_line.bar_line_string
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
            return self._bar_line_string
        def fset(self, bar_line_string):
            assert isinstance(bar_line_string, str)
            self._bar_line_string = bar_line_string
        return property(**locals())
