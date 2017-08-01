# -*- coding: utf-8 -*-
import collections
import inspect
import numbers
from abjad import Fraction
from abjad.tools import mathtools
from abjad.tools import schemetools
from abjad.tools import datastructuretools
from abjad.tools import systemtools
from abjad.tools.topleveltools import new
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.markuptools.MarkupCommand import MarkupCommand
from abjad.tools.markuptools.Postscript import Postscript


class Markup(AbjadValueObject):
    r'''LilyPond markup.

    ::

        >>> import abjad

    ..  container:: example

        Initializes from string:

        ..  container:: example

            ::

                >>> string = r'\italic { "Allegro assai" }'
                >>> markup = abjad.Markup(string)
                >>> f(markup)
                \markup { \italic { "Allegro assai" } }

            ::

                >>> show(markup) # doctest: +SKIP

    ..  container:: example

        Initializes from other markup:

        ..  container:: example

            ::

                >>> markup = abjad.Markup('Allegro assai', direction=Up)
                >>> markup = markup.italic()
                >>> markup = abjad.Markup(markup, direction=Down)
                >>> f(markup)
                _ \markup {
                    \italic
                        "Allegro assai"
                    }

            ::
            
                >>> show(markup) # doctest: +SKIP

    ..  container:: example

        Attaches markup to score components:

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> string = r'\italic { "Allegro assai" }'
                >>> markup = abjad.Markup(string, direction=Up)
                >>> f(markup)
                ^ \markup {
                    \italic
                        {
                            "Allegro assai"
                        }
                    }

            ::

                >>> abjad.attach(markup, staff[0])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'8
                        ^ \markup {
                            \italic
                                {
                                    "Allegro assai"
                                }
                            }
                    d'8
                    e'8
                    f'8
                }

    ..  note:: Make sure all static markup methods implement a direction
        keyword when extending this class.

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
        '_lilypond_tweak_manager',
        '_stack_priority',
        )

    _private_attributes_to_copy = (
        '_lilypond_tweak_manager',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        contents=None,
        direction=None,
        stack_priority=0,
        ):
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
        elif isinstance(contents, MarkupCommand):
            new_contents = (contents,)
        elif isinstance(contents, type(self)):
            direction = direction or contents._direction
            new_contents = tuple(contents._contents)
        elif isinstance(contents, collections.Sequence) and 0 < len(contents):
            new_contents = []
            for argument in contents:
                if isinstance(argument, (str, MarkupCommand)):
                    new_contents.append(argument)
                elif isinstance(argument, type(self)):
                    new_contents.extend(argument.contents)
                else:
                    new_contents.append(str(argument))
            new_contents = tuple(new_contents)
        else:
            new_contents = (str(contents),)
        self._contents = new_contents
        self._format_slot = 'right'
        direction = datastructuretools.String.to_tridirectional_ordinal_constant(
            direction)
        self._direction = direction
        self._lilypond_tweak_manager = None
        assert isinstance(stack_priority, int), repr(stack_priority)
        self._stack_priority = stack_priority

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r'''Adds markup to `argument`.

        ..  container:: example

            Adds markup to markup:

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro') + abjad.Markup('assai')
                    >>> f(markup)
                    \markup {
                        Allegro
                        assai
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        ..  container:: example

            Adds markup command to markup:

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro') + abjad.Markup.hspace(0.75)
                    >>> markup = markup + abjad.Markup('assai')
                    >>> f(markup)
                    \markup {
                        Allegro
                        \hspace
                            #0.75
                        assai
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        commands = list(self.contents)
        if isinstance(argument, type(self)):
            commands.extend(argument.contents)
        elif isinstance(argument, MarkupCommand):
            commands.append(argument)
        else:
            message = 'must be markup or markup command: {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        markup = type(self)(contents=commands, direction=self.direction)
        return markup

    def __copy__(self, *arguments):
        r'''Copies markup.

        ::

            >>> import copy

        ..  container:: example

            ::

                >>> markup_1 = abjad.Markup('Allegro assai', direction=Up)
                >>> markup_2 = copy.copy(markup_1)

            ::

                >>> markup_1
                Markup(contents=['Allegro assai'], direction=Up)

            ::

                >>> markup_2
                Markup(contents=['Allegro assai'], direction=Up)

            ::

                >>> markup_1 == markup_2
                True

            ::

                >>> markup_1 is markup_2
                False

        Returns new markup.
        '''
        superclass = super(Markup, self)
        return superclass.__copy__(*arguments)

    def __eq__(self, argument):
        r'''Is true markup equals `argument`.

        ..  container:: example

            Without keywords:

            ::

                >>> markup_1 = abjad.Markup('Allegro')
                >>> markup_2 = abjad.Markup('Allegro')
                >>> markup_3 = abjad.Markup('Allegro assai')

            ::

                >>> markup_1 == markup_1
                True
                >>> markup_1 == markup_2
                True
                >>> markup_1 == markup_3
                False
                >>> markup_2 == markup_1
                True
                >>> markup_2 == markup_2
                True
                >>> markup_2 == markup_3
                False
                >>> markup_3 == markup_1
                False
                >>> markup_3 == markup_2
                False
                >>> markup_3 == markup_3
                True

        ..  container:: example

            With keywords:

            ::

                >>> markup_1 = abjad.Markup('Allegro')
                >>> markup_2 = abjad.Markup('Allegro', direction=Up)

            ::

                >>> markup_1 == markup_1
                True
                >>> markup_1 == markup_2
                False
                >>> markup_2 == markup_1
                False
                >>> markup_2 == markup_2
                True

        Returns new markup.
        '''
        return super(Markup, self).__eq__(argument)

    def __format__(self, format_specification=''):
        r'''Formats markup.

        ..  container:: example

            ..  container:: example

                Formats markup:

                ::

                    >>> string = r'\italic { Allegro assai }'
                    >>> markup = abjad.Markup(string)
                    >>> f(markup)
                    \markup {
                        \italic
                            {
                                Allegro
                                assai
                            }
                        }


        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._get_lilypond_format()
        elif format_specification == 'storage':
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __hash__(self):
        r'''Hashes markup.

        ..  container:: example

            Without keywords:

            ::

                >>> hash_1 = hash(abjad.Markup('Allegro'))
                >>> hash_2 = hash(abjad.Markup('Allegro'))
                >>> hash_3 = hash(abjad.Markup('Allegro assai'))

            ::

                >>> hash_1 == hash_1
                True
                >>> hash_1 == hash_2
                True
                >>> hash_1 == hash_3
                False
                >>> hash_2 == hash_1
                True
                >>> hash_2 == hash_2
                True
                >>> hash_2 == hash_3
                False
                >>> hash_3 == hash_1
                False
                >>> hash_3 == hash_2
                False
                >>> hash_3 == hash_3
                True

        ..  container:: example

            With keywords:

            ::

                >>> hash_1 = hash(abjad.Markup('Allegro'))
                >>> hash_2 = hash(abjad.Markup('Allegro', direction=Up))

            ::

                >>> hash_1 == hash_1
                True
                >>> hash_1 == hash_2
                False
                >>> hash_2 == hash_1
                False
                >>> hash_2 == hash_2
                True

        '''
        return super(Markup, self).__hash__()

    def __illustrate__(self):
        r'''Illustrates markup.

        ..  container:: example

            ..  container:: example

                ::

                    >>> string = r'\italic { Allegro assai }'
                    >>> markup = abjad.Markup(string)
                    >>> f(markup)
                    \markup {
                        \italic
                            {
                                Allegro
                                assai
                            }
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = markup.__illustrate__()
                    >>> f(lilypond_file.items[-1])
                    \markup {
                        \italic
                            {
                                Allegro
                                assai
                            }
                        }

        Returns LilyPond file.
        '''
        import abjad
        lilypond_file = abjad.LilyPondFile.new()
        lilypond_file.header_block.tagline = False
        markup = new(self, direction=None)
        lilypond_file.items.append(markup)
        return lilypond_file

    def __lt__(self, argument):
        r'''Is true when markup contents compare less than `argument` contents.

        ..  container:: example

            ::

                >>> markup_1 = abjad.Markup('Allegro')
                >>> markup_2 = abjad.Markup('assai')

            ::

                >>> markup_1 < markup_2
                True
                >>> markup_2 < markup_1
                False

        Raises type error when `argument` is not markup.

        Returns true or false.
        '''
        if not isinstance(argument, type(self)):
            message = 'can only compare markup to markup: {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        return self.contents < argument.contents 

    def __radd__(self, argument):
        r'''Adds `argument` to markup.

        ..  container:: example

            Adds markup to markup:

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro') + abjad.Markup('assai')
                    >>> f(markup)
                    \markup {
                        Allegro
                        assai
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        ..  container:: example

            Adds markup to markup command:

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro') + abjad.Markup.hspace(0.75)
                    >>> markup = markup + abjad.Markup('assai')
                    >>> f(markup)
                    \markup {
                        Allegro
                        \hspace
                            #0.75
                        assai
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        commands = []
        if isinstance(argument, type(self)):
            commands.extend(argument.contents)
        elif isinstance(argument, MarkupCommand):
            commands.append(argument)
        else:
            message = 'must be markup or markup command: {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        commands.extend(self.contents)
        markup = type(self)(contents=commands, direction=self.direction)
        return markup

    def __str__(self):
        r'''Gets string representation of markup.

        ..  container:: example

            ..  container:: example

                ::

                    >>> string = r'\italic { Allegro assai }'
                    >>> markup = abjad.Markup(string)
                    >>> print(str(markup))
                    \markup {
                        \italic
                            {
                                Allegro
                                assai
                            }
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns string.
        '''
        return self._get_lilypond_format()

    ### PRIVATE METHODS ###

    def _get_format_pieces(self):
        from abjad.tools import systemtools
        if self._lilypond_tweak_manager is None:
            tweaks = []
        else:
            tweaks = self._lilypond_tweak_manager._list_format_contributions()
        indent = systemtools.LilyPondFormatManager.indent
        direction = ''
        if self.direction is not None:
            direction = datastructuretools.String.to_tridirectional_lilypond_symbol(
                self.direction)
        if len(self.contents) == 1 and isinstance(self.contents[0], str):
            content = self.contents[0]
            content = schemetools.Scheme.format_scheme_value(content)
            if content:
                content = '{{ {} }}'.format(content)
            else:
                content = '{}'
            if direction:
                return tweaks + [r'{} \markup {}'.format(direction, content)]
            return tweaks + [r'\markup {}'.format(content)]
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
        return tweaks + pieces

    def _get_format_specification(self):
        agent = systemtools.StorageFormatAgent(self)
        names = list(agent.signature_keyword_names)
        names.remove('stack_priority')
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_kwargs_names=names,
            )

    def _get_lilypond_format(self):
        return '\n'.join(self._get_format_pieces())

    @staticmethod
    def _parse_markup_command_argument(argument):
        if isinstance(argument, Markup):
            if len(argument.contents) == 1:
                contents = argument.contents[0]
            else:
                contents = list(argument.contents)
        elif isinstance(argument, (str, MarkupCommand)):
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

            ..  container:: example

                Initializes contents positionally:

                ::

                    >>> abjad.Markup('Allegro assai')
                    Markup(contents=['Allegro assai'])

                Initializes contents from keyword:

                ::

                    >>> abjad.Markup(contents='Allegro assai')
                    Markup(contents=['Allegro assai'])

        Returns tuple.
        '''
        return list(self._contents)

    @property
    def direction(self):
        r'''Gets direction of markup.

        ..  container:: example

            ..  container:: example

                Initializes without direction:

                ::

                    >>> abjad.Markup('Allegro')
                    Markup(contents=['Allegro'])

                Initializes with direction:

                ::

                    >>> abjad.Markup('Allegro', direction=Up)
                    Markup(contents=['Allegro'], direction=Up)

        Defaults to none.

        Set to up, down, center or none.

        Returns up, down, center or none.
        '''
        return self._direction

    @property
    def stack_priority(self):
        r'''Gets stack priority of markup.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> abjad.attach(abjad.Markup(('Non',  'troppo'), stack_priority=1000), staff[1])
                >>> abjad.attach(abjad.Markup('allegro', stack_priority=0), staff[1])

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
                                    \line
                                        {
                                            Non
                                            troppo
                                        }
                                    \line
                                        {
                                            allegro
                                        }
                                }
                            }
                    e'8
                    f'8
                }

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> abjad.attach(abjad.Markup(('non',  'troppo'), stack_priority=0), staff[1])
                >>> abjad.attach(abjad.Markup('Allegro', stack_priority=1000), staff[1])

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
                                    \line
                                        {
                                            Allegro
                                        }
                                    \line
                                        {
                                            non
                                            troppo
                                        }
                                }
                            }
                    e'8
                    f'8
                }

        Higher priority equals greater absolute distance from staff.

        Defaults to zero.

        Set to integer.

        Returns integer.
        '''
        return self._stack_priority

    ### PUBLIC METHODS ###

    def bold(self):
        r'''LilyPond ``\bold`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.bold()
                    >>> f(markup)
                    \markup {
                        \bold
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand(
            'bold',
            contents,
            )
        return new(self, contents=command)

    def box(self):
        r'''LilyPond ``\box`` markup command.

        ..  container:: example

            Default box:

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.box()
                    >>> f(markup)
                    \markup {
                        \box
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        ..  container:: example

            Customized box:

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.box()
                    >>> markup = markup.override(('box-padding', 0.5))
                    >>> f(markup)
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
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('box', contents)
        return new(self, contents=command)

    def bracket(self):
        r'''LilyPond ``\bracket`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.bracket()
                    >>> f(markup)
                    \markup {
                        \bracket
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('bracket', contents)
        return new(self, contents=command)

    def caps(self):
        r'''LilyPond ``\caps`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.caps()
                    >>> f(markup)
                    \markup {
                        \caps
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('caps', contents)
        return new(self, contents=command)

    def center_align(self):
        r'''LilyPond ``\center-align`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup_a = abjad.Markup('allegro')
                    >>> markup_b = abjad.Markup('non').center_align()
                    >>> markup_c = abjad.Markup('troppo')
                    >>> markup = abjad.Markup.column([markup_a, markup_b, markup_c])
                    >>> f(markup)
                    \markup {
                        \column
                            {
                                allegro
                                \center-align
                                    non
                                troppo
                            }
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('center-align', contents)
        return new(self, contents=command)

    @staticmethod
    def center_column(markup_list, direction=None):
        r'''LilyPond ``\center-column`` markup command.

        ..  container:: example

            ::

                >>> city = abjad.Markup('Los Angeles')
                >>> date = abjad.Markup('May - August 2014')
                >>> markup = abjad.Markup.center_column([city, date])
                >>> f(markup)
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
                >>> markup = abjad.Markup.center_column([city, date])
                >>> f(markup)
                \markup {
                    \center-column
                        {
                            "Los Angeles"
                            "May - August 2014"
                        }
                    }

            ::

                >>> show(markup) # doctest: +SKIP    

        Returns new markup.
        '''
        contents = []
        for markup in markup_list:
            contents.append(Markup._parse_markup_command_argument(markup))
        command = MarkupCommand('center-column', contents)
        return Markup(contents=command, direction=direction)

    def circle(self):
        r'''LilyPond ``\circle`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup.fraction(3, 5)
                    >>> markup = markup.circle()
                    >>> markup = markup.override(('circle-padding', 0.45))
                    >>> f(markup)
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
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('circle', contents)
        return new(self, contents=command)

    @staticmethod
    def column(markup_list, direction=None):
        r'''LilyPond ``\column`` markup command.

        ..  container:: example

            ::

                >>> city = abjad.Markup('Los Angeles')
                >>> date = abjad.Markup('May - August 2014')
                >>> markup = abjad.Markup.column([city, date])
                >>> f(markup)
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
        contents = []
        for markup in markup_list:
            contents.extend(markup.contents)
        command = MarkupCommand('column', contents)
        return Markup(contents=command, direction=direction)

    @staticmethod
    def combine(markup_list, direction=None):
        r'''LilyPond ``\combine`` markup command.

        ..  container:: example

            ::

                >>> markup_one = abjad.Markup('Allegro assai')
                >>> markup_two = abjad.Markup.draw_line(13, 0)
                >>> markup_list = [markup_one, markup_two]
                >>> markup = abjad.Markup.combine(markup_list, direction=Up)
                >>> f(markup)
                ^ \markup {
                    \combine
                        "Allegro assai"
                        \draw-line
                            #'(13 . 0)
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        if not len(markup_list) == 2:
            message = 'markup list must be length 2: {!r}.'
            message = message.format(markup_list)
            raise Exception(message)
        markup_1, markup_2 = markup_list
        contents_1 = Markup._parse_markup_command_argument(markup_1)
        contents_2 = Markup._parse_markup_command_argument(markup_2)
        command = MarkupCommand('combine', contents_1, contents_2)
        return Markup(contents=command, direction=direction)

    @staticmethod
    def concat(markup_list, direction=None):
        r'''LilyPond ``\concat`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> downbow = abjad.Markup.musicglyph('scripts.downbow')
                    >>> hspace = abjad.Markup.hspace(1)
                    >>> upbow = abjad.Markup.musicglyph('scripts.upbow')
                    >>> markup_list = [downbow, hspace, upbow]
                    >>> markup = abjad.Markup.concat(markup_list, direction=Up)
                    >>> f(markup)
                    ^ \markup {
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
        result = []
        for markup in markup_list:
            contents = Markup._parse_markup_command_argument(markup)
            result.append(contents)
        command = MarkupCommand('concat', result)
        return Markup(contents=command, direction=direction)

    @staticmethod
    def draw_circle(radius, thickness, direction=None, filled=False):
        r'''LilyPond ``\draw-circle`` markup command.

        ..  container:: example

            ::

                >>> markup = abjad.Markup.draw_circle(10, 1.5, direction=Up)
                >>> f(markup)
                ^ \markup {
                    \draw-circle
                        #10
                        #1.5
                        ##f
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup
        '''
        command = MarkupCommand('draw-circle', radius, thickness, filled)
        return Markup(contents=command, direction=direction)

    @staticmethod
    def draw_line(x, y, direction=None):
        r'''LilyPond ``\draw-line`` markup command.

        ..  container:: example

            ::

                >>> markup = abjad.Markup.draw_line(5, -2.5, direction=Up)
                >>> f(markup)
                ^ \markup {
                    \draw-line
                        #'(5 . -2.5)
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup
        '''
        pair = schemetools.SchemePair((x, y))
        command = MarkupCommand('draw-line', pair)
        return Markup(contents=command, direction=direction)

    def dynamic(self):
        r'''LilyPond ``\dynamic`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('sffz')
                    >>> markup = markup.dynamic()
                    >>> f(markup)
                    \markup {
                        \dynamic
                            sffz
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('dynamic', contents)
        return new(self, contents=command)

    @staticmethod
    def filled_box(x_extent, y_extent, blot=0, direction=None):
        r'''LilyPond ``filled-box`` markup command.

        ..  container:: example

            ::

                >>> markup = abjad.Markup.filled_box((0, 10), (2, 5), 1.5, direction=Up)
                >>> f(markup)
                ^ \markup {
                    \filled-box
                        #'(0 . 10)
                        #'(2 . 5)
                        #1.5
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        x_extent = schemetools.SchemePair(x_extent)
        y_extent = schemetools.SchemePair(y_extent)
        blot = float(blot)
        command = MarkupCommand('filled-box', x_extent, y_extent, blot)
        return Markup(command, direction=direction)

    def finger(self):
        r'''LilyPond ``\finger`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup(1)
                    >>> markup = markup.finger()
                    >>> f(markup)
                    \markup {
                        \finger
                            1
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('finger', contents)
        return new(self, contents=command)

    @staticmethod
    def flat(direction=None):
        r'''LilyPond ``\flat`` markup command.

        ..  container:: example

            ::

                >>> markup = abjad.Markup.flat(direction=Up)
                >>> f(markup)
                ^ \markup {
                    \flat
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        command = MarkupCommand('flat')
        return Markup(contents=command, direction=direction)

    def fontsize(self, fontsize):
        r'''LilyPond ``\fontsize`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.fontsize(-3)
                    >>> f(markup)
                    \markup {
                        \fontsize #-3
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup
        '''
        fontsize = float(fontsize)
        fontsize = mathtools.integer_equivalent_number_to_integer(fontsize)
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('fontsize', fontsize, contents)
        return new(self, contents=command)

    @staticmethod
    def fraction(numerator, denominator, direction=None):
        r'''LilyPond ``\fraction`` markup command.

        ..  container:: example

            Fraction with integer numerator and denominator:

            ::

                >>> markup = abjad.Markup.fraction(1, 4, direction=Up)
                >>> f(markup)
                ^ \markup {
                    \fraction
                        1
                        4
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        ..  container:: example

            Fraction with string numerator and integer denominator:

            ::

                >>> markup = abjad.Markup.fraction('π', 4)
                >>> f(markup)
                \markup {
                    \fraction
                        π
                        4
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup
        '''
        command = MarkupCommand('fraction', str(numerator), str(denominator))
        return Markup(contents=command, direction=direction)

    def general_align(self, axis, direction):
        r'''LilyPond ``\general-align`` markup command.

        ..  container:: example

            With Abjad direction constant:

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.general_align('Y', Up)
                    >>> f(markup)
                    \markup {
                        \general-align
                            #Y
                            #UP
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        ..  container:: example

            With numeric direction value:

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.general_align('Y', 0.75)
                    >>> f(markup)
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
        command = MarkupCommand('general-align', axis, direction, contents)
        return new(self, contents=command)

    def halign(self, direction):
        r'''LilyPond ``halign`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.halign(0)
                    >>> f(markup)
                    \markup {
                        \halign
                            #0
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('halign', direction, contents)
        return new(self, contents=command)

    def hcenter_in(self, length):
        r'''LilyPond ``\hcenter-in`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.hcenter_in(12)
                    >>> f(markup)
                    \markup {
                        \hcenter-in
                            #12
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('hcenter-in', length, contents)
        return new(self, contents=command)

    @staticmethod
    def hspace(amount, direction=None):
        r'''LilyPond ``\hspace`` markup command.

        ..  container:: example

            ::

                >>> markup = abjad.Markup.hspace(0.75, direction=Up)
                >>> f(markup)
                ^ \markup {
                    \hspace
                        #0.75
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        command = MarkupCommand('hspace', amount)
        return Markup(contents=command, direction=direction)

    def huge(self):
        r'''LilyPond ``\huge`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.huge()
                    >>> f(markup)
                    \markup {
                        \huge
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('huge', contents)
        return new(self, contents=command)

    def italic(self):
        r'''LilyPond ``\italic`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.italic()
                    >>> f(markup)
                    \markup {
                        \italic
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('italic', contents)
        return new(self, contents=command)

    def larger(self):
        r'''LilyPond ``\larger`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.larger()
                    >>> f(markup)
                    \markup {
                        \larger
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('larger', contents)
        return new(self, contents=command)

    @staticmethod
    def left_column(markup_list, direction=None):
        r'''LilyPond ``\left-column`` markup command.

        ..  container:: example

            ::

                >>> city = abjad.Markup('Los Angeles')
                >>> date = abjad.Markup('May - August 2014')
                >>> markup = abjad.Markup.left_column([city, date])
                >>> f(markup)
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
        contents = []
        for markup in markup_list:
            contents.append(Markup._parse_markup_command_argument(markup))
        command = MarkupCommand('left-column', contents)
        return Markup(contents=command, direction=direction)

    @staticmethod
    def line(markup_list, direction=None):
        r'''LilyPond ``\line`` markup command.

        ..  container:: example

            ::

                >>> markups = ['Allegro', 'assai']
                >>> markups = [abjad.Markup(_) for _ in markups]
                >>> markup = abjad.Markup.line(markups)
                >>> f(markup)
                \markup {
                    \line
                        {
                            Allegro
                            assai
                        }
                    }


            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = []
        for markup in markup_list:
            contents.extend(markup.contents)
        command = MarkupCommand('line', contents)
        return Markup(contents=command, direction=direction)

    @staticmethod
    def make_improper_fraction_markup(rational, direction=None):
        r'''Makes improper fraction markup.

        ..  container:: example

            With integer-equivalent number:

            ::

                >>> markup = abjad.Markup.make_improper_fraction_markup(
                ...     abjad.Fraction(6, 3),
                ...     direction=Up,
                ...     )
                >>> f(markup)
                ^ \markup { 2 }

            ::

                >>> show(markup) # doctest: +SKIP

        ..  container:: example

            With non-integer-equivalent number:

            ::

                >>> markup = abjad.Markup.make_improper_fraction_markup(
                ...     abjad.Fraction(7, 3),
                ...     )
                >>> f(markup)
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
            markup = Markup(number, direction=direction)
            return markup
        assert isinstance(rational, Fraction), repr(rational)
        integer_part = int(rational)
        fraction_part = rational - integer_part
        integer_markup = Markup(integer_part, direction=direction)
        numerator = fraction_part.numerator
        denominator = fraction_part.denominator
        fraction_markup = Markup.fraction(
            numerator,
            denominator,
            )
        fraction_markup = fraction_markup.tiny()
        markup = integer_markup + fraction_markup
        return markup

    @staticmethod
    def musicglyph(glyph_name=None, direction=None):
        r'''LilyPond ``\musicglyph`` markup command.

        ..  container:: example

            ::

                >>> markup = abjad.Markup.musicglyph(
                ...     'accidentals.sharp',
                ...     direction=Up,
                ...     )
                >>> f(markup)
                ^ \markup {
                    \musicglyph
                        #"accidentals.sharp"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.ly import music_glyphs
        glyph_name = glyph_name or 'accidentals.sharp'
        message = 'not a valid LilyPond glyph name.'
        assert glyph_name in music_glyphs, message
        glyph_scheme = schemetools.Scheme(glyph_name, force_quotes=True)
        command = MarkupCommand('musicglyph', glyph_scheme)
        return Markup(contents=command, direction=direction)

    @staticmethod
    def natural(direction=None):
        r'''LilyPond ``\natural`` markup command.

        ..  container:: example

            ::

                >>> markup = abjad.Markup.natural(direction=Up)
                >>> f(markup)
                ^ \markup {
                    \natural
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        command = MarkupCommand('natural')
        return Markup(contents=command, direction=direction)

    @staticmethod
    def note_by_number(log, dot_count, stem_direction, direction=None):
        r'''LilyPond ``\note-by-number`` markup command.

        ..  container:: example

            ::

                >>> markup = abjad.Markup.note_by_number(3, 2, 1, direction=Up)
                >>> f(markup)
                ^ \markup {
                    \note-by-number
                        #3
                        #2
                        #1
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        command = MarkupCommand(
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

                >>> markup = abjad.Markup.null()
                >>> f(markup)
                \markup {
                    \null
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        command = MarkupCommand('null')
        return Markup(contents=command, direction=direction)

    @staticmethod
    def overlay(markup_list, direction=None):
        r'''LilyPond ``\overlay`` markup command.

        ..  container:: example

            ::

                >>> city = abjad.Markup('Los Angeles')
                >>> date = abjad.Markup('May - August 2014')
                >>> markup = abjad.Markup.overlay([city, date], direction=Up)
                >>> f(markup)
                ^ \markup {
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
        contents = []
        for markup in markup_list:
            contents.append(Markup._parse_markup_command_argument(markup))
        command = MarkupCommand('overlay', contents)
        return Markup(contents=command, direction=direction)

    def override(self, pair):
        r'''LilyPond ``\override`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.parenthesize()
                    >>> markup = markup.override(('padding', 0.75))
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
        contents = self._parse_markup_command_argument(self)
        pair = schemetools.SchemePair(pair)
        command = MarkupCommand('override', pair, contents)
        return new(self, contents=command)

    def pad_around(self, padding):
        r'''LilyPond ``\pad-around`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.pad_around(10)
                    >>> markup = markup.box()
                    >>> f(markup)
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
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('pad-around', padding, contents)
        return new(self, contents=command)

    def pad_to_box(self, x_extent, y_extent):
        r'''LilyPond ``pad-to-box`` markup command.

        ..  container:: example

            Positive extents.

            The following postscript describes a filled box between the
            x-coordinates of 0 and 10 and the y-coordinates of 0 and 10.
            Normally, this would be drawn off the edge of the page.

            ::

                >>> up_postscript = abjad.Postscript()
                >>> up_postscript = up_postscript.newpath()
                >>> up_postscript = up_postscript.moveto(0, 0)
                >>> up_postscript = up_postscript.rlineto(10, 0)
                >>> up_postscript = up_postscript.rlineto(0, 10)
                >>> up_postscript = up_postscript.rlineto(-10, 0)
                >>> up_postscript = up_postscript.closepath()
                >>> up_postscript = up_postscript.setgray(0.75)
                >>> up_postscript = up_postscript.fill()
                >>> up_postscript_markup = up_postscript.as_markup()
                >>> f(up_postscript_markup)
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

            Negative extents.

            LilyPond does not appear to handle negative extents in the same was
            as it handles positive extents.

            The following postscript describes a box of the same shape as in
            the previous example. However, this box's x- and y-coordinates
            range between 0 and 10 and 0 and -10 respectively.

            ::

                >>> down_postscript = abjad.Postscript()
                >>> down_postscript = down_postscript.newpath()
                >>> down_postscript = down_postscript.moveto(0, 0)
                >>> down_postscript = down_postscript.rlineto(10, 0)
                >>> down_postscript = down_postscript.rlineto(0, -10)
                >>> down_postscript = down_postscript.rlineto(-10, 0)
                >>> down_postscript = down_postscript.closepath()
                >>> down_postscript = down_postscript.setgray(0.75)
                >>> down_postscript = down_postscript.fill()
                >>> down_postscript_markup = down_postscript.as_markup()
                >>> f(down_postscript_markup)
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
        contents = self._parse_markup_command_argument(self)
        x_extent = schemetools.SchemePair(x_extent)
        y_extent = schemetools.SchemePair(y_extent)
        command = MarkupCommand('pad-to-box', x_extent, y_extent, contents)
        return new(self, contents=command)

    def parenthesize(self):
        r'''LilyPond ``\parenthesize`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.parenthesize()
                    >>> f(markup)
                    \markup {
                        \parenthesize
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('parenthesize', contents)
        return new(self, contents=command)

    @staticmethod
    def postscript(postscript, direction=None):
        r'''LilyPond ``\postscript`` markup command.

        ..  container:: example

            ::

                >>> postscript = abjad.Postscript()
                >>> postscript = postscript.moveto(1, 1)
                >>> postscript = postscript.setlinewidth(2.5)
                >>> postscript = postscript.setdash((2, 1))
                >>> postscript = postscript.lineto(3, -4)
                >>> postscript = postscript.stroke()
                >>> markup = abjad.Markup.postscript(postscript, direction=Up)
                >>> f(markup)
                ^ \markup {
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
        if isinstance(postscript, Postscript):
            postscript = str(postscript)
        assert isinstance(postscript, str)
        command = MarkupCommand('postscript', postscript)
        return Markup(contents=command, direction=direction)

    def raise_(self, amount):
        r'''LilyPond ``\raise`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.raise_(0.35)
                    >>> f(markup)
                    \markup {
                        \raise
                            #0.35
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('raise', amount, contents)
        return new(self, contents=command)

    @staticmethod
    def right_column(markup_list, direction=None):
        r'''LilyPond ``\right-column`` markup command.

        ..  container:: example

            ::

                >>> city = abjad.Markup('Los Angeles')
                >>> date = abjad.Markup('May - August 2014')
                >>> markup = abjad.Markup.right_column(
                ...     [city, date],
                ...     direction=Up,
                ...     )
                >>> f(markup)
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
        contents = []
        for markup in markup_list:
            contents.append(Markup._parse_markup_command_argument(markup))
        command = MarkupCommand('right-column', contents)
        return Markup(contents=command, direction=direction)

    def rotate(self, angle):
        r'''LilyPond ``\rotate`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.rotate(45)
                    >>> f(markup)
                    \markup {
                        \rotate
                            #45
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('rotate', angle, contents)
        return new(self, contents=command)

    def sans(self):
        r'''LilyPond ``\sans`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.sans()
                    >>> f(markup)
                    \markup {
                        \sans
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('sans', contents)
        return new(self, contents=command)

    def scale(self, factor_pair):
        r'''LilyPond ``\scale`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.scale((0.75, 0.75))
                    >>> f(markup)
                    \markup {
                        \scale
                            #'(0.75 . 0.75)
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        factor_pair = schemetools.SchemePair(factor_pair)
        command = MarkupCommand('scale', factor_pair, contents)
        return new(self, contents=command)

    @staticmethod
    def sharp(direction=None):
        r'''LilyPond ``\sharp`` markup command.

        ..  container:: example

            ::

                >>> markup = abjad.Markup.sharp(direction=Up)
                >>> f(markup)
                ^ \markup {
                    \sharp
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        command = MarkupCommand('sharp')
        return Markup(contents=command, direction=direction)

    def small(self):
        r'''LilyPond ``\small`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.small()
                    >>> f(markup)
                    \markup {
                        \small
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('small', contents)
        return new(self, contents=command)

    def smaller(self):
        r'''LilyPond ``\smaller`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.smaller()
                    >>> f(markup)
                    \markup {
                        \smaller
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('smaller', contents)
        return new(self, contents=command)

    def sub(self):
        r'''LilyPond ``\sub`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup_list = [
                    ...     abjad.Markup('A'),
                    ...     abjad.Markup('j').sub(),
                    ...     ]
                    >>> markup = abjad.Markup.concat(markup_list)
                    >>> f(markup)
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
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('sub', contents)
        return new(self, contents=command)

    def super(self):
        r'''LilyPond ``\super`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markups = [
                    ...     abjad.Markup('1'),
                    ...     abjad.Markup('st').super(),
                    ...     ]
                    >>> markup_list = abjad.MarkupList(markups)
                    >>> markup = markup_list.concat()
                    >>> f(markup)
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
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('super', contents)
        return new(self, contents=command)

    def tiny(self):
        r'''LilyPond ``\tiny`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.tiny()
                    >>> f(markup)
                    \markup {
                        \tiny
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('tiny', contents)
        return new(self, contents=command)

    def translate(self, offset_pair):
        r'''LilyPond ``translate`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.translate((2, 1))
                    >>> f(markup)
                    \markup {
                        \translate
                            #'(2 . 1)
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        offset_pair = schemetools.SchemePair(offset_pair)
        command = MarkupCommand('translate', offset_pair, contents)
        return new(self, contents=command)

    @staticmethod
    def triangle(direction=None, is_filled=True):
        r'''LilyPond ``\triangle`` markup command.

        ..  container:: example

            ::

                >>> markup = abjad.Markup.triangle(direction=Up)
                >>> f(markup)
                ^ \markup {
                    \triangle
                        ##t
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup
        '''
        command = MarkupCommand('triangle', bool(is_filled))
        return Markup(contents=command, direction=direction)

    def upright(self):
        r'''LilyPond ``\upright`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.upright()
                    >>> f(markup)
                    \markup {
                        \upright
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('upright', contents)
        return new(self, contents=command)

    def vcenter(self):
        r'''LilyPond ``\vcenter`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.vcenter()
                    >>> f(markup)
                    \markup {
                        \vcenter
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('vcenter', contents)
        return new(self, contents=command)

    @staticmethod
    def vspace(amount, direction=None):
        r'''LilyPond ``\vspace`` markup command.

        ..  container:: example

            ::

                >>> markup = abjad.Markup.vspace(0.75, direction=Up)
                >>> f(markup)
                ^ \markup {
                    \vspace
                        #0.75
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        command = MarkupCommand('vspace', amount)
        return Markup(contents=command, direction=direction)

    def whiteout(self):
        r'''LilyPond ``\whiteout`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.whiteout()
                    >>> f(markup)
                    \markup {
                        \whiteout
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('whiteout', contents)
        return new(self, contents=command)

    def with_color(self, color):
        r'''LilyPond ``\with-color`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup = abjad.Markup('Allegro assai')
                    >>> markup = markup.with_color('blue')
                    >>> f(markup)
                    \markup {
                        \with-color
                            #blue
                            "Allegro assai"
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        contents = self._parse_markup_command_argument(self)
        color = schemetools.Scheme(color)
        command = MarkupCommand('with-color', color, contents)
        return new(self, contents=command)

    def with_dimensions(self, x_extent, y_extent):
        r'''LilyPond ``with-dimensions`` markup command.

        ..  note::

            See the API entry for ``Markup.pad_to_box()`` for an extensive
            discussion of setting explicit markup extents.

        ..  container:: example

            ::

                >>> up_postscript = abjad.Postscript()
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

            ::

                >>> down_postscript = abjad.Postscript()
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
        contents = self._parse_markup_command_argument(self)
        x_extent = schemetools.SchemePair(x_extent)
        y_extent = schemetools.SchemePair(y_extent)
        command = MarkupCommand(
            'with-dimensions',
            x_extent,
            y_extent,
            contents,
            )
        return new(self, contents=command)
