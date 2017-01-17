# -*- coding: utf-8 -*-
from abjad.tools import schemetools
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadValueObject


class MarkupCommand(AbjadValueObject):
    r'''LilyPond markup command.

    ..  container:: example

        Initializes a complex LilyPond markup command:

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

        Works with the LilyPond ``\score`` markup command:

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

    def __init__(self, command=None, *arguments):
        if command is None:
            # TODO: Generalize these arbitrary default arguments away.
            command = 'draw-circle'
            assert len(arguments) == 0
        assert isinstance(command, str) \
            and len(command) and command.find(' ') == -1
        self._command = command
        self._args = tuple(arguments)
        self._force_quotes = False

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is a markup command with command and
        arguments equal to those of this markup command. Otherwise false.

        ..  container:: example

            ::

                >>> command_1 = markuptools.MarkupCommand('box')
                >>> command_2 = markuptools.MarkupCommand('box')
                >>> command_3 = markuptools.MarkupCommand('line')

            ::
            
                >>> command_1 == command_1
                True
                >>> command_1 == command_2
                True
                >>> command_1 == command_3
                False
                >>> command_2 == command_1
                True
                >>> command_2 == command_2
                True
                >>> command_2 == command_3
                False
                >>> command_3 == command_1
                False
                >>> command_3 == command_2
                False
                >>> command_3 == command_3
                True

        Returns true or false.
        '''
        if isinstance(argument, type(self)):
            if self.command == argument.command:
                if self.arguments == argument.arguments:
                    return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats markup command.

        ..  container:: example

            Prints storage format:

            ::

                >>> circle = markuptools.MarkupCommand('draw-circle', 2.5, 0.1, False)
                >>> square = markuptools.MarkupCommand('rounded-box', 'hello?')
                >>> line = markuptools.MarkupCommand('line', [square, 'wow!'])
                >>> rotate = markuptools.MarkupCommand('rotate', 60, line)
                >>> combine = markuptools.MarkupCommand('combine', rotate, circle)

            ::

                >>> print(format(combine, 'storage'))
                markuptools.MarkupCommand(
                    'combine',
                    markuptools.MarkupCommand(
                        'rotate',
                        60,
                        markuptools.MarkupCommand(
                            'line',
                            [
                                markuptools.MarkupCommand(
                                    'rounded-box',
                                    'hello?'
                                    ),
                                'wow!',
                                ]
                            )
                        ),
                    markuptools.MarkupCommand(
                        'draw-circle',
                        2.5,
                        0.1,
                        False
                        )
                    )

        ..  container:: example

            Prints LilyPond format:

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

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        elif format_specification == 'lilypond':
            return self._get_lilypond_format()
        return str(self)

    def __hash__(self):
        r'''Hashes markup command.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(MarkupCommand, self).__hash__()

    def __repr__(self):
        r'''Gets markup command interpreter representation.

        ..  container:: example

            Interpreter representation is evaluable.

            ::

                >>> command = markuptools.MarkupCommand('hspace', 0)
                >>> command
                markuptools.MarkupCommand(
                    'hspace',
                    0
                    )

            ::

                >>> eval(repr(command))
                markuptools.MarkupCommand(
                    'hspace',
                    0
                    )

        Returns string.
        '''
        superclass = super(MarkupCommand, self)
        return superclass.__format__()

    def __str__(self):
        r'''Gets string representation of markup command.

        ..  container:: example

            ::

                >>> circle = markuptools.MarkupCommand('draw-circle', 2.5, 0.1, False)
                >>> square = markuptools.MarkupCommand('rounded-box', 'hello?')
                >>> line = markuptools.MarkupCommand('line', [square, 'wow!'])
                >>> rotate = markuptools.MarkupCommand('rotate', 60, line)
                >>> combine = markuptools.MarkupCommand('combine', rotate, circle)

            ::

                >>> print(str(combine))
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

        Returns string.
        '''
        return self._get_lilypond_format()

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
        def recurse(iterable):
            result = []
            for x in iterable:
                if isinstance(x, (list, tuple)):
                    result.append('{')
                    result.extend(recurse(x))
                    result.append('}')
                elif isinstance(x, schemetools.Scheme):
                    result.append(format(x))
                elif hasattr(x, '_get_format_pieces'):
                    result.extend(x._get_format_pieces())
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
        from abjad.tools import systemtools
        indent = systemtools.LilyPondFormatManager.indent
        parts = [r'\{}'.format(self.command)]
        parts.extend(recurse(self.arguments))
        return parts

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=(self.command,) + self.arguments,
            storage_format_kwargs_names=[],
            )

    def _get_lilypond_format(self):
        return '\n'.join(self._get_format_pieces())

    ### PUBLIC PROPERTIES ###

    @property
    def arguments(self):
        r'''Gets markup command arguments.

        ..  container:: example

            ::

                >>> arguments = ('draw-circle', 1, 0.1, False)
                >>> command = markuptools.MarkupCommand(*arguments)
                >>> command.arguments
                (1, 0.1, False)

        Returns tuple.
        '''
        return self._args

    # TODO: change to MarkupCommand.name
    @property
    def command(self):
        r'''Gets markup command name.

        ..  container:: example

            ::

                >>> arguments = ('draw-circle', 1, 0.1, False)
                >>> command = markuptools.MarkupCommand(*arguments)
                >>> command.command
                'draw-circle'

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

        Returns true or false.
        '''
        return self._force_quotes

    @force_quotes.setter
    def force_quotes(self, argument):
        assert isinstance(argument, bool), repr(argument)
        self._force_quotes = argument

    ### PUBLIC METHODS ###

    @staticmethod
    def combine_markup_commands(*commands):
        r'''Combines markup command and / or strings.

        LilyPond's '\combine' markup command can only take two arguments, so in
        order to combine more than two stencils, a cascade of '\combine'
        commands must be employed.  `combine_markup_commands` simplifies this
        process.

        ..  container:: example

            ::

                >>> markup_a = markuptools.MarkupCommand(
                ...     'draw-circle',
                ...     4,
                ...     0.4,
                ...     False,
                ...     )
                >>> markup_b = markuptools.MarkupCommand(
                ...     'filled-box',
                ...     schemetools.SchemePair(-4, 4),
                ...     schemetools.SchemePair(-0.5, 0.5), 1)
                >>> markup_c = "some text"

            ::

                >>> markup = markuptools.MarkupCommand.combine_markup_commands(
                ...     markup_a,
                ...     markup_b,
                ...     markup_c,
                ...     )
                >>> result = format(markup, 'lilypond')

            ::

                >>> print(result)
                \combine \combine \draw-circle #4 #0.4 ##f
                    \filled-box #'(-4 . 4) #'(-0.5 . 0.5) #1 "some text"

        Returns a markup command instance, or a string if that was the only
        argument.
        '''
        from abjad.tools import markuptools

        assert len(commands)
        assert all(
            isinstance(command, (markuptools.MarkupCommand, str))
            for command in commands
            )

        if 1 == len(commands):
            return commands[0]

        combined = MarkupCommand('combine', commands[0], commands[1])
        for command in commands[2:]:
            combined = MarkupCommand('combine', combined, command)
        return combined
