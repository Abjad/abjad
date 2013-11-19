# -*- encoding: utf-8 -*-
from abjad.tools import schemetools
from abjad.tools.abctools import AbjadObject


class MarkupCommand(AbjadObject):
    r'''Abjad model of a LilyPond markup command:

    ::

        >>> circle = markuptools.MarkupCommand('draw-circle', 2.5, 0.1, False)
        >>> square = markuptools.MarkupCommand('rounded-box', 'hello?')
        >>> line = markuptools.MarkupCommand('line', [square, 'wow!'])
        >>> rotate = markuptools.MarkupCommand('rotate', 60, line)
        >>> combine = markuptools.MarkupCommand('combine', rotate, circle)

    ::

        >>> print format(combine, 'lilypond')
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

    Insert a markup command in markup in order to attach it to 
    score components:

    ::

        >>> note = Note("c'4")

    ::

        >>> markup = markuptools.Markup(combine)

    ::

        >>> attach(markup, note)

    ..  doctest::

        >>> print format(note)
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

    ::

        >>> show(note) # doctest: +SKIP

    Markup commands are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_args', 
        '_command',
        )

    ### INITIALIZER ###

    def __init__(self, command, *args):
        assert isinstance(command, str) \
            and len(command) and command.find(' ') == -1
        self._command = command
        self._args = tuple(args)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.command == expr.command:
                if self.args == expr.args:
                    return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats markup command.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        elif format_specification == 'lilypond':
            return self._lilypond_format
        return str(self)

    def __str__(self):
        return self._lilypond_format

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return '\n'.join(self._get_format_pieces())

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=(self.command,) + self.args,
            )

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

    def _get_format_pieces(self):
        indent = '\t'
        def recurse(iterable):
            result = []
            for x in iterable:
                if isinstance(x, (list, tuple)):
                    result.append('{')
                    result.extend(recurse(x))
                    result.append('}')
                elif isinstance(x, type(self)):
                    result.extend(x._get_format_pieces())
                elif isinstance(x, schemetools.Scheme):
                    result.append(format(x))
                else:
                    formatted = schemetools.Scheme.format_scheme_value(x)
                    if isinstance(x, str):
                        result.append(formatted)
                    else:
                        result.append('#{}'.format(formatted))
            return ['{}{}'.format(indent, x) for x in result]
        parts = [r'\{}'.format(self.command)]
        parts.extend(recurse(self.args))
        return parts

    ### PUBLIC PROPERTIES ###

    @property
    def args(self):
        r'''Tuple of markup command arguments.
        '''
        return self._args

    @property
    def command(self):
        r'''String of markup command command-name.
        '''
        return self._command
