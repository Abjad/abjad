from abjad.tools.marktools.Mark import Mark


### TODO: extend LilyPond command marks to attach to spanners.
class LilyPondCommandMark(Mark):
    r'''.. versionadded:: 2.0

    LilyPond command mark::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> slur = spannertools.SlurSpanner(staff.leaves)

    ::

        abjad> lilypond_command = marktools.LilyPondCommandMark('slurDotted')(staff[0])

    ::

        abjad> f(staff)
        \new Staff {
            \slurDotted
            c'8 (
            d'8
            e'8
            f'8 )
        }

    LilyPond command marks implement ``__slots__``.
    '''

    __slots__ = ('_command_name', '_format_slot', )

    def __init__(self, command_name, format_slot = 'opening'):
        Mark.__init__(self)
        self._command_name = command_name
        self._format_slot = format_slot

    ### OVERLOADS ###

    def __copy__(self, *args):
        return type(self)(self._command_name)

    __deepcopy__ = __copy__

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return self._command_name == arg._command_name
        return False

    ### PRIVATE ATTRIBUTES ###

    @property
    def _contents_repr_string(self):
        return repr(self.command_name)

    ### PUBLIC ATTRIBUTES ###

    @apply
    def command_name():
        def fget(self):
            '''Get command name string of LilyPond command mark::

                abjad> lilypond_command = marktools.LilyPondCommandMark('slurDotted')
                abjad> lilypond_command.command_name
                'slurDotted'

            Set command name string of LilyPond command mark::

                abjad> lilypond_command.command_name = 'slurDashed'
                abjad> lilypond_command.command_name
                'slurDashed'

            Set string.
            '''
            return self._command_name
        def fset(self, command_name):
            assert isinstance(command_name, str)
            self._command_name = command_name
        return property(**locals())

    @property
    def format(self):
        '''Read-only LilyPond input format of LilyPond command mark::

            abjad> note = Note("c'4")
            abjad> lilypond_command = marktools.LilyPondCommandMark('slurDotted')(note)
            abjad> lilypond_command.format
            '\\slurDotted'

        Return string.
        '''
        from abjad.tools import iotools
        command = self._command_name
        if command.startswith('#'):
            return command
        else:
            return '\\' + iotools.underscore_delimited_lowercase_to_lowercamelcase(command)

