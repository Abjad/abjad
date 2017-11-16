from abjad.tools.abctools import AbjadValueObject


class MarkupCommand(AbjadValueObject):
    r'''LilyPond markup command.

    ..  container:: example

        Initializes a complex LilyPond markup command:

        >>> circle = abjad.MarkupCommand('draw-circle', 2.5, 0.1, False)
        >>> square = abjad.MarkupCommand('rounded-box', 'hello?')
        >>> line = abjad.MarkupCommand('line', [square, 'wow!'])
        >>> rotate = abjad.MarkupCommand('rotate', 60, line)
        >>> combine = abjad.MarkupCommand('combine', rotate, circle)

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

        >>> note = abjad.Note("c'4")
        >>> markup = abjad.Markup(combine)
        >>> abjad.attach(markup, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
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

        >>> small_staff = abjad.Staff("fs'16 gs'16 as'16 b'16")
        >>> small_staff.remove_commands.append('Clef_engraver')
        >>> small_staff.remove_commands.append('Time_signature_engraver')
        >>> abjad.setting(small_staff).font_size = -3
        >>> layout_block = abjad.lilypondfiletools.Block(name='layout')
        >>> layout_block.indent = 0
        >>> layout_block.ragged_right = True
        >>> command = abjad.MarkupCommand(
        ...     'score',
        ...     [small_staff, layout_block],
        ...     )

        >>> abjad.f(command)
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

        >>> markup = abjad.Markup(contents=command, direction=abjad.Up)
        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> abjad.attach(markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
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
        '_arguments',
        '_deactivate',
        '_force_quotes',
        '_name',
        '_tag',
        )

    ### INITIALIZER ###

    def __init__(self, name=None, *arguments):
        if name is None:
            # TODO: Generalize these arbitrary default arguments away.
            name = 'draw-circle'
            assert len(arguments) == 0
        self._arguments = tuple(arguments)
        self._deactivate = None
        self._force_quotes = False
        assert isinstance(name, str) and len(name) and name.find(' ') == -1
        self._name = name
        self._tag = None

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is a markup command with name and
        arguments equal to those of this markup command. Otherwise false.

        ..  container:: example

            >>> command_1 = abjad.MarkupCommand('bold', 'foo')
            >>> command_2 = abjad.MarkupCommand('bold', 'foo')
            >>> command_3 = abjad.MarkupCommand('bold', 'bar')

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
        # defined explicitly because of initializer *arguments
        if isinstance(argument, type(self)):
            if self.name == argument.name:
                if self.arguments == argument.arguments:
                    return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats markup command.

        ..  container:: example

            Prints storage format:

            >>> circle = abjad.MarkupCommand('draw-circle', 2.5, 0.1, False)
            >>> square = abjad.MarkupCommand('rounded-box', 'hello?')
            >>> line = abjad.MarkupCommand('line', [square, 'wow!'])
            >>> rotate = abjad.MarkupCommand('rotate', 60, line)
            >>> combine = abjad.MarkupCommand('combine', rotate, circle)

            >>> print(format(combine, 'storage'))
            abjad.MarkupCommand(
                'combine',
                abjad.MarkupCommand(
                    'rotate',
                    60,
                    abjad.MarkupCommand(
                        'line',
                        [
                            abjad.MarkupCommand(
                                'rounded-box',
                                'hello?'
                                ),
                            'wow!',
                            ]
                        )
                    ),
                abjad.MarkupCommand(
                    'draw-circle',
                    2.5,
                    0.1,
                    False
                    )
                )

        ..  container:: example

            Prints LilyPond format:

            >>> circle = abjad.MarkupCommand('draw-circle', 2.5, 0.1, False)
            >>> square = abjad.MarkupCommand('rounded-box', 'hello?')
            >>> line = abjad.MarkupCommand('line', [square, 'wow!'])
            >>> rotate = abjad.MarkupCommand('rotate', 60, line)
            >>> combine = abjad.MarkupCommand('combine', rotate, circle)

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
        import abjad
        if format_specification in ('', 'storage'):
            return abjad.StorageFormatManager(self).get_storage_format()
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

            >>> command = abjad.MarkupCommand('hspace', 0)
            >>> command
            abjad.MarkupCommand(
                'hspace',
                0
                )

            >>> eval(repr(command))
            abjad.MarkupCommand(
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

            >>> circle = abjad.MarkupCommand('draw-circle', 2.5, 0.1, False)
            >>> square = abjad.MarkupCommand('rounded-box', 'hello?')
            >>> line = abjad.MarkupCommand('line', [square, 'wow!'])
            >>> rotate = abjad.MarkupCommand('rotate', 60, line)
            >>> combine = abjad.MarkupCommand('combine', rotate, circle)

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
        import abjad
        def recurse(iterable):
            result = []
            for item in iterable:
                if isinstance(item, (list, tuple)):
                    result.append('{')
                    result.extend(recurse(item))
                    result.append('}')
                elif isinstance(item, abjad.Scheme):
                    result.append(format(item))
                elif hasattr(item, '_get_format_pieces'):
                    result.extend(item._get_format_pieces())
                elif isinstance(item, str) and '\n' in item:
                    result.append('#"')
                    result.extend(item.splitlines())
                    result.append('"')
                else:
                    formatted = abjad.Scheme.format_scheme_value(
                        item,
                        force_quotes=self.force_quotes,
                        )
                    if isinstance(item, str):
                        result.append(formatted)
                    else:
                        result.append('#{}'.format(formatted))
            return ['{}{}'.format(indent, item) for item in result]
        indent = abjad.LilyPondFormatManager.indent
        parts = [r'\{}'.format(self.name)]
        parts.extend(recurse(self.arguments))
        if self.tag:
            tag = ' %! ' + self.tag
            parts = [_ + tag for _ in parts]
            if self.deactivate:
                parts = ['%%% ' + _ for _ in parts]
        return parts

    def _get_format_specification(self):
        import abjad
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=(self.name,) + self.arguments,
            storage_format_kwargs_names=[],
            )

    def _get_lilypond_format(self):
        return '\n'.join(self._get_format_pieces())

    ### PUBLIC PROPERTIES ###

    @property
    def arguments(self):
        r'''Gets markup command arguments.

        ..  container:: example

            >>> arguments = ('draw-circle', 1, 0.1, False)
            >>> command = abjad.MarkupCommand(*arguments)
            >>> command.arguments
            (1, 0.1, False)

        Returns tuple.
        '''
        return self._arguments

    @property
    def deactivate(self):
        r'''Is true when markup command deactivates tag.

        Returns true, false or none.
        '''
        return self._deactivate

    @deactivate.setter
    def deactivate(self, argument):
        if argument is not None:
            argument = bool(argument)
        self._deactivate = argument

    @property
    def force_quotes(self):
        r'''Is true when markup command should force quotes around arguments.
        Otherwise false.

        ..  container:: example

            Here's a markup command formatted in the usual way without forced
            quotes:

            >>> lines = ['foo', 'bar blah', 'baz']
            >>> command = abjad.MarkupCommand('column', lines)
            >>> markup = abjad.Markup(command)

            >>> abjad.f(markup)
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
                >>> command = abjad.MarkupCommand('column', lines)
                >>> command.force_quotes = True
                >>> markup = abjad.Markup(command)

            >>> abjad.f(markup)
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

    @property
    def name(self):
        r'''Gets markup command name.

        ..  container:: example

            >>> arguments = ('draw-circle', 1, 0.1, False)
            >>> command = abjad.MarkupCommand(*arguments)
            >>> command.name
            'draw-circle'

        Returns string.
        '''
        return self._name

    @property
    def tag(self):
        r'''Gets tag.

        Returns string or none.
        '''
        return self._tag

    @tag.setter
    def tag(self, argument):
        assert isinstance(argument, (str, type(None))), repr(argument)
        self._tag = argument

    ### PUBLIC METHODS ###

    @staticmethod
    def combine_markup_commands(*commands):
        r'''Combines markup command and / or strings.

        LilyPond's '\combine' markup command can only take two arguments, so in
        order to combine more than two stencils, a cascade of '\combine'
        commands must be employed.  `combine_markup_commands` simplifies this
        process.

        ..  container:: example

            >>> markup_a = abjad.MarkupCommand(
            ...     'draw-circle',
            ...     4,
            ...     0.4,
            ...     False,
            ...     )
            >>> markup_b = abjad.MarkupCommand(
            ...     'filled-box',
            ...     abjad.SchemePair((-4, 4)),
            ...     abjad.SchemePair((-0.5, 0.5)),
            ...     1,
            ...     )
            >>> markup_c = "some text"

            >>> markup = abjad.MarkupCommand.combine_markup_commands(
            ...     markup_a,
            ...     markup_b,
            ...     markup_c,
            ...     )
            >>> result = format(markup, 'lilypond')

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
