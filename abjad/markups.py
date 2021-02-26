"""
Tools for modeling LilyPond's markup and postscript.
"""
import collections
import typing

from . import enums, math
from . import tag as _tag
from .bundle import LilyPondFormatBundle
from .fsv import format_scheme_value
from .new import new
from .overrides import TweakInterface
from .storage import FormatSpecification, StorageFormatManager
from .string import String


class Markup:
    r"""
    LilyPond markup.

    ..  container:: example

        Initializes from string:

        >>> string = r'\italic { "Allegro assai" }'
        >>> markup = abjad.Markup(string)
        >>> string = abjad.lilypond(markup)
        >>> print(string)
        \markup {
            \italic
                {
                    "Allegro assai"
                }
            }

        >>> abjad.show(markup) # doctest: +SKIP

    ..  container:: example

        Initializes from other markup:

        >>> markup = abjad.Markup(r'\italic "Allegro assai"', direction=abjad.Up)
        >>> markup = abjad.Markup(markup, direction=abjad.Down)
        >>> string = abjad.lilypond(markup)
        >>> print(string)
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
        >>> string = abjad.lilypond(markup)
        >>> print(string)
        ^ \markup {
            \italic
                {
                    "Allegro assai"
                }
            }

        >>> abjad.attach(markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
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

    ..  note:: Make sure all markup methods implement a direction
        keyword when extending this class.

    Set ``direction`` to ``Up``, ``Down``, ``"neutral"``, ``"^"``, ``"_"``,
    ``"-"`` or None.

    ..  container:: example

        Markup can be tagged:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup(r"\italic Allegro", direction=abjad.Up)
        >>> abjad.attach(markup, staff[0], tag=abjad.Tag("RED:M1"))
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
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
        >>> markup = abjad.Markup(r"\italic Allegro", direction=abjad.Up)
        >>> abjad.attach(
        ...     markup,
        ...     staff[0],
        ...     deactivate=True,
        ...     tag=abjad.Tag("RED:M1"),
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
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
        >>> markup_1 = abjad.Markup(r"\italic Allegro", direction=abjad.Up)
        >>> markup_2 = abjad.Markup(r'\italic "non troppo"', direction=abjad.Up)
        >>> abjad.attach(markup_1, staff[0])
        >>> abjad.attach(markup_2, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff)
        >>> print(string)
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
        "_annotation",
        "_contents",
        "_direction",
        "_literal",
        "_tweaks",
    )

    _private_attributes_to_copy = ("_tweaks",)

    ### INITIALIZER ###

    def __init__(
        self,
        contents=None,
        *,
        direction: typing.Union[int, enums.VerticalAlignment] = None,
        literal: bool = None,
        tweaks: TweakInterface = None,
    ) -> None:
        from .parsers.parse import parse

        self._annotation = None
        new_contents: typing.Tuple[typing.Union[str, MarkupCommand], ...]
        if contents is None:
            new_contents = ("",)
        elif isinstance(contents, str) and not literal:
            to_parse = rf"\markup {{ {contents} }}"
            parsed = parse(to_parse)
            if all(isinstance(_, str) for _ in parsed.contents):
                new_contents = (" ".join(parsed.contents),)
            else:
                new_contents = tuple(parsed.contents)
        elif isinstance(contents, str) and literal is True:
            new_contents = (contents,)
        elif isinstance(contents, MarkupCommand):
            new_contents = (contents,)
        elif isinstance(contents, type(self)):
            direction = direction or contents.direction
            if direction is not None:
                assert isinstance(direction, (str, enums.VerticalAlignment)), repr(
                    direction
                )
            literal = literal or contents.literal
            new_contents = tuple(contents.contents)
        elif isinstance(contents, collections.abc.Sequence) and 0 < len(contents):
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
        assert all(isinstance(_, (str, MarkupCommand)) for _ in new_contents), repr(
            new_contents
        )
        self._contents = new_contents
        direction_ = String.to_tridirectional_ordinal_constant(direction)
        if direction_ is not None:
            assert isinstance(direction_, enums.VerticalAlignment), repr(direction_)
        self._direction = direction_
        if literal is not None:
            literal = bool(literal)
        self._literal = literal
        if tweaks is not None:
            assert isinstance(tweaks, TweakInterface), repr(tweaks)
        self._tweaks = TweakInterface.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r"""
        Adds markup to ``argument``.

        ..  container:: example

            Adds markup to markup:

            >>> markup = abjad.Markup("Allegro") + abjad.Markup("assai")
            >>> string = abjad.lilypond(markup)
            >>> print(string)
            \markup {
                Allegro
                assai
                }

            >>> abjad.show(markup) # doctest: +SKIP

        ..  container:: example

            Adds markup command to markup:

            >>> markup = abjad.Markup(r"Allegro \hspace #0.75")
            >>> markup = markup + abjad.Markup("assai")
            >>> string = abjad.lilypond(markup)
            >>> print(string)
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
            raise TypeError(f"must be markup or markup command: {argument!r}.")
        markup = type(self)(contents=commands, direction=self.direction)
        return markup

    def __copy__(self, *arguments):
        """
        Copies markup.

        >>> import copy

        ..  container:: example

            >>> markup_1 = abjad.Markup("Allegro assai", direction=abjad.Up)
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

            >>> markup_1 = abjad.Markup("Allegro")
            >>> markup_2 = abjad.Markup("Allegro")
            >>> markup_3 = abjad.Markup("Allegro assai")

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

            >>> markup_1 = abjad.Markup("Allegro")
            >>> markup_2 = abjad.Markup("Allegro", direction=abjad.Up)

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
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self):
        """
        Hashes markup.

        ..  container:: example

            Without keywords:

            >>> hash_1 = hash(abjad.Markup("Allegro"))
            >>> hash_2 = hash(abjad.Markup("Allegro"))
            >>> hash_3 = hash(abjad.Markup("Allegro assai"))

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

            >>> hash_1 = hash(abjad.Markup("Allegro"))
            >>> hash_2 = hash(abjad.Markup("Allegro", direction=abjad.Up))

            >>> hash_1 == hash_1
            True
            >>> hash_1 == hash_2
            False
            >>> hash_2 == hash_1
            False
            >>> hash_2 == hash_2
            True

        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __lt__(self, argument):
        """
        Is true when markup contents compare less than ``argument`` contents.

        ..  container:: example

            >>> markup_1 = abjad.Markup("Allegro")
            >>> markup_2 = abjad.Markup("assai")

            >>> markup_1 < markup_2
            True
            >>> markup_2 < markup_1
            False

        Raises type error when ``argument`` is not markup.

        Returns true or false.
        """
        if not isinstance(argument, type(self)):
            raise TypeError(f"can only compare markup to markup: {argument!r}.")
        return self.contents < argument.contents

    def __radd__(self, argument):
        r"""
        Adds ``argument`` to markup.

        ..  container:: example

            Adds markup to markup:

            >>> markup = abjad.Markup("Allegro") + abjad.Markup("assai")
            >>> string = abjad.lilypond(markup)
            >>> print(string)
            \markup {
                Allegro
                assai
                }

            >>> abjad.show(markup) # doctest: +SKIP

        ..  container:: example

            Adds markup to markup command:

            >>> markup = abjad.Markup(r"Allegro \hspace #0.75")
            >>> markup = markup + abjad.Markup("assai")
            >>> string = abjad.lilypond(markup)
            >>> print(string)
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
            raise TypeError(f"must be markup or markup command: {argument!r}.")
        commands.extend(self.contents)
        markup = type(self)(contents=commands, direction=self.direction)
        return markup

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

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
        tweaks = []
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
        indent = LilyPondFormatBundle.indent
        direction = ""
        if self.direction is not None:
            direction = String.to_tridirectional_lilypond_symbol(self.direction)
        if len(self.contents) == 1 and isinstance(self.contents[0], str):
            content = self.contents[0]
            if not self.literal:
                if content:
                    content = rf"\markup {{ {content} }}"
                else:
                    content = r"\markup {}"
            if direction:
                string = rf"{direction} {content}"
            else:
                string = content
            return tweaks + [string]
        if direction:
            string = rf"{direction} \markup {{"
            pieces = [string]
        else:
            pieces = [r"\markup {"]
        for content in self.contents:
            if isinstance(content, str):
                pieces.append(f"{indent}{content}")
            else:
                pieces_ = content._get_format_pieces()
                pieces.extend([f"{indent}{_}" for _ in pieces_])
        pieces.append(f"{indent}}}")
        return tweaks + pieces

    def _get_format_specification(self):
        names = list(StorageFormatManager(self).signature_keyword_names)
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_keyword_names=names,
        )

    def _get_lilypond_format(self):
        return "\n".join(self._get_format_pieces())

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
            raise TypeError(f"must be markup, markup command or string: {argument!r}.")
        return contents

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self) -> typing.List[typing.Union[str, "MarkupCommand"]]:
        r"""
        Gets contents of markup.

        ..  container:: example

            Initializes contents positionally:

            >>> abjad.Markup("Allegro assai")
            Markup(contents=['Allegro assai'])

            Initializes contents from keyword:

            >>> abjad.Markup(contents="Allegro assai")
            Markup(contents=['Allegro assai'])

        """
        return list(self._contents)

    @property
    def direction(self) -> typing.Optional[enums.VerticalAlignment]:
        r"""
        Gets direction of markup.

        ..  container:: example

            With ``direction`` unset:

            >>> markup = abjad.Markup("Allegro")
            >>> note = abjad.Note("c'4")
            >>> abjad.attach(markup, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c'4
                - \markup { Allegro }

            With ``direction=abjad.Up``:

            >>> markup = abjad.Markup("Allegro", direction=abjad.Up)
            >>> note = abjad.Note("c'4")
            >>> abjad.attach(markup, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c'4
                ^ \markup { Allegro }


            With ``direction=abjad.Down``:

            >>> markup = abjad.Markup("Allegro", direction=abjad.Down)
            >>> note = abjad.Note("c'4")
            >>> abjad.attach(markup, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c'4
                _ \markup { Allegro }

        ..  container:: example

            REGRESSSION #806. Markup preserves tweaks when ``direction=None``:

            >>> markup = abjad.Markup("Allegro")
            >>> abjad.tweak(markup).color = "#red"
            >>> note = abjad.Note("c'4")
            >>> abjad.attach(markup, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c'4
                - \tweak color #red
                - \markup { Allegro }

        """
        return self._direction

    @property
    def literal(self) -> typing.Optional[bool]:
        r"""
        Is true when markup formats contents literally.

        ..  container:: example

            Adds neither quotes nor braces:

            >>> string = r"\custom-function #1 #4"
            >>> markup = abjad.Markup(string, literal=True)
            >>> string = abjad.lilypond(markup)
            >>> print(string)
            \custom-function #1 #4

            Works with normal initializer, too:

            >>> string = r"\custom-function #1 #4"
            >>> markup = abjad.Markup(string, literal=True)
            >>> string = abjad.lilypond(markup)
            >>> print(string)
            \custom-function #1 #4

        ..  container:: example

            Works with direction:

            >>> string = r"\custom-function #1 #4"
            >>> markup = abjad.Markup(
            ...     string,
            ...     direction=abjad.Up,
            ...     literal=True,
            ...     )
            >>> string = abjad.lilypond(markup)
            >>> print(string)
            ^ \custom-function #1 #4

            Works with normal initialier, too:

            >>> string = r"\custom-function #1 #4"
            >>> markup = abjad.Markup(
            ...     string,
            ...     direction=abjad.Up,
            ...     literal=True,
            ...     )
            >>> string = abjad.lilypond(markup)
            >>> print(string)
            ^ \custom-function #1 #4

        ..  container:: example

            REGRESSION. Input string accepts LilyPond \markup command:

            >>> string = r'\markup { \note {4} #1 }'
            >>> markup = abjad.Markup(
            ...     string,
            ...     direction=abjad.Up,
            ...     literal=True,
            ...     )
            >>> string = abjad.lilypond(markup)
            >>> print(string)
            ^ \markup { \note {4} #1 }

            >>> note = abjad.Note("c'4")
            >>> abjad.attach(markup, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c'4
                ^ \markup { \note {4} #1 }

        """
        return self._literal

    # TODO: Tweaks do not appear on markup without direction!
    @property
    def tweaks(self) -> typing.Optional[TweakInterface]:
        r"""
        Gets tweaks.

        ..  container:: example

            >>> markup = abjad.Markup(r'\bold "Allegro assai"', direction=abjad.Up)
            >>> abjad.tweak(markup).color = "#blue"
            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(markup, staff[0])
            >>> string = abjad.lilypond(staff)
            >>> print(string)
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

    # TODO: move to abjad.illustrators._illustrate_postscript
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
            >>> string = abjad.lilypond(markup)
            >>> print(string)
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
        command = MarkupCommand("postscript", postscript)
        return class_(contents=command, direction=direction)


class MarkupCommand:
    r"""
    LilyPond markup command.

    ..  container:: example

        Initializes a complex LilyPond markup command:

        >>> circle = abjad.markups.MarkupCommand("draw-circle", 2.5, 0.1, False)
        >>> square = abjad.markups.MarkupCommand("rounded-box", "hello?")
        >>> line = abjad.markups.MarkupCommand("line", [square, "wow!"])
        >>> rotate = abjad.markups.MarkupCommand("rotate", 60, line)
        >>> combine = abjad.markups.MarkupCommand("combine", rotate, circle)

        >>> print(abjad.lilypond(combine))
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

            >>> string = abjad.lilypond(note)
            >>> print(string)
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
        >>> small_staff.remove_commands.append("Clef_engraver")
        >>> small_staff.remove_commands.append("Time_signature_engraver")
        >>> abjad.setting(small_staff).fontSize = -3
        >>> layout_block = abjad.Block(name="layout")
        >>> layout_block.indent = 0
        >>> layout_block.ragged_right = "##t"
        >>> command = abjad.markups.MarkupCommand(
        ...     "score",
        ...     [small_staff, layout_block],
        ...     )

        >>> string = abjad.lilypond(command)
        >>> print(string)
        \score
            {
                \new Staff
                \with
                {
                    \remove Clef_engraver
                    \remove Time_signature_engraver
                    fontSize = -3
                }
                {
                    fs'16
                    gs'16
                    as'16
                    b'16
                }
                \layout {
                    indent = 0
                    ragged-right = ##t
                }
            }

        >>> markup = abjad.Markup(contents=command, direction=abjad.Up)
        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> abjad.attach(markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
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
                                fontSize = -3
                            }
                            {
                                fs'16
                                gs'16
                                as'16
                                b'16
                            }
                            \layout {
                                indent = 0
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

    __slots__ = ("_arguments", "_deactivate", "_name", "_tag")

    ### INITIALIZER ###

    def __init__(self, name=None, *arguments):
        if name is None:
            # TODO: Generalize these arbitrary default arguments away.
            name = "draw-circle"
            assert len(arguments) == 0
        self._arguments = tuple(arguments)
        self._deactivate = None
        assert isinstance(name, str) and len(name)
        self._name = name
        self._tag = None

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a markup command with name and
        arguments equal to those of this markup command.

        ..  container:: example

            >>> command_1 = abjad.markups.MarkupCommand("bold", "foo")
            >>> command_2 = abjad.markups.MarkupCommand("bold", "foo")
            >>> command_3 = abjad.markups.MarkupCommand("bold", "bar")

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

    def __hash__(self):
        """
        Hashes markup command.

        Redefined in tandem with __eq__.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self):
        r"""
        Gets markup command interpreter representation.

        ..  container:: example

            Interpreter representation is evaluable.

            >>> command = abjad.markups.MarkupCommand("hspace", 0)
            >>> command
            MarkupCommand('hspace', 0)

        Returns string.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self):
        r"""
        Gets string representation of markup command.

        ..  container:: example

            >>> circle = abjad.markups.MarkupCommand("draw-circle", 2.5, 0.1, False)
            >>> square = abjad.markups.MarkupCommand("rounded-box", "hello?")
            >>> line = abjad.markups.MarkupCommand("line", [square, "wow!"])
            >>> rotate = abjad.markups.MarkupCommand("rotate", 60, line)
            >>> combine = abjad.markups.MarkupCommand("combine", rotate, circle)
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
        def recurse(iterable):
            result = []
            for item in iterable:
                if isinstance(item, (list, tuple)):
                    result.append("{")
                    result.extend(recurse(item))
                    result.append("}")
                elif hasattr(item, "_get_format_pieces"):
                    result.extend(item._get_format_pieces())
                elif isinstance(item, str) and "\n" in item:
                    result.append('#"')
                    result.extend(item.splitlines())
                    result.append('"')
                else:
                    formatted = format_scheme_value(item)
                    if isinstance(item, str):
                        result.append(formatted)
                        # result.append(item)
                    else:
                        result.append(f"#{formatted}")
                        # result.append(f"#{item}")
            return [f"{indent}{item}" for item in result]

        indent = LilyPondFormatBundle.indent
        parts = [rf"\{self.name}"]
        parts.extend(recurse(self.arguments))
        parts = _tag.tag(parts, self.tag, deactivate=self.deactivate)
        return parts

    def _get_format_specification(self):
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=(self.name,) + self.arguments,
            storage_format_keyword_names=[],
        )

    def _get_lilypond_format(self):
        return "\n".join(self._get_format_pieces())

    ### PUBLIC PROPERTIES ###

    @property
    def arguments(self):
        """
        Gets markup command arguments.

        ..  container:: example

            >>> arguments = ("draw-circle", 1, 0.1, False)
            >>> command = abjad.markups.MarkupCommand(*arguments)
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
    def name(self):
        """
        Gets markup command name.

        ..  container:: example

            >>> arguments = ("draw-circle", 1, 0.1, False)
            >>> command = abjad.markups.MarkupCommand(*arguments)
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
        if argument is not None:
            tag = _tag.Tag(argument)
        else:
            tag = None
        self._tag = tag

    ### PUBLIC METHODS ###


class Postscript:
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
        create text, use ``.show("text")`` preceded by ``.scale()`` or
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
        >>> print(abjad.storage(postscript))
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

    __slots__ = ("_operators",)

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

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

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

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self):
        """
        Gets string representation of Postscript.

        Return string.
        """
        if not self.operators:
            return ""
        return "\n".join(str(_) for _ in self.operators)

    ### PRIVATE METHODS ###

    @staticmethod
    def _format_argument(argument):
        if isinstance(argument, str):
            if argument.startswith("/"):
                return argument
            return f"({argument})"
        elif isinstance(argument, collections.abc.Sequence):
            if not argument:
                return "[ ]"
            contents = " ".join(Postscript._format_argument(_) for _ in argument)
            return f"[ {contents} ]"
        elif isinstance(argument, bool):
            return str(argument).lower()
        elif isinstance(argument, (int, float)):
            argument = math.integer_equivalent_number_to_integer(argument)
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
            >>> print(abjad.lilypond(markup))
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
        return Markup(rf'\postscript #"{self}"')

    def charpath(self, text, modify_font=True):
        """
        Postscript ``charpath`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.findfont("Times Roman")
            >>> postscript = postscript.scalefont(32)
            >>> postscript = postscript.setfont()
            >>> postscript = postscript.translate(100, 200)
            >>> postscript = postscript.rotate(45)
            >>> postscript = postscript.scale(2, 1)
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(0, 0)
            >>> postscript = postscript.charpath("This is text.", True)
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
        operator = PostscriptOperator("charpath", text, modify_font)
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
        operator = PostscriptOperator("closepath")
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
        operator = PostscriptOperator("curveto", x1, y1, x2, y2, x3, y3)
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
        operator = PostscriptOperator("fill")
        return self._with_operator(operator)

    def findfont(self, font_name):
        """
        Postscript ``findfont`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.findfont("Times Roman")
            >>> postscript = postscript.scalefont(12)
            >>> postscript = postscript.setfont()
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(100, 200)
            >>> postscript = postscript.show("This is text.")
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
        font_name = font_name.replace(" ", "-")
        font_name = f"/{font_name}"
        operator = PostscriptOperator("findfont", font_name)
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
        operator = PostscriptOperator("grestore")
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
        operator = PostscriptOperator("gsave")
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
        operator = PostscriptOperator("lineto", x, y)
        return self._with_operator(operator)

    def moveto(self, x, y):
        """
        Postscript ``moveto`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.moveto(1, 1)
            >>> postscript = postscript.lineto(3, -4)
            >>> postscript = postscript.stroke()
            >>> print(abjad.storage(postscript))
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
        operator = PostscriptOperator("moveto", x, y)
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
        operator = PostscriptOperator("newpath")
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
        operator = PostscriptOperator("rcurveto", dx1, dy1, dx2, dy2, dx3, dy3)
        return self._with_operator(operator)

    def rlineto(self, dx, dy):
        """
        Postscript ``rlineto`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.rmoveto(1, 1)
            >>> postscript = postscript.rlineto(3, -4)
            >>> postscript = postscript.stroke()
            >>> print(abjad.storage(postscript))
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
        operator = PostscriptOperator("rlineto", dx, dy)
        return self._with_operator(operator)

    def rmoveto(self, dx, dy):
        """
        Postscript ``rmoveto`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.rmoveto(1, 1)
            >>> postscript = postscript.rlineto(3, -4)
            >>> postscript = postscript.stroke()
            >>> print(abjad.storage(postscript))
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
        operator = PostscriptOperator("rmoveto", dx, dy)
        return self._with_operator(operator)

    def rotate(self, degrees):
        """
        Postscript ``restore`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.findfont("Times Roman")
            >>> postscript = postscript.scalefont(32)
            >>> postscript = postscript.setfont()
            >>> postscript = postscript.translate(100, 200)
            >>> postscript = postscript.rotate(45)
            >>> postscript = postscript.scale(2, 1)
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(0, 0)
            >>> postscript = postscript.charpath("This is text.", True)
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
        operator = PostscriptOperator("rotate", degrees)
        return self._with_operator(operator)

    def scale(self, dx, dy):
        """
        Postscript ``scale`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.findfont("Times Roman")
            >>> postscript = postscript.scalefont(32)
            >>> postscript = postscript.setfont()
            >>> postscript = postscript.translate(100, 200)
            >>> postscript = postscript.rotate(45)
            >>> postscript = postscript.scale(2, 1)
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(0, 0)
            >>> postscript = postscript.charpath("This is text.", True)
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
        operator = PostscriptOperator("scale", dx, dy)
        return self._with_operator(operator)

    def scalefont(self, font_size):
        """
        Postscript ``scalefont`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.findfont("Times Roman")
            >>> postscript = postscript.scalefont(12)
            >>> postscript = postscript.setfont()
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(100, 200)
            >>> postscript = postscript.show("This is text.")
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
        operator = PostscriptOperator("scalefont", font_size)
        return self._with_operator(operator)

    def setdash(self, array=None, offset=0):
        """
        Postscript ``setdash`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript().setdash([2, 1], 3)
            >>> print(abjad.storage(postscript))
            abjad.Postscript(
                operators=(
                    abjad.PostscriptOperator('setdash', (2.0, 1.0), 3.0),
                    ),
                )

            >>> print(str(postscript))
            [ 2 1 ] 3 setdash

        ..  container:: example

            >>> postscript = abjad.Postscript().setdash()
            >>> print(abjad.storage(postscript))
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
        operator = PostscriptOperator("setdash", array, offset)
        return self._with_operator(operator)

    def setfont(self):
        """
        Postscript ``setfont`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.findfont("Times Roman")
            >>> postscript = postscript.scalefont(12)
            >>> postscript = postscript.setfont()
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(100, 200)
            >>> postscript = postscript.show("This is text.")
            >>> print(str(postscript))
            /Times-Roman findfont
            12 scalefont
            setfont
            newpath
            100 200 moveto
            (This is text.) show

        Returns new Postscript.
        """
        operator = PostscriptOperator("setfont")
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
        operator = PostscriptOperator("setgray", gray_value)
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
            >>> print(abjad.storage(postscript))
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
        operator = PostscriptOperator("setlinewidth", width)
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
        operator = PostscriptOperator("setrgbcolor", red, green, blue)
        return self._with_operator(operator)

    def show(self, text):
        """
        Postscript ``show`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.findfont("Times Roman")
            >>> postscript = postscript.scalefont(12)
            >>> postscript = postscript.setfont()
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(100, 200)
            >>> postscript = postscript.show("This is text.")
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
        operator = PostscriptOperator("show", text)
        return self._with_operator(operator)

    def stroke(self):
        """
        Postscript ``stroke`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.lineto(3, -4)
            >>> postscript = postscript.stroke()
            >>> print(abjad.storage(postscript))
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
        operator = PostscriptOperator("stroke")
        return self._with_operator(operator)

    def translate(self, dx, dy):
        """
        Postscript ``translate`` operator.

        ..  container:: example

            >>> postscript = abjad.Postscript()
            >>> postscript = postscript.findfont("Times Roman")
            >>> postscript = postscript.scalefont(32)
            >>> postscript = postscript.setfont()
            >>> postscript = postscript.translate(100, 200)
            >>> postscript = postscript.rotate(45)
            >>> postscript = postscript.scale(2, 1)
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(0, 0)
            >>> postscript = postscript.charpath("This is text.", True)
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
        operator = PostscriptOperator("translate", dx, dy)
        return self._with_operator(operator)

    ### PUBLIC PROPERTIES ###

    @property
    def operators(self):
        """
        Gets Postscript operators.

        Returns tuple or none.
        """
        return self._operators


class PostscriptOperator:
    """
    Postscript operator.

    ..  container:: example

        >>> operator = abjad.PostscriptOperator("rmoveto", 1, 1.5)
        >>> abjad.storage(operator)
        "abjad.PostscriptOperator('rmoveto', 1, 1.5)"

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_name", "_arguments")

    ### INITIALIZER ###

    def __init__(self, name="stroke", *arguments):
        name = str(name)
        self._name = name
        if arguments:
            self._arguments = tuple(arguments)
        else:
            self._arguments = None

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self):
        """
        Gets string representation of Postscript operator.

        ..  container:: example

            >>> operator = abjad.PostscriptOperator("rmoveto", 1, 1.5)
            >>> str(operator)
            '1 1.5 rmoveto'

        Returns string.
        """
        parts = []
        if self.arguments:
            for argument in self.arguments:
                parts.append(Postscript._format_argument(argument))
        parts.append(self.name)
        string = " ".join(parts)
        return string

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.name] + list(self.arguments or ())
        return FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_is_indented=False,
            storage_format_keyword_names=[],
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


### FUNCTIONS ###


def abjad_metronome_mark(
    duration_log,
    dot_count,
    stem_height,
    units_per_minute,
    direction=None,
) -> Markup:
    r"""
    Abjad ``\abjad-metronome-mark-markup`` command.

    ..  container:: example

        >>> markup = abjad.markups.abjad_metronome_mark(
        ...     2, 0, 1, 67.5, direction=abjad.Up,
        ... )
        >>> string = abjad.lilypond(markup)
        >>> print(string)
        ^ \markup {
            \abjad-metronome-mark-markup #2 #0 #1 #"67.5"
            }

        >>> abjad.show(markup) # doctest: +SKIP

    Returns new markup
    """
    string = "abjad-metronome-mark-markup"
    string += f" #{duration_log}"
    string += f" #{dot_count}"
    string += f" #{stem_height}"
    string += f' #"{units_per_minute}"'
    command = MarkupCommand(string)
    return Markup(contents=command, direction=direction)
