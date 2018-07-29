"""
Tools for modeling LilyPond's markup and postscript.
"""

import collections
import numbers
import typing
from abjad import Fraction
from abjad import enums
from abjad import mathtools
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.scheme import Scheme
from abjad.scheme import SchemeColor
from abjad.scheme import SchemePair
from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.utilities.String import String
from abjad.utilities.TypedList import TypedList
from abjad.top import new


class Markup(AbjadValueObject):
    r"""
    LilyPond markup.

    ..  container:: example

        Initializes from string:

        >>> string = r'\italic { "Allegro assai" }'
        >>> markup = abjad.Markup(string)
        >>> abjad.f(markup)
        \markup {
            \italic
                {
                    "Allegro assai"
                }
            }

        >>> abjad.show(markup) # doctest: +SKIP

    ..  container:: example

        Initializes from other markup:

        >>> markup = abjad.Markup('Allegro assai', direction=abjad.Up)
        >>> markup = markup.italic()
        >>> markup = abjad.Markup(markup, direction=abjad.Down)
        >>> abjad.f(markup)
        _ \markup {
            \italic
                "Allegro assai"
            }

        >>> abjad.show(markup) # doctest: +SKIP

    ..  container:: example

        Attaches markup to score components:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> string = r'\italic { "Allegro assai" }'
        >>> markup = abjad.Markup(string, direction=abjad.Up)
        >>> abjad.f(markup)
        ^ \markup {
            \italic
                {
                    "Allegro assai"
                }
            }

        >>> abjad.attach(markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
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

    Set ``direction`` to ``Up``, ``Down``, ``'neutral'``, ``'^'``, ``'_'``,
    ``'-'`` or None.

    ..  container:: example

        Markup can be tagged:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup('Allegro', direction=abjad.Up).italic()
        >>> abjad.attach(markup, staff[0], tag='RED:M1')
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            ^ \markup { %! RED:M1
                \italic %! RED:M1
                    Allegro %! RED:M1
                } %! RED:M1
            d'4
            e'4
            f'4
        }

    ..  container:: example

        Markup can be deactively tagged:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup('Allegro', direction=abjad.Up).italic()
        >>> abjad.attach(
        ...     markup,
        ...     staff[0],
        ...     deactivate=True,
        ...     tag='RED:M1',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff)
        \new Staff
        {
            c'4
        %@% ^ \markup { %! RED:M1
        %@%     \italic %! RED:M1
        %@%         Allegro %! RED:M1
        %@%     } %! RED:M1
            d'4
            e'4
            f'4
        }

    ..  container:: example

        REGRESSION: make sure the first italic markup doesn't disappear after
        the second italic markup is attached:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup_1 = abjad.Markup('Allegro', direction=abjad.Up).italic()
        >>> markup_2 = abjad.Markup('non troppo', direction=abjad.Up).italic()
        >>> abjad.attach(markup_1, staff[0])
        >>> abjad.attach(markup_2, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            ^ \markup {
                \italic
                    Allegro
                }
            ^ \markup {
                \italic
                    "non troppo"
                }
            d'4
            e'4
            f'4
        }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_annotation',
        '_contents',
        '_direction',
        '_literal',
        '_tweaks',
        )

    _private_attributes_to_copy = (
        '_tweaks',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        contents=None,
        *,
        direction: enums.VerticalAlignment = None,
        literal: bool = None,
        tweaks: typing.Union[
            typing.List[typing.Tuple], LilyPondTweakManager] = None,
        ) -> None:
        from abjad.top.parse import parse
        from abjad.markups import MarkupCommand
        self._annotation = None
        new_contents: typing.Tuple[typing.Union[str, MarkupCommand], ...]
        if contents is None:
            new_contents = ('',)
        elif isinstance(contents, str):
            to_parse = rf'\markup {{ {contents} }}'
            parsed = parse(to_parse)
            if all(isinstance(_, str) for _ in parsed.contents):
                new_contents = (' '.join(parsed.contents),)
            else:
                new_contents = tuple(parsed.contents)
        elif isinstance(contents, MarkupCommand):
            new_contents = (contents,)
        elif isinstance(contents, type(self)):
            direction = direction or contents.direction
            if direction is not None:
                assert isinstance(direction, (str, enums.VerticalAlignment)), repr(direction)
            new_contents = tuple(contents.contents)
        elif isinstance(contents, collections.Sequence) and 0 < len(contents):
            new_contents_ = []
            for argument in contents:
                if isinstance(argument, (str, MarkupCommand)):
                    new_contents_.append(argument)
                elif isinstance(argument, type(self)):
                    new_contents_.extend(argument.contents)
                else:
                    new_contents_.append(str(argument))
            new_contents = tuple(new_contents_)
        else:
            new_contents = (str(contents),)
        assert isinstance(new_contents, tuple), repr(new_contents)
        assert all(isinstance(_, (str, MarkupCommand)) for _ in new_contents), repr(new_contents)
        self._contents = new_contents
        direction_ = String.to_tridirectional_ordinal_constant(direction)
        if direction_ is not None:
            assert isinstance(direction_, enums.VerticalAlignment), repr(direction_)
        self._direction = direction_
        if literal is not None:
            literal = bool(literal)
        self._literal = literal
        self._tweaks = None
        LilyPondTweakManager.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r"""
        Adds markup to ``argument``.

        ..  container:: example

            Adds markup to markup:

            >>> markup = abjad.Markup('Allegro') + abjad.Markup('assai')
            >>> abjad.f(markup)
            \markup {
                Allegro
                assai
                }

            >>> abjad.show(markup) # doctest: +SKIP

        ..  container:: example

            Adds markup command to markup:

            >>> markup = abjad.Markup('Allegro') + abjad.Markup.hspace(0.75)
            >>> markup = markup + abjad.Markup('assai')
            >>> abjad.f(markup)
            \markup {
                Allegro
                \hspace
                    #0.75
                assai
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
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
        """
        Copies markup.

        >>> import copy

        ..  container:: example

            >>> markup_1 = abjad.Markup('Allegro assai', direction=abjad.Up)
            >>> markup_2 = copy.copy(markup_1)

            >>> markup_1
            Markup(contents=['Allegro assai'], direction=Up)

            >>> markup_2
            Markup(contents=['Allegro assai'], direction=Up)

            >>> markup_1 == markup_2
            True

            >>> markup_1 is markup_2
            False

        Returns new markup.
        """
        return new(self)

    def __eq__(self, argument):
        """
        Is true markup equals ``argument``.

        ..  container:: example

            Without keywords:

            >>> markup_1 = abjad.Markup('Allegro')
            >>> markup_2 = abjad.Markup('Allegro')
            >>> markup_3 = abjad.Markup('Allegro assai')

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

            >>> markup_1 = abjad.Markup('Allegro')
            >>> markup_2 = abjad.Markup('Allegro', direction=abjad.Up)

            >>> markup_1 == markup_1
            True
            >>> markup_1 == markup_2
            False
            >>> markup_2 == markup_1
            False
            >>> markup_2 == markup_2
            True

        Returns new markup.
        """
        return super().__eq__(argument)

    def __format__(self, format_specification=''):
        r"""
        Formats markup.

        ..  container:: example

            Formats markup:

            >>> string = r'\italic { Allegro assai }'
            >>> markup = abjad.Markup(string)
            >>> abjad.f(markup)
            \markup {
                \italic
                    {
                        Allegro
                        assai
                    }
                }

        Returns string.
        """
        if format_specification in ('', 'lilypond'):
            return self._get_lilypond_format()
        elif format_specification == 'storage':
            return StorageFormatManager(self).get_storage_format()
        return str(self)

    def __hash__(self):
        """
        Hashes markup.

        ..  container:: example

            Without keywords:

            >>> hash_1 = hash(abjad.Markup('Allegro'))
            >>> hash_2 = hash(abjad.Markup('Allegro'))
            >>> hash_3 = hash(abjad.Markup('Allegro assai'))

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

            >>> hash_1 = hash(abjad.Markup('Allegro'))
            >>> hash_2 = hash(abjad.Markup('Allegro', direction=abjad.Up))

            >>> hash_1 == hash_1
            True
            >>> hash_1 == hash_2
            False
            >>> hash_2 == hash_1
            False
            >>> hash_2 == hash_2
            True

        """
        return super().__hash__()

    def __illustrate__(self):
        r"""
        Illustrates markup.

        ..  container:: example

            >>> string = r'\italic { Allegro assai }'
            >>> markup = abjad.Markup(string)
            >>> abjad.f(markup)
            \markup {
                \italic
                    {
                        Allegro
                        assai
                    }
                }

            >>> abjad.show(markup) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = markup.__illustrate__()
                >>> abjad.f(lilypond_file.items[-1])
                \markup {
                    \italic
                        {
                            Allegro
                            assai
                        }
                    }

        Returns LilyPond file.
        """
        import abjad
        lilypond_file = abjad.LilyPondFile.new()
        markup = new(self, direction=None)
        lilypond_file.items.append(markup)
        return lilypond_file

    def __lt__(self, argument):
        """
        Is true when markup contents compare less than ``argument`` contents.

        ..  container:: example

            >>> markup_1 = abjad.Markup('Allegro')
            >>> markup_2 = abjad.Markup('assai')

            >>> markup_1 < markup_2
            True
            >>> markup_2 < markup_1
            False

        Raises type error when ``argument`` is not markup.

        Returns true or false.
        """
        if not isinstance(argument, type(self)):
            message = 'can only compare markup to markup: {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        return self.contents < argument.contents

    def __radd__(self, argument):
        r"""
        Adds ``argument`` to markup.

        ..  container:: example

            Adds markup to markup:

            >>> markup = abjad.Markup('Allegro') + abjad.Markup('assai')
            >>> abjad.f(markup)
            \markup {
                Allegro
                assai
                }

            >>> abjad.show(markup) # doctest: +SKIP

        ..  container:: example

            Adds markup to markup command:

            >>> markup = abjad.Markup('Allegro') + abjad.Markup.hspace(0.75)
            >>> markup = markup + abjad.Markup('assai')
            >>> abjad.f(markup)
            \markup {
                Allegro
                \hspace
                    #0.75
                assai
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
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
        r"""
        Gets string representation of markup.

        ..  container:: example

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

            >>> abjad.show(markup) # doctest: +SKIP

        Returns string.
        """
        return self._get_lilypond_format()

    ### PRIVATE METHODS ###

    def _get_format_pieces(self):
        import abjad
        tweaks = []
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
        indent = abjad.LilyPondFormatManager.indent
        direction = ''
        if self.direction is not None:
            direction = String.to_tridirectional_lilypond_symbol(
                self.direction)
        if len(self.contents) == 1 and isinstance(self.contents[0], str):
            content = self.contents[0]
            if not self.literal:
                content = Scheme.format_scheme_value(content)
                if content:
                    content = '{{ {} }}'.format(content)
                else:
                    content = '{}'
            if direction:
                string = r'{} \markup {}'.format(direction, content)
                return tweaks + [string]
            else:
                return tweaks + [r'\markup {}'.format(content)]
        if direction:
            string = r'{} \markup {{'.format(direction)
            pieces = [string]
        else:
            pieces = [r'\markup {']
        for content in self.contents:
            if isinstance(content, str):
                content = Scheme.format_scheme_value(content)
                pieces.append('{}{}'.format(indent, content))
            else:
                pieces_ = content._get_format_pieces()
                pieces.extend(['{}{}'.format(indent, _) for _ in pieces_])
        pieces.append('{}}}'.format(indent))
        return tweaks + pieces

    def _get_format_specification(self):
        agent = StorageFormatManager(self)
        names = list(agent.signature_keyword_names)
        return FormatSpecification(
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
    def contents(self) -> typing.List[typing.Union[str, 'MarkupCommand']]:
        r"""
        Gets contents of markup.

        ..  container:: example

            Initializes contents positionally:

            >>> abjad.Markup('Allegro assai')
            Markup(contents=['Allegro assai'])

            Initializes contents from keyword:

            >>> abjad.Markup(contents='Allegro assai')
            Markup(contents=['Allegro assai'])

        """
        return list(self._contents)

    @property
    def direction(self) -> typing.Optional[enums.VerticalAlignment]:
        r"""
        Gets direction of markup.

        ..  container:: example

            Initializes without direction:

            >>> abjad.Markup('Allegro')
            Markup(contents=['Allegro'])

            Initializes with direction:

            >>> abjad.Markup('Allegro', direction=abjad.Up)
            Markup(contents=['Allegro'], direction=Up)

        """
        return self._direction

    @property
    def literal(self) -> typing.Optional[bool]:
        """
        Is true when markup formats contents literally.

        ..  container:: example

            Adds neither quotes nor braces:

            >>> string = r'\custom-function #1 #4'
            >>> markup = abjad.Markup.from_literal(string, literal=True)
            >>> abjad.f(markup)
            \markup \custom-function #1 #4

        ..  container:: example

            Works with direction:

            >>> string = r'\custom-function #1 #4'
            >>> markup = abjad.Markup.from_literal(
            ...     string,
            ...     direction=abjad.Up,
            ...     literal=True,
            ...     )
            >>> abjad.f(markup)
            ^ \markup \custom-function #1 #4

        """
        return self._literal

    # TODO: Tweaks do not appear on markup without direction!
    @property
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai', direction=abjad.Up)
            >>> markup = markup.bold()
            >>> abjad.tweak(markup).color = 'blue'
            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(markup, staff[0])
            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                - \tweak color #blue
                ^ \markup {
                    \bold
                        "Allegro assai"
                    }
                d'4
                e'4
                f'4
            }

            >>> abjad.show(staff) # doctest: +SKIP

        ..  container:: example

            >>> markup = abjad.Markup(
            ...     'Allegro assai',
            ...     direction=abjad.Up,
            ...     tweaks=[('color', 'blue')],
            ...     )
            >>> markup = markup.bold()
            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(markup, staff[0])
            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                - \tweak color #blue
                ^ \markup {
                    \bold
                        "Allegro assai"
                    }
                d'4
                e'4
                f'4
            }

            >>> abjad.show(staff) # doctest: +SKIP

        """
        return self._tweaks

    ### PUBLIC METHODS ###

    @classmethod
    def abjad_metronome_mark(
        class_,
        duration_log,
        dot_count,
        stem_height,
        units_per_minute,
        direction=None,
        ):
        r"""
        Abjad ``\abjad-metronome-mark-markup`` command.

        ..  container:: example

            >>> markup = abjad.Markup.abjad_metronome_mark(
            ...     2, 0, 1, 67.5, direction=abjad.Up,
            ...     )
            >>> abjad.f(markup)
            ^ \markup {
                \abjad-metronome-mark-markup #2 #0 #1 #"67.5"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup
        """
        string = 'abjad-metronome-mark-markup'
        string += f' #{duration_log}'
        string += f' #{dot_count}'
        string += f' #{stem_height}'
        string += f' #"{units_per_minute}"'
        command = MarkupCommand(string)
        return class_(contents=command, direction=direction)

    def bold(self):
        r"""
        LilyPond ``\bold`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.bold()
            >>> abjad.f(markup)
            \markup {
                \bold
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand(
            'bold',
            contents,
            )
        return new(self, contents=command)

    def box(self):
        r"""
        LilyPond ``\box`` markup command.

        ..  container:: example

            Default box:

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.box()
            >>> abjad.f(markup)
            \markup {
                \box
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        ..  container:: example

            Customized box:

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.box()
            >>> markup = markup.override(('box-padding', 0.5))
            >>> abjad.f(markup)
            \markup {
                \override
                    #'(box-padding . 0.5)
                    \box
                        "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('box', contents)
        return new(self, contents=command)

    def bracket(self):
        r"""
        LilyPond ``\bracket`` markup command.

        ..  container:: example

            ..  container:: example

                >>> markup = abjad.Markup('Allegro assai')
                >>> markup = markup.bracket()
                >>> abjad.f(markup)
                \markup {
                    \bracket
                        "Allegro assai"
                    }

                >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('bracket', contents)
        return new(self, contents=command)

    def caps(self):
        r"""
        LilyPond ``\caps`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.caps()
            >>> abjad.f(markup)
            \markup {
                \caps
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('caps', contents)
        return new(self, contents=command)

    def center_align(self):
        r"""
        LilyPond ``\center-align`` markup command.

        ..  container:: example

            >>> markup_a = abjad.Markup('allegro')
            >>> markup_b = abjad.Markup('non').center_align()
            >>> markup_c = abjad.Markup('troppo')
            >>> markup = abjad.Markup.column([markup_a, markup_b, markup_c])
            >>> abjad.f(markup)
            \markup {
                \column
                    {
                        allegro
                        \center-align
                            non
                        troppo
                    }
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('center-align', contents)
        return new(self, contents=command)

    @classmethod
    def center_column(class_, markup_list, direction=None):
        r"""
        LilyPond ``\center-column`` markup command.

        ..  container:: example

            >>> city = abjad.Markup('Los Angeles')
            >>> date = abjad.Markup('May - August 2014')
            >>> markup = abjad.Markup.center_column([city, date])
            >>> abjad.f(markup)
            \markup {
                \center-column
                    {
                        "Los Angeles"
                        "May - August 2014"
                    }
                }

            >>> abjad.show(markup) # doctest: +SKIP

        ..  container:: example

            Also works with a list of strings:

            >>> city = 'Los Angeles'
            >>> date = 'May - August 2014'
            >>> markup = abjad.Markup.center_column([city, date])
            >>> abjad.f(markup)
            \markup {
                \center-column
                    {
                        "Los Angeles"
                        "May - August 2014"
                    }
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = []
        for markup in markup_list:
            contents.append(Markup._parse_markup_command_argument(markup))
        command = MarkupCommand('center-column', contents)
        return class_(contents=command, direction=direction)

    def circle(self):
        r"""
        LilyPond ``\circle`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup.fraction(3, 5)
            >>> markup = markup.circle()
            >>> markup = markup.override(('circle-padding', 0.45))
            >>> abjad.f(markup)
            \markup {
                \override
                    #'(circle-padding . 0.45)
                    \circle
                        \fraction
                            3
                            5
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('circle', contents)
        return new(self, contents=command)

    @classmethod
    def column(class_, markup_list, direction=None):
        r"""
        LilyPond ``\column`` markup command.

        ..  container:: example

            >>> city = abjad.Markup('Los Angeles')
            >>> date = abjad.Markup('May - August 2014')
            >>> markup = abjad.Markup.column([city, date])
            >>> abjad.f(markup)
            \markup {
                \column
                    {
                        "Los Angeles"
                        "May - August 2014"
                    }
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = []
        for markup in markup_list:
            contents.extend(markup.contents)
        command = MarkupCommand('column', contents)
        return class_(contents=command, direction=direction)

    @classmethod
    def combine(class_, markup_list, direction=None):
        r"""
        LilyPond ``\combine`` markup command.

        ..  container:: example

            >>> markup_one = abjad.Markup('Allegro assai')
            >>> markup_two = abjad.Markup.draw_line(13, 0)
            >>> markup_list = [markup_one, markup_two]
            >>> markup = abjad.Markup.combine(markup_list, direction=abjad.Up)
            >>> abjad.f(markup)
            ^ \markup {
                \combine
                    "Allegro assai"
                    \draw-line
                        #'(13 . 0)
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        if not len(markup_list) == 2:
            message = 'markup list must be length 2: {!r}.'
            message = message.format(markup_list)
            raise Exception(message)
        markup_1, markup_2 = markup_list
        contents_1 = class_._parse_markup_command_argument(markup_1)
        contents_2 = class_._parse_markup_command_argument(markup_2)
        command = MarkupCommand('combine', contents_1, contents_2)
        return class_(contents=command, direction=direction)

    @classmethod
    def concat(class_, markup_list, direction=None):
        r"""
        LilyPond ``\concat`` markup command.

        ..  container:: example

            >>> downbow = abjad.Markup.musicglyph('scripts.downbow')
            >>> hspace = abjad.Markup.hspace(1)
            >>> upbow = abjad.Markup.musicglyph('scripts.upbow')
            >>> markup_list = [downbow, hspace, upbow]
            >>> markup = abjad.Markup.concat(markup_list, direction=abjad.Up)
            >>> abjad.f(markup)
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

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        result = []
        for markup in markup_list:
            contents = Markup._parse_markup_command_argument(markup)
            result.append(contents)
        command = MarkupCommand('concat', result)
        return class_(contents=command, direction=direction)

    @classmethod
    def draw_circle(class_, radius, thickness, direction=None, filled=False):
        r"""
        LilyPond ``\draw-circle`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup.draw_circle(10, 1.5, direction=abjad.Up)
            >>> abjad.f(markup)
            ^ \markup {
                \draw-circle
                    #10
                    #1.5
                    ##f
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup
        """
        command = MarkupCommand('draw-circle', radius, thickness, filled)
        return class_(contents=command, direction=direction)

    @classmethod
    def draw_line(class_, x, y, direction=None):
        r"""
        LilyPond ``\draw-line`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup.draw_line(5, -2.5, direction=abjad.Up)
            >>> abjad.f(markup)
            ^ \markup {
                \draw-line
                    #'(5 . -2.5)
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup
        """
        pair = SchemePair((x, y))
        command = MarkupCommand('draw-line', pair)
        return class_(contents=command, direction=direction)

    def dynamic(self):
        r"""
        LilyPond ``\dynamic`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('sffz')
            >>> markup = markup.dynamic()
            >>> abjad.f(markup)
            \markup {
                \dynamic
                    sffz
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('dynamic', contents)
        return new(self, contents=command)

    @classmethod
    def filled_box(class_, x_extent, y_extent, blot=0, direction=None):
        r"""
        LilyPond ``filled-box`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup.filled_box((0, 10), (2, 5), 1.5, direction=abjad.Up)
            >>> abjad.f(markup)
            ^ \markup {
                \filled-box
                    #'(0 . 10)
                    #'(2 . 5)
                    #1.5
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        x_extent = SchemePair(x_extent)
        y_extent = SchemePair(y_extent)
        blot = float(blot)
        command = MarkupCommand('filled-box', x_extent, y_extent, blot)
        return class_(command, direction=direction)

    def finger(self):
        r"""
        LilyPond ``\finger`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup(1)
            >>> markup = markup.finger()
            >>> abjad.f(markup)
            \markup {
                \finger
                    1
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('finger', contents)
        return new(self, contents=command)

    @classmethod
    def flat(class_, direction=None):
        r"""
        LilyPond ``\flat`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup.flat(direction=abjad.Up)
            >>> abjad.f(markup)
            ^ \markup {
                \flat
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        command = MarkupCommand('flat')
        return class_(contents=command, direction=direction)

    def fontsize(self, fontsize):
        r"""
        LilyPond ``\fontsize`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.fontsize(-3)
            >>> abjad.f(markup)
            \markup {
                \fontsize
                    #-3
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup
        """
        fontsize = float(fontsize)
        fontsize = mathtools.integer_equivalent_number_to_integer(fontsize)
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('fontsize', fontsize, contents)
        return new(self, contents=command)

    @classmethod
    def fraction(class_, numerator, denominator, direction=None):
        r"""
        LilyPond ``\fraction`` markup command.

        ..  container:: example

            Fraction with integer numerator and denominator:

            >>> markup = abjad.Markup.fraction(1, 4, direction=abjad.Up)
            >>> abjad.f(markup)
            ^ \markup {
                \fraction
                    1
                    4
                }

            >>> abjad.show(markup) # doctest: +SKIP

        ..  container:: example

            Fraction with string numerator and integer denominator:

            >>> markup = abjad.Markup.fraction('π', 4)
            >>> abjad.f(markup)
            \markup {
                \fraction
                    π
                    4
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup
        """
        command = MarkupCommand('fraction', str(numerator), str(denominator))
        return class_(contents=command, direction=direction)

    @classmethod
    def from_literal(class_, string, direction=None, literal=None):
        r"""
        Makes markup from literal ``string`` and bypasses parser.

        ..  container:: example

            >>> markup = abjad.Markup.from_literal('F#4')
            >>> abjad.f(markup)
            \markup { "F#4" }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        markup = class_(
            contents='',
            direction=direction,
            literal=literal,
            )
        markup._contents = (string,)
        return markup

    def general_align(self, axis, direction):
        r"""
        LilyPond ``\general-align`` markup command.

        ..  container:: example

            With Abjad direction constant:

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.general_align('Y', direction=abjad.Up)
            >>> abjad.f(markup)
            \markup {
                \general-align
                    #Y
                    #UP
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        ..  container:: example

            With numeric direction value:

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.general_align('Y', 0.75)
            >>> abjad.f(markup)
            \markup {
                \general-align
                    #Y
                    #0.75
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        import abjad
        contents = self._parse_markup_command_argument(self)
        axis = Scheme(axis)
        # TODO: make Scheme(Up) work
        if direction is enums.Up:
            direction = Scheme('UP')
        elif direction is enums.Down:
            direction = Scheme('DOWN')
        elif direction is enums.Center:
            direction = Scheme('CENTER')
        elif isinstance(direction, numbers.Number):
            direction = Scheme(str(direction))
        else:
            message = 'unknown direction: {!r}.'
            message = message.format(direction)
            raise ValueError(message)
        command = MarkupCommand('general-align', axis, direction, contents)
        return new(self, contents=command)

    def halign(self, direction):
        r"""
        LilyPond ``halign`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.halign(0)
            >>> abjad.f(markup)
            \markup {
                \halign
                    #0
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('halign', direction, contents)
        return new(self, contents=command)

    def hcenter_in(self, length):
        r"""
        LilyPond ``\hcenter-in`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.hcenter_in(12)
            >>> abjad.f(markup)
            \markup {
                \hcenter-in
                    #12
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('hcenter-in', length, contents)
        return new(self, contents=command)

    @classmethod
    def hspace(class_, amount, direction=None):
        r"""
        LilyPond ``\hspace`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup.hspace(0.75, direction=abjad.Up)
            >>> abjad.f(markup)
            ^ \markup {
                \hspace
                    #0.75
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        command = MarkupCommand('hspace', amount)
        return class_(contents=command, direction=direction)

    def huge(self):
        r"""
        LilyPond ``\huge`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.huge()
            >>> abjad.f(markup)
            \markup {
                \huge
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('huge', contents)
        return new(self, contents=command)

    def italic(self):
        r"""
        LilyPond ``\italic`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.italic()
            >>> abjad.f(markup)
            \markup {
                \italic
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('italic', contents)
        return new(self, contents=command)

    def larger(self):
        r"""
        LilyPond ``\larger`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.larger()
            >>> abjad.f(markup)
            \markup {
                \larger
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('larger', contents)
        return new(self, contents=command)

    @classmethod
    def left_column(class_, markup_list, direction=None):
        r"""
        LilyPond ``\left-column`` markup command.

        ..  container:: example

            >>> city = abjad.Markup('Los Angeles')
            >>> date = abjad.Markup('May - August 2014')
            >>> markup = abjad.Markup.left_column([city, date])
            >>> abjad.f(markup)
            \markup {
                \left-column
                    {
                        "Los Angeles"
                        "May - August 2014"
                    }
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = []
        for markup in markup_list:
            contents.append(Markup._parse_markup_command_argument(markup))
        command = MarkupCommand('left-column', contents)
        return class_(contents=command, direction=direction)

    @classmethod
    def line(
        class_,
        markup_list,
        direction=None,
        deactivate=None,
        tag=None,
        ):
        r"""
        LilyPond ``\line`` markup command.

        ..  container:: example

            >>> markups = ['Allegro', 'assai']
            >>> markups = [abjad.Markup(_) for _ in markups]
            >>> markup = abjad.Markup.line(markups)
            >>> abjad.f(markup)
            \markup {
                \line
                    {
                        Allegro
                        assai
                    }
                }


            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = []
        for markup in markup_list:
            contents.extend(markup.contents)
        command = MarkupCommand('line', contents)
        command.deactivate = deactivate
        command.tag = tag
        return class_(contents=command, direction=direction)

    @classmethod
    def make_improper_fraction_markup(class_, rational, direction=None):
        r"""
        Makes improper fraction markup.

        ..  container:: example

            With integer-equivalent number:

            >>> markup = abjad.Markup.make_improper_fraction_markup(
            ...     abjad.Fraction(6, 3),
            ...     direction=abjad.Up,
            ...     )
            >>> abjad.f(markup)
            ^ \markup { 2 }

            >>> abjad.show(markup) # doctest: +SKIP

        ..  container:: example

            With non-integer-equivalent number:

            >>> markup = abjad.Markup.make_improper_fraction_markup(
            ...     abjad.Fraction(7, 3),
            ...     )
            >>> abjad.f(markup)
            \markup {
                2
                \tiny
                    \fraction
                        1
                        3
                }

            >>> abjad.show(markup) # doctest: +SKIP

        """
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

    @classmethod
    def musicglyph(class_, glyph_name=None, direction=None):
        r"""
        LilyPond ``\musicglyph`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup.musicglyph(
            ...     'accidentals.sharp',
            ...     direction=abjad.Up,
            ...     )
            >>> abjad.f(markup)
            ^ \markup {
                \musicglyph
                    #"accidentals.sharp"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        from abjad.ly import music_glyphs
        glyph_name = glyph_name or 'accidentals.sharp'
        message = 'not a valid LilyPond glyph name.'
        assert glyph_name in music_glyphs, message
        glyph_scheme = Scheme(glyph_name, force_quotes=True)
        command = MarkupCommand('musicglyph', glyph_scheme)
        return class_(contents=command, direction=direction)

    @classmethod
    def natural(class_, direction=None):
        r"""
        LilyPond ``\natural`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup.natural(direction=abjad.Up)
            >>> abjad.f(markup)
            ^ \markup {
                \natural
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        command = MarkupCommand('natural')
        return class_(contents=command, direction=direction)

    def normal_text(self):
        r"""
        LilyPond ``\bold`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.normal_text()
            >>> abjad.f(markup)
            \markup {
                \normal-text
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand(
            'normal-text',
            contents,
            )
        return new(self, contents=command)

    @classmethod
    def note_by_number(class_, log, dot_count, stem_direction, direction=None):
        r"""
        LilyPond ``\note-by-number`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup.note_by_number(3, 2, 1, direction=abjad.Up)
            >>> abjad.f(markup)
            ^ \markup {
                \note-by-number
                    #3
                    #2
                    #1
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        command = MarkupCommand(
            'note-by-number',
            log,
            dot_count,
            stem_direction,
            )
        return class_(contents=command, direction=direction)

    @classmethod
    def null(class_, direction=None):
        r"""
        LilyPond ``\null`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup.null()
            >>> abjad.f(markup)
            \markup {
                \null
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        command = MarkupCommand('null')
        return class_(contents=command, direction=direction)

    @classmethod
    def overlay(class_, markup_list, direction=None):
        r"""
        LilyPond ``\overlay`` markup command.

        ..  container:: example

            >>> city = abjad.Markup('Los Angeles')
            >>> date = abjad.Markup('May - August 2014')
            >>> markup = abjad.Markup.overlay([city, date], direction=abjad.Up)
            >>> abjad.f(markup)
            ^ \markup {
                \overlay
                    {
                        "Los Angeles"
                        "May - August 2014"
                    }
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = []
        for markup in markup_list:
            contents.append(Markup._parse_markup_command_argument(markup))
        command = MarkupCommand('overlay', contents)
        return class_(contents=command, direction=direction)

    def override(self, pair):
        r"""
        LilyPond ``\override`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.parenthesize()
            >>> markup = markup.override(('padding', 0.75))
            >>> abjad.f(markup)
            \markup {
                \override
                    #'(padding . 0.75)
                    \parenthesize
                        "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        pair = SchemePair(pair)
        command = MarkupCommand('override', pair, contents)
        return new(self, contents=command)

    def pad_around(self, padding):
        r"""
        LilyPond ``\pad-around`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.pad_around(10)
            >>> markup = markup.box()
            >>> abjad.f(markup)
            \markup {
                \box
                    \pad-around
                        #10
                        "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('pad-around', padding, contents)
        return new(self, contents=command)

    def pad_markup(self, padding):
        r"""
        LilyPond ``\pad-markup`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.pad_markup(10)
            >>> markup = markup.box()
            >>> abjad.f(markup)
            \markup {
                \box
                    \pad-markup
                        #10
                        "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('pad-markup', padding, contents)
        return new(self, contents=command)

    def pad_to_box(self, x_extent, y_extent):
        r"""
        LilyPond ``pad-to-box`` markup command.

        ..  container:: example

            Positive extents.

            The following postscript describes a filled box between the
            x-coordinates of 0 and 10 and the y-coordinates of 0 and 10.
            Normally, this would be drawn off the edge of the page.

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
            >>> abjad.f(up_postscript_markup)
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

            >>> abjad.show(up_postscript_markup) # doctest: +SKIP

            Wrapping the postscript in a box shows that LilyPond believes the
            postscript has effectively no x or y extent:

            >>> abjad.show(up_postscript_markup.box()) # doctest: +SKIP

            By giving the postscript markup explicit extents, we can instruct
            LilyPond to position it properly:

            >>> up_postscript_markup = up_postscript_markup.pad_to_box(
            ...     (0, 10), (0, 10))
            >>> abjad.show(up_postscript_markup) # doctest: +SKIP

            Boxing also shows that extents have been applied correctly:

            >>> abjad.show(up_postscript_markup.box()) # doctest: +SKIP

        ..  container:: example

            Negative extents.

            LilyPond does not appear to handle negative extents in the same was
            as it handles positive extents.

            The following postscript describes a box of the same shape as in
            the previous example. However, this box's x- and y-coordinates
            range between 0 and 10 and 0 and -10 respectively.

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
            >>> abjad.f(down_postscript_markup)
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

            >>> abjad.show(down_postscript_markup) # doctest: +SKIP

            However, boxing the markup shows that LilyPond still believes it to
            be of 0-height and 0-width. Notice that the box appears in a
            different corner of the grey square than in the previous example.
            This corner is the markup *origin*. The grey box in example 2
            *descends* from the origin, while the grey box in example 1
            *ascends* from it.

            >>> abjad.show(down_postscript_markup.box()) # doctest: +SKIP

            Giving the postscript markup positive extents does not work:

            >>> markup = down_postscript_markup.pad_to_box(
            ...     (0, 10), (0, 10))
            >>> abjad.show(markup.box()) # doctest: +SKIP

            Likewise, giving the postscript markup negative extents also
            does not work. The negative extents are treated as 0. In this case,
            the postscript markup is treated as though it had a height of 0:

            >>> markup = down_postscript_markup.pad_to_box(
            ...     (0, 10), (0, -10))
            >>> abjad.show(markup.box()) # doctest: +SKIP

            Unfortunately, this means that any part of a postscript-created
            markup that uses negative coordinates cannot be treated properly by
            LilyPond's markup spacing logic. To avoid this, only use positive
            coordinates in postscript.

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        x_extent = SchemePair(x_extent)
        y_extent = SchemePair(y_extent)
        command = MarkupCommand('pad-to-box', x_extent, y_extent, contents)
        return new(self, contents=command)

    def parenthesize(self):
        r"""
        LilyPond ``\parenthesize`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.parenthesize()
            >>> abjad.f(markup)
            \markup {
                \parenthesize
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('parenthesize', contents)
        return new(self, contents=command)

    @classmethod
    def postscript(class_, postscript, direction=None):
        r"""
        LilyPond ``\postscript`` markup command.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.moveto(1, 1)
            >>> postscript = postscript.setlinewidth(2.5)
            >>> postscript = postscript.setdash((2, 1))
            >>> postscript = postscript.lineto(3, -4)
            >>> postscript = postscript.stroke()
            >>> markup = abjad.Markup.postscript(postscript, direction=abjad.Up)
            >>> abjad.f(markup)
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

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        if isinstance(postscript, Postscript):
            postscript = str(postscript)
        assert isinstance(postscript, str)
        command = MarkupCommand('postscript', postscript)
        return class_(contents=command, direction=direction)

    def raise_(self, amount):
        r"""
        LilyPond ``\raise`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.raise_(0.35)
            >>> abjad.f(markup)
            \markup {
                \raise
                    #0.35
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('raise', amount, contents)
        return new(self, contents=command)

    @classmethod
    def right_column(class_, markup_list, direction=None):
        r"""
        LilyPond ``\right-column`` markup command.

        ..  container:: example

            >>> city = abjad.Markup('Los Angeles')
            >>> date = abjad.Markup('May - August 2014')
            >>> markup = abjad.Markup.right_column(
            ...     [city, date],
            ...     direction=abjad.Up,
            ...     )
            >>> abjad.f(markup)
            ^ \markup {
                \right-column
                    {
                        "Los Angeles"
                        "May - August 2014"
                    }
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = []
        for markup in markup_list:
            contents.append(Markup._parse_markup_command_argument(markup))
        command = MarkupCommand('right-column', contents)
        return class_(contents=command, direction=direction)

    def rotate(self, angle):
        r"""
        LilyPond ``\rotate`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.rotate(45)
            >>> abjad.f(markup)
            \markup {
                \rotate
                    #45
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('rotate', angle, contents)
        return new(self, contents=command)

    def sans(self):
        r"""
        LilyPond ``\sans`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.sans()
            >>> abjad.f(markup)
            \markup {
                \sans
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('sans', contents)
        return new(self, contents=command)

    def scale(self, factor_pair):
        r"""
        LilyPond ``\scale`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.scale((0.75, 0.75))
            >>> abjad.f(markup)
            \markup {
                \scale
                    #'(0.75 . 0.75)
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        factor_pair = SchemePair(factor_pair)
        command = MarkupCommand('scale', factor_pair, contents)
        return new(self, contents=command)

    @classmethod
    def sharp(class_, direction=None):
        r"""
        LilyPond ``\sharp`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup.sharp(direction=abjad.Up)
            >>> abjad.f(markup)
            ^ \markup {
                \sharp
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        command = MarkupCommand('sharp')
        return class_(contents=command, direction=direction)

    def small(self):
        r"""
        LilyPond ``\small`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.small()
            >>> abjad.f(markup)
            \markup {
                \small
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('small', contents)
        return new(self, contents=command)

    def smaller(self):
        r"""
        LilyPond ``\smaller`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.smaller()
            >>> abjad.f(markup)
            \markup {
                \smaller
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('smaller', contents)
        return new(self, contents=command)

    def sub(self):
        r"""
        LilyPond ``\sub`` markup command.

        ..  container:: example

            >>> markup_list = [
            ...     abjad.Markup('A'),
            ...     abjad.Markup('j').sub(),
            ...     ]
            >>> markup = abjad.Markup.concat(markup_list)
            >>> abjad.f(markup)
            \markup {
                \concat
                    {
                        A
                        \sub
                            j
                    }
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('sub', contents)
        return new(self, contents=command)

    def super(self):
        r"""
        LilyPond ``\super`` markup command.

        ..  container:: example

            >>> markups = [
            ...     abjad.Markup('1'),
            ...     abjad.Markup('st').super(),
            ...     ]
            >>> markup_list = abjad.MarkupList(markups)
            >>> markup = markup_list.concat()
            >>> abjad.f(markup)
            \markup {
                \concat
                    {
                        1
                        \super
                            st
                    }
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('super', contents)
        return new(self, contents=command)

    def tiny(self):
        r"""
        LilyPond ``\tiny`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.tiny()
            >>> abjad.f(markup)
            \markup {
                \tiny
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('tiny', contents)
        return new(self, contents=command)

    def translate(self, offset_pair):
        r"""
        LilyPond ``translate`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.translate((2, 1))
            >>> abjad.f(markup)
            \markup {
                \translate
                    #'(2 . 1)
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        offset_pair = SchemePair(offset_pair)
        command = MarkupCommand('translate', offset_pair, contents)
        return new(self, contents=command)

    @classmethod
    def triangle(class_, direction=None, is_filled=True):
        r"""
        LilyPond ``\triangle`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup.triangle(direction=abjad.Up)
            >>> abjad.f(markup)
            ^ \markup {
                \triangle
                    ##t
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup
        """
        command = MarkupCommand('triangle', bool(is_filled))
        return class_(contents=command, direction=direction)

    def upright(self):
        r"""
        LilyPond ``\upright`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.upright()
            >>> abjad.f(markup)
            \markup {
                \upright
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('upright', contents)
        return new(self, contents=command)

    def vcenter(self):
        r"""
        LilyPond ``\vcenter`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.vcenter()
            >>> abjad.f(markup)
            \markup {
                \vcenter
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('vcenter', contents)
        return new(self, contents=command)

    @classmethod
    def vspace(class_, amount, direction=None):
        r"""
        LilyPond ``\vspace`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup.vspace(0.75, direction=abjad.Up)
            >>> abjad.f(markup)
            ^ \markup {
                \vspace
                    #0.75
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        command = MarkupCommand('vspace', amount)
        return class_(contents=command, direction=direction)

    def whiteout(self):
        r"""
        LilyPond ``\whiteout`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.whiteout()
            >>> abjad.f(markup)
            \markup {
                \whiteout
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('whiteout', contents)
        return new(self, contents=command)

    def with_color(self, color):
        r"""
        LilyPond ``\with-color`` markup command.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.with_color('blue')
            >>> abjad.f(markup)
            \markup {
                \with-color
                    #blue
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        ..  container:: example

            X-11 colors are supported:

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.with_color(abjad.SchemeColor('LimeGreen'))
            >>> abjad.f(markup)
            \markup {
                \with-color
                    #(x11-color 'LimeGreen)
                    "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        if isinstance(color, str):
            color = Scheme(color)
        elif isinstance(color, SchemeColor):
            pass
        else:
            raise TypeError(color)
        command = MarkupCommand('with-color', color, contents)
        return new(self, contents=command)

    def with_dimensions(self, x_extent, y_extent):
        r"""
        LilyPond ``with-dimensions`` markup command.

        ..  note::

            See the API entry for ``Markup.pad_to_box()`` for an extensive
            discussion of setting explicit markup extents.

        ..  container:: example

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

            >>> abjad.show(up_markup.box()) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(up_markup.box())
                \markup {
                    \box
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

            >>> up_markup = up_markup.with_dimensions((0, 10), (0, 10))
            >>> up_markup = up_markup.box()
            >>> abjad.show(up_markup) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(up_markup)
                \markup {
                    \box
                        \with-dimensions
                            #'(0 . 10)
                            #'(0 . 10)
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

            >>> up_markup = up_postscript.as_markup()
            >>> up_markup = up_markup.with_dimensions((0, 20), (0, 20))
            >>> up_markup = up_markup.box()
            >>> abjad.show(up_markup) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(up_markup)
                \markup {
                    \box
                        \with-dimensions
                            #'(0 . 20)
                            #'(0 . 20)
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

            >>> up_markup = up_postscript.as_markup()
            >>> up_markup = up_markup.with_dimensions((0, 20), (0, -20))
            >>> up_markup = up_markup.box()
            >>> abjad.show(up_markup) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(up_markup)
                \markup {
                    \box
                        \with-dimensions
                            #'(0 . 20)
                            #'(0 . -20)
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

        ..  container:: example

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

            >>> abjad.show(down_markup.box()) # doctest: +SKIP

            >>> down_markup = down_markup.with_dimensions((0, 10), (0, 10))
            >>> down_markup = down_markup.box()
            >>> abjad.show(down_markup) # doctest: +SKIP

            >>> down_markup = down_postscript.as_markup()
            >>> down_markup = down_markup.with_dimensions(
            ...     (0, 10), (0, -10))
            >>> down_markup = down_markup.box()
            >>> abjad.show(down_markup) # doctest: +SKIP

            >>> down_markup = down_postscript.as_markup()
            >>> down_markup = down_markup.with_dimensions(
            ...     (-5, 15), (5, -15))
            >>> down_markup = down_markup.box()
            >>> abjad.show(down_markup) # doctest: +SKIP

        ..  container:: example

            Simple example:

            >>> markup = abjad.Markup('Allegro').box()
            >>> abjad.show(markup) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup)
                \markup {
                    \box
                        Allegro
                    }

            >>> markup = abjad.Markup('Allegro')
            >>> markup = markup.with_dimensions((-10, 10), (-10, 10))
            >>> markup = markup.box()
            >>> abjad.show(markup) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup)
                \markup {
                    \box
                        \with-dimensions
                            #'(-10 . 10)
                            #'(-10 . 10)
                            Allegro
                    }

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        x_extent = SchemePair(x_extent)
        y_extent = SchemePair(y_extent)
        command = MarkupCommand(
            'with-dimensions',
            x_extent,
            y_extent,
            contents,
            )
        return new(self, contents=command)

    def with_dimensions_from(self, command):
        r"""
        LilyPond ``with-dimensions`` markup command.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d' e' f'")
            >>> markup = abjad.Markup('Allegro', direction=abjad.Up)
            >>> markup = markup.with_dimensions_from(r'\null')
            >>> abjad.attach(markup, staff[0])
            >>> markup = abjad.Markup('non troppo', direction=abjad.Up)
            >>> markup = markup.with_dimensions_from(r'\null')
            >>> abjad.attach(markup, staff[1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::
            
                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    ^ \markup {
                        \with-dimensions-from
                            \null
                            Allegro
                        }
                    d'8
                    ^ \markup {
                        \with-dimensions-from
                            \null
                            "non troppo"
                        }
                    e'8
                    f'8
                }

        """
        contents = self._parse_markup_command_argument(self)
        command = MarkupCommand('with-dimensions-from', command, contents)
        return new(self, contents=command)

    def with_literal(self, string):
        r"""
        Makes markup with literal ``string``.

        ..  container:: example

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.bold()
            >>> markup = markup.with_literal(r'\user-markup-command')
            >>> abjad.f(markup)
            \markup {
                \user-markup-command
                    \bold
                        "Allegro assai"
                }

            >>> markup = abjad.Markup('Allegro assai')
            >>> markup = markup.with_literal(r'\user-markup-command')
            >>> markup = markup.bold()
            >>> abjad.f(markup)
            \markup {
                \bold
                    \user-markup-command
                        "Allegro assai"
                }

        Returns new markup.
        """
        contents = self._parse_markup_command_argument(self)
        if string.startswith('\\'):
            string = string[1:]
        command = MarkupCommand(
            string,
            contents,
            )
        return new(self, contents=command)


class MarkupCommand(AbjadValueObject):
    r"""
    LilyPond markup command.

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
        >>> layout_block = abjad.Block(name='layout')
        >>> layout_block.indent = 0
        >>> layout_block.ragged_right = True
        >>> command = abjad.MarkupCommand(
        ...     'score',
        ...     [small_staff, layout_block],
        ...     )

        >>> abjad.f(command)
        \score
            {
                \new Staff
                \with
                {
                    \remove Clef_engraver
                    \remove Time_signature_engraver
                    fontSize = #-3
                }
                {
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
            \new Staff
            {
                c'4
                ^ \markup {
                    \score
                        {
                            \new Staff
                            \with
                            {
                                \remove Clef_engraver
                                \remove Time_signature_engraver
                                fontSize = #-3
                            }
                            {
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

    """

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
        assert isinstance(name, str) and len(name)
        self._name = name
        self._tag = None

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a markup command with name and
        arguments equal to those of this markup command.

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
        """
        # defined explicitly because of initializer *arguments
        if isinstance(argument, type(self)):
            if self.name == argument.name:
                if self.arguments == argument.arguments:
                    return True
        return False

    def __format__(self, format_specification=''):
        r"""
        Formats markup command.

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

        Set ``format_specification`` to ``''``, ``'lilypond'`` or
        ``'storage'``. Interprets ``''`` equal to ``'storage'``.

        Returns string.
        """
        if format_specification in ('', 'storage'):
            return StorageFormatManager(self).get_storage_format()
        elif format_specification == 'lilypond':
            return self._get_lilypond_format()
        return str(self)

    def __hash__(self):
        """
        Hashes markup command.

        Redefined in tandem with __eq__.
        """
        return super().__hash__()

    def __repr__(self):
        r"""
        Gets markup command interpreter representation.

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
        """
        return super().__format__()

    def __str__(self):
        r"""
        Gets string representation of markup command.

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
        """
        return self._get_lilypond_format()

    ### PRIVATE METHODS ###

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
        parts = abjad.LilyPondFormatManager.tag(
            parts,
            self.tag,
            deactivate=self.deactivate,
            )
        return parts

    def _get_format_specification(self):
        return FormatSpecification(
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
        """
        Gets markup command arguments.

        ..  container:: example

            >>> arguments = ('draw-circle', 1, 0.1, False)
            >>> command = abjad.MarkupCommand(*arguments)
            >>> command.arguments
            (1, 0.1, False)

        Returns tuple.
        """
        return self._arguments

    @property
    def deactivate(self):
        """
        Is true when markup command deactivates tag.

        Returns true, false or none.
        """
        return self._deactivate

    @deactivate.setter
    def deactivate(self, argument):
        if argument is not None:
            argument = bool(argument)
        self._deactivate = argument

    @property
    def force_quotes(self):
        r"""
        Is true when markup command should force quotes around arguments.

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
        """
        return self._force_quotes

    @force_quotes.setter
    def force_quotes(self, argument):
        assert isinstance(argument, bool), repr(argument)
        self._force_quotes = argument

    @property
    def name(self):
        """
        Gets markup command name.

        ..  container:: example

            >>> arguments = ('draw-circle', 1, 0.1, False)
            >>> command = abjad.MarkupCommand(*arguments)
            >>> command.name
            'draw-circle'

        Returns string.
        """
        return self._name

    @property
    def tag(self):
        """
        Gets tag.
        """
        return self._tag

    @tag.setter
    def tag(self, argument):
        import abjad
        if argument is not None:
            tag = abjad.Tag(argument)
        else:
            tag = None
        self._tag = tag

    ### PUBLIC METHODS ###

    @staticmethod
    def combine_markup_commands(*commands):
        r"""
        Combines markup command and / or strings.

        LilyPond's '\combine' markup command can only take two arguments, so in
        order to combine more than two stencils, a cascade of '\combine'
        commands must be employed.  ``combine_markup_commands`` simplifies this
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
        """
        assert len(commands)
        assert all(
            isinstance(command, (MarkupCommand, str))
            for command in commands
            )
        if 1 == len(commands):
            return commands[0]
        combined = MarkupCommand('combine', commands[0], commands[1])
        for command in commands[2:]:
            combined = MarkupCommand('combine', combined, command)
        return combined


class MarkupList(TypedList):
    """
    Markup list.

    ..  container:: example

        Initializes from strings:

        ..  container:: example

            >>> markups = ['Allegro', 'assai']
            >>> markup_list = abjad.MarkupList(markups)
            >>> abjad.f(markup_list)
            abjad.MarkupList(
                items=[
                    abjad.Markup(
                        contents=['Allegro'],
                        ),
                    abjad.Markup(
                        contents=['assai'],
                        ),
                    ],
                )

            >>> abjad.show(markup_list) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup_list.__illustrate__().items[-1])
                \markup {
                    \column
                        {
                            Allegro
                            assai
                        }
                    }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_expression',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        item_class=None,
        keep_sorted=None,
        ):
        self._expression = None
        item_class = item_class or Markup
        TypedList.__init__(
            self,
            item_class=item_class,
            items=items,
            keep_sorted=keep_sorted,
            )

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        """
        Is true when markup markup list contains ``item``.

        ..  container:: example

            ..  container:: example

                >>> markups = ['Allegro', 'assai']
                >>> markup_list = abjad.MarkupList(markups)

                >>> 'assai' in markup_list
                True

        Returns true or false.
        """
        return super().__contains__(item)

    def __format__(self, format_specification=''):
        """
        Formats markup list.

        ..  container:: example

            ..  container:: example

                Formats markup list:


                    >>> markups = ['Allegro', 'assai']
                    >>> markup_list = abjad.MarkupList(markups)
                    >>> abjad.f(markup_list)
                    abjad.MarkupList(
                        items=[
                            abjad.Markup(
                                contents=['Allegro'],
                                ),
                            abjad.Markup(
                                contents=['assai'],
                                ),
                            ],
                        )

        Returns string.
        """
        return super().__format__(format_specification=format_specification)

    def __iadd__(self, argument):
        r"""
        Changes items in ``argument`` to items and extends markup list.

        ..  container:: example

            ..  container:: example

                >>> markup_list = abjad.MarkupList()
                >>> markup_list.extend(['Allegro', 'assai'])
                >>> markup_list += ['ma', 'non', 'troppo']
                >>> abjad.f(markup_list)
                abjad.MarkupList(
                    items=[
                        abjad.Markup(
                            contents=['Allegro'],
                            ),
                        abjad.Markup(
                            contents=['assai'],
                            ),
                        abjad.Markup(
                            contents=['ma'],
                            ),
                        abjad.Markup(
                            contents=['non'],
                            ),
                        abjad.Markup(
                            contents=['troppo'],
                            ),
                        ],
                    )

                >>> abjad.show(markup_list) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup_list.__illustrate__().items[-1])
                    \markup {
                        \column
                            {
                                Allegro
                                assai
                                ma
                                non
                                troppo
                            }
                        }

        Returns none.
        """
        return super().__iadd__(argument)

    def __illustrate__(self):
        r"""
        Illustrates markup markup list.

        ..  container:: example

            ..  container:: example

                >>> markups = ['Allegro', 'assai']
                >>> markup_list = abjad.MarkupList(markups)
                >>> abjad.f(markup_list)
                abjad.MarkupList(
                    items=[
                        abjad.Markup(
                            contents=['Allegro'],
                            ),
                        abjad.Markup(
                            contents=['assai'],
                            ),
                        ],
                    )

                >>> abjad.show(markup_list) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup_list.__illustrate__().items[-1])
                    \markup {
                        \column
                            {
                                Allegro
                                assai
                            }
                        }

        Returns LilyPond file.
        """
        import abjad
        lilypond_file = abjad.LilyPondFile.new()
        for name in ('layout', 'paper', 'score'):
            block = lilypond_file[name]
            lilypond_file.items.remove(block)
        markup = Markup.column(list(self))
        lilypond_file.items.append(markup)
        return lilypond_file

    def __setitem__(self, i, argument):
        r"""
        Sets item ``i`` equal to ``argument``.

        ..  container:: example

            ..  container:: example

                >>> markup_list = abjad.MarkupList()
                >>> markup_list.extend(['Allegro', 'assai'])
                >>> markup_list[-1] = 'non troppo'
                >>> abjad.f(markup_list)
                abjad.MarkupList(
                    items=[
                        abjad.Markup(
                            contents=['Allegro'],
                            ),
                        abjad.Markup(
                            contents=['non troppo'],
                            ),
                        ],
                    )

                >>> abjad.show(markup_list) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup_list.__illustrate__().items[-1])
                    \markup {
                        \column
                            {
                                Allegro
                                "non troppo"
                            }
                        }

        Returns none.
        """
        return super().__setitem__(i, argument)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        agent = StorageFormatManager(self)
        names = list(agent.signature_keyword_names)
        if self.item_class is Markup:
            names.remove('item_class')
        return FormatSpecification(
            client=self,
            storage_format_kwargs_names=names,
            )

    def _update_expression(self, frame, force_return=None):
        import abjad
        callback = abjad.Expression._frame_to_callback(
            frame,
            force_return=force_return,
            )
        return self._expression.append_callback(callback)

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        """
        Gets markup list item class.

        ..  container:: example

            >>> abjad.MarkupList().item_class
            <class 'abjad.markups.Markup'>

        Returns markup class.
        """
        return super().item_class

    @property
    def items(self):
        """
        Gets markup list items.

        ..  container:: example

            ..  container:: example

                Initializes items positionally:

                >>> items = ['Allegro', 'assai']
                >>> markup_list = abjad.MarkupList(items)
                >>> for item in markup_list.items:
                ...     item
                ...
                Markup(contents=['Allegro'])
                Markup(contents=['assai'])

                Initializes items from keyword:

                >>> items = ['Allegro', 'assai']
                >>> markup_list = abjad.MarkupList(items=items)
                >>> for item in markup_list.items:
                ...     item
                ...
                Markup(contents=['Allegro'])
                Markup(contents=['assai'])

        Returns tuple.
        """
        return super().items

    @property
    def keep_sorted(self):
        r"""
        Is true when markup list keeps markups sorted.

        ..  container:: example

            Keeps markup sorted:

            >>> markups = ['Allegro', 'assai']
            >>> markup_list = abjad.MarkupList(keep_sorted=True)
            >>> markup_list.append('assai')
            >>> markup_list.append('Allegro')
            >>> abjad.show(markup_list) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup_list.__illustrate__().items[-1])
                \markup {
                    \column
                        {
                            Allegro
                            assai
                        }
                    }

        ..  container:: example

            Does not keep markup sorted:

            >>> markups = ['Allegro', 'assai']
            >>> markup_list = abjad.MarkupList()
            >>> markup_list.append('assai')
            >>> markup_list.append('Allegro')
            >>> abjad.show(markup_list) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup_list.__illustrate__().items[-1])
                \markup {
                    \column
                        {
                            assai
                            Allegro
                        }
                    }

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return super().keep_sorted

    @keep_sorted.setter
    def keep_sorted(self, keep_sorted):
        self._keep_sorted = bool(keep_sorted)

    ### PUBLIC METHODS ###

    def append(self, item):
        """
        Appends ``item`` to markup list.

        ..  container:: example

            ..  container:: example

                >>> markup_list = abjad.MarkupList(['Allegro'])
                >>> markup_list.append('assai')
                >>> abjad.f(markup_list)
                abjad.MarkupList(
                    items=[
                        abjad.Markup(
                            contents=['Allegro'],
                            ),
                        abjad.Markup(
                            contents=['assai'],
                            ),
                        ],
                    )

                >>> abjad.show(markup_list) # doctest: +SKIP

        Returns none.
        """
        super().append(item)

    def center_column(self, direction=None):
        r"""
        LilyPond ``\center-column`` markup command.

        ..  container:: example

            ..  container:: example

                >>> city = abjad.Markup('Los Angeles')
                >>> date = abjad.Markup('May - August 2014')
                >>> markups = [city, date]
                >>> markup_list = abjad.MarkupList(markups)
                >>> markup = markup_list.center_column(direction=abjad.Up)
                >>> abjad.f(markup)
                ^ \markup {
                    \center-column
                        {
                            "Los Angeles"
                            "May - August 2014"
                        }
                    }

                >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = []
        for markup in self:
            string = Markup._parse_markup_command_argument(markup)
            contents.append(string)
        command = MarkupCommand('center-column', contents)
        return Markup(contents=command, direction=direction)

    def column(self, direction=None):
        r"""
        LilyPond ``\column`` markup command.

        ..  container:: example

            ..  container:: example

                >>> city = abjad.Markup('Los Angeles')
                >>> date = abjad.Markup('May - August 2014')
                >>> markup_list = abjad.MarkupList([city, date])
                >>> markup = markup_list.column()
                >>> abjad.f(markup)
                \markup {
                    \column
                        {
                            "Los Angeles"
                            "May - August 2014"
                        }
                    }

                >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = []
        for markup in self:
            contents.extend(markup.contents)
        command = MarkupCommand('column', contents)
        return Markup(contents=command, direction=direction)

    def combine(self, direction=None):
        r"""
        LilyPond ``\combine`` markup command.

        ..  container:: example

            ..  container:: example

                >>> markup_one = abjad.Markup('Allegro assai')
                >>> markup_two = abjad.Markup.draw_line(13, 0)
                >>> markup_list = [markup_one, markup_two]
                >>> markup_list = abjad.MarkupList(markup_list)
                >>> markup = markup_list.combine(direction=abjad.Up)
                >>> abjad.f(markup)
                ^ \markup {
                    \combine
                        "Allegro assai"
                        \draw-line
                            #'(13 . 0)
                    }

                >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        if not len(self) == 2:
            message = 'markup list must be length 2: {!r}.'
            message = message.format(self)
            raise Exception(message)
        markup_1, markup_2 = self.items
        contents_1 = Markup._parse_markup_command_argument(markup_1)
        contents_2 = Markup._parse_markup_command_argument(markup_2)
        command = MarkupCommand('combine', contents_1, contents_2)
        return Markup(contents=command, direction=direction)

    def concat(self, direction=None):
        r"""
        LilyPond ``\concat`` markup command.

        ..  container:: example

            ..  container:: example

                >>> downbow = abjad.Markup.musicglyph('scripts.downbow')
                >>> hspace = abjad.Markup.hspace(1)
                >>> upbow = abjad.Markup.musicglyph('scripts.upbow')
                >>> markups = [downbow, hspace, upbow]
                >>> markup_list = abjad.MarkupList(markups)
                >>> markup = markup_list.concat(direction=abjad.Up)
                >>> abjad.f(markup)
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

                >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        result = []
        for markup in self:
            contents = Markup._parse_markup_command_argument(markup)
            result.append(contents)
        command = MarkupCommand('concat', result)
        return Markup(contents=command, direction=direction)

    def count(self, item):
        """
        Counts ``item`` in markup list.

        ..  container:: example

            >>> markup_list = abjad.MarkupList()
            >>> markup_list.extend(['Allegro', 'assai'])

            >>> abjad.show(markup_list) # doctest: +SKIP

            >>> markup_list.count('Allegro')
            1
            >>> markup_list.count('assai')
            1
            >>> markup_list.count('ma non troppo')
            0

        Returns none.
        """
        return super().count(item)

    def extend(self, items):
        r"""
        Extends markup list with ``items``.

        ..  container:: example

            ..  container:: example

                >>> markup_list = abjad.MarkupList()
                >>> markup_list.extend(['Allegro', 'assai'])
                >>> abjad.f(markup_list)
                abjad.MarkupList(
                    items=[
                        abjad.Markup(
                            contents=['Allegro'],
                            ),
                        abjad.Markup(
                            contents=['assai'],
                            ),
                        ],
                    )

                >>> abjad.show(markup_list) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup_list.__illustrate__().items[-1])
                    \markup {
                        \column
                            {
                                Allegro
                                assai
                            }
                        }

        Returns none.
        """
        super().extend(items)

    def index(self, item):
        r"""
        Gets index of ``item`` in markup list.

        ..  container:: example

            >>> markup_list = abjad.MarkupList()
            >>> markup_list.extend(['Allegro', 'assai'])
            >>> abjad.f(markup_list)
            abjad.MarkupList(
                items=[
                    abjad.Markup(
                        contents=['Allegro'],
                        ),
                    abjad.Markup(
                        contents=['assai'],
                        ),
                    ],
                )

            >>> abjad.show(markup_list) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup_list.__illustrate__().items[-1])
                \markup {
                    \column
                        {
                            Allegro
                            assai
                        }
                    }

            >>> markup_list.index('Allegro')
            0
            >>> markup_list.index('assai')
            1

        Returns none.
        """
        return super().index(item)

    def insert(self, i, item):
        """
        Inserts ``item`` in markup markup list.

        ..  container:: example

            ..  container:: example

                >>> markup_list = abjad.MarkupList(['assai'])
                >>> markup_list.insert(0, 'Allegro')
                >>> abjad.f(markup_list)
                abjad.MarkupList(
                    items=[
                        abjad.Markup(
                            contents=['Allegro'],
                            ),
                        abjad.Markup(
                            contents=['assai'],
                            ),
                        ],
                    )

                >>> abjad.show(markup_list) # doctest: +SKIP

        Returns markup class.
        """
        super().insert(i, item)

    def left_column(self, direction=None):
        r"""
        LilyPond ``\left-column`` markup command.

        ..  container:: example

            ..  container:: example

                >>> city = abjad.Markup('Los Angeles')
                >>> date = abjad.Markup('May - August 2014')
                >>> markup_list = abjad.MarkupList([city, date])
                >>> markup = markup_list.left_column()
                >>> abjad.f(markup)
                \markup {
                    \left-column
                        {
                            "Los Angeles"
                            "May - August 2014"
                        }
                    }

                >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = []
        for markup in self:
            contents.append(Markup._parse_markup_command_argument(markup))
        command = MarkupCommand('left-column', contents)
        return Markup(contents=command, direction=direction)

    def line(self, direction=None):
        r"""
        LilyPond ``\line`` markup command.

        ..  container:: example

            ..  container:: example

                >>> markups = ['Allegro', 'assai']
                >>> markup_list = abjad.MarkupList(markups)
                >>> markup = markup_list.line()
                >>> abjad.f(markup)
                \markup {
                    \line
                        {
                            Allegro
                            assai
                        }
                    }


                >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = []
        for markup in self:
            contents.extend(markup.contents)
        command = MarkupCommand('line', contents)
        return Markup(contents=command, direction=direction)

    def overlay(self, direction=None):
        r"""
        LilyPond ``\overlay`` markup command.

        ..  container:: example

            ..  container:: example

                >>> city = abjad.Markup('Los Angeles')
                >>> date = abjad.Markup('May - August 2014')
                >>> markup_list = abjad.MarkupList([city, date])
                >>> markup = markup_list.overlay(direction=abjad.Up)
                >>> abjad.f(markup)
                ^ \markup {
                    \overlay
                        {
                            "Los Angeles"
                            "May - August 2014"
                        }
                    }

                >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = []
        for markup in self:
            contents.append(Markup._parse_markup_command_argument(markup))
        command = MarkupCommand('overlay', contents)
        return Markup(contents=command, direction=direction)

    def pop(self, i=-1):
        r"""
        Pops item ``i`` from markup list.

        ..  container:: example

            ..  container:: example

                >>> markup_list = abjad.MarkupList()
                >>> markup_list.extend(['Allegro', 'assai'])
                >>> markup_list.pop()
                Markup(contents=['assai'])

                >>> abjad.f(markup_list)
                abjad.MarkupList(
                    items=[
                        abjad.Markup(
                            contents=['Allegro'],
                            ),
                        ],
                    )

                >>> abjad.show(markup_list) # doctest: +SKIP

        Returns none.
        """
        return super().pop(i=i)

    def remove(self, item):
        r"""
        Removes ``item`` from markup list.

        ..  container:: example

            ..  container:: example

                >>> markup_list = abjad.MarkupList()
                >>> markup_list.extend(['Allegro', 'assai'])
                >>> markup_list.remove('assai')
                >>> abjad.f(markup_list)
                abjad.MarkupList(
                    items=[
                        abjad.Markup(
                            contents=['Allegro'],
                            ),
                        ],
                    )

                >>> abjad.show(markup_list) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup_list.__illustrate__().items[-1])
                    \markup {
                        \column
                            {
                                Allegro
                            }
                        }

        Returns none.
        """
        super().remove(item)

    def right_column(self, direction=None):
        r"""
        LilyPond ``\right-column`` markup command.

        ..  container:: example

            ..  container:: example

                >>> city = abjad.Markup('Los Angeles')
                >>> date = abjad.Markup('May - August 2014')
                >>> markup_list = abjad.MarkupList([city, date])
                >>> markup = markup_list.right_column()
                >>> abjad.f(markup)
                \markup {
                    \right-column
                        {
                            "Los Angeles"
                            "May - August 2014"
                        }
                    }

                >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        """
        contents = []
        for markup in self:
            contents.append(Markup._parse_markup_command_argument(markup))
        command = MarkupCommand('right-column', contents)
        return Markup(contents=command, direction=direction)


class Postscript(AbjadValueObject):
    r"""
    Postscript session.

    ..  note::

        The markup resulting from the ``\postscript`` markup command is both
        0-height and 0-width. Make sure to wrap the ``\postscript`` command
        with a ``\pad-to-box`` or ``\with-dimensions`` markup command to give
        it explicit height and width. Likewise, use only positive coordinates
        in your postscript markup if at all possible. When specifying explicit
        extents with ``\pad-to-box`` or ``\with-dimensions``, negative extents
        will *not* be interpreted by LilyPond as resulting in positive height
        or width, and may have unexpected behavior.

    ..  note::

        LilyPond will fail to render if *any* of the font commands are used. To
        create text, use ``.show('text')`` preceded by ``.scale()`` or
        ``.rotate()`` to provide the appropriate transformation.
        ``.charpath()`` is also useable. However, ``.findfont()``,
        ``.scalefont()``, ``.setfont()`` will cause LilyPond to error.

    ..  container:: example

        >>> postscript = abjad.Postscript()
        >>> postscript = postscript.moveto(1, 1)
        >>> postscript = postscript.setlinewidth(2.5)
        >>> postscript = postscript.setdash((2, 1))
        >>> postscript = postscript.lineto(3, -4)
        >>> postscript = postscript.stroke()
        >>> print(format(postscript))
        abjad.Postscript(
            operators=(
                abjad.PostscriptOperator('moveto', 1.0, 1.0),
                abjad.PostscriptOperator('setlinewidth', 2.5),
                abjad.PostscriptOperator('setdash', (2.0, 1.0), 0.0),
                abjad.PostscriptOperator('lineto', 3.0, -4.0),
                abjad.PostscriptOperator('stroke'),
                ),
            )

        >>> print(str(postscript))
        1 1 moveto
        2.5 setlinewidth
        [ 2 1 ] 0 setdash
        3 -4 lineto
        stroke

        >>> postscript = abjad.Postscript()
        >>> postscript = postscript.newpath()
        >>> postscript = postscript.moveto(0, 0)
        >>> postscript = postscript.rlineto(0, -10)
        >>> postscript = postscript.rlineto(10, 0)
        >>> postscript = postscript.rlineto(0, 10)
        >>> postscript = postscript.rlineto(-10, 0)
        >>> postscript = postscript.closepath()
        >>> postscript = postscript.gsave()
        >>> postscript = postscript.setrgbcolor(0.5, 1, 0.5)
        >>> postscript = postscript.fill()
        >>> postscript = postscript.grestore()
        >>> postscript = postscript.setrgbcolor(1, 0, 0)
        >>> postscript = postscript.setlinewidth(1)
        >>> postscript = postscript.stroke()
        >>> abjad.show(postscript) # doctest: +SKIP

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_operators',
        )

    ### INITIALIZER ###

    def __init__(self, operators=None):
        prototype = PostscriptOperator
        if operators is not None:
            assert all(isinstance(_, prototype) for _ in operators)
            operators = tuple(operators)
        self._operators = operators

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        """
        Adds postscript to ``argument``.

        Returns new postscript.
        """
        assert isinstance(argument, type(self))
        self_operators = self.operators or ()
        argument_operators = argument.operators or ()
        operators = self_operators + argument_operators
        operators = operators or None
        return type(self)(operators)

    def __illustrate__(self):
        """
        Illustrates Postscript.

        Returns LilyPond file.
        """
        markup = Markup.postscript(self)
        return markup.__illustrate__()

    def __radd__(self, argument):
        """
        Adds ``argument`` to postscript.

        Returns new postscript.
        """
        assert isinstance(argument, type(self))
        self_operators = self.operators or ()
        argument_operators = argument.operators or ()
        operators = argument_operators + self_operators
        operators = operators or None
        return type(self)(operators)

    def __str__(self):
        """
        Gets string representation of Postscript.

        Return string.
        """
        if not self.operators:
            return ''
        return '\n'.join(str(_) for _ in self.operators)

    ### PRIVATE METHODS ###

    @staticmethod
    def _format_argument(argument):
        if isinstance(argument, str):
            if argument.startswith('/'):
                return argument
            return '({})'.format(argument)
        elif isinstance(argument, collections.Sequence):
            if not argument:
                return '[ ]'
            contents = ' '.join(
                Postscript._format_argument(_) for _ in argument
                )
            return '[ {} ]'.format(contents)
        elif isinstance(argument, bool):
            return str(argument).lower()
        elif isinstance(argument, (int, float)):
            argument = mathtools.integer_equivalent_number_to_integer(argument)
            return str(argument)
        return str(argument)

    def _with_operator(self, operator):
        operators = self.operators or ()
        operators = operators + (operator,)
        return type(self)(operators)

    ### PUBLIC METHODS ###

    def as_markup(self):
        r"""
        Converts postscript to markup.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(100, 200)
            >>> postscript = postscript.lineto(200, 250)
            >>> postscript = postscript.lineto(100, 300)
            >>> postscript = postscript.closepath()
            >>> postscript = postscript.gsave()
            >>> postscript = postscript.setgray(0.5)
            >>> postscript = postscript.fill()
            >>> postscript = postscript.grestore()
            >>> postscript = postscript.setlinewidth(4)
            >>> postscript = postscript.setgray(0.75)
            >>> postscript = postscript.stroke()

            >>> markup = postscript.as_markup()
            >>> print(format(markup))
            \markup {
                \postscript
                    #"
                    newpath
                    100 200 moveto
                    200 250 lineto
                    100 300 lineto
                    closepath
                    gsave
                    0.5 setgray
                    fill
                    grestore
                    4 setlinewidth
                    0.75 setgray
                    stroke
                    "
                }

        Returns new markup.
        """
        return Markup.postscript(self)

    def charpath(self, text, modify_font=True):
        """
        Postscript ``charpath`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.findfont('Times Roman')
            >>> postscript = postscript.scalefont(32)
            >>> postscript = postscript.setfont()
            >>> postscript = postscript.translate(100, 200)
            >>> postscript = postscript.rotate(45)
            >>> postscript = postscript.scale(2, 1)
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(0, 0)
            >>> postscript = postscript.charpath('This is text.', True)
            >>> postscript = postscript.setlinewidth(0.5)
            >>> postscript = postscript.setgray(0.25)
            >>> postscript = postscript.stroke()
            >>> print(str(postscript))
            /Times-Roman findfont
            32 scalefont
            setfont
            100 200 translate
            45 rotate
            2 1 scale
            newpath
            0 0 moveto
            (This is text.) true charpath
            0.5 setlinewidth
            0.25 setgray
            stroke

        Returns new Postscript.
        """
        text = str(text)
        modify_font = bool(modify_font)
        operator = PostscriptOperator(
            'charpath',
            text,
            modify_font,
            )
        return self._with_operator(operator)

    def closepath(self):
        """
        Postscript ``closepath`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(100, 200)
            >>> postscript = postscript.lineto(200, 250)
            >>> postscript = postscript.lineto(100, 300)
            >>> postscript = postscript.closepath()
            >>> postscript = postscript.gsave()
            >>> postscript = postscript.setgray(0.5)
            >>> postscript = postscript.fill()
            >>> postscript = postscript.grestore()
            >>> postscript = postscript.setlinewidth(4)
            >>> postscript = postscript.setgray(0.75)
            >>> postscript = postscript.stroke()
            >>> print(str(postscript))
            newpath
            100 200 moveto
            200 250 lineto
            100 300 lineto
            closepath
            gsave
            0.5 setgray
            fill
            grestore
            4 setlinewidth
            0.75 setgray
            stroke

        Returns new Postscript.
        """
        operator = PostscriptOperator('closepath')
        return self._with_operator(operator)

    def curveto(self, x1, y1, x2, y2, x3, y3):
        """
        Postscript ``curveto`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.curveto(0, 1, 1.5, 2, 3, 6)
            >>> print(str(postscript))
            0 1 1.5 2 3 6 curveto

        Returns new Postscript.
        """
        x1 = float(x1)
        x2 = float(x2)
        x3 = float(x3)
        y1 = float(y1)
        y2 = float(y2)
        y3 = float(y3)
        operator = PostscriptOperator(
            'curveto',
            x1, y1,
            x2, y2,
            x3, y3,
            )
        return self._with_operator(operator)

    def fill(self):
        """
        Postscript ``fill`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(100, 200)
            >>> postscript = postscript.lineto(200, 250)
            >>> postscript = postscript.lineto(100, 300)
            >>> postscript = postscript.closepath()
            >>> postscript = postscript.gsave()
            >>> postscript = postscript.setgray(0.5)
            >>> postscript = postscript.fill()
            >>> postscript = postscript.grestore()
            >>> postscript = postscript.setlinewidth(4)
            >>> postscript = postscript.setgray(0.75)
            >>> postscript = postscript.stroke()
            >>> print(str(postscript))
            newpath
            100 200 moveto
            200 250 lineto
            100 300 lineto
            closepath
            gsave
            0.5 setgray
            fill
            grestore
            4 setlinewidth
            0.75 setgray
            stroke

        Returns new Postscript.
        """
        operator = PostscriptOperator('fill')
        return self._with_operator(operator)

    def findfont(self, font_name):
        """
        Postscript ``findfont`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.findfont('Times Roman')
            >>> postscript = postscript.scalefont(12)
            >>> postscript = postscript.setfont()
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(100, 200)
            >>> postscript = postscript.show('This is text.')
            >>> print(str(postscript))
            /Times-Roman findfont
            12 scalefont
            setfont
            newpath
            100 200 moveto
            (This is text.) show

        Returns new Postscript.
        """
        font_name = str(font_name)
        font_name = font_name.replace(' ', '-')
        font_name = '/{}'.format(font_name)
        operator = PostscriptOperator('findfont', font_name)
        return self._with_operator(operator)

    def grestore(self):
        """
        Postscript ``grestore`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(100, 200)
            >>> postscript = postscript.lineto(200, 250)
            >>> postscript = postscript.lineto(100, 300)
            >>> postscript = postscript.closepath()
            >>> postscript = postscript.gsave()
            >>> postscript = postscript.setgray(0.5)
            >>> postscript = postscript.fill()
            >>> postscript = postscript.grestore()
            >>> postscript = postscript.setlinewidth(4)
            >>> postscript = postscript.setgray(0.75)
            >>> postscript = postscript.stroke()
            >>> print(str(postscript))
            newpath
            100 200 moveto
            200 250 lineto
            100 300 lineto
            closepath
            gsave
            0.5 setgray
            fill
            grestore
            4 setlinewidth
            0.75 setgray
            stroke

        Returns new Postscript.
        """
        operator = PostscriptOperator('grestore')
        return self._with_operator(operator)

    def gsave(self):
        """
        Postscript ``gsave`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(100, 200)
            >>> postscript = postscript.lineto(200, 250)
            >>> postscript = postscript.lineto(100, 300)
            >>> postscript = postscript.closepath()
            >>> postscript = postscript.gsave()
            >>> postscript = postscript.setgray(0.5)
            >>> postscript = postscript.fill()
            >>> postscript = postscript.grestore()
            >>> postscript = postscript.setlinewidth(4)
            >>> postscript = postscript.setgray(0.75)
            >>> postscript = postscript.stroke()
            >>> print(str(postscript))
            newpath
            100 200 moveto
            200 250 lineto
            100 300 lineto
            closepath
            gsave
            0.5 setgray
            fill
            grestore
            4 setlinewidth
            0.75 setgray
            stroke

        Returns new Postscript.
        """
        operator = PostscriptOperator('gsave')
        return self._with_operator(operator)

    def lineto(self, x, y):
        """
        Postscript ``lineto`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.moveto(1, 1)
            >>> postscript = postscript.lineto(3, -4)
            >>> postscript = postscript.stroke()
            >>> print(str(postscript))
            1 1 moveto
            3 -4 lineto
            stroke

        Returns new Postscript.
        """
        x = float(x)
        y = float(y)
        operator = PostscriptOperator('lineto', x, y)
        return self._with_operator(operator)

    def moveto(self, x, y):
        """
        Postscript ``moveto`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.moveto(1, 1)
            >>> postscript = postscript.lineto(3, -4)
            >>> postscript = postscript.stroke()
            >>> print(format(postscript))
            abjad.Postscript(
                operators=(
                    abjad.PostscriptOperator('moveto', 1.0, 1.0),
                    abjad.PostscriptOperator('lineto', 3.0, -4.0),
                    abjad.PostscriptOperator('stroke'),
                    ),
                )

            >>> print(str(postscript))
            1 1 moveto
            3 -4 lineto
            stroke

        Returns new Postscript.
        """
        x = float(x)
        y = float(y)
        operator = PostscriptOperator('moveto', x, y)
        return self._with_operator(operator)

    def newpath(self):
        """
        Postscript ``newpath`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(100, 200)
            >>> postscript = postscript.lineto(200, 250)
            >>> postscript = postscript.lineto(100, 300)
            >>> postscript = postscript.closepath()
            >>> postscript = postscript.gsave()
            >>> postscript = postscript.setgray(0.5)
            >>> postscript = postscript.fill()
            >>> postscript = postscript.grestore()
            >>> postscript = postscript.setlinewidth(4)
            >>> postscript = postscript.setgray(0.75)
            >>> postscript = postscript.stroke()
            >>> print(str(postscript))
            newpath
            100 200 moveto
            200 250 lineto
            100 300 lineto
            closepath
            gsave
            0.5 setgray
            fill
            grestore
            4 setlinewidth
            0.75 setgray
            stroke

        Returns new Postscript.
        """
        operator = PostscriptOperator('newpath')
        return self._with_operator(operator)

    def rcurveto(self, dx1, dy1, dx2, dy2, dx3, dy3):
        """
        Postscript ``rcurveto`` operator.

        ..  container:: edxample

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.rcurveto(0, 1, 1.5, 2, 3, 6)
            >>> print(str(postscript))
            0 1 1.5 2 3 6 rcurveto

        Returns new Postscript.
        """
        dx1 = float(dx1)
        dx2 = float(dx2)
        dx3 = float(dx3)
        dy1 = float(dy1)
        dy2 = float(dy2)
        dy3 = float(dy3)
        operator = PostscriptOperator(
            'rcurveto',
            dx1, dy1,
            dx2, dy2,
            dx3, dy3,
            )
        return self._with_operator(operator)

    def rlineto(self, dx, dy):
        """
        Postscript ``rlineto`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.rmoveto(1, 1)
            >>> postscript = postscript.rlineto(3, -4)
            >>> postscript = postscript.stroke()
            >>> print(format(postscript))
            abjad.Postscript(
                operators=(
                    abjad.PostscriptOperator('rmoveto', 1.0, 1.0),
                    abjad.PostscriptOperator('rlineto', 3.0, -4.0),
                    abjad.PostscriptOperator('stroke'),
                    ),
                )

            >>> print(str(postscript))
            1 1 rmoveto
            3 -4 rlineto
            stroke

        Returns new Postscript.
        """
        dx = float(dx)
        dy = float(dy)
        operator = PostscriptOperator('rlineto', dx, dy)
        return self._with_operator(operator)

    def rmoveto(self, dx, dy):
        """
        Postscript ``rmoveto`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.rmoveto(1, 1)
            >>> postscript = postscript.rlineto(3, -4)
            >>> postscript = postscript.stroke()
            >>> print(format(postscript))
            abjad.Postscript(
                operators=(
                    abjad.PostscriptOperator('rmoveto', 1.0, 1.0),
                    abjad.PostscriptOperator('rlineto', 3.0, -4.0),
                    abjad.PostscriptOperator('stroke'),
                    ),
                )

            >>> print(str(postscript))
            1 1 rmoveto
            3 -4 rlineto
            stroke

        Returns new Postscript.
        """
        dx = float(dx)
        dy = float(dy)
        operator = PostscriptOperator('rmoveto', dx, dy)
        return self._with_operator(operator)

    def rotate(self, degrees):
        """
        Postscript ``restore`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.findfont('Times Roman')
            >>> postscript = postscript.scalefont(32)
            >>> postscript = postscript.setfont()
            >>> postscript = postscript.translate(100, 200)
            >>> postscript = postscript.rotate(45)
            >>> postscript = postscript.scale(2, 1)
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(0, 0)
            >>> postscript = postscript.charpath('This is text.', True)
            >>> postscript = postscript.setlinewidth(0.5)
            >>> postscript = postscript.setgray(0.25)
            >>> postscript = postscript.stroke()
            >>> print(str(postscript))
            /Times-Roman findfont
            32 scalefont
            setfont
            100 200 translate
            45 rotate
            2 1 scale
            newpath
            0 0 moveto
            (This is text.) true charpath
            0.5 setlinewidth
            0.25 setgray
            stroke

        Returns new Postscript.
        """
        degrees = float(degrees)
        operator = PostscriptOperator('rotate', degrees)
        return self._with_operator(operator)

    def scale(self, dx, dy):
        """
        Postscript ``scale`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.findfont('Times Roman')
            >>> postscript = postscript.scalefont(32)
            >>> postscript = postscript.setfont()
            >>> postscript = postscript.translate(100, 200)
            >>> postscript = postscript.rotate(45)
            >>> postscript = postscript.scale(2, 1)
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(0, 0)
            >>> postscript = postscript.charpath('This is text.', True)
            >>> postscript = postscript.setlinewidth(0.5)
            >>> postscript = postscript.setgray(0.25)
            >>> postscript = postscript.stroke()
            >>> print(str(postscript))
            /Times-Roman findfont
            32 scalefont
            setfont
            100 200 translate
            45 rotate
            2 1 scale
            newpath
            0 0 moveto
            (This is text.) true charpath
            0.5 setlinewidth
            0.25 setgray
            stroke

        Returns new Postscript.
        """
        dx = float(dx)
        dy = float(dy)
        operator = PostscriptOperator('scale', dx, dy)
        return self._with_operator(operator)

    def scalefont(self, font_size):
        """
        Postscript ``scalefont`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.findfont('Times Roman')
            >>> postscript = postscript.scalefont(12)
            >>> postscript = postscript.setfont()
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(100, 200)
            >>> postscript = postscript.show('This is text.')
            >>> print(str(postscript))
            /Times-Roman findfont
            12 scalefont
            setfont
            newpath
            100 200 moveto
            (This is text.) show

        Returns new Postscript.
        """
        font_size = float(font_size)
        operator = PostscriptOperator('scalefont', font_size)
        return self._with_operator(operator)

    def setdash(self, array=None, offset=0):
        """
        Postscript ``setdash`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript().setdash([2, 1], 3)
            >>> print(format(postscript))
            abjad.Postscript(
                operators=(
                    abjad.PostscriptOperator('setdash', (2.0, 1.0), 3.0),
                    ),
                )

            >>> print(str(postscript))
            [ 2 1 ] 3 setdash

        ..  container:: example

            >>> postscript = abjad.Postscript().setdash()
            >>> print(format(postscript))
            abjad.Postscript(
                operators=(
                    abjad.PostscriptOperator('setdash', (), 0.0),
                    ),
                )

            >>> print(str(postscript))
            [ ] 0 setdash

        Returns new Postscript.
        """
        if array is None:
            array = ()
        else:
            array = tuple(float(_) for _ in array)
        offset = float(offset)
        operator = PostscriptOperator('setdash', array, offset)
        return self._with_operator(operator)

    def setfont(self):
        """
        Postscript ``setfont`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.findfont('Times Roman')
            >>> postscript = postscript.scalefont(12)
            >>> postscript = postscript.setfont()
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(100, 200)
            >>> postscript = postscript.show('This is text.')
            >>> print(str(postscript))
            /Times-Roman findfont
            12 scalefont
            setfont
            newpath
            100 200 moveto
            (This is text.) show

        Returns new Postscript.
        """
        operator = PostscriptOperator('setfont')
        return self._with_operator(operator)

    def setgray(self, gray_value):
        """
        Postscript ``setgray`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(100, 200)
            >>> postscript = postscript.lineto(200, 250)
            >>> postscript = postscript.lineto(100, 300)
            >>> postscript = postscript.closepath()
            >>> postscript = postscript.gsave()
            >>> postscript = postscript.setgray(0.5)
            >>> postscript = postscript.fill()
            >>> postscript = postscript.grestore()
            >>> postscript = postscript.setlinewidth(4)
            >>> postscript = postscript.setgray(0.75)
            >>> postscript = postscript.stroke()
            >>> print(str(postscript))
            newpath
            100 200 moveto
            200 250 lineto
            100 300 lineto
            closepath
            gsave
            0.5 setgray
            fill
            grestore
            4 setlinewidth
            0.75 setgray
            stroke

        Returns new Postscript.
        """
        gray_value = float(gray_value)
        assert 0 <= gray_value <= 1
        operator = PostscriptOperator('setgray', gray_value)
        return self._with_operator(operator)

    def setlinewidth(self, width):
        """
        Postscript ``setlinewidth`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.moveto(1, 1)
            >>> postscript = postscript.setlinewidth(2.5)
            >>> postscript = postscript.lineto(3, -4)
            >>> postscript = postscript.stroke()
            >>> print(format(postscript))
            abjad.Postscript(
                operators=(
                    abjad.PostscriptOperator('moveto', 1.0, 1.0),
                    abjad.PostscriptOperator('setlinewidth', 2.5),
                    abjad.PostscriptOperator('lineto', 3.0, -4.0),
                    abjad.PostscriptOperator('stroke'),
                    ),
                )

            >>> print(str(postscript))
            1 1 moveto
            2.5 setlinewidth
            3 -4 lineto
            stroke

        Returns new Postscript.
        """
        width = float(width)
        operator = PostscriptOperator('setlinewidth', width)
        return self._with_operator(operator)

    def setrgbcolor(self, red, green, blue):
        """
        Postscript ``setrgb`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(100, 100)
            >>> postscript = postscript.rlineto(0, 100)
            >>> postscript = postscript.rlineto(100, 0)
            >>> postscript = postscript.rlineto(0, -100)
            >>> postscript = postscript.rlineto(-100, 0)
            >>> postscript = postscript.closepath()
            >>> postscript = postscript.gsave()
            >>> postscript = postscript.setrgbcolor(0.5, 1, 0.5)
            >>> postscript = postscript.fill()
            >>> postscript = postscript.grestore()
            >>> postscript = postscript.setrgbcolor(1, 0, 0)
            >>> postscript = postscript.setlinewidth(4)
            >>> postscript = postscript.stroke()

            >>> print(str(postscript))
            newpath
            100 100 moveto
            0 100 rlineto
            100 0 rlineto
            0 -100 rlineto
            -100 0 rlineto
            closepath
            gsave
            0.5 1 0.5 setrgbcolor
            fill
            grestore
            1 0 0 setrgbcolor
            4 setlinewidth
            stroke

        Returns new Postscript.
        """
        red = float(red)
        green = float(green)
        blue = float(blue)
        assert 0 <= red <= 1
        assert 0 <= green <= 1
        assert 0 <= blue <= 1
        operator = PostscriptOperator(
            'setrgbcolor',
            red,
            green,
            blue,
            )
        return self._with_operator(operator)

    def show(self, text):
        """
        Postscript ``show`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.findfont('Times Roman')
            >>> postscript = postscript.scalefont(12)
            >>> postscript = postscript.setfont()
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(100, 200)
            >>> postscript = postscript.show('This is text.')
            >>> print(str(postscript))
            /Times-Roman findfont
            12 scalefont
            setfont
            newpath
            100 200 moveto
            (This is text.) show

        Returns new Postscript.
        """
        text = str(text)
        operator = PostscriptOperator('show', text)
        return self._with_operator(operator)

    def stroke(self):
        """
        Postscript ``stroke`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.lineto(3, -4)
            >>> postscript = postscript.stroke()
            >>> print(format(postscript))
            abjad.Postscript(
                operators=(
                    abjad.PostscriptOperator('lineto', 3.0, -4.0),
                    abjad.PostscriptOperator('stroke'),
                    ),
                )

            >>> print(str(postscript))
            3 -4 lineto
            stroke

        Returns new Postscript.
        """
        operator = PostscriptOperator('stroke')
        return self._with_operator(operator)

    def translate(self, dx, dy):
        """
        Postscript ``translate`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.findfont('Times Roman')
            >>> postscript = postscript.scalefont(32)
            >>> postscript = postscript.setfont()
            >>> postscript = postscript.translate(100, 200)
            >>> postscript = postscript.rotate(45)
            >>> postscript = postscript.scale(2, 1)
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(0, 0)
            >>> postscript = postscript.charpath('This is text.', True)
            >>> postscript = postscript.setlinewidth(0.5)
            >>> postscript = postscript.setgray(0.25)
            >>> postscript = postscript.stroke()
            >>> print(str(postscript))
            /Times-Roman findfont
            32 scalefont
            setfont
            100 200 translate
            45 rotate
            2 1 scale
            newpath
            0 0 moveto
            (This is text.) true charpath
            0.5 setlinewidth
            0.25 setgray
            stroke

        Returns new Postscript.
        """
        dx = float(dx)
        dy = float(dy)
        operator = PostscriptOperator('translate', dx, dy)
        return self._with_operator(operator)

    ### PUBLIC PROPERTIES ###

    @property
    def operators(self):
        """
        Gets Postscript operators.

        Returns tuple or none.
        """
        return self._operators


class PostscriptOperator(AbjadValueObject):
    """
    Postscript operator.

    ..  container:: example

        >>> operator = abjad.PostscriptOperator('rmoveto', 1, 1.5)
        >>> print(format(operator))
        abjad.PostscriptOperator('rmoveto', 1, 1.5)

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        '_arguments',
        )

    ### INITIALIZER ###

    def __init__(self, name='stroke', *arguments):
        name = str(name)
        self._name = name
        if arguments:
            self._arguments = tuple(arguments)
        else:
            self._arguments = None

    ### SPECIAL METHODS ###

    def __str__(self):
        """
        Gets string representation of Postscript operator.

        ..  container:: example

            >>> operator = abjad.PostscriptOperator('rmoveto', 1, 1.5)
            >>> str(operator)
            '1 1.5 rmoveto'

        Returns string.
        """
        parts = []
        if self.arguments:
            for argument in self.arguments:
                parts.append(Postscript._format_argument(argument))
        parts.append(self.name)
        string = ' '.join(parts)
        return string

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.name] + list(self.arguments or ())
        return FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_is_indented=False,
            storage_format_kwargs_names=[],
            )

    ### PUBLIC PROPERTIES ###

    @property
    def arguments(self):
        """
        Gets Postscript operator arguments.

        Returns tuple or none.
        """
        return self._arguments

    @property
    def name(self):
        """
        Gets Postscript operator name.

        Returns string.
        """
        return self._name
