import typing

from .. import enums, math
from ..bundle import LilyPondFormatBundle
from ..overrides import TweakInterface
from ..storage import FormatSpecification, StorageFormatManager
from ..string import String


class Dynamic:
    r"""
    Dynamic.

    ..  container:: example

        Initializes from dynamic name:

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8")
        >>> dynamic = abjad.Dynamic('f')
        >>> abjad.attach(dynamic, voice[0])

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'8
                \f
                d'8
                e'8
                f'8
            }

        >>> abjad.show(voice) # doctest: +SKIP

    ..  container:: example

        Initializes from other dynamic:

        >>> dynamic_1 = abjad.Dynamic('f')
        >>> dynamic_2 = abjad.Dynamic(dynamic_1)

        >>> dynamic_1
        Dynamic('f')

        >>> dynamic_2
        Dynamic('f')

    ..  container:: example

        Initializes niente:

        >>> abjad.Dynamic('niente')
        Dynamic('niente', direction=Down, name_is_textual=True)

    ..  container:: example

        Simultaneous dynamics in a single staff:

        >>> voice_1 = abjad.Voice("e'8 g'8 f'8 a'8")
        >>> abjad.attach(abjad.Dynamic('f'), voice_1[0], context='Voice')
        >>> literal = abjad.LilyPondLiteral(r"\voiceOne", "opening")
        >>> abjad.attach(literal, voice_1)
        >>> abjad.override(voice_1).DynamicLineSpanner.direction = abjad.Up
        >>> voice_2 = abjad.Voice("c'2")
        >>> literal = abjad.LilyPondLiteral(r"\voiceTwo", "opening")
        >>> abjad.attach(literal, voice_2)
        >>> abjad.attach(abjad.Dynamic('mf'), voice_2[0], context='Voice')
        >>> staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            <<
                \new Voice
                \with
                {
                    \override DynamicLineSpanner.direction = #up
                }
                {
                    \voiceOne
                    e'8
                    \f
                    g'8
                    f'8
                    a'8
                }
                \new Voice
                {
                    \voiceTwo
                    c'2
                    \mf
                }
            >>

        >>> for leaf in abjad.select(staff).leaves():
        ...     leaf, abjad.get.effective(leaf, abjad.Dynamic)
        ...
        (Note("e'8"), Dynamic('f'))
        (Note("g'8"), Dynamic('f'))
        (Note("f'8"), Dynamic('f'))
        (Note("a'8"), Dynamic('f'))
        (Note("c'2"), Dynamic('mf'))

    ..  container:: example exception

        Errors on nondynamic input:

        >>> abjad.Dynamic('text')
        Traceback (most recent call last):
            ...
        Exception: the letter 't' (in 'text') is not a dynamic.

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_command",
        "_direction",
        "_format_hairpin_stop",
        "_hide",
        "_leak",
        "_name",
        "_name_is_textual",
        "_ordinal",
        "_sforzando",
        "_tweaks",
    )

    _composite_dynamic_name_to_steady_state_dynamic_name = {
        "fp": "p",
        "sf": "f",
        "sff": "ff",
        "sfp": "p",
        "sfpp": "pp",
        "sffp": "p",
        "sffpp": "pp",
        "sfz": "f",
        "sp": "p",
        "spp": "pp",
        "rfz": "f",
    }

    _context = "Voice"

    _dynamic_name_to_dynamic_ordinal = {
        "ppppp": -6,
        "pppp": -5,
        "ppp": -4,
        "pp": -3,
        "p": -2,
        "niente": math.NegativeInfinity(),
        "mp": -1,
        "mf": 1,
        "f": 2,
        "ff": 3,
        "fff": 4,
        "ffff": 5,
        "fffff": 6,
    }

    _dynamic_names = (
        "ppppp",
        "pppp",
        "ppp",
        "pp",
        "p",
        "mp",
        "mf",
        "f",
        "ff",
        "fff",
        "ffff",
        "fffff",
        "fp",
        "sf",
        "sff",
        "sp",
        "spp",
        "sfz",
        "sffz",
        "sfffz",
        "sffp",
        "sffpp",
        "sfp",
        "sfpp",
        "rfz",
        "niente",
    )

    _dynamic_ordinal_to_dynamic_name = {
        -6: "ppppp",
        -5: "pppp",
        -4: "ppp",
        -3: "pp",
        -2: "p",
        -1: "mp",
        math.NegativeInfinity(): "niente",
        1: "mf",
        2: "f",
        3: "ff",
        4: "fff",
        5: "ffff",
        6: "fffff",
    }

    _format_slot = "after"

    _lilypond_dynamic_commands = [_ for _ in _dynamic_names if not _ == "niente"]

    _lilypond_dynamic_alphabet = "fmprsz"

    _parameter = "DYNAMIC"

    _persistent = True

    _to_width = {'"f"': 2, '"mf"': 3.5, '"mp"': 3.5, '"p"': 2, "sfz": 2.5}

    ### INITIALIZER ###

    def __init__(
        self,
        name: typing.Union[str, "Dynamic"] = "f",
        *,
        command: str = None,
        direction: enums.VerticalAlignment = None,
        format_hairpin_stop: bool = None,
        hide: bool = None,
        leak: bool = None,
        name_is_textual: bool = None,
        ordinal: typing.Union[int, math.Infinity, math.NegativeInfinity] = None,
        sforzando: bool = None,
        tweaks: TweakInterface = None,
    ) -> None:
        if name is not None:
            assert isinstance(name, (str, type(self))), repr(name)
        if isinstance(name, type(self)):
            name_ = name.name
        elif isinstance(name, str):
            name_ = name
        if name_ == "niente":
            if name_is_textual not in (None, True):
                raise Exception("niente dynamic name is always textual.")
            name_is_textual = True
        if not name_is_textual:
            for letter in name_.strip('"'):
                if letter not in self._lilypond_dynamic_alphabet:
                    message = f"the letter {letter!r} (in {name!r})"
                    message += " is not a dynamic."
                    raise Exception(message)
        self._name = name_
        if command is not None:
            assert isinstance(command, str), repr(command)
            assert command.startswith("\\"), repr(command)
        self._command = command
        if direction is not None:
            assert direction in (enums.Down, enums.Up), repr(direction)
        self._direction = direction
        if format_hairpin_stop is not None:
            format_hairpin_stop = bool(format_hairpin_stop)
        self._format_hairpin_stop = format_hairpin_stop
        if hide is not None:
            hide = bool(hide)
        self._hide = hide
        if leak is not None:
            leak = bool(leak)
        self._leak = leak
        if name_is_textual is not None:
            name_is_textual = bool(name_is_textual)
        self._name_is_textual = name_is_textual
        if ordinal is not None:
            assert isinstance(ordinal, (int, math.Infinity, math.NegativeInfinity))
        self._ordinal = ordinal
        if sforzando is not None:
            sforzando = bool(sforzando)
        self._sforzando = sforzando
        if tweaks is not None:
            assert isinstance(tweaks, TweakInterface), repr(tweaks)
        self._tweaks = TweakInterface.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` equals dynamic.

        ..  container:: example

            >>> dynamic_1 = abjad.Dynamic('p')
            >>> dynamic_2 = abjad.Dynamic('p')
            >>> dynamic_3 = abjad.Dynamic('f')

            >>> dynamic_1 == dynamic_1
            True
            >>> dynamic_1 == dynamic_2
            True
            >>> dynamic_1 == dynamic_3
            False

            >>> dynamic_2 == dynamic_1
            True
            >>> dynamic_2 == dynamic_2
            True
            >>> dynamic_2 == dynamic_3
            False

            >>> dynamic_3 == dynamic_1
            False
            >>> dynamic_3 == dynamic_2
            False
            >>> dynamic_3 == dynamic_3
            True

        """
        if not isinstance(argument, type(self)):
            return False
        if self.name == argument.name and self.ordinal == argument.ordinal:
            return True
        return False

    def __hash__(self) -> int:
        """
        Hashes dynamic.

        Redefined in tandem with __eq__.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, component_expression):
        if not hasattr(component_expression, "written_duration"):
            strings = [f"Must be leaf (not {component_expression})."]
            return strings
        return True

    def _format_effort_dynamic(self):
        name = self.name.strip('"')
        before = {"f": -0.4, "m": -0.1, "p": -0.1, "r": -0.1, "s": -0.3, "z": -0.2}[
            name[0]
        ]
        after = {"f": -0.2, "m": -0.1, "p": -0.25, "r": 0, "s": 0, "z": -0.2}[name[-1]]
        direction = self.direction
        direction = String.to_tridirectional_lilypond_symbol(direction)
        strings = []
        strings.append(f"{direction} #(make-dynamic-script")
        strings.append("    (markup")
        strings.append("        #:whiteout")
        strings.append("        #:line (")
        strings.append('            #:general-align Y -2 #:normal-text #:larger "“"')
        strings.append(f"            #:hspace {before}")
        strings.append(f'            #:dynamic "{name}"')
        strings.append(f"            #:hspace {after}")
        strings.append('            #:general-align Y -2 #:normal-text #:larger "”"')
        strings.append("            )")
        strings.append("        )")
        strings.append("    )")
        string = "\n".join(strings)
        return string

    @staticmethod
    def _format_textual(direction, string):
        if direction is None:
            direction = enums.Down
        direction = String.to_tridirectional_lilypond_symbol(direction)
        assert isinstance(string, str), repr(string)
        string = f'(markup #:whiteout #:normal-text #:italic "{string}")'
        string = f"{direction} #(make-dynamic-script {string})"
        return string

    def _get_format_specification(self):
        keywords = ["command", "direction", "hide", "leak"]
        if self._ordinal is not None:
            keywords.append("ordinal")
        keywords.append("name_is_textual")
        if self._sforzando is not None:
            keywords.append("sforzando")
        return FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=[self.name],
            storage_format_is_indented=False,
            storage_format_keyword_names=keywords,
        )

    def _get_lilypond_format(self):
        if self.command:
            string = self.command
        elif self.effort:
            string = self._format_effort_dynamic()
        elif self.name_is_textual:
            string = self._format_textual(self.direction, self.name)
        else:
            string = rf"\{self.name}"
            if self.direction is not None:
                direction_ = self.direction
                direction = String.to_tridirectional_lilypond_symbol(direction_)
                string = f"{direction} {string}"
        return string

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.leak:
            bundle.after.leaks.append("<>")
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            if self.leak:
                bundle.after.leaks.extend(tweaks)
            else:
                bundle.after.articulations.extend(tweaks)
        if not self.hide:
            string = self._get_lilypond_format()
            if self.leak:
                bundle.after.leaks.append(string)
            else:
                bundle.after.articulations.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def command(self) -> typing.Optional[str]:
        r"""
        Gets explicit command.

        ..  container:: example

            >>> abjad.Dynamic('f', command=r'\sub_f').command
            '\\sub_f'

        Use to override LilyPond output when a custom dynamic has been defined
        in an external stylesheet. (In the example above, ``\sub_f`` is a
        nonstandard LilyPond dynamic. LilyPond will interpret the output above
        only when the command ``\sub_f`` is defined somewhere in an external
        stylesheet.)
        """
        return self._command

    @property
    def context(self) -> str:
        """
        Returns (historically conventional) context ``'Voice'``.

        ..  container:: example

            >>> abjad.Dynamic('f').context
            'Voice'

        Class constant.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def direction(self) -> typing.Optional[enums.VerticalAlignment]:
        r"""
        Gets direction for effort dynamics only.

        ..  container:: example

            With ``direction`` unset:

            >>> staff = abjad.Staff("c'2 c''2")
            >>> abjad.attach(abjad.Dynamic("p"), staff[0])
            >>> abjad.attach(abjad.Dynamic("f"), staff[1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'2
                    \p
                    c''2
                    \f
                }

            With ``direction=abjad.Up``:

            >>> staff = abjad.Staff("c'2 c''2")
            >>> abjad.attach(abjad.Dynamic("p", direction=abjad.Up), staff[0])
            >>> abjad.attach(abjad.Dynamic("f", direction=abjad.Up), staff[1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'2
                    ^ \p
                    c''2
                    ^ \f
                }

            With ``direction=abjad.Down``:

            >>> staff = abjad.Staff("c'2 c''2")
            >>> abjad.attach(abjad.Dynamic("p", direction=abjad.Down), staff[0])
            >>> abjad.attach(abjad.Dynamic("f", direction=abjad.Down), staff[1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'2
                    _ \p
                    c''2
                    _ \f
                }

        ..  container:: example

            REGRESSION. Effort dynamics default to down:

            >>> staff = abjad.Staff("c'2 c''2")
            >>> abjad.attach(abjad.Dynamic('"p"'), staff[0])
            >>> abjad.attach(abjad.Dynamic('"f"'), staff[1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'2
                    _ #(make-dynamic-script
                        (markup
                            #:whiteout
                            #:line (
                                #:general-align Y -2 #:normal-text #:larger "“"
                                #:hspace -0.1
                                #:dynamic "p"
                                #:hspace -0.25
                                #:general-align Y -2 #:normal-text #:larger "”"
                                )
                            )
                        )
                    c''2
                    _ #(make-dynamic-script
                        (markup
                            #:whiteout
                            #:line (
                                #:general-align Y -2 #:normal-text #:larger "“"
                                #:hspace -0.4
                                #:dynamic "f"
                                #:hspace -0.2
                                #:general-align Y -2 #:normal-text #:larger "”"
                                )
                            )
                        )
                }

            And may be overriden:

            >>> staff = abjad.Staff("c'2 c''2")
            >>> abjad.attach(abjad.Dynamic('"p"', direction=abjad.Up), staff[0])
            >>> abjad.attach(abjad.Dynamic('"f"', direction=abjad.Up), staff[1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'2
                    ^ #(make-dynamic-script
                        (markup
                            #:whiteout
                            #:line (
                                #:general-align Y -2 #:normal-text #:larger "“"
                                #:hspace -0.1
                                #:dynamic "p"
                                #:hspace -0.25
                                #:general-align Y -2 #:normal-text #:larger "”"
                                )
                            )
                        )
                    c''2
                    ^ #(make-dynamic-script
                        (markup
                            #:whiteout
                            #:line (
                                #:general-align Y -2 #:normal-text #:larger "“"
                                #:hspace -0.4
                                #:dynamic "f"
                                #:hspace -0.2
                                #:general-align Y -2 #:normal-text #:larger "”"
                                )
                            )
                        )
                }

        """
        if self._direction is not None:
            return self._direction
        elif self.name == "niente" or self.effort:
            result = enums.Down
            assert isinstance(result, enums.VerticalAlignment)
            return result
        else:
            return None

    @property
    def effort(self) -> typing.Optional[bool]:
        r"""
        Is true when double quotes enclose dynamic.

        ..  container:: example

            >>> voice = abjad.Voice("c'4 r d' r e' r f' r")
            >>> abjad.attach(abjad.Dynamic('"pp"'), voice[0])
            >>> abjad.attach(abjad.Dynamic('"mp"'), voice[2])
            >>> abjad.attach(abjad.Dynamic('"mf"'), voice[4])
            >>> abjad.attach(abjad.Dynamic('"ff"'), voice[6])
            >>> abjad.override(voice).DynamicLineSpanner.staff_padding = 4
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                \with
                {
                    \override DynamicLineSpanner.staff-padding = 4
                }
                {
                    c'4
                    _ #(make-dynamic-script
                        (markup
                            #:whiteout
                            #:line (
                                #:general-align Y -2 #:normal-text #:larger "“"
                                #:hspace -0.1
                                #:dynamic "pp"
                                #:hspace -0.25
                                #:general-align Y -2 #:normal-text #:larger "”"
                                )
                            )
                        )
                    r4
                    d'4
                    _ #(make-dynamic-script
                        (markup
                            #:whiteout
                            #:line (
                                #:general-align Y -2 #:normal-text #:larger "“"
                                #:hspace -0.1
                                #:dynamic "mp"
                                #:hspace -0.25
                                #:general-align Y -2 #:normal-text #:larger "”"
                                )
                            )
                        )
                    r4
                    e'4
                    _ #(make-dynamic-script
                        (markup
                            #:whiteout
                            #:line (
                                #:general-align Y -2 #:normal-text #:larger "“"
                                #:hspace -0.1
                                #:dynamic "mf"
                                #:hspace -0.2
                                #:general-align Y -2 #:normal-text #:larger "”"
                                )
                            )
                        )
                    r4
                    f'4
                    _ #(make-dynamic-script
                        (markup
                            #:whiteout
                            #:line (
                                #:general-align Y -2 #:normal-text #:larger "“"
                                #:hspace -0.4
                                #:dynamic "ff"
                                #:hspace -0.2
                                #:general-align Y -2 #:normal-text #:larger "”"
                                )
                            )
                        )
                    r4
                }

        ..  container:: example

            >>> voice = abjad.Voice("c'4 r d' r e' r f' r")
            >>> abjad.attach(abjad.Dynamic('"sf"'), voice[0])
            >>> abjad.attach(abjad.Dynamic('"sfz"'), voice[2])
            >>> abjad.attach(abjad.Dynamic('"rf"'), voice[4])
            >>> abjad.attach(abjad.Dynamic('"rfz"'), voice[6])
            >>> abjad.override(voice).DynamicLineSpanner.staff_padding = 4
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                \with
                {
                    \override DynamicLineSpanner.staff-padding = 4
                }
                {
                    c'4
                    _ #(make-dynamic-script
                        (markup
                            #:whiteout
                            #:line (
                                #:general-align Y -2 #:normal-text #:larger "“"
                                #:hspace -0.3
                                #:dynamic "sf"
                                #:hspace -0.2
                                #:general-align Y -2 #:normal-text #:larger "”"
                                )
                            )
                        )
                    r4
                    d'4
                    _ #(make-dynamic-script
                        (markup
                            #:whiteout
                            #:line (
                                #:general-align Y -2 #:normal-text #:larger "“"
                                #:hspace -0.3
                                #:dynamic "sfz"
                                #:hspace -0.2
                                #:general-align Y -2 #:normal-text #:larger "”"
                                )
                            )
                        )
                    r4
                    e'4
                    _ #(make-dynamic-script
                        (markup
                            #:whiteout
                            #:line (
                                #:general-align Y -2 #:normal-text #:larger "“"
                                #:hspace -0.1
                                #:dynamic "rf"
                                #:hspace -0.2
                                #:general-align Y -2 #:normal-text #:larger "”"
                                )
                            )
                        )
                    r4
                    f'4
                    _ #(make-dynamic-script
                        (markup
                            #:whiteout
                            #:line (
                                #:general-align Y -2 #:normal-text #:larger "“"
                                #:hspace -0.1
                                #:dynamic "rfz"
                                #:hspace -0.2
                                #:general-align Y -2 #:normal-text #:larger "”"
                                )
                            )
                        )
                    r4
                }

        """
        return bool(self.name) and self.name[0] == '"'

    @property
    def format_hairpin_stop(self) -> typing.Optional[bool]:
        r"""
        Is true when dynamic formats LilyPond ``\!`` hairpin stop.
        """
        return self._format_hairpin_stop

    @property
    def hide(self) -> typing.Optional[bool]:
        r"""
        Is true when dynamic should not appear in output (but should still
        determine effective dynamic).

        ..  container:: example

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('f'), voice[0])
            >>> abjad.attach(abjad.Dynamic('mf', hide=True), voice[2])
            >>> abjad.show(voice) # doctest: +SKIP

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                \f
                d'4
                e'4
                f'4
            }

            >>> for leaf in abjad.iterate(voice).leaves():
            ...     leaf, abjad.get.effective(leaf, abjad.Dynamic)
            ...
            (Note("c'4"), Dynamic('f'))
            (Note("d'4"), Dynamic('f'))
            (Note("e'4"), Dynamic('mf', hide=True))
            (Note("f'4"), Dynamic('mf', hide=True))

        """
        return self._hide

    @property
    def leak(self) -> typing.Optional[bool]:
        r"""
        Is true when dynamic formats LilyPond empty chord ``<>`` symbol.

        ..  container:: example

            Without leaked stop dynamic:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> start_dynamic = abjad.Dynamic('mf')
            >>> start_hairpin = abjad.StartHairpin('>')
            >>> stop_dynamic = abjad.Dynamic('pp')
            >>> abjad.attach(start_dynamic, staff[0])
            >>> abjad.attach(start_hairpin, staff[0])
            >>> abjad.attach(stop_dynamic, staff[-2])
            >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = 4
                }
                {
                    c'4
                    \mf
                    \>
                    d'4
                    e'4
                    \pp
                    r4
                }

            With leaked stop dynamic:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> start_dynamic = abjad.Dynamic('mf')
            >>> start_hairpin = abjad.StartHairpin('>')
            >>> stop_dynamic = abjad.Dynamic('pp', leak=True)
            >>> abjad.attach(start_dynamic, staff[0])
            >>> abjad.attach(start_hairpin, staff[0])
            >>> abjad.attach(stop_dynamic, staff[-2])
            >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = 4
                }
                {
                    c'4
                    \mf
                    \>
                    d'4
                    e'4
                    <>
                    \pp
                    r4
                }

        ..  container:: example

            Leaks format after spanners:

            >>> staff = abjad.Staff("c'8 [ d' e' ] f'")
            >>> start_dynamic = abjad.Dynamic('mf')
            >>> start_hairpin = abjad.StartHairpin('>')
            >>> stop_dynamic = abjad.Dynamic('pp', leak=True)
            >>> abjad.attach(start_dynamic, staff[0])
            >>> abjad.attach(start_hairpin, staff[0])
            >>> abjad.attach(stop_dynamic, staff[-2])
            >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = 4
                }
                {
                    c'8
                    \mf
                    \>
                    [
                    d'8
                    e'8
                    ]
                    <>
                    \pp
                    f'8
                }

        ..  container:: example

            Leaked and nonleaked dynamic may be attached to the same leaf:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('f'), staff[0])
            >>> abjad.attach(abjad.Dynamic('p', leak=True), staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    \f
                    <> \p
                    d'4
                    e'4
                    f'4
                }

        ..  container:: example

            Leaks and tweaks on the same dynamic format correctly;
            LilyPond empty chord ``<>`` symbol appears before postevents:

            >>> staff = abjad.Staff("r4 d' e' f'")
            >>> dynamic = abjad.Dynamic('f', leak=True)
            >>> abjad.tweak(dynamic).color = "#blue"
            >>> abjad.attach(dynamic, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                r4
                <>
                - \tweak color #blue
                \f
                d'4
                e'4
                f'4
            }

        ..  container:: example

            Leak survives copy:

            >>> import copy
            >>> dynamic = abjad.Dynamic('pp', leak=True)
            >>> copy.copy(dynamic)
            Dynamic('pp', leak=True)

        """
        return self._leak

    @property
    def name(self) -> str:
        r"""
        Gets name.

        ..  container:: example

            >>> abjad.Dynamic('f').name
            'f'

            >>> abjad.Dynamic('p').name
            'p'

            >>> abjad.Dynamic('sffz').name
            'sffz'

            >>> abjad.Dynamic('sffp').name
            'sffp'

            >>> abjad.Dynamic('"f"').name
            '"f"'

        ..  container:: example

            Niente dynamics format like this:

            >>> voice = abjad.Voice("c'4 r r c'4")
            >>> abjad.attach(abjad.Dynamic('p'), voice[0])
            >>> abjad.attach(abjad.Dynamic('niente'), voice[1])
            >>> abjad.attach(abjad.Dynamic('p'), voice[3])
            >>> abjad.override(voice).DynamicLineSpanner.staff_padding = 4
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                \with
                {
                    \override DynamicLineSpanner.staff-padding = 4
                }
                {
                    c'4
                    \p
                    r4
                    _ #(make-dynamic-script (markup #:whiteout #:normal-text #:italic "niente"))
                    r4
                    c'4
                    \p
                }

        """
        return self._name

    @property
    def name_is_textual(self) -> typing.Optional[bool]:
        r"""
        Is true when name is textual.

        ..  container:: example

            >>> abjad.Dynamic('f').name_is_textual is None
            True

            >>> abjad.Dynamic('niente').name_is_textual
            True

            >>> dynamic = abjad.Dynamic('appena udibile', name_is_textual=True)
            >>> dynamic.name_is_textual
            True

        ..  container:: example

            Textual dynamics format like this when initialized without an
            explicit command:

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> dynamic = abjad.Dynamic('appena udibile', name_is_textual=True)
            >>> abjad.attach(dynamic, voice[0])
            >>> abjad.override(voice).DynamicLineSpanner.staff_padding = 4
            >>> abjad.override(voice).DynamicText.X_extent = "#'(0 . 0)"
            >>> abjad.override(voice).DynamicText.self_alignment_X = abjad.Left
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                \with
                {
                    \override DynamicLineSpanner.staff-padding = 4
                    \override DynamicText.X-extent = #'(0 . 0)
                    \override DynamicText.self-alignment-X = #left
                }
                {
                    c'4
                    _ #(make-dynamic-script (markup #:whiteout #:normal-text #:italic "appena udibile"))
                    d'4
                    e'4
                    f'4
                }

        ..  container:: example

            Textual dynamics format like this when initialized with an
            explicit command:

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> dynamic = abjad.Dynamic(
            ...     'appena udibile',
            ...     command=r'\appena_udibile',
            ...     name_is_textual=True,
            ...     )
            >>> abjad.attach(dynamic, voice[0])

            Only LilyPond output is shown here because dynamic commands (like
            ``\appena_udibile`` shown here) are meant to be user-defined (and
            not included in Abjad):

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                \appena_udibile
                d'4
                e'4
                f'4
            }

        ..  container:: example

            REGRESSION. Textual names work with new:

            >>> dynamic = abjad.Dynamic('niente')
            >>> abjad.new(dynamic)
            Dynamic('niente', direction=Down, ordinal=NegativeInfinity, name_is_textual=True, sforzando=False)

            >>> dynamic = abjad.Dynamic('appena udibile', name_is_textual=True)
            >>> abjad.new(dynamic)
            Dynamic('appena udibile', name_is_textual=True, sforzando=False)

        """
        return self._name_is_textual

    @property
    # def ordinal(self) -> typing.Union[int, math.Infinity, math.NegativeInfinity]:
    def ordinal(self):
        """
        Gets ordinal.

        ..  container:: example

            >>> abjad.Dynamic('f').ordinal
            2

            >>> abjad.Dynamic('p').ordinal
            -2

        ..  container:: example

            >>> abjad.Dynamic('niente').ordinal
            NegativeInfinity

        ..  container:: example

            >>> abjad.Dynamic('"f"').ordinal
            2

            >>> abjad.Dynamic('"p"').ordinal
            -2

        ..  container:: example

            User-defined ordinals:

            >>> barely_audible = abjad.Dynamic(
            ...     'barely audible',
            ...     name_is_textual=True,
            ...     ordinal=-99,
            ...     )
            >>> barely_audible.ordinal
            -99

            >>> extremely_loud = abjad.Dynamic(
            ...     'extremely loud',
            ...     name_is_textual=True,
            ...     ordinal=99,
            ...     )
            >>> extremely_loud.ordinal
            99

        ..  container:: example

            REGRESSION. Textual names without explicit ordinal return none:

            >>> dynamic = abjad.Dynamic('appena udibile', name_is_textual=True)
            >>> dynamic.ordinal is None
            True

        """
        if self._ordinal is not None:
            return self._ordinal
        name = None
        if self.name:
            name = self.name.strip('"')
        if name in self._composite_dynamic_name_to_steady_state_dynamic_name:
            name = self._composite_dynamic_name_to_steady_state_dynamic_name[name]
        ordinal = self._dynamic_name_to_dynamic_ordinal.get(name)
        return ordinal

    @property
    def parameter(self) -> str:
        """
        Returns ``'DYNAMIC'``.

        ..  container:: example

            >>> abjad.Dynamic('f').parameter
            'DYNAMIC'

        """
        return self._parameter

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.Dynamic('f').persistent
            True

        """
        return self._persistent

    @property
    def regression(self):
        r"""
        Documents regressions.

        ..  container:: example

            Duplicate dynamics raise exception on attach:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> dynamic = abjad.Dynamic('p')
            >>> abjad.attach(dynamic, staff[0])
            >>> dynamic = abjad.Dynamic('p')
            >>> abjad.attach(dynamic, staff[0])
            Traceback (most recent call last):
                ...
            abjad.exceptions.PersistentIndicatorError:
            <BLANKLINE>
            Can not attach ...
            <BLANKLINE>
            abjad.Wrapper(
                context='Voice',
                indicator=abjad.Dynamic('p'),
                tag=abjad.Tag(),
                )
            <BLANKLINE>
                ... to Note("c'4") in None because ...
            <BLANKLINE>
            abjad.Wrapper(
                context='Voice',
                indicator=abjad.Dynamic('p'),
                tag=abjad.Tag(),
                )
            <BLANKLINE>
                ... is already attached to the same leaf.

        """
        pass

    @property
    def sforzando(self) -> typing.Optional[bool]:
        """
        Is true when dynamic name begins in s- and ends in -z.

        ..  container:: example

            >>> abjad.Dynamic('f').sforzando
            False

            >>> abjad.Dynamic('sfz').sforzando
            True

            >>> abjad.Dynamic('sffz').sforzando
            True

            >>> abjad.Dynamic('sfp').sforzando
            False

            >>> abjad.Dynamic('sf').sforzando
            False

            >>> abjad.Dynamic('rfz').sforzando
            False

        """
        if self._sforzando is not None:
            return self._sforzando
        if self.name and self.name.startswith("s") and self.name.endswith("z"):
            return True
        return False

    ### PUBLIC METHODS ###

    @staticmethod
    def composite_dynamic_name_to_steady_state_dynamic_name(name) -> str:
        """
        Changes composite ``name`` to steady state dynamic name.

        ..  container:: example

            >>> abjad.Dynamic.composite_dynamic_name_to_steady_state_dynamic_name('sfp')
            'p'

            >>> abjad.Dynamic.composite_dynamic_name_to_steady_state_dynamic_name('rfz')
            'f'

        """
        return Dynamic._composite_dynamic_name_to_steady_state_dynamic_name[name]

    @staticmethod
    # def dynamic_name_to_dynamic_ordinal(name) -> typing.Union[
    #    int, Infinity, NegativeInfinity,
    #    ]:
    def dynamic_name_to_dynamic_ordinal(name):
        """
        Changes ``name`` to dynamic ordinal.

        ..  container:: example

            >>> abjad.Dynamic.dynamic_name_to_dynamic_ordinal('fff')
            4

            >>> abjad.Dynamic.dynamic_name_to_dynamic_ordinal('niente')
            NegativeInfinity

        """
        try:
            return Dynamic._dynamic_name_to_dynamic_ordinal[name]
        except KeyError:
            name = Dynamic.composite_dynamic_name_to_steady_state_dynamic_name(name)
            return Dynamic._dynamic_name_to_dynamic_ordinal[name]

    @staticmethod
    def dynamic_ordinal_to_dynamic_name(dynamic_ordinal) -> str:
        """
        Changes ``dynamic_ordinal`` to dynamic name.

        ..  container:: example

            >>> abjad.Dynamic.dynamic_ordinal_to_dynamic_name(-5)
            'pppp'

            >>> negative_infinity = abjad.math.NegativeInfinity()
            >>> abjad.Dynamic.dynamic_ordinal_to_dynamic_name(negative_infinity)
            'niente'

        """
        if dynamic_ordinal == math.NegativeInfinity():
            return "niente"
        else:
            return Dynamic._dynamic_ordinal_to_dynamic_name[dynamic_ordinal]

    @staticmethod
    def is_dynamic_name(argument) -> bool:
        """
        Is true when ``argument`` is dynamic name.

        ..  container:: example

            >>> abjad.Dynamic.is_dynamic_name('f')
            True

            >>> abjad.Dynamic.is_dynamic_name('sfz')
            True

            >>> abjad.Dynamic.is_dynamic_name('niente')
            True

        """
        return argument in Dynamic._dynamic_names

    @property
    def spanner_stop(self) -> bool:
        """
        Is true

        ..  container:: example

            >>> abjad.Dynamic("p").spanner_stop
            True

            >>> abjad.Dynamic("niente").spanner_stop
            True

        """
        return True

    @property
    def tweaks(self) -> typing.Optional[TweakInterface]:
        r"""
        Gets tweaks

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> dynamic = abjad.Dynamic('f')
            >>> abjad.tweak(dynamic).color = "#blue"
            >>> abjad.attach(dynamic, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c'4
                - \tweak color #blue
                \f

        """
        return self._tweaks
