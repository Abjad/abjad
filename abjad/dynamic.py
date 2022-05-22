import dataclasses
import typing

from . import contributions as _contributions
from . import enums as _enums
from . import math as _math
from . import string as _string

_EMPTY_CHORD = "<>"


# TODO: move to indicators.py
# TODO: frozen=True
@dataclasses.dataclass(eq=False, slots=True, unsafe_hash=True)
class Dynamic:
    r"""
    Dynamic.

    ..  container:: example

        Initializes from dynamic name:

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8")
        >>> dynamic = abjad.Dynamic("f")
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

        >>> dynamic_1 = abjad.Dynamic("f")
        >>> dynamic_2 = abjad.Dynamic(dynamic_1)

        >>> dynamic_1
        Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

        >>> dynamic_2
        Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Initializes niente:

        >>> abjad.Dynamic("niente")
        Dynamic(name='niente', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=NegativeInfinity())

    ..  container:: example

        Simultaneous dynamics in a single staff:

        >>> voice_1 = abjad.Voice("e'8 g'8 f'8 a'8")
        >>> abjad.attach(abjad.Dynamic('f'), voice_1[0], context='Voice')
        >>> literal = abjad.LilyPondLiteral(r"\voiceOne", "opening")
        >>> abjad.attach(literal, voice_1)
        >>> abjad.override(voice_1).DynamicLineSpanner.direction = abjad.UP
        >>> voice_2 = abjad.Voice("c'2")
        >>> literal = abjad.LilyPondLiteral(r"\voiceTwo", "opening")
        >>> abjad.attach(literal, voice_2)
        >>> abjad.attach(abjad.Dynamic("mf"), voice_2[0], context="Voice")
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

        >>> for leaf in abjad.select.leaves(staff):
        ...     dynamic = abjad.get.effective(leaf, abjad.Dynamic)
        ...     print(f"{leaf!r}:")
        ...     print(f"    {dynamic!r}")
        Note("e'8"):
            Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)
        Note("g'8"):
            Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)
        Note("f'8"):
            Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)
        Note("a'8"):
            Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)
        Note("c'2"):
            Dynamic(name='mf', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=1)

    ..  container:: example exception

        Errors on nondynamic input:

        >>> abjad.Dynamic("text")
        Traceback (most recent call last):
            ...
        Exception: letter 't' (in 'text') is not a dynamic.

    ..  container:: example

        REGRESSION. Duplicate dynamics raise exception on attach:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> dynamic = abjad.Dynamic("p")
        >>> abjad.attach(dynamic, staff[0])
        >>> dynamic = abjad.Dynamic("p")
        >>> abjad.attach(dynamic, staff[0], check_duplicate_indicator=True)
        Traceback (most recent call last):
            ...
        abjad.exceptions.PersistentIndicatorError:
        <BLANKLINE>
        Can not attach ...
        <BLANKLINE>
        Wrapper(...)
        <BLANKLINE>
            ... to Note("c'4") in None because ...
        <BLANKLINE>
        Wrapper(...)
        <BLANKLINE>
            ... is already attached to the same leaf.

    ..  container:: example

        Tweaks:

        >>> note = abjad.Note("c'4")
        >>> dynamic = abjad.Dynamic("f")
        >>> bundle = abjad.bundle(dynamic, r"- \tweak color #blue")
        >>> abjad.attach(bundle, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            - \tweak color #blue
            \f

    ..  container:: example

        Use ``command`` like this:

        >>> abjad.Dynamic("f", command=r"\sub_f").command
        '\\sub_f'

        Use to override LilyPond output when a custom dynamic has been defined in an
        external stylesheet. (In the example above, ``\sub_f`` is a nonstandard LilyPond
        dynamic. LilyPond will interpret the output above only when the command
        ``\sub_f`` is defined somewhere in an external stylesheet.)


    ..  container:: example

        Direction:

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

        With ``direction=abjad.UP``:

        >>> staff = abjad.Staff("c'2 c''2")
        >>> abjad.attach(abjad.Dynamic("p"), staff[0], direction=abjad.UP)
        >>> abjad.attach(abjad.Dynamic("f"), staff[1], direction=abjad.UP)
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

        With ``direction=abjad.DOWN``:

        >>> staff = abjad.Staff("c'2 c''2")
        >>> abjad.attach(abjad.Dynamic("p"), staff[0], direction=abjad.DOWN)
        >>> abjad.attach(abjad.Dynamic("f"), staff[1], direction=abjad.DOWN)
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
        >>> abjad.attach(abjad.Dynamic('"p"'), staff[0], direction=abjad.UP)
        >>> abjad.attach(abjad.Dynamic('"f"'), staff[1], direction=abjad.UP)
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

    ..  container:: example

        Set ``hide=True`` when dynamic should not appear in output (but should still
        determine effective dynamic):

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> abjad.attach(abjad.Dynamic("f"), voice[0])
        >>> abjad.attach(abjad.Dynamic("mf", hide=True), voice[2])
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

        >>> for leaf in abjad.iterate.leaves(voice):
        ...     dynamic = abjad.get.effective(leaf, abjad.Dynamic)
        ...     print(f"{leaf!r}:")
        ...     print(f"    {dynamic!r}")
        Note("c'4"):
            Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)
        Note("d'4"):
            Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)
        Note("e'4"):
            Dynamic(name='mf', command=None, format_hairpin_stop=False, hide=True, leak=False, name_is_textual=False, ordinal=1)
        Note("f'4"):
            Dynamic(name='mf', command=None, format_hairpin_stop=False, hide=True, leak=False, name_is_textual=False, ordinal=1)

    ..  container:: example

        Set ``leak=True`` Is true to format LilyPond empty chord ``<>`` symbol:

        Without leaked stop dynamic:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> start_dynamic = abjad.Dynamic("mf")
        >>> start_hairpin = abjad.StartHairpin(">")
        >>> stop_dynamic = abjad.Dynamic("pp")
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
        >>> start_dynamic = abjad.Dynamic("mf")
        >>> start_hairpin = abjad.StartHairpin(">")
        >>> stop_dynamic = abjad.Dynamic("pp", leak=True)
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
        >>> start_dynamic = abjad.Dynamic("mf")
        >>> start_hairpin = abjad.StartHairpin(">")
        >>> stop_dynamic = abjad.Dynamic("pp", leak=True)
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
                [
                \>
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
        >>> abjad.attach(abjad.Dynamic("f"), staff[0])
        >>> abjad.attach(abjad.Dynamic("p", leak=True), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                \f
                <>
                \p
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Leaks and tweaks on the same dynamic format correctly; LilyPond empty chord
        ``<>`` symbol appears before postevents:

        >>> staff = abjad.Staff("r4 d' e' f'")
        >>> dynamic = abjad.Dynamic("f", leak=True)
        >>> bundle = abjad.bundle(dynamic, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
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
        >>> dynamic = abjad.Dynamic("pp", leak=True)
        >>> copy.copy(dynamic)
        Dynamic(name='pp', command=None, format_hairpin_stop=False, hide=False, leak=True, name_is_textual=False, ordinal=-3)

    ..  container:: example

        Niente dynamics format like this:

        >>> voice = abjad.Voice("c'4 r r c'4")
        >>> abjad.attach(abjad.Dynamic("p"), voice[0])
        >>> abjad.attach(abjad.Dynamic("niente"), voice[1])
        >>> abjad.attach(abjad.Dynamic("p"), voice[3])
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

    ..  container:: example

        Name-is-textual:

        >>> abjad.Dynamic("f").name_is_textual
        False

        >>> abjad.Dynamic("niente").name_is_textual
        True

        >>> dynamic = abjad.Dynamic("appena udibile", name_is_textual=True)
        >>> dynamic.name_is_textual
        True

        Textual dynamics format like this when initialized without an explicit command:

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> dynamic = abjad.Dynamic("appena udibile", name_is_textual=True)
        >>> abjad.attach(dynamic, voice[0])
        >>> abjad.override(voice).DynamicLineSpanner.staff_padding = 4
        >>> abjad.override(voice).DynamicText.X_extent = "#'(0 . 0)"
        >>> abjad.override(voice).DynamicText.self_alignment_X = abjad.LEFT
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

        Textual dynamics format like this when initialized with an explicit command:

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> dynamic = abjad.Dynamic(
        ...     "appena udibile",
        ...     command=r"\appena_udibile",
        ...     name_is_textual=True,
        ... )
        >>> abjad.attach(dynamic, voice[0])

        Only LilyPond output is shown here because dynamic commands (like
        ``\appena_udibile`` shown here) are meant to be user-defined (and not included in
        Abjad):

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

        REGRESSION. Textual names work with replace:

        >>> import dataclasses
        >>> dynamic = abjad.Dynamic("niente")
        >>> dataclasses.replace(dynamic)
        Dynamic(name='niente', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=NegativeInfinity())

        >>> dynamic = abjad.Dynamic("appena udibile", name_is_textual=True)
        >>> dataclasses.replace(dynamic)
        Dynamic(name='appena udibile', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=None)

    ..  container:: example

        Ordinal value of a dynamic:

        >>> abjad.Dynamic("f").ordinal
        2

        >>> abjad.Dynamic("p").ordinal
        -2

        >>> abjad.Dynamic("niente").ordinal
        NegativeInfinity()

        >>> abjad.Dynamic('"f"').ordinal
        2

        >>> abjad.Dynamic('"p"').ordinal
        -2

        User-defined ordinals:

        >>> barely_audible = abjad.Dynamic(
        ...     "barely audible",
        ...     name_is_textual=True,
        ...     ordinal=-99,
        ... )
        >>> barely_audible.ordinal
        -99

        >>> extremely_loud = abjad.Dynamic(
        ...     "extremely loud",
        ...     name_is_textual=True,
        ...     ordinal=99,
        ... )
        >>> extremely_loud.ordinal
        99

        REGRESSION. Textual names without explicit ordinal return none:

        >>> dynamic = abjad.Dynamic("appena udibile", name_is_textual=True)
        >>> dynamic.ordinal is None
        True

    """

    name: typing.Union[str, "Dynamic"] = "f"
    command: str | None = None
    format_hairpin_stop: bool = False
    hide: bool = False
    leak: bool = dataclasses.field(default=False, compare=False)
    name_is_textual: bool = False
    ordinal: int | _math.Infinity | _math.NegativeInfinity | None = None

    context: typing.ClassVar[str] = "Voice"
    directed: typing.ClassVar[bool] = True
    parameter: typing.ClassVar[str] = "DYNAMIC"
    persistent: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True
    spanner_stop: typing.ClassVar[bool] = True

    def __post_init__(self):
        if self.name is not None:
            assert isinstance(self.name, str | Dynamic), repr(self.name)
        if isinstance(self.name, Dynamic):
            name_ = self.name.name
        elif isinstance(self.name, str):
            name_ = self.name
        if name_ == "niente":
            self.name_is_textual = True
        if not self.name_is_textual:
            for letter in name_.strip('"'):
                if letter not in self._lilypond_dynamic_alphabet:
                    message = f"letter {letter!r} (in {self.name!r}) is not a dynamic."
                    raise Exception(message)
        self.name = name_
        if self.command is not None:
            assert isinstance(self.command, str), repr(self.command)
            assert self.command.startswith("\\"), repr(self.command)
        assert isinstance(self.format_hairpin_stop, bool), repr(
            self.format_hairpin_stop
        )
        assert isinstance(self.hide, bool), repr(self.hide)
        assert isinstance(self.leak, bool), repr(self.leak)
        assert isinstance(self.name_is_textual, bool), repr(self.name_is_textual)
        if self.ordinal is not None:
            assert isinstance(
                self.ordinal, (int, _math.Infinity, _math.NegativeInfinity)
            )
        else:
            stripped_name = None
            if self.name:
                stripped_name = self.name.strip('"')
            if (
                stripped_name
                in self._composite_dynamic_name_to_steady_state_dynamic_name
            ):
                stripped_name = (
                    self._composite_dynamic_name_to_steady_state_dynamic_name[
                        stripped_name
                    ]
                )
            if stripped_name is None:
                ordinal = None
            else:
                assert isinstance(stripped_name, str), repr(stripped_name)
                ordinal_ = self._dynamic_name_to_dynamic_ordinal.get(stripped_name)
                prototype = (int, _math.Infinity, _math.NegativeInfinity, type(None))
                assert isinstance(ordinal_, prototype), repr(ordinal_)
                ordinal = ordinal_
            self.ordinal = ordinal

    _composite_dynamic_name_to_steady_state_dynamic_name: typing.ClassVar = {
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

    _dynamic_name_to_dynamic_ordinal: typing.ClassVar = {
        "ppppp": -6,
        "pppp": -5,
        "ppp": -4,
        "pp": -3,
        "p": -2,
        "niente": _math.NegativeInfinity(),
        "mp": -1,
        "mf": 1,
        "f": 2,
        "ff": 3,
        "fff": 4,
        "ffff": 5,
        "fffff": 6,
    }

    _dynamic_names: typing.ClassVar = (
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

    _dynamic_ordinal_to_dynamic_name: typing.ClassVar = {
        -6: "ppppp",
        -5: "pppp",
        -4: "ppp",
        -3: "pp",
        -2: "p",
        -1: "mp",
        _math.NegativeInfinity(): "niente",
        1: "mf",
        2: "f",
        3: "ff",
        4: "fff",
        5: "ffff",
        6: "fffff",
    }

    _site: typing.ClassVar[str] = "after"

    _lilypond_dynamic_commands: typing.ClassVar = [
        _ for _ in _dynamic_names if not _ == "niente"
    ]

    _lilypond_dynamic_alphabet: typing.ClassVar = "fmprsz"

    _to_width: typing.ClassVar = {
        '"f"': 2,
        '"mf"': 3.5,
        '"mp"': 3.5,
        '"p"': 2,
        "sfz": 2.5,
    }

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` equals dynamic.

        ..  container:: example

            >>> dynamic_1 = abjad.Dynamic("p")
            >>> dynamic_2 = abjad.Dynamic("p")
            >>> dynamic_3 = abjad.Dynamic("f")

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

    def _attachment_test_all(self, component_expression):
        if not hasattr(component_expression, "written_duration"):
            strings = [f"Must be leaf (not {component_expression})."]
            return strings
        return True

    def _format_effort_dynamic(self, *, wrapper=None):
        name = self.name.strip('"')
        before = {"f": -0.4, "m": -0.1, "p": -0.1, "r": -0.1, "s": -0.3, "z": -0.2}[
            name[0]
        ]
        after = {"f": -0.2, "m": -0.1, "p": -0.25, "r": 0, "s": 0, "z": -0.2}[name[-1]]
        # direction = self.direction
        direction = wrapper.direction or _enums.DOWN
        direction = _string.to_tridirectional_lilypond_symbol(direction)
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
    # def _format_textual(direction, string):
    def _format_textual(string, *, wrapper=None):
        if wrapper.direction is None:
            direction = _enums.DOWN
        direction = _string.to_tridirectional_lilypond_symbol(direction)
        assert isinstance(string, str), repr(string)
        string = f'(markup #:whiteout #:normal-text #:italic "{string}")'
        string = f"{direction} #(make-dynamic-script {string})"
        return string

    def _get_lilypond_format(self, *, wrapper=None):
        if self.command:
            string = self.command
        elif self.effort:
            string = self._format_effort_dynamic(wrapper=wrapper)
        elif self.name_is_textual:
            string = self._format_textual(self.name, wrapper=wrapper)
        else:
            string = rf"\{self.name}"
            if wrapper.direction is not None:
                direction_ = wrapper.direction
                direction = _string.to_tridirectional_lilypond_symbol(direction_)
                string = f"{direction} {string}"
        return string

    def _get_contributions(self, *, component=None, wrapper=None):
        contributions = _contributions.ContributionsBySite()
        command = self._get_lilypond_format(wrapper=wrapper)
        if self.leak:
            contributions.after.leak.append(_EMPTY_CHORD)
            if not self.hide:
                contributions.after.leaks.append(command)
        else:
            if not self.hide:
                contributions.after.articulations.append(command)
        return contributions

    # TODO: make markup function and shorten docstring
    @property
    def effort(self) -> bool:
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
        assert isinstance(self.name, str), repr(self.name)
        return bool(self.name) and self.name[0] == '"'

    @property
    def sforzando(self) -> bool:
        """
        Is true when dynamic name begins in s- and ends in -z.

        ..  container:: example

            >>> abjad.Dynamic("f").sforzando
            False

            >>> abjad.Dynamic("sfz").sforzando
            True

            >>> abjad.Dynamic("sffz").sforzando
            True

            >>> abjad.Dynamic("sfp").sforzando
            False

            >>> abjad.Dynamic("sf").sforzando
            False

            >>> abjad.Dynamic("rfz").sforzando
            False

        """
        assert isinstance(self.name, str), repr(self.name)
        if self.name and self.name.startswith("s") and self.name.endswith("z"):
            return True
        return False

    # TODO: make module-level function
    @staticmethod
    def composite_dynamic_name_to_steady_state_dynamic_name(name) -> str:
        """
        Changes composite ``name`` to steady state dynamic name.

        ..  container:: example

            >>> abjad.Dynamic.composite_dynamic_name_to_steady_state_dynamic_name("sfp")
            'p'

            >>> abjad.Dynamic.composite_dynamic_name_to_steady_state_dynamic_name("rfz")
            'f'

        """
        return Dynamic._composite_dynamic_name_to_steady_state_dynamic_name[name]

    # TODO: make module-level function
    @staticmethod
    def dynamic_name_to_dynamic_ordinal(name):
        """
        Changes ``name`` to dynamic ordinal.

        ..  container:: example

            >>> abjad.Dynamic.dynamic_name_to_dynamic_ordinal("fff")
            4

            >>> abjad.Dynamic.dynamic_name_to_dynamic_ordinal("niente")
            NegativeInfinity()

        """
        try:
            return Dynamic._dynamic_name_to_dynamic_ordinal[name]
        except KeyError:
            name = Dynamic.composite_dynamic_name_to_steady_state_dynamic_name(name)
            return Dynamic._dynamic_name_to_dynamic_ordinal[name]

    # TODO: make module-level function
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
        if dynamic_ordinal == _math.NegativeInfinity():
            return "niente"
        else:
            return Dynamic._dynamic_ordinal_to_dynamic_name[dynamic_ordinal]

    # TODO: make module-level function
    @staticmethod
    def is_dynamic_name(argument) -> bool:
        """
        Is true when ``argument`` is dynamic name.

        ..  container:: example

            >>> abjad.Dynamic.is_dynamic_name("f")
            True

            >>> abjad.Dynamic.is_dynamic_name("sfz")
            True

            >>> abjad.Dynamic.is_dynamic_name("niente")
            True

        """
        return argument in Dynamic._dynamic_names
