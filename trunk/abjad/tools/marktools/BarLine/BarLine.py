from abjad.tools.marktools.LilyPondCommandMark import LilyPondCommandMark


class BarLine(LilyPondCommandMark):
    r'''.. versionadded:: 2.4

    Abjad model of bar line::

        abjad> staff = Staff("c'4 d'4 e'4 f'4")

    ::

        abjad> bar_line = marktools.BarLine('|.')(staff[-1])

    ::

        abjad> bar_line
        BarLine('|.')(f'4)

    ::

        abjad> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
            \bar "|."
        }

    Return bar line.
    '''

    def __init__(self, bar_line_string='|', format_slot='after'):
        self.bar_line_string = bar_line_string
        command_name = 'bar "%s"' % bar_line_string
        LilyPondCommandMark.__init__(self, command_name, format_slot)

    ## OVERRIDE ##

    def __copy__(self, *args):
        return type(self)(self.bar_line_string, format_slot=self.format_slot)

    ## PRIVATE ATTRIBUTES ##

    @property
    def _contents_repr_string(self):
        return repr(self.bar_line_string)

    ## PUBLIC ATTRIBUTES ##

    @apply
    def bar_line_string():
        def fget(self):
            r'''Get bar line string of bar line::

                abjad> staff = Staff("c'4 d'4 e'4 f'4")
                abjad> bar_line = marktools.BarLine()(staff[-1])
                abjad> bar_line.bar_line_string
                '|'

            Set bar line string of bar line::

                abjad> bar_line.bar_line_string = '|.'
                abjad> bar_line.bar_line_string
                '|.'

            ::

                abjad> f(staff)
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
