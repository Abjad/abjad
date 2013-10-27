# -*- encoding: utf-8 -*-
from abjad.tools.marktools.LilyPondCommandMark import LilyPondCommandMark


class BarLine(LilyPondCommandMark):
    r'''A bar line.

    ::

        >>> staff = Staff("c'4 d'4 e'4 f'4")

    ::

        >>> bar_line = marktools.BarLine('|.')(staff[-1])

    ::

        >>> bar_line
        BarLine('|.')(f'4)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
            \bar "|."
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Returns bar line.
    '''

    ### INITIALIZER ##

    def __init__(self, bar_line_string='|', format_slot='after'):
        self.bar_line_string = bar_line_string
        command_name = 'bar "%s"' % bar_line_string
        LilyPondCommandMark.__init__(self, command_name, format_slot)

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)(self.bar_line_string, format_slot=self.format_slot)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.bar_line_string)

    ## PUBLIC PROPERTIES ##

    @apply
    def bar_line_string():
        def fget(self):
            r'''Get bar line string of bar line:

            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> bar_line = marktools.BarLine()(staff[-1])
                >>> bar_line.bar_line_string
                '|'

            Set bar line string of bar line:

            ::

                >>> bar_line.bar_line_string = '|.'
                >>> bar_line.bar_line_string
                '|.'

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'4
                    e'4
                    f'4
                    \bar "|."
                }

            Set string.
            '''
            return self._bar_line_string
        def fset(self, bar_line_string):
            assert isinstance(bar_line_string, str)
            self._bar_line_string = bar_line_string
            command_name = 'bar "%s"' % bar_line_string
            self.command_name = command_name
        return property(**locals())
