# -*- encoding: utf-8 -*-
from abjad.tools import schemetools
from abjad.tools import stringtools
from abjad.tools.topleveltools import new
from abjad.tools.abctools.AbjadObject import AbjadObject


class Markup(AbjadObject):
    r'''A LilyPond markup.

    ..  container:: example

        Initializes from string:

        ::

            >>> string = r'\bold { "This is markup text." }'
            >>> markup = Markup(string)
            >>> show(markup) # doctest: +SKIP

        ..  doctest::

            >>> print(format(markup))
            \markup { \bold { "This is markup text." } }

    ..  container:: example

        Initializes from other markup:

        ::

            >>> markup_1 = Markup('foo', direction=Up)
            >>> markup_2 = Markup(markup_1, direction=Down)
            >>> show(markup_2) # doctest: +SKIP

        ..  doctest::

            >>> print(format(markup_1))
            ^ \markup { foo }

        ..  doctest::

            >>> print(format(markup_2))
            _ \markup { foo }

    ..  container:: example

        Attaches markup to score components:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> string = r'\italic { "This is also markup text." }'
            >>> markup = Markup(string, direction=Up)
            >>> attach(markup, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'8
                    ^ \markup {
                        \italic
                            {
                                "This is also markup text."
                            }
                        }
                d'8
                e'8
                f'8
            }

    Set `direction` to ``Up``, ``Down``, ``'neutral'``,
    ``'^'``, ``'_'``, ``'-'`` or None.

    Markup objects are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contents',
        '_direction',
        '_format_slot',
        '_stack_priority',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        contents=None, 
        direction=None,
        stack_priority=0,
        ):
        from abjad.tools import lilypondparsertools
        from abjad.tools import markuptools
        if contents is None:
            new_contents = ('',)
        elif isinstance(contents, str):
            to_parse = r'\markup {{ {} }}'.format(contents)
            parsed = lilypondparsertools.LilyPondParser()(to_parse)
            if all(isinstance(x, str) for x in parsed.contents):
                new_contents = (' '.join(parsed.contents),)
            else:
                new_contents = tuple(parsed.contents)
        elif isinstance(contents, markuptools.MarkupCommand):
            new_contents = (contents,)
        elif isinstance(contents, type(self)):
            direction = direction or contents._direction
            new_contents = tuple(contents._contents)
        elif isinstance(contents, (list, tuple)) and 0 < len(contents):
            new_contents = []
            for arg in contents:
                if isinstance(arg, (str, markuptools.MarkupCommand)):
                    new_contents.append(arg)
                else:
                    new_contents.append(str(arg))
            new_contents = tuple(new_contents)
        else:
            new_contents = (str(contents),)
        self._contents = new_contents
        self._format_slot = 'right'
        direction = \
            stringtools.arg_to_tridirectional_ordinal_constant(direction)
        self._direction = direction
        assert isinstance(stack_priority, int), repr(stack_priority)
        self._stack_priority = stack_priority

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Adds contents of this markup to `expr`.

        ..  container:: example

            **Example 1.** Adds markup to markup:

            ::

                >>> Markup('foo') + Markup('bar')
                Markup(contents=('foo', 'bar'))

        ..  container:: example

            **Example 2.** Adds markup command to markup:

            ::

                >>> Markup('foo') + Markup.hspace(0.75)
                Markup(contents=('foo', MarkupCommand('hspace', 0.75)))

        Returns new markup.
        '''
        from abjad.tools import markuptools
        commands = list(self.contents)
        if isinstance(expr, type(self)):
            commands.extend(expr.contents)
        elif isinstance(expr, markuptools.MarkupCommand):
            commands.append(expr)
        else:
            message = 'must be markup or markup command: {!r}.'
            message = message.format(expr)
            raise TypeError(message)
        markup = type(self)(contents=commands)
        return markup

    def __copy__(self, *args):
        r'''Copies markup.

        ..  container:: example

            ::

                >>> import copy
                >>> string = r'\bold { allegro ma non troppo }'
                >>> markup = Markup(string)
                >>> new_markup = copy.copy(markup)
                >>> show(new_markup) # doctest: +SKIP

        Returns new markup.
        '''
        return type(self)(
            self.contents,
            direction=self.direction,
            stack_priority=self.stack_priority
            )

    def __eq__(self, expr):
        r'''Is true when `expr` is a markup with format equal to that
        of this markup. Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if format(self) == format(expr):
                return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats markup.

        ..  container:: example

            ::

                >>> string = r'\bold { allegro ma non troppo }'
                >>> markup = Markup(string)
                >>> print(format(markup))
                \markup {
                    \bold
                        {
                            allegro
                            ma
                            non
                            troppo
                        }
                    }

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.
        Interprets `''` equal to `'lilypond'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __hash__(self):
        r'''Hashes markup.

        Returns integer.
        '''
        return hash((type(self).__name__, self.contents))

    def __illustrate__(self):
        r'''Illustrates markup.

        ..  container:: example

            ::

                >>> string = r'\bold { allegro ma non troppo }'
                >>> markup = Markup(string)
                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = markup.__illustrate__()
                >>> markup = lilypond_file.items[-1]
                >>> print(format(markup))
                \markup {
                    \bold
                        {
                            allegro
                            ma
                            non
                            troppo
                        }
                    }

        Returns LilyPond file.
        '''
        from abjad.tools import lilypondfiletools
        from abjad.tools import markuptools
        lilypond_file = lilypondfiletools.make_basic_lilypond_file()
        lilypond_file.header_block.tagline = markuptools.Markup('""')
        lilypond_file.items.append(self)
        return lilypond_file

    def __str__(self):
        r'''Gets string representation of markup.

        ..  container:: example

            ::

                >>> string = r'\bold { allegro ma non troppo }'
                >>> markup = Markup(string)
                >>> print(str(markup))
                \markup {
                    \bold
                        {
                            allegro
                            ma
                            non
                            troppo
                        }
                    }

        Returns string.
        '''
        return self._lilypond_format

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='contents',
                display_string='arg',
                command='ag',
                editor=idetools.getters.get_string,
                ),
            systemtools.AttributeDetail(
                name='direction',
                command='dr',
                editor=idetools.getters.get_direction_string,
                ),
            systemtools.AttributeDetail(
                name='stack_priority',
                command='sp',
                editor=idetools.getters.get_integer,
                ),
            )

    @property
    def _format_pieces(self):
        return self._get_format_pieces()

    @property
    def _lilypond_format(self):
        return '\n'.join(self._get_format_pieces())

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        manager = systemtools.StorageFormatManager
        keyword_argument_names = \
            manager.get_signature_keyword_argument_names(self)
        keyword_argument_names = list(keyword_argument_names)
        keyword_argument_names.remove('stack_priority')
        keyword_argument_names = tuple(keyword_argument_names)
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    ### PRIVATE METHODS ###

    def _get_format_pieces(self):
        indent = '\t'
        direction = ''
        if self.direction is not None:
            direction = stringtools.arg_to_tridirectional_lilypond_symbol(
                self.direction)
        # none
        if self.contents is None:
            return [r'\markup {}']
        # a single string
        if len(self.contents) == 1 and isinstance(self.contents[0], str):
            content = self.contents[0]
            if '"' in content:
                content = schemetools.Scheme.format_scheme_value(content)
            if content:
                content = '{{ {} }}'.format(content)
            else:
                content = '{}'
            if direction:
                return [r'{} \markup {}'.format(direction, content)]
            return [r'\markup {}'.format(content)]
        # multiple strings or markup commands
        if direction:
            pieces = [r'{} \markup {{'.format(direction)]
        else:
            pieces = [r'\markup {']
        for content in self.contents:
            if isinstance(content, str):
                content = schemetools.Scheme.format_scheme_value(content)
                pieces.append('{}{}'.format(indent, content))
            else:
                pieces.extend(['{}{}'.format(indent, x) for x in
                    content._get_format_pieces()])
        pieces.append('{}}}'.format(indent))
        return pieces

    def _parse_markup_command_argument(self, argument):
        if isinstance(argument, type(self)):
            if len(argument.contents) == 1:
                contents = argument.contents[0]
            else:
                contents = list(argument.contents)
        elif isinstance(argument, (str, markuptools.MarkupCommand)):
            contents = argument
        else:
            message = 'must be markup, markup command or string: {!r}.'
            message = message.format(argument)
            raise TypeError(argument)
        return contents

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self):
        r'''Gets contents of markup.

        ..  container:: example

            ::

                >>> string = r'\bold { "This is markup text." }'
                >>> markup = Markup(string)
                >>> show(markup) # doctest: +SKIP

            ::

                >>> markup.contents
                (MarkupCommand('bold', ['This is markup text.']),)

        Returns tuple.
        '''
        return self._contents

    @property
    def direction(self):
        r'''Gets direction of markup.

        ..  container:: example

            ::

                >>> string = r'\bold { "This is markup text." }'
                >>> markup = Markup(string, direction=Up)
                >>> show(markup) # doctest: +SKIP

            ::

                >>> markup.direction
                Up

        Returns up, down, center or none.
        '''
        return self._direction

    @property
    def stack_priority(self):
        r'''Gets stack priority of markup.

        ..  container:: example

            **Example 1.** ``'foo'`` appears higher in stack than ``'bar'``:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> attach(Markup('foo', stack_priority=1000), staff[1])
                >>> attach(Markup('bar', stack_priority=0), staff[1])

            ::

                >>> show(staff) # doctest: +SKIP

            ..  doctest:

                >>> f(staff)
                \new Staff {
                    c'8
                    d'8
                        - \markup {
                            \column
                                {
                                    foo
                                    bar
                                }
                            }
                    e'8
                    f'8
                }

        ..  container:: example

            **Example 2.** ``'foo'`` appears lower in stack than ``'bar'``:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> attach(Markup('foo', stack_priority=0), staff[1])
                >>> attach(Markup('bar', stack_priority=1000), staff[1])

            ::

                >>> show(staff) # doctest: +SKIP

            ..  doctest:

                >>> f(staff)
                \new Staff {
                    c'8
                    d'8
                        - \markup {
                            \column
                                {
                                    bar
                                    foo
                                }
                            }
                    e'8
                    f'8
                }


        Higher priority equals higher position.

        Defaults to zero.

        Set to integer.
        '''
        return self._stack_priority

    ### PUBLIC METHODS ###

    def bold(self):
        r'''LilyPond ``\bold`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.bold()

            ::

                >>> print(format(markup))
                \markup {
                    \bold
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'bold',
            contents,
            )
        return new(self, contents=command)

    def box(self):
        r'''LilyPond ``\box`` markup command.

        ..  container:: example

            **Example 1.** Default box:

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.box()

            ::

                >>> print(format(markup))
                \markup {
                    \box
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        ..  container:: example

            **Example 2.** Customized box:

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.box()
                >>> markup = markup.override(('box-padding', 0.5))

            ::

                >>> print(format(markup))
                \markup {
                    \override
                        #'(box-padding . 0.5)
                        \box
                            "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP


        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'box',
            contents,
            )
        return new(self, contents=command)

    def caps(self):
        r'''LilyPond ``\caps`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.caps()

            ::

                >>> print(format(markup))
                \markup {
                    \caps
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'caps',
            contents,
            )
        return new(self, contents=command)

    def circle(self):
        r'''LilyPond ``\circle`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup.fraction(3, 5)
                >>> markup = markup.circle()
                >>> markup = markup.override(('circle-padding', 0.45))

            ::

                >>> print(format(markup))
                \markup {
                    \override
                        #'(circle-padding . 0.45)
                        \circle
                            \fraction
                                3
                                5
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'circle',
            contents,
            )
        return new(self, contents=command)

    @staticmethod
    def column(markups, direction=Up):
        r'''LilyPond ``\column`` markup command.

        ..  container:: example

            ::

                >>> city = Markup('Los Angeles')
                >>> date = Markup('May - August 2014')
                >>> markup = Markup.column([city, date])

            ::

                >>> print(format(markup))
                ^ \markup {
                    \column
                        {
                            "Los Angeles"
                            "May - August 2014"
                        }
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = []
        for markup in markups:
            contents.extend(markup.contents)
        command = markuptools.MarkupCommand(
            'column',
            contents,
            )
        return Markup(contents=command, direction=direction)

    def dynamic(self):
        r'''LilyPond ``\dynamic`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('sffz')
                >>> markup = markup.dynamic()

            ::

                >>> print(format(markup))
                \markup {
                    \dynamic
                        sffz
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'dynamic',
            contents,
            )
        return new(self, contents=command)

    def finger(self):
        r'''LilyPond ``\finger`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup(1)
                >>> markup = markup.finger()

            ::

                >>> print(format(markup))
                \markup {
                    \finger
                        1
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'finger',
            contents,
            )
        return new(self, contents=command)
            
    @staticmethod
    def fraction(numerator, denominator):
        r'''LilyPond ``\fraction`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup.fraction(3, 5)

            ::

                >>> print(format(markup))
                \markup {
                    \fraction
                        3
                        5
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup
        '''
        from abjad.tools import markuptools
        command = markuptools.MarkupCommand(
            'fraction',
            str(numerator),
            str(denominator),
            )
        return Markup(contents=command)

    def general_align(self, axis, direction):
        r'''LilyPond ``\general-align`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.general_align('Y', Up)
                >>> print(format(markup))
                \markup {
                    \general-align
                        #Y
                        #UP
                        "Allegro assai"
                    }

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        axis = schemetools.Scheme(axis)
        # TODO: make schemetools.Scheme(direction) work
        if direction == Up:
            direction = schemetools.Scheme('UP')
        elif direction == Down:
            direction = schemetools.Scheme('DOWN')
        elif direction == Center:
            direction = schemetools.Scheme('CENTER')
        else:
            message = 'unknown direction: {!r}.'
            message = message.format(direction)
            raise ValueError(message)
        command = markuptools.MarkupCommand(
            'general-align',
            axis,
            direction,
            contents,
            )
        return new(self, contents=command)

    def hcenter_in(self, length):
        r'''LilyPond ``\hcenter-in`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.hcenter_in(12)
                >>> print(format(markup))
                \markup {
                    \hcenter-in
                        #12
                        "Allegro assai"
                    }

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'hcenter-in',
            length,
            contents,
            )
        return new(self, contents=command)

    @staticmethod
    def hspace(amount):
        r'''LilyPond ``\hspace`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup.hspace(0.75)

            ::

                >>> f(markup)
                \markup {
                    \hspace
                        #0.75
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        command = markuptools.MarkupCommand(
            'hspace',
            amount,
            )
        return Markup(contents=command)

    def italic(self):
        r'''LilyPond ``\italic`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.italic()

            ::

                >>> print(format(markup))
                \markup {
                    \italic
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'italic',
            contents,
            )
        return new(self, contents=command)

    def larger(self):
        r'''LilyPond ``\larger`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.larger()

            ::

                >>> print(format(markup))
                \markup {
                    \larger
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'larger',
            contents,
            )
        return new(self, contents=command)

    def line(self, *markups):
        r'''LilyPond ``\line`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.line(Markup('ma'), Markup('non troppo'))

            ::

                >>> print(format(markup))
                \markup {
                    \line
                        {
                            "Allegro assai"
                            ma
                            "non troppo"
                        }
                    }


            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = []
        contents.extend(self.contents)
        for markup in markups:
            contents.extend(markup.contents)
        command = markuptools.MarkupCommand(
            'line',
            contents,
            )
        return new(self, contents=command)

    @staticmethod
    def musicglyph(glyph_name=None, direction=Up):
        r'''LilyPond ``\musicglyph`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup.musicglyph('accidentals.sharp')

            ::

                >>> print(format(markup))
                ^ \markup {
                    \musicglyph
                        #"accidentals.sharp"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.ly import music_glyphs
        from abjad.tools import markuptools
        glyph_name = glyph_name or 'accidentals.sharp'
        message = 'not a valid LilyPond glyph name.'
        assert glyph_name in music_glyphs, message
        glyph_scheme = schemetools.Scheme(glyph_name, force_quotes=True)
        command = markuptools.MarkupCommand(
            'musicglyph',
            glyph_scheme,
            )
        return markuptools.Markup(contents=command, direction=direction)

    def override(self, new_property):
        r'''LilyPond ``\override`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.parenthesize()
                >>> markup = markup.override(('padding', 0.75))

            ::

                >>> f(markup)
                \markup {
                    \override
                        #'(padding . 0.75)
                        \parenthesize
                            "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        new_property = schemetools.SchemePair(new_property)
        command = markuptools.MarkupCommand(
            'override',
            new_property,
            contents,
            )
        return new(self, contents=command)

    def pad_around(self, padding):
        r'''LilyPond ``\pad-around`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.pad_around(10)
                >>> markup = markup.box()

            ::

                >>> print(format(markup))
                \markup {
                    \box
                        \pad-around
                            #10
                            "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'pad-around',
            padding,
            contents,
            )
        return new(self, contents=command)

    def parenthesize(self):
        r'''LilyPond ``\parenthesie`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.parenthesize()

            ::
            
                >>> f(markup)
                \markup {
                    \parenthesize
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'parenthesize',
            contents,
            )
        return new(self, contents=command)

    def raise_(self, amount):
        r'''LilyPond ``\raise`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.raise_(0.35)

            ::

                >>> print(format(markup))
                \markup {
                    \raise
                        #0.35
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'raise',
            amount,
            contents,
            )
        return new(self, contents=command)

    @staticmethod
    def right_column(markups, direction=Up):
        r'''LilyPond ``\right-column`` markup command.

        ..  container:: example

            ::

                >>> city = Markup('Los Angeles')
                >>> date = Markup('May - August 2014')
                >>> markup = Markup.right_column([city, date])

            ::

                >>> print(format(markup))
                ^ \markup {
                    \right-column
                        {
                            "Los Angeles"
                            "May - August 2014"
                        }
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = []
        for markup in markups:
            contents.extend(markup.contents)
        command = markuptools.MarkupCommand(
            'right-column',
            contents,
            )
        return Markup(contents=command, direction=direction)

    def rotate(self, angle):
        r'''LilyPond ``\rotate`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.rotate(45)

            ::

                >>> print(format(markup))
                \markup {
                    \rotate
                        #45
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'rotate',
            angle,
            contents,
            )
        return new(self, contents=command)

    def scale(self, factor_pair):
        r'''LilyPond ``\scale`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.scale((0.75, 0.75))

            ::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        factor_pair = schemetools.SchemePair(factor_pair)
        command = markuptools.MarkupCommand(
            'scale',
            factor_pair,
            contents,
            )
        return new(self, contents=command)

    def smaller(self):
        r'''LilyPond ``\smaller`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.smaller()

            ::

                >>> print(format(markup))
                \markup {
                    \smaller
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'smaller',
            contents,
            )
        return new(self, contents=command)

    def tiny(self):
        r'''LilyPond ``\tiny`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.tiny()

            ::

                >>> print(format(markup))
                \markup {
                    \tiny
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'tiny',
            contents,
            )
        return new(self, contents=command)

    def translate(self, offset_pair):
        r'''LilyPond ``translate`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.translate((2, 1))

            ::

                >>> print(format(markup))
                \markup {
                    \translate
                        #'(2 . 1)
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        offset_pair = schemetools.SchemePair(offset_pair)
        command = markuptools.MarkupCommand(
            'translate',
            offset_pair,
            contents,
            )
        return new(self, contents=command)

    @staticmethod
    def triangle(is_filled=True):
        r'''LilyPond ``\triangle`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup.triangle()

            ::

                >>> print(format(markup))
                \markup {
                    \triangle
                        ##t
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup
        '''
        from abjad.tools import markuptools
        command = markuptools.MarkupCommand(
            'triangle',
            bool(is_filled),
            )
        return Markup(contents=command)

    def vcenter(self):
        r'''LilyPond ``\vcenter`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.vcenter()

            ::

                >>> print(format(markup))
                \markup {
                    \vcenter
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'vcenter',
            contents,
            )
        return new(self,
            contents=command,
            )

    def with_color(self, color):
        r'''LilyPond ``\with-color`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.with_color('blue')

            ::

                >>> print(format(markup))
                \markup {
                    \with-color
                        #blue
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        color = schemetools.Scheme(color)
        command = markuptools.MarkupCommand(
            'with-color',
            color,
            contents,
            )
        return new(self,
            contents=command,
            )