from abjad.tools.abctools import AbjadObject
from abjad.tools.schemetools import Scheme
from abjad.tools.schemetools import format_scheme_value


class MarkupCommand(AbjadObject):
    r'''Abjad model of a LilyPond markup command::

        >>> circle = markuptools.MarkupCommand('draw-circle', 2.5, 0.1, False)
        >>> square = markuptools.MarkupCommand('rounded-box', 'hello?')
        >>> line = markuptools.MarkupCommand('line', [square, 'wow!'])
        >>> rotate = markuptools.MarkupCommand('rotate', 60, line)
        >>> combine = markuptools.MarkupCommand('combine', rotate, circle)

    ::

        >>> print combine
        \combine \rotate #60 \line { \rounded-box hello? wow! } \draw-circle #2.5 #0.1 ##f

    Insert markup command in markup to attach to score components::

        >>> note = Note("c'4")

    ::

        >>> markup = markuptools.Markup(combine)

    ::

        >>> markup = markup(note)

    ::

        >>> f(note)
        c'4
            - \markup {
                \combine
                    \rotate
                        #60
                        \line
                            {
                                \rounded-box
                                    hello?
                                wow!
                            }
                    \draw-circle
                        #2.5
                        #0.1
                        ##f
                }


    Markup commands are immutable.
    '''

    __slots__ = ('_args', '_command')

    def __init__(self, command, *args):
        assert isinstance(command, str) \
            and len(command) and command.find(' ') == -1
        object.__setattr__(self, '_command', command)
        object.__setattr__(self, '_args', tuple(args))

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.command == other.command:
                if self.args == other.args:
                    return True
        return False

    def __repr__(self):
        result = [repr(self.command)]
        result.extend([repr(x) for x in self.args])
        return '%s(%s)' % (type(self).__name__, ', '.join(result))

    def __str__(self):
        return self.lilypond_format

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        return self._get_format_pieces(is_indented=False)

    ### PRIVATE METHODS ###

    def _escape_string(self, string):
        if -1 == string.find(' '):
            return string
        string = repr(string)
        if string.startswith("'") and string.endswith("'"):
            string = string.replace('"', '\"')
            string = '"' + string[1:]
            string = string[:-1] + '"'
        return string

    def _get_format_pieces(self, is_indented=True):
        indent = ''
        if is_indented:
            indent = '\t'
        def recurse(iterable):
            result = []
            for x in iterable:
                if isinstance(x, (list, tuple)):
                    result.append('{')
                    result.extend(recurse(x))
                    result.append('}')
                elif isinstance(x, type(self)):
                    result.extend(x._get_format_pieces(is_indented=is_indented))
                elif isinstance(x, Scheme):
                    result.append(x.lilypond_format)
                else:
                    formatted = format_scheme_value(x)
                    if formatted == x and isinstance(x, str):
                        result.append(x)
                    else:
                        result.append('#%s' % formatted)
            return ['{}{}'.format(indent, x) for x in result]
        parts = [r'\%s' % self.command]
        parts.extend(recurse(self.args))
        return parts

    ### PUBLIC PROPERTIES ###

    @property
    def args(self):
        r'''Read-only tuple of markup command arguments.'''
        return self._args

    @property
    def command(self):
        r'''Read-only string of markup command command-name.'''
        return self._command

    @property
    def lilypond_format(self):
        r'''Read-only format of markup command::

            >>> markup_command = markuptools.MarkupCommand('draw-circle', 2.5, 0.1, False)
            >>> markup_command.lilypond_format
            '\\draw-circle #2.5 #0.1 ##f'

        Returns string.
        '''

        return ' '.join(self._format_pieces)
