from abjad.core import _Immutable
from abjad.tools.schemetools import Scheme


class MarkupCommand(_Immutable):
    r'''Abjad model of a LilyPond markup command::

        abjad> circle = markuptools.MarkupCommand('draw-circle', 2.5, 0.1, False)
        abjad> square = markuptools.MarkupCommand('rounded-box', 'hello?')
        abjad> line = markuptools.MarkupCommand('line', [square, 'wow!'])
        abjad> rotate = markuptools.MarkupCommand('rotate', 60, line)
        abjad> combine = markuptools.MarkupCommand('combine', rotate, circle)

    ::

        abjad> print combine
        \combine \rotate #60 \line { \rounded-box hello? wow! } \draw-circle #2.5 #0.1 ##f

    Insert markup command in markup to attach to score components::

        abjad> note = Note("c'4")

    ::

        abjad> markup = markuptools.Markup(combine)

    ::

        abjad> markup(note)
        Markup('\\combine \\rotate #60 \\line { \\rounded-box hello? wow! } \\draw-circle #2.5 #0.1 ##f')

    ::

        abjad> f(note)
        c'4 - \markup { \combine \rotate #60 \line { \rounded-box hello? wow! } \draw-circle #2.5 #0.1 ##f }

    Markup commands are immutable.
    '''

    __slots__ = ('_args', '_command')

    def __init__(self, command, *args):
        assert isinstance(command, str) \
            and len(command) and command.find(' ') == -1
        object.__setattr__(self, '_command', command)
        object.__setattr__(self, '_args', tuple(args))

    ### OVERRIDES ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.command == other.command:
                if self.args == other.args:
                    return True
        return False

    def __repr__(self):
        result = [self.command]
        result.extend([repr(x) for x in self.args])
        return '%s(%s)' % (type(self).__name__, ', '.join(result))

    def __str__(self):
        return self.format

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_pieces(self):
        def recurse(iterable):
            result = []
            for x in iterable:
                if isinstance(x, (list, tuple)):
                    result.append('{')
                    result.extend(recurse(x))
                    result.append('}')
                elif isinstance(x, type(self)):
                    result.extend(x._format_pieces)
                elif isinstance(x, Scheme):
                    result.append(x.format)
                else:
                    formatted = Scheme._format_value(x)
                    if formatted == x and isinstance(x, str):
                        result.append(x)
                    else:
                        result.append('#%s' % formatted)
            return result
        parts = [r'\%s' % self.command]
        parts.extend(recurse(self.args))
        return parts

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

    ### PUBLIC ATTRIBUTES ###

    @property
    def args(self):
        r'''Read-only tuple of markup command arguments.'''
        return self._args

    @property
    def command(self):
        r'''Read-only string of markup command command-name.'''
        return self._command

    @property
    def format(self):
        r'''Read-only format of markup command::

            abjad> markup_command = markuptools.MarkupCommand('draw-circle', 2.5, 0.1, False)
            abjad> markup_command.format
            '\\draw-circle #2.5 #0.1 ##f'

        Returns string.
        '''

        return ' '.join(self._format_pieces)
