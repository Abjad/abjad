# -*- coding: utf-8 -*-
import collections
import fractions
import numbers
from abjad.tools import mathtools
from abjad.tools import schemetools
from abjad.tools import stringtools
from abjad.tools import systemtools
from abjad.tools.topleveltools import new
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Markup(AbjadValueObject):
    r'''A LilyPond markup.

    ..  container:: example

        **Example 1.** Initializes from string:

        ::

            >>> string = r'\bold { "This is markup text." }'
            >>> markup = Markup(string)
            >>> show(markup) # doctest: +SKIP

        ..  doctest::

            >>> print(format(markup))
            \markup { \bold { "This is markup text." } }

    ..  container:: example

        **Example 2.** Initializes from other markup:

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

        **Example 3.** Attaches markup to score components:

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
        '_annotation',
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
        from abjad.tools import markuptools
        from abjad.tools.topleveltools import parse
        self._annotation = None
        if contents is None:
            new_contents = ('',)
        elif isinstance(contents, str):
            to_parse = r'\markup {{ {} }}'.format(contents)
            parsed = parse(to_parse)
            if all(isinstance(x, str) for x in parsed.contents):
                new_contents = (' '.join(parsed.contents),)
            else:
                new_contents = tuple(parsed.contents)
        elif isinstance(contents, markuptools.MarkupCommand):
            new_contents = (contents,)
        elif isinstance(contents, type(self)):
            direction = direction or contents._direction
            new_contents = tuple(contents._contents)
        elif isinstance(contents, collections.Sequence) and 0 < len(contents):
            new_contents = []
            for arg in contents:
                if isinstance(arg, (str, markuptools.MarkupCommand)):
                    new_contents.append(arg)
                elif isinstance(arg, type(self)):
                    new_contents.extend(arg.contents)
                else:
                    new_contents.append(str(arg))
            new_contents = tuple(new_contents)
        else:
            new_contents = (str(contents),)
        self._contents = new_contents
        self._format_slot = 'right'
        direction = stringtools.expr_to_tridirectional_ordinal_constant(
            direction)
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
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

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
        lilypond_file = lilypondfiletools.make_basic_lilypond_file()
        lilypond_file.header_block.tagline = False
        markup = new(self, direction=None)
        lilypond_file.items.append(markup)
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

    ### PRIVATE METHODS ###

    def _get_format_pieces(self):
        from abjad.tools import systemtools
        indent = systemtools.LilyPondFormatManager.indent
        direction = ''
        if self.direction is not None:
            direction = stringtools.expr_to_tridirectional_lilypond_symbol(
                self.direction)
        # none
        if self.contents is None:
            return [r'\markup {}']
        # a single string
        if len(self.contents) == 1 and isinstance(self.contents[0], str):
            content = self.contents[0]
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

    def _get_format_specification(self):
        agent = systemtools.StorageFormatAgent(self)
        names = list(agent.signature_keyword_names)
        names.remove('stack_priority')
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_kwargs_names=names,
            )

    @staticmethod
    def _parse_markup_command_argument(argument):
        from abjad.tools import markuptools
        if isinstance(argument, Markup):
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

    def bracket(self):
        r'''LilyPond ``\bracket`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.bracket()

            ::

                >>> print(format(markup))
                \markup {
                    \bracket
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'bracket',
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

    def center_align(self):
        r'''LilyPond ``\center-align`` markup command.

        ..  container:: example

            ::

                >>> markup_a = Markup('one')
                >>> markup_b = Markup('two').center_align()
                >>> markup_c = Markup('three')
                >>> markup = Markup.column([markup_a, markup_b, markup_c])

            ::

                >>> print(format(markup))
                \markup {
                    \column
                        {
                            one
                            \center-align
                                two
                            three
                        }
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'center-align',
            contents,
            )
        return new(self, contents=command)

    @staticmethod
    def center_column(markups, direction=None):
        r'''LilyPond ``\center-column`` markup command.

        ..  container:: example

            ::

                >>> city = Markup('Los Angeles')
                >>> date = Markup('May - August 2014')
                >>> markup = Markup.center_column([city, date])

            ::

                >>> print(format(markup))
                \markup {
                    \center-column
                        {
                            "Los Angeles"
                            "May - August 2014"
                        }
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        ..  container:: example

            Also works with a list of strings:

            ::

                >>> city = 'Los Angeles'
                >>> date = 'May - August 2014'
                >>> markup = Markup.center_column([city, date])

            ::

                >>> print(format(markup))
                \markup {
                    \center-column
                        {
                            "Los Angeles"
                            "May - August 2014"
                        }
                    }

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = []
        for markup in markups:
            contents.append(Markup._parse_markup_command_argument(markup))
        command = markuptools.MarkupCommand(
            'center-column',
            contents,
            )
        return Markup(contents=command, direction=direction)

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
    def column(markups, direction=None):
        r'''LilyPond ``\column`` markup command.

        ..  container:: example

            ::

                >>> city = Markup('Los Angeles')
                >>> date = Markup('May - August 2014')
                >>> markup = Markup.column([city, date])

            ::

                >>> print(format(markup))
                \markup {
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

    @staticmethod
    def combine(markup_one, markup_two):
        r'''LilyPond ``\combine`` markup command.

        ..  container:: example

            ::

                >>> markup_one = Markup('a few words')
                >>> markup_two = Markup.draw_line(10, 0)
                >>> markup = Markup.combine(markup_one, markup_two)
                >>> print(format(markup))
                \markup {
                    \combine
                        "a few words"
                        \draw-line
                            #'(10 . 0)
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents_one = Markup._parse_markup_command_argument(markup_one)
        contents_two = Markup._parse_markup_command_argument(markup_two)
        command = markuptools.MarkupCommand(
            'combine',
            contents_one,
            contents_two,
            )
        return Markup(contents=command)

    @staticmethod
    def concat(markup_list):
        r'''LilyPond ``\concat`` markup command.

        ..  container:: example

            ::

                >>> downbow = Markup.musicglyph('scripts.downbow')
                >>> hspace = Markup.hspace(1)
                >>> upbow = Markup.musicglyph('scripts.upbow')
                >>> markup = Markup.concat([downbow, hspace, upbow])
                >>> print(format(markup))
                \markup {
                    \concat
                        {
                            \musicglyph
                                #"scripts.downbow"
                            \hspace
                                #1
                            \musicglyph
                                #"scripts.upbow"
                        }
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        result = []
        for markup in markup_list:
            contents = Markup._parse_markup_command_argument(markup)
            result.append(contents)
        command = markuptools.MarkupCommand(
            'concat',
            result,
            )
        return Markup(contents=command)

    @staticmethod
    def draw_circle(radius, thickness, filled=False):
        r'''LilyPond ``\draw-circle`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup.draw_circle(10, 1.5)

            ::

                >>> print(format(markup))
                \markup {
                    \draw-circle
                        #10
                        #1.5
                        ##f
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup
        '''
        from abjad.tools import markuptools
        command = markuptools.MarkupCommand(
            'draw-circle',
            radius,
            thickness,
            filled,
            )
        return Markup(contents=command)

    @staticmethod
    def draw_line(x, y):
        r'''LilyPond ``\draw-line`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup.draw_line(5, -2.5)

            ::

                >>> print(format(markup))
                \markup {
                    \draw-line
                        #'(5 . -2.5)
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup
        '''
        from abjad.tools import markuptools
        pair = schemetools.SchemePair(x, y)
        command = markuptools.MarkupCommand(
            'draw-line',
            pair,
            )
        return Markup(contents=command)

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

    @staticmethod
    def filled_box(x_extent, y_extent, blot=0):
        r'''LilyPond ``filled-box`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup.filled_box((0, 10), (2, 5), 1.5)
                >>> print(format(markup))
                \markup {
                    \filled-box
                        #'(0 . 10)
                        #'(2 . 5)
                        #1.5
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        x_extent = schemetools.SchemePair(x_extent)
        y_extent = schemetools.SchemePair(y_extent)
        blot = float(blot)
        command = markuptools.MarkupCommand(
            'filled-box',
            x_extent,
            y_extent,
            blot,
            )
        return Markup(command)

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
    def flat():
        r'''LilyPond ``\flat`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup.flat()

            ::

                >>> print(format(markup))
                \markup {
                    \flat
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        command = markuptools.MarkupCommand('flat')
        return Markup(contents=command)

    def fontsize(self, fontsize):
        r'''LilyPond ``\fontsize`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('foo')
                >>> markup = markup.fontsize(-3)

            ::

                >>> print(format(markup))
                \markup {
                    \fontsize #-3
                        foo
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup
        '''
        from abjad.tools import markuptools
        fontsize = float(fontsize)
        fontsize = mathtools.integer_equivalent_number_to_integer(fontsize)
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'fontsize',
            fontsize,
            contents,
            )
        return new(self, contents=command)

    @staticmethod
    def fraction(numerator, denominator):
        r'''LilyPond ``\fraction`` markup command.

        ..  container:: example

            **Example 1.** Fraction with integer numerator and denominator:

            ::

                >>> markup = Markup.fraction(1, 4)

            ::

                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> print(format(markup))
                \markup {
                    \fraction
                        1
                        4
                    }

        ..  container:: example

            **Example 2.** Fraction with string numerator and integer
            denominator:

            ::

                >>> markup = Markup.fraction('π', 4)

            ::

                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> print(format(markup))
                \markup {
                    \fraction
                        π
                        4
                    }

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

            **Example 1.** With Abjad direction constant:

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.general_align('Y', Up)

            ::

                >>> print(format(markup))
                \markup {
                    \general-align
                        #Y
                        #UP
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        ..  container:: example

            **Example 2.** With numeric direction value:

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.general_align('Y', 0.75)

            ::

                >>> print(format(markup))
                \markup {
                    \general-align
                        #Y
                        #0.75
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        axis = schemetools.Scheme(axis)
        # TODO: make schemetools.Scheme(Up) work
        if direction == Up:
            direction = schemetools.Scheme('UP')
        elif direction == Down:
            direction = schemetools.Scheme('DOWN')
        elif direction == Center:
            direction = schemetools.Scheme('CENTER')
        elif isinstance(direction, numbers.Number):
            direction = schemetools.Scheme(str(direction))
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

    def halign(self, direction):
        r'''LilyPond ``halign`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.halign(0)

            ::

                >>> print(format(markup))
                \markup {
                    \halign
                        #0
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'halign',
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

            ::

                >>> print(format(markup))
                \markup {
                    \hcenter-in
                        #12
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

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

    def huge(self):
        r'''LilyPond ``\huge`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.huge()

            ::

                >>> print(format(markup))
                \markup {
                    \huge
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'huge',
            contents,
            )
        return new(self, contents=command)

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

    @staticmethod
    def left_column(markups, direction=None):
        r'''LilyPond ``\left-column`` markup command.

        ..  container:: example

            ::

                >>> city = Markup('Los Angeles')
                >>> date = Markup('May - August 2014')
                >>> markup = Markup.left_column([city, date])

            ::

                >>> print(format(markup))
                \markup {
                    \left-column
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
            contents.append(Markup._parse_markup_command_argument(markup))
        command = markuptools.MarkupCommand(
            'left-column',
            contents,
            )
        return Markup(contents=command, direction=direction)

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
    def make_big_centered_page_number_markup(text=None):
        r'''Makes big centered page number markup.

        ..  container:: example

            ::

                >>> markup = Markup.make_big_centered_page_number_markup()

            ::

                >>> print(format(markup, 'lilypond'))
                \markup {
                    \fill-line
                        {
                            \bold
                                \fontsize
                                    #3
                                    \concat
                                        {
                                            \on-the-fly
                                                #print-page-number-check-first
                                                \fromproperty
                                                    #'page:page-number-string
                                        }
                        }
                    }

        Returns markup.
        '''
        assert isinstance(text, (str, type(None))), repr(text)
        if text is None:
            contents = r'''
            \fill-line {
            \bold \fontsize #3 \concat {
            \on-the-fly #print-page-number-check-first
            \fromproperty #'page:page-number-string } }'''
        else:
            contents = r'''
            \fill-line {{
            \bold \fontsize #3 \concat {{
            {} " " \char #x2014 " "
            \on-the-fly #print-page-number-check-first
            \fromproperty #'page:page-number-string }} }}'''
            contents = contents.format(text)
        markup = Markup(contents)
        return markup

    @staticmethod
    def make_blank_line_markup():
        r'''Makes blank line markup.

        ..  container:: example

            ::

                >>> markup = Markup.make_blank_line_markup()

            ::

                >>> print(format(markup))
                \markup { \fill-line { " " } }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns markup.
        '''
        return Markup(r'\fill-line { " " }')

    @staticmethod
    def make_centered_title_markup(
        title,
        font_name='Times New Roman',
        font_size=18,
        vspace_before=6,
        vspace_after=12,
        ):
        r'''Makes centered `title` markup.

        ..  container:: example

            ::

                >>> markup = Markup.make_centered_title_markup('String Quartet')

            ::

                >>> print(format(markup, 'lilypond'))
                \markup {
                    \override
                        #'(font-name . "Times New Roman")
                        \fontsize
                            #18
                            \column
                                {
                                    \center-align
                                        {
                                            {
                                                \vspace
                                                    #6
                                                \line
                                                    {
                                                        "String Quartet"
                                                    }
                                                \vspace
                                                    #12
                                            }
                                        }
                                }
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns markup.
        '''
        assert isinstance(title, (str, list))
        assert isinstance(font_name, str)
        assert isinstance(font_size, (int, float))
        if isinstance(title, str):
            title_lines = [title]
        else:
            title_lines = title
        title_lines_string = ''
        for title_line in title_lines:
            line = '                    \\line {{ "{}" }}\n'
            line = line.format(title_line)
            title_lines_string += line
        title_lines_string = title_lines_string.strip('\n')
        contents = r'''
            \override #'(font-name . "{}")
            \fontsize #{}
            \column {{
                \center-align {{
                    {{
                        \vspace #{}
                        {}
                        \vspace #{}
                    }}
                }}
            }}'''
        contents = contents.format(
            font_name,
            font_size,
            vspace_before,
            title_lines_string,
            vspace_after,
            )
        return Markup(contents)

    @staticmethod
    def make_improper_fraction_markup(rational):
        r'''Makes improper fraction markup.

        ..  container:: example

            **Example 1.** With integer-equivalent number:

            ::

                >>> markup = Markup.make_improper_fraction_markup(Fraction(6, 3))

            ::

                >>> print(format(markup))
                \markup { 2 }

            ::

                >>> show(markup) # doctest: +SKIP

        ..  container:: example

            **Example 2.** With non-integer-equivalent number:

            ::

                >>> markup = Markup.make_improper_fraction_markup(Fraction(7, 3))

            ::

                >>> print(format(markup))
                \markup {
                    2
                    \tiny
                        \fraction
                            1
                            3
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        '''
        from abjad.tools import mathtools
        if mathtools.is_integer_equivalent_number(rational):
            number = int(rational)
            markup = Markup(number)
            return markup
        assert isinstance(rational, fractions.Fraction), repr(rational)
        integer_part = int(rational)
        fraction_part = rational - integer_part
        integer_markup = Markup(integer_part)
        numerator = fraction_part.numerator
        denominator = fraction_part.denominator
        fraction_markup = Markup.fraction(numerator, denominator)
        fraction_markup = fraction_markup.tiny()
        markup = integer_markup + fraction_markup
        return markup

    @staticmethod
    def make_vertically_adjusted_composer_markup(
        composer,
        font_name='Times New Roman',
        font_size=3,
        space_above=20,
        space_right=0,
        ):
        r'''Makes vertically adjusted `composer` markup.

        ..  container:: example

            ::

                >>> markup = Markup.make_vertically_adjusted_composer_markup(
                ...     'Josquin Desprez',
                ...     )

            ::

                >>> print(format(markup, 'lilypond'))
                \markup {
                    \override
                        #'(font-name . "Times New Roman")
                        {
                            \hspace
                                #0
                            \raise
                                #-20
                                \fontsize
                                    #3
                                    "Josquin Desprez"
                            \hspace
                                #0
                        }
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns markup.
        '''
        assert isinstance(composer, str)
        assert isinstance(font_name, str)
        assert isinstance(font_size, (int, float))
        assert isinstance(space_above, (int, float))
        assert isinstance(space_right, (int, float))
        contents = r'''
            \override #'(font-name . "{}") {{
                \hspace #0
                \raise #-{} \fontsize #{} "{}"
                \hspace #{}
            }}
        '''
        contents = contents.format(
            font_name,
            space_above,
            font_size,
            composer,
            space_right,
            )
        return Markup(contents)

    @staticmethod
    def musicglyph(glyph_name=None, direction=None):
        r'''LilyPond ``\musicglyph`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup.musicglyph('accidentals.sharp')

            ::

                >>> print(format(markup))
                \markup {
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

    @staticmethod
    def natural():
        r'''LilyPond ``\natural`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup.natural()

            ::

                >>> print(format(markup))
                \markup {
                    \natural
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        command = markuptools.MarkupCommand('natural')
        return Markup(contents=command)

    @staticmethod
    def note_by_number(log, dot_count, stem_direction, direction=None):
        r'''LilyPond ``\note-by-number`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup.note_by_number(3, 2, 1)

            ::

                >>> print(format(markup))
                \markup {
                    \note-by-number
                        #3
                        #2
                        #1
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        command = markuptools.MarkupCommand(
            'note-by-number',
            log,
            dot_count,
            stem_direction,
            )
        return Markup(contents=command, direction=direction)

    @staticmethod
    def null(direction=None):
        r'''LilyPond ``\null`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup.null()

            ::

                >>> print(format(markup))
                \markup {
                    \null
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        command = markuptools.MarkupCommand(
            'null',
            )
        return Markup(contents=command, direction=direction)

    @staticmethod
    def overlay(markups, direction=None):
        r'''LilyPond ``\overlay`` markup command.

        ..  container:: example

            ::

                >>> city = Markup('Los Angeles')
                >>> date = Markup('May - August 2014')
                >>> markup = Markup.overlay([city, date])

            ::

                >>> print(format(markup))
                \markup {
                    \overlay
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
            contents.append(Markup._parse_markup_command_argument(markup))
        command = markuptools.MarkupCommand(
            'overlay',
            contents,
            )
        return Markup(contents=command, direction=direction)

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

    def pad_to_box(self, x_extent, y_extent):
        r'''LilyPond ``pad-to-box`` markup command.

        ..  container:: example

            **Example 1.** Positive extents.

            The following postscript describes a filled box between the
            x-coordinates of 0 and 10 and the y-coordinates of 0 and 10.
            Normally, this would be drawn off the edge of the page.

            ::

                >>> up_postscript = markuptools.Postscript()
                >>> up_postscript = up_postscript.newpath()
                >>> up_postscript = up_postscript.moveto(0, 0)
                >>> up_postscript = up_postscript.rlineto(10, 0)
                >>> up_postscript = up_postscript.rlineto(0, 10)
                >>> up_postscript = up_postscript.rlineto(-10, 0)
                >>> up_postscript = up_postscript.closepath()
                >>> up_postscript = up_postscript.setgray(0.75)
                >>> up_postscript = up_postscript.fill()
                >>> up_postscript_markup = up_postscript.as_markup()
                >>> print(format(up_postscript_markup))
                \markup {
                    \postscript
                        #"
                        newpath
                        0 0 moveto
                        10 0 rlineto
                        0 10 rlineto
                        -10 0 rlineto
                        closepath
                        0.75 setgray
                        fill
                        "
                    }

            Notice how the top half of the square is cut off. The coordinates
            of the postscript put most of the drawing off the edge of the page.
            LilyPond does not know what the size of the postscript is, so it
            does not attempt to reposition it:

            ::

                >>> show(up_postscript_markup) # doctest: +SKIP

            Wrapping the postscript in a box shows that LilyPond believes the
            postscript has effectively no x or y extent:

            ::

                >>> show(up_postscript_markup.box()) # doctest: +SKIP

            By giving the postscript markup explicit extents, we can instruct
            LilyPond to position it properly:

            ::

                >>> up_postscript_markup = up_postscript_markup.pad_to_box(
                ...     (0, 10), (0, 10))
                >>> show(up_postscript_markup) # doctest: +SKIP

            Boxing also shows that extents have been applied correctly:

            ::

                >>> show(up_postscript_markup.box()) # doctest: +SKIP

        ..  container:: example

            **Example 2.** Negative extents.

            LilyPond does not appear to handle negative extents in the same was
            as it handles positive extents.

            The following postscript describes a box of the same shape as in
            the previous example. However, this box's x- and y-coordinates
            range between 0 and 10 and 0 and -10 respectively.

            ::

                >>> down_postscript = markuptools.Postscript()
                >>> down_postscript = down_postscript.newpath()
                >>> down_postscript = down_postscript.moveto(0, 0)
                >>> down_postscript = down_postscript.rlineto(10, 0)
                >>> down_postscript = down_postscript.rlineto(0, -10)
                >>> down_postscript = down_postscript.rlineto(-10, 0)
                >>> down_postscript = down_postscript.closepath()
                >>> down_postscript = down_postscript.setgray(0.75)
                >>> down_postscript = down_postscript.fill()
                >>> down_postscript_markup = down_postscript.as_markup()
                >>> print(format(down_postscript_markup))
                \markup {
                    \postscript
                        #"
                        newpath
                        0 0 moveto
                        10 0 rlineto
                        0 -10 rlineto
                        -10 0 rlineto
                        closepath
                        0.75 setgray
                        fill
                        "
                    }

            This time, the entire markup appears to display, without being cut
            off:

            ::

                >>> show(down_postscript_markup) # doctest: +SKIP

            However, boxing the markup shows that LilyPond still believes it to
            be of 0-height and 0-width. Notice that the box appears in a
            different corner of the grey square than in the previous example.
            This corner is the markup *origin*. The grey box in example 2
            *descends* from the origin, while the grey box in example 1
            *ascends* from it.

            ::

                >>> show(down_postscript_markup.box()) # doctest: +SKIP

            Giving the postscript markup positive extents does not work:

            ::

                >>> markup = down_postscript_markup.pad_to_box(
                ...     (0, 10), (0, 10))
                >>> show(markup.box()) # doctest: +SKIP

            Likewise, giving the postscript markup negative extents also
            does not work. The negative extents are treated as 0. In this case,
            the postscript markup is treated as though it had a height of 0:

            ::

                >>> markup = down_postscript_markup.pad_to_box(
                ...     (0, 10), (0, -10))
                >>> show(markup.box()) # doctest: +SKIP

            Unfortunately, this means that any part of a postscript-created
            markup that uses negative coordinates cannot be treated properly by
            LilyPond's markup spacing logic. To avoid this, only use positive
            coordinates in postscript.

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        x_extent = schemetools.SchemePair(x_extent)
        y_extent = schemetools.SchemePair(y_extent)
        command = markuptools.MarkupCommand(
            'pad-to-box',
            x_extent,
            y_extent,
            contents,
            )
        return new(self, contents=command)

    def parenthesize(self):
        r'''LilyPond ``\parenthesize`` markup command.

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

    @staticmethod
    def postscript(postscript):
        r'''LilyPond ``\postscript`` markup command.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.moveto(1, 1)
                >>> postscript = postscript.setlinewidth(2.5)
                >>> postscript = postscript.setdash((2, 1))
                >>> postscript = postscript.lineto(3, -4)
                >>> postscript = postscript.stroke()
                >>> markup = markuptools.Markup.postscript(postscript)

            ::

                >>> print(format(markup))
                \markup {
                    \postscript
                        #"
                        1 1 moveto
                        2.5 setlinewidth
                        [ 2 1 ] 0 setdash
                        3 -4 lineto
                        stroke
                        "
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        if isinstance(postscript, markuptools.Postscript):
            postscript = str(postscript)
        assert isinstance(postscript, str)
        command = markuptools.MarkupCommand(
            'postscript',
            postscript,
            )
        return Markup(contents=command)

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
    def right_column(markups, direction=None):
        r'''LilyPond ``\right-column`` markup command.

        ..  container:: example

            ::

                >>> city = Markup('Los Angeles')
                >>> date = Markup('May - August 2014')
                >>> markup = Markup.right_column([city, date])

            ::

                >>> print(format(markup))
                \markup {
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
            contents.append(Markup._parse_markup_command_argument(markup))
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

    def sans(self):
        r'''LilyPond ``\sans`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.sans()

            ::

                >>> print(format(markup))
                \markup {
                    \sans
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'sans',
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

    @staticmethod
    def sharp():
        r'''LilyPond ``\sharp`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup.sharp()

            ::

                >>> print(format(markup))
                \markup {
                    \sharp
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        command = markuptools.MarkupCommand('sharp')
        return Markup(contents=command)

    def small(self):
        r'''LilyPond ``\small`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.small()

            ::

                >>> print(format(markup))
                \markup {
                    \small
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'small',
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

    def sub(self):
        r'''LilyPond ``\sub`` markup command.

        ..  container:: example

            ::

                >>> markups = [Markup('A'), Markup('j').sub()]
                >>> markup = Markup.concat(markups)

            ::

                >>> print(format(markup))
                \markup {
                    \concat
                        {
                            A
                            \sub
                                j
                        }
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'sub',
            contents,
            )
        return new(self, contents=command)

    def super_(self):
        r'''LilyPond ``\super`` markup command.

        ..  container:: example

            ::

                >>> markups = [Markup('1'), Markup('st').super_()]
                >>> markup = Markup.concat(markups)

            ::

                >>> print(format(markup))
                \markup {
                    \concat
                        {
                            1
                            \super
                                st
                        }
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'super',
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

    def upright(self):
        r'''LilyPond ``\upright`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup('Allegro assai')
                >>> markup = markup.upright()

            ::

                >>> print(format(markup))
                \markup {
                    \upright
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'upright',
            contents,
            )
        return new(self, contents=command)

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
        return new(self, contents=command)

    @staticmethod
    def vspace(amount):
        r'''LilyPond ``\vspace`` markup command.

        ..  container:: example

            ::

                >>> markup = Markup.vspace(0.75)

            ::

                >>> f(markup)
                \markup {
                    \vspace
                        #0.75
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        command = markuptools.MarkupCommand(
            'vspace',
            amount,
            )
        return Markup(contents=command)

    def whiteout(self):
        r'''LilyPond ``\whiteout`` markup command.

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        command = markuptools.MarkupCommand(
            'whiteout',
            contents,
            )
        return new(self, contents=command)

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

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        color = schemetools.Scheme(color)
        command = markuptools.MarkupCommand(
            'with-color',
            color,
            contents,
            )
        return new(self, contents=command)

    def with_dimensions(self, x_extent, y_extent):
        r'''LilyPond ``with-dimensions`` markup command.

        ..  note::

            See the API entry for ``Markup.pad_to_box()`` for an extensive
            discussion of setting explicit markup extents.

        ..  container:: example

            **Example 1.**

            ::

                >>> up_postscript = markuptools.Postscript()
                >>> up_postscript = up_postscript.newpath()
                >>> up_postscript = up_postscript.moveto(0, 0)
                >>> up_postscript = up_postscript.rlineto(10, 0)
                >>> up_postscript = up_postscript.rlineto(0, 10)
                >>> up_postscript = up_postscript.rlineto(-10, 0)
                >>> up_postscript = up_postscript.closepath()
                >>> up_postscript = up_postscript.setgray(0.75)
                >>> up_postscript = up_postscript.fill()
                >>> up_markup = up_postscript.as_markup()

            ::

                >>> show(up_markup.box()) # doctest: +SKIP

            ::

                >>> up_markup = up_markup.with_dimensions((0, 10), (0, 10))
                >>> up_markup = up_markup.box()
                >>> show(up_markup) # doctest: +SKIP

            ::

                >>> up_markup = up_postscript.as_markup()
                >>> up_markup = up_markup.with_dimensions((0, 20), (0, 20))
                >>> up_markup = up_markup.box()
                >>> show(up_markup) # doctest: +SKIP

            ::

                >>> up_markup = up_postscript.as_markup()
                >>> up_markup = up_markup.with_dimensions((0, 20), (0, -20))
                >>> up_markup = up_markup.box()
                >>> show(up_markup) # doctest: +SKIP

        ..  container:: example

            **Example 2.**

            ::

                >>> down_postscript = markuptools.Postscript()
                >>> down_postscript = down_postscript.newpath()
                >>> down_postscript = down_postscript.moveto(0, 0)
                >>> down_postscript = down_postscript.rlineto(10, 0)
                >>> down_postscript = down_postscript.rlineto(0, -10)
                >>> down_postscript = down_postscript.rlineto(-10, 0)
                >>> down_postscript = down_postscript.closepath()
                >>> down_postscript = down_postscript.setgray(0.75)
                >>> down_postscript = down_postscript.fill()
                >>> down_markup = down_postscript.as_markup()

            ::

                >>> show(down_markup.box()) # doctest: +SKIP

            ::

                >>> down_markup = down_markup.with_dimensions((0, 10), (0, 10))
                >>> down_markup = down_markup.box()
                >>> show(down_markup) # doctest: +SKIP

            ::

                >>> down_markup = down_postscript.as_markup()
                >>> down_markup = down_markup.with_dimensions(
                ...     (0, 10), (0, -10))
                >>> down_markup = down_markup.box()
                >>> show(down_markup) # doctest: +SKIP

            ::

                >>> down_markup = down_postscript.as_markup()
                >>> down_markup = down_markup.with_dimensions(
                ...     (-5, 15), (5, -15))
                >>> down_markup = down_markup.box()
                >>> show(down_markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        contents = self._parse_markup_command_argument(self)
        x_extent = schemetools.SchemePair(x_extent)
        y_extent = schemetools.SchemePair(y_extent)
        command = markuptools.MarkupCommand(
            'with-dimensions',
            x_extent,
            y_extent,
            contents,
            )
        return new(self, contents=command)

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return '\n'.join(self._get_format_pieces())

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
