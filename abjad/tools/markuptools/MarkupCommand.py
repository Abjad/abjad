# -*- encoding: utf-8 -*-
from abjad.tools import schemetools
from abjad.tools.abctools import AbjadValueObject


class MarkupCommand(AbjadValueObject):
    r'''A LilyPond markup command.

    ..  container:: example

        **Example 1.** A complex LilyPond markup command:

        ::

            >>> circle = markuptools.MarkupCommand('draw-circle', 2.5, 0.1, False)
            >>> square = markuptools.MarkupCommand('rounded-box', 'hello?')
            >>> line = markuptools.MarkupCommand('line', [square, 'wow!'])
            >>> rotate = markuptools.MarkupCommand('rotate', 60, line)
            >>> combine = markuptools.MarkupCommand('combine', rotate, circle)

        ::

            >>> print(format(combine, 'lilypond'))
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
            >>> markup = markuptools.Markup(combine)
            >>> attach(markup, note)
            >>> show(note) # doctest: +SKIP

        ..  doctest::

            >>> print(format(note))
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

    ..  container:: example

        **Example 2.** Works with the LilyPond ``\score`` markup command:

        ::

            >>> small_staff = Staff("fs'16 gs'16 as'16 b'16")
            >>> small_staff.remove_commands.append('Clef_engraver')
            >>> small_staff.remove_commands.append('Time_signature_engraver')
            >>> set_(small_staff).font_size = -3
            >>> layout_block = lilypondfiletools.Block(name='layout')
            >>> layout_block.indent = 0
            >>> layout_block.ragged_right = True
            >>> command = markuptools.MarkupCommand(
            ...     'score',
            ...     [small_staff, layout_block],
            ...     )

        ::

            >>> f(command)
            \score
                {
                    \new Staff \with {
                        \remove Clef_engraver
                        \remove Time_signature_engraver
                        fontSize = #-3
                    } {
                        fs'16
                        gs'16
                        as'16
                        b'16
                    }
                    \layout {
                        indent = #0
                        ragged-right = ##t
                    }
                }

        ::

            >>> markup = Markup(contents=command, direction=Up)
            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> attach(markup, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'4
                    ^ \markup {
                        \score
                            {
                                \new Staff \with {
                                    \remove Clef_engraver
                                    \remove Time_signature_engraver
                                    fontSize = #-3
                                } {
                                    fs'16
                                    gs'16
                                    as'16
                                    b'16
                                }
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                        }
                d'4
                e'4
                f'4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_args',
        '_command',
        '_force_quotes',
        )

    ### INITIALIZER ###

    def __init__(self, command=None, *args):
        if command is None:
            command = 'draw-circle'
            assert len(args) == 0
        assert isinstance(command, str) \
            and len(command) and command.find(' ') == -1
        self._command = command
        self._args = tuple(args)
        self._force_quotes = False

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a markup command with command and
        args equal to those of this markup command. Otherwise false.

        Returns boolean.
        '''
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

    def __hash__(self):
        r'''Hashes markup command.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(MarkupCommand, self).__hash__()

    def __str__(self):
        r'''Gets string representation of markup command.

        Returns string.
        '''
        return self._lilypond_format

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return '\n'.join(self._get_format_pieces())

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = (self.command,) + self.args
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=(),
            positional_argument_values=positional_argument_values,
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
        from abjad.tools import lilypondfiletools
        from abjad.tools import scoretools
        from abjad.tools import systemtools
        indent = systemtools.LilyPondFormatManager.indent
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
                elif isinstance(x, scoretools.Component):
                    result.extend(x._format_pieces)
                elif isinstance(x, lilypondfiletools.Block):
                    result.extend(x._format_pieces)
                elif isinstance(x, str) and '\n' in x:
                    result.append('#"')
                    result.extend(x.splitlines())
                    result.append('"')
                else:
                    formatted = schemetools.Scheme.format_scheme_value(
                        x,
                        force_quotes=self.force_quotes,
                        )
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
        r'''Markup command arguments.

        Returns tuple.
        '''
        return self._args

    # TODO: change to MarkupCommand.name
    @property
    def command(self):
        r'''Markup command name.

        Returns string.
        '''
        return self._command

    @property
    def force_quotes(self):
        r'''Is true when markup command should force quotes around arguments.
        Otherwise false.

        ..  container:: example

            Here's a markup command formatted in the usual way without forced
            quotes:

            ::

                >>> lines = ['foo', 'bar blah', 'baz']
                >>> command = markuptools.MarkupCommand('column', lines)
                >>> markup = Markup(command)

            ::

                >>> f(markup)
                \markup {
                    \column
                        {
                            foo
                            "bar blah"
                            baz
                        }
                    }

            The markup command forces quotes around only the spaced string
            ``'bar blah'``.

        ..  container:: example

            Here's the same markup command with forced quotes:

                >>> lines = ['foo', 'bar blah', 'baz']
                >>> command = markuptools.MarkupCommand('column', lines)
                >>> command.force_quotes = True
                >>> markup = Markup(command)

            ::

                >>> f(markup)
                \markup {
                    \column
                        {
                            "foo"
                            "bar blah"
                            "baz"
                        }
                    }

            The markup command forces quotes around all strings.

        The rendered result of forced and unforced quotes is the same.

        Defaults to false.

        Returns boolean.
        '''
        return self._force_quotes

    @force_quotes.setter
    def force_quotes(self, arg):
        assert isinstance(arg, bool), repr(arg)
        self._force_quotes = arg