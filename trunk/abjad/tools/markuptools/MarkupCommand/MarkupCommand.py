from abjad.core import _Immutable


class MarkupCommand(_Immutable):
    r'''Abjad model of a LilyPond markup command::

        abjad> circle = markuptools.MarkupCommand('draw-circle', ['#2.5', '#0.1', '##f'], None)
        abjad> square = markuptools.MarkupCommand('rounded-box', None, ['hello?'])
        abjad> line = markuptools.MarkupCommand('line', None, [square, 'wow!'])
        abjad> rotate = markuptools.MarkupCommand('rotate', ['#60'], [line])
        abjad> combine = markuptools.MarkupCommand('combine', None, [rotate, circle], is_braced = False)

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
        c'4 \markup { \combine \rotate #60 \line { \rounded-box hello? wow! } \draw-circle #2.5 #0.1 ##f }

    Markup commands are immutable.
    '''

    # TODO: Implement a multi-line, indented version for human readability. #

    __slots__ = ('_args', '_is_braced', '_command', '_markup')

    def __init__(self, command, args, markup, is_braced = True):
        assert isinstance(command, str) \
            and len(command) and command.find(' ') == -1
        assert isinstance(args, type(None)) or \
            (isinstance(args, (list, tuple)) and len(args))
        assert isinstance(markup, type(None)) or \
            (isinstance(markup, (list, tuple)) and len(markup))
        if markup:
            assert all([isinstance(x, (MarkupCommand, str)) for x in markup])

        object.__setattr__(self, '_is_braced', bool(is_braced))
        object.__setattr__(self, '_command', command)

        if args:
            object.__setattr__(self, '_args', tuple(args))
        else:
            object.__setattr__(self, '_args', args)

        if markup:
            object.__setattr__(self, '_markup', tuple(markup))
        else:
            object.__setattr__(self, '_markup', markup)

    # OVERRIDES #

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.args == arg.args and \
                self.is_braced == arg.is_braced and \
                self.command == arg.command and \
                self.markup == arg.markup:
                return True
        return False

    def __repr__(self):
        return '%s(%r, %s, %s)' % (type(self).__name__, self.command, self.args, self.markup)

    def __str__(self):
        return self.format

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_pieces(self):
        indent_delimiter = ''
        parts = [r'\%s' % self.command]
        if self.args is not None:
            for arg in self.args:
                if 'format' in dir(arg) and not isinstance(arg, str):
                    parts[0] += ' %s' % arg.format
                else:
                    parts[0] += ' %s' % arg
        if self.markup is not None:
            for markup in self.markup:
                if '_format_pieces' in dir(markup) and not isinstance(markup, str):
                    parts.extend([indent_delimiter + x for x in markup._format_pieces])
                else: # markup is a string
                    parts.append(indent_delimiter + self._escape_string(markup))
        if self.is_braced and self.markup and 1 < len(self.markup):
            parts[0] += ' {'
            parts.append('}')
        return parts

    @property
    def _report_pieces(self):
        indent_delimiter = '\t'
        parts = [r'\%s' % self.command]
        if self.args is not None:
            for arg in self.args:
                if 'format' in dir(arg) and not isinstance(arg, str):
                    parts[0] += ' %s' % arg.format
                else:
                    parts[0] += ' %s' % arg
        if self.markup is not None:
            for markup in self.markup:
                if '_report_pieces' in dir(markup) and not isinstance(markup, str):
                    parts.extend([indent_delimiter + x for x in markup._report_pieces])
                else: # markup is a string
                    parts.append(indent_delimiter + self._escape_string(markup))
        if self.is_braced and self.markup and 1 < len(self.markup):
            parts[0] += ' {'
            parts.append('}')
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

            abjad> markup_command = markuptools.MarkupCommand('draw-circle', ['#2.5', '#0.1', '##f'], None)
            abjad> markup_command.format
            '\\draw-circle #2.5 #0.1 ##f'

        Return list of strings.
        '''

        return ' '.join(self._format_pieces)

    @property
    def is_braced(self):
        r'''Read-only boolean of markup command bracing.'''
        return self._is_braced

    @property
    def markup(self):
        r'''Read-only tuple of markup command's child markup.'''
        return self._markup

    ### PUBLIC METHODS ###

    def report(self, output = 'screen'):
        '''Report, in an indented human-readable format, the structure of a formatted MarkupCommand.'''
        if output == 'screen':
            print '\n'.join(self._report_pieces)
        else:
            return '\n'.join(self._report_pieces)
