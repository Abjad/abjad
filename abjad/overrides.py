import copy
import typing

from . import enums
from . import tag as _tag
from .bundle import LilyPondFormatBundle
from .fsv import format_scheme_value
from .lyenv import contexts, grob_interfaces
from .storage import FormatSpecification, StorageFormatManager
from .string import String


def format_embedded_scheme_value(value):
    result = format_scheme_value(value)
    if isinstance(value, bool):
        result = "#" + result
    return result


def format_lilypond_attribute(attribute) -> str:
    assert isinstance(attribute, str), repr(attribute)
    attribute = attribute.replace("__", ".")
    result = attribute.replace("_", "-")
    return result


lilypond_color_constants = (
    "black",
    "blue",
    "center",
    "cyan",
    "darkblue",
    "darkcyan",
    "darkgreen",
    "darkmagenta",
    "darkred",
    "darkyellow",
    "down",
    "green",
    "grey",
    "left",
    "magenta",
    "red",
    "right",
    "up",
    "white",
    "yellow",
)


def format_lilypond_value(argument) -> str:
    if "_get_lilypond_format" in dir(argument):
        return argument._get_lilypond_format()
    if argument is True:
        return "##t"
    if argument is False:
        return "##f"
    if argument in (
        enums.Up,
        enums.Down,
        enums.Left,
        enums.Right,
        enums.Center,
    ):
        return rf"#{repr(argument).lower()}"
    if argument in lilypond_color_constants:
        return rf"#{argument}"
    if isinstance(argument, tuple) and len(argument) == 2:
        return f"#'({argument[0]} . {argument[1]})"
    return str(argument)


def make_lilypond_override_string(
    grob, attribute, value, context=None, once=False
) -> str:
    # camel_name = String(grob).to_upper_camel_case()
    # assert grob == camel_name, repr((grob, camel_name))
    grob = String(grob).to_upper_camel_case()
    attribute = format_lilypond_attribute(attribute)
    value = format_lilypond_value(value)
    if context is not None:
        context = String(context).capitalize_start() + "."
    else:
        context = ""
    if once is True:
        once = r"\once "
    else:
        once = ""
    result = rf"{once}\override {context}{grob}.{attribute} = {value}"
    return result


def make_lilypond_revert_string(grob, attribute, context=None) -> str:
    # camel_name = String(grob).to_upper_camel_case()
    # assert grob == camel_name, repr((grob, camel_name))
    grob = String(grob).to_upper_camel_case()
    dotted = format_lilypond_attribute(attribute)
    if context is not None:
        # camel_name = String(context).to_upper_camel_case()
        # assert context == camel_name, repr((context, camel_name))
        context = String(context).to_upper_camel_case()
        context += "."
    else:
        context = ""
    result = rf"\revert {context}{grob}.{dotted}"
    return result


def make_lilypond_tweak_string(
    attribute, value, *, directed=True, grob=None, literal=None
) -> str:
    if grob is not None:
        # camel_name = String(grob).to_upper_camel_case()
        # assert grob == camel_name, repr((grob, camel_name))
        grob = String(grob).to_upper_camel_case()
        grob += "."
    else:
        grob = ""
    attribute = format_lilypond_attribute(attribute)
    if not literal:
        value = format_lilypond_value(value)
    string = rf"\tweak {grob}{attribute} {value}"
    if directed:
        string = "- " + string
    return string


class LilyPondLiteral:
    r"""
    LilyPond literal.

    ..  container:: example

        Dotted slur:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.slur(staff[:])
        >>> literal = abjad.LilyPondLiteral(r"\slurDotted")
        >>> abjad.attach(literal, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \slurDotted
                c'8
                (
                d'8
                e'8
                f'8
                )
            }

    ..  container:: example

        Use the absolute before and absolute after format slots like this:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.slur(staff[:])
        >>> literal = abjad.LilyPondLiteral(r"\slurDotted")
        >>> abjad.attach(literal, staff[0])
        >>> literal = abjad.LilyPondLiteral("", format_slot="absolute_before")
        >>> abjad.attach(literal, staff[0])
        >>> literal = abjad.LilyPondLiteral(
        ...     "% before all formatting",
        ...     format_slot="absolute_before",
        ...     )
        >>> abjad.attach(literal, staff[0])
        >>> literal = abjad.LilyPondLiteral("", format_slot="absolute_after")
        >>> abjad.attach(literal, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
            <BLANKLINE>
                % before all formatting
                \slurDotted
                c'8
                (
                d'8
                e'8
                f'8
                )
            <BLANKLINE>
            }

    ..  container:: example

        LilyPond literals can be tagged:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.slur(staff[:])
        >>> literal = abjad.LilyPondLiteral(r"\slurDotted")
        >>> abjad.attach(literal, staff[0], tag=abjad.Tag("+PARTS"))
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
        \new Staff
        {
            \slurDotted %! +PARTS
            c'8
            (
            d'8
            e'8
            f'8
            )
        }

    ..  container:: example

        Multiline input is allowed:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.slur(staff[:])
        >>> lines = [
        ...     r"\stopStaff",
        ...     r"\startStaff",
        ...     r"\once \override Staff.StaffSymbol.color = #red",
        ...     ]
        >>> literal = abjad.LilyPondLiteral(lines)
        >>> abjad.attach(literal, staff[2], tag=abjad.Tag("+PARTS"))
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
        \new Staff
        {
            c'8
            (
            d'8
            \stopStaff %! +PARTS
            \startStaff %! +PARTS
            \once \override Staff.StaffSymbol.color = #red %! +PARTS
            e'8
            f'8
            )
        }

    ..  container:: example

        REGRESSION. Duplicate literals are allowed:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> literal = abjad.LilyPondLiteral("% text")
        >>> abjad.attach(literal, staff[0])
        >>> literal = abjad.LilyPondLiteral("% text")
        >>> abjad.attach(literal, staff[0])

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        {
            % text
            % text
            c'4
            d'4
            e'4
            f'4
        }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_argument", "_directed", "_format_slot", "_tweaks")

    _allowable_format_slots = (
        "absolute_after",
        "absolute_before",
        "after",
        "before",
        "closing",
        "opening",
    )

    _can_attach_to_containers = True

    _format_leaf_children = False

    ### INITIALIZER ###

    def __init__(
        self,
        argument: typing.Union[str, typing.List[str]] = "",
        # TODO: probaby change default to "before"
        format_slot: str = "opening",
        *,
        directed: bool = None,
        tweaks: "TweakInterface" = None,
    ) -> None:
        self._argument = argument
        assert format_slot in self._allowable_format_slots, repr(format_slot)
        self._format_slot = format_slot
        if directed is not None:
            directed = bool(directed)
        self._directed = directed
        if tweaks is not None:
            assert isinstance(tweaks, TweakInterface), repr(tweaks)
        self._tweaks = TweakInterface.set_tweaks(self, tweaks)

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

    ### PRIVATE METHODS ###

    # TODO: activate this:
    #    def _before_attach(self, component):
    #        if self.format_slot not in component._allowable_format_slots:
    #            message = f"{type(component).__name__} does not accept"
    #            message += f" format slot {repr(self.format_slot)}."
    #            raise Exception(message)

    def _get_format_pieces(self):
        if isinstance(self.argument, str):
            return [self.argument]
        assert isinstance(self.argument, list)
        return self.argument[:]

    def _get_format_specification(self):
        return FormatSpecification(
            client=self,
            storage_format_args_values=[self.argument],
            storage_format_is_indented=False,
        )

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        format_slot = bundle.get(self.format_slot)
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions(directed=self.directed)
            format_slot.commands.extend(tweaks)
        pieces = self._get_format_pieces()
        format_slot.commands.extend(pieces)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def argument(self) -> typing.Union[str, typing.List[str]]:
        r"""
        Gets argument of LilyPond literal.

        ..  container:: example

            >>> literal = abjad.LilyPondLiteral(r"\slurDotted")
            >>> literal.argument
            '\\slurDotted'

        """
        return self._argument

    @property
    def directed(self) -> typing.Optional[bool]:
        r"""
        Is true when literal is directed.

        ..  container:: example

            Directed literal:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> literal = abjad.LilyPondLiteral(r"\f", "after", directed=True)
            >>> abjad.tweak(literal).color = "#blue"
            >>> abjad.tweak(literal).DynamicLineSpanner.staff_padding = 5
            >>> abjad.attach(literal, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \tweak DynamicLineSpanner.staff-padding 5
                    - \tweak color #blue
                    \f
                    d'4
                    e'4
                    f'4
                }

        ..  container:: example

            Nondirected literal:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> literal = abjad.LilyPondLiteral(
            ...     r"\breathe",
            ...     "after",
            ...     directed=False,
            ...     )
            >>> abjad.tweak(literal).color = "#blue"
            >>> abjad.attach(literal, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    \tweak color #blue
                    \breathe
                    d'4
                    e'4
                    f'4
                }

        Proper use of the ``directed`` property entails searching the LilyPond
        docs to understand whether LilyPond treats any particular command as
        directed or not. Most LilyPond commands are directed. LilyPond insists
        that a few commands (include ``\breathe``, ``\key``, ``\mark``) must
        not be directed.
        """
        return self._directed

    @property
    def format_slot(self) -> str:
        r"""
        Gets format slot of LilyPond literal.

        ..  container:: example

            >>> literal = abjad.LilyPondLiteral(r"\slurDotted")
            >>> literal.format_slot
            'opening'

        """
        return self._format_slot

    @property
    def tweaks(self) -> typing.Optional["TweakInterface"]:
        r"""
        Gets tweaks.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> literal = abjad.LilyPondLiteral(r"\f", "after", directed=True)
            >>> abjad.tweak(literal).color = "#blue"
            >>> abjad.attach(literal, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    \f
                    d'4
                    e'4
                    f'4
                }

        """
        return self._tweaks


class Interface:
    """
    LilyPond name manager.

    Base class from which grob, setting and tweak managers inherit.
    """

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a LilyPond name manager with attribute
        pairs equal to those of this LilyPond name manager.

        ..  container:: example

            >>> note_1 = abjad.Note("c'4")
            >>> abjad.setting(note_1).Voice.auto_beaming = False
            >>> abjad.setting(note_1).Staff.tupletFullLength = True

            >>> note_2 = abjad.Note("c'4")
            >>> abjad.setting(note_2).Voice.auto_beaming = False
            >>> abjad.setting(note_2).Staff.tupletFullLength = True

            >>> note_3 = abjad.Note("c'4")
            >>> abjad.setting(note_3).Voice.auto_beaming = True

            >>> setting_1 = abjad.setting(note_1)
            >>> setting_2 = abjad.setting(note_2)
            >>> setting_3 = abjad.setting(note_3)

            >>> setting_1 == setting_1
            True
            >>> setting_1 == setting_2
            True
            >>> setting_1 == setting_3
            False

            >>> setting_2 == setting_1
            True
            >>> setting_2 == setting_2
            True
            >>> setting_2 == setting_3
            False

            >>> setting_3 == setting_1
            False
            >>> setting_3 == setting_2
            False
            >>> setting_3 == setting_3
            True

        ..  container:: example

            >>> note_1 = abjad.Note("c'4")
            >>> abjad.override(note_1).NoteHead.color = "#red"
            >>> abjad.override(note_1).Stem.color = "#red"

            >>> note_2 = abjad.Note("c'4")
            >>> abjad.override(note_2).NoteHead.color = "#red"
            >>> abjad.override(note_2).Stem.color = "#red"

            >>> note_3 = abjad.Note("c'4")
            >>> abjad.override(note_3).NoteHead.color = "#red"

            >>> override_1 = abjad.override(note_1)
            >>> override_2 = abjad.override(note_2)
            >>> override_3 = abjad.override(note_3)

            >>> override_1 == override_1
            True
            >>> override_1 == override_2
            True
            >>> override_1 == override_3
            False

            >>> override_2 == override_1
            True
            >>> override_2 == override_2
            True
            >>> override_2 == override_3
            False

            >>> override_3 == override_1
            False
            >>> override_3 == override_2
            False
            >>> override_3 == override_3
            True

        """
        if isinstance(argument, type(self)):
            attribute_pairs_1 = self._get_attribute_pairs()
            attribute_pairs_2 = argument._get_attribute_pairs()
            return attribute_pairs_1 == attribute_pairs_2
        return False

    def __getstate__(self) -> dict:
        """
        Gets object state.
        """
        return copy.deepcopy(vars(self))

    def __hash__(self) -> int:
        """
        Hashes LilyPond name manager.

        Redefined in tandem with __eq__.
        """
        return super().__hash__()

    def __repr__(self) -> str:
        """
        Gets interpreter representation of LilyPond name manager.
        """
        body_string = ""
        pairs = self._get_attribute_pairs()
        pairs = [str(_) for _ in pairs]
        body_string = ", ".join(pairs)
        return f"{type(self).__name__}({body_string})"

    def __setstate__(self, state) -> None:
        """
        Sets object state.
        """
        for key, value in state.items():
            self.__dict__[key] = value

    ### PRIVATE METHODS ###

    def _get_attribute_pairs(self):
        return list(sorted(vars(self).items()))


class LilyPondOverride:
    r"""
    LilyPond grob override.

    ..  container:: example

        >>> override = abjad.LilyPondOverride(
        ...    lilypond_type="Staff",
        ...    grob_name="TextSpanner",
        ...    once=True,
        ...    property_path=(
        ...        "bound-details",
        ...        "left",
        ...        "text",
        ...        ),
        ...    value=abjad.Markup(r"\bold { over pressure }"),
        ...    )

        >>> print(override.override_string)
        \once \override Staff.TextSpanner.bound-details.left.text = \markup {
            \bold
                {
                    over
                    pressure
                }
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_grob_name",
        "_is_revert",
        "_lilypond_type",
        "_once",
        "_property_path",
        "_value",
    )

    _format_leaf_children = False

    ### INITIALIZER ###

    def __init__(
        self,
        lilypond_type: str = None,
        grob_name: str = "NoteHead",
        once: bool = None,
        is_revert: bool = None,
        property_path: typing.Union[str, typing.Iterable[str]] = "color",
        value: typing.Any = "#red",
    ) -> None:
        if lilypond_type is not None:
            lilypond_type = str(lilypond_type)
        self._lilypond_type = lilypond_type
        assert grob_name
        self._grob_name = str(grob_name)
        if once is not None:
            once = bool(once)
        self._once = once
        if is_revert is not None:
            is_revert = bool(is_revert)
        self._is_revert = is_revert
        if isinstance(property_path, str):
            property_path_: typing.Tuple[str, ...] = (property_path,)
        else:
            property_path_ = tuple(property_path)
        assert isinstance(property_path_, tuple), repr(property_path_)
        assert all(isinstance(_, str) for _ in property_path_)
        assert all(_ != "" for _ in property_path_)
        self._property_path = property_path_
        self._value = value

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a LilyPond grob override with equivalent
        keyword values.
        """
        return super().__eq__(argument)

    def __hash__(self) -> int:
        """
        Hashes LilyPond grob override.

        Redefined in tandem with __eq__.
        """
        return super().__hash__()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if not self.once:
            revert_format = "\n".join(self.revert_format_pieces)
            bundle.grob_reverts.append(revert_format)
        if not self.is_revert:
            override_format = "\n".join(self.override_format_pieces)
            bundle.grob_overrides.append(override_format)
        return bundle

    def _override_property_path_string(self):
        parts = []
        if self.lilypond_type is not None:
            parts.append(self.lilypond_type)
        parts.append(self.grob_name)
        parts.extend(self.property_path)
        path = ".".join(parts)
        return path

    def _revert_property_path_string(self):
        parts = []
        if self.lilypond_type is not None:
            parts.append(self.lilypond_type)
        parts.append(self.grob_name)
        parts.append(self.property_path[0])
        path = ".".join(parts)
        return path

    ### PUBLIC PROPERTIES ###

    @property
    def grob_name(self) -> str:
        r"""
        Gets grob name.

        ..  container:: example

            >>> override = abjad.LilyPondOverride(
            ...     grob_name="Glissando",
            ...     property_path="style",
            ...     value="#'zigzag",
            ...     )
            >>> override.grob_name
            'Glissando'

        """
        return self._grob_name

    @property
    def is_revert(self) -> typing.Optional[bool]:
        r"""
        Is true if grob override is a grob revert.

        ..  container:: example

            >>> override = abjad.LilyPondOverride(
            ...     grob_name="Glissando",
            ...     property_path="style",
            ...     value="#'zigzag",
            ...     )
            >>> bool(override.is_revert)
            False

            >>> override = abjad.LilyPondOverride(
            ...     grob_name="Glissando",
            ...     is_revert=True,
            ...     property_path="style",
            ...     )
            >>> bool(override.is_revert)
            True

        """
        return self._is_revert

    @property
    def lilypond_type(self) -> typing.Optional[str]:
        r"""
        Gets LilyPond type of context.

        ..  container:: example

            >>> override = abjad.LilyPondOverride(
            ...    lilypond_type="Staff",
            ...    grob_name="TextSpanner",
            ...    once=True,
            ...    property_path=(
            ...        "bound-details",
            ...        "left",
            ...        "text",
            ...        ),
            ...    value=abjad.Markup(r"\bold { over pressure }"),
            ...    )
            >>> override.lilypond_type
            'Staff'

            >>> override = abjad.LilyPondOverride(
            ...     grob_name="Glissando",
            ...     property_path="style",
            ...     value="#'zigzag",
            ...     )
            >>> override.lilypond_type is None
            True

        """
        return self._lilypond_type

    @property
    def once(self) -> typing.Optional[bool]:
        r"""
        Is true when grob override is to be applied only once.

        ..  container:: example

            >>> override = abjad.LilyPondOverride(
            ...    lilypond_type="Staff",
            ...    grob_name="TextSpanner",
            ...    once=True,
            ...    property_path=(
            ...        "bound-details",
            ...        "left",
            ...        "text",
            ...        ),
            ...    value=abjad.Markup(r"\bold { over pressure }"),
            ...    )
            >>> bool(override.once)
            True

            >>> override = abjad.LilyPondOverride(
            ...     grob_name="Glissando",
            ...     property_path="style",
            ...     value="#'zigzag",
            ...     )
            >>> bool(override.once)
            False

        """
        return self._once

    @property
    def override_format_pieces(self) -> typing.Tuple[str, ...]:
        r"""
        Gets LilyPond grob override \override format pieces.

        ..  container:: example

            >>> override = abjad.LilyPondOverride(
            ...    lilypond_type="Staff",
            ...    grob_name="TextSpanner",
            ...    once=True,
            ...    property_path=(
            ...        "bound-details",
            ...        "left",
            ...        "text",
            ...        ),
            ...    value=abjad.Markup(r"\bold { over pressure }"),
            ...    )
            >>> for line in override.override_format_pieces:
            ...     line
            ...
            '\\once \\override Staff.TextSpanner.bound-details.left.text = \\markup {'
            '    \\bold'
            '        {'
            '            over'
            '            pressure'
            '        }'
            '    }'

        """
        result = []
        if self.once:
            result.append(r"\once")
        result.append(r"\override")
        result.append(self._override_property_path_string())
        result.append("=")
        string = format_embedded_scheme_value(self.value)
        # string = str(self.value)
        value_pieces = string.split("\n")
        result.append(value_pieces[0])
        result[:] = [" ".join(result)]
        result.extend(value_pieces[1:])
        return tuple(result)

    @property
    def override_string(self) -> str:
        r"""
        Gets LilyPond grob override \override string.

        ..  container:: example

            >>> override = abjad.LilyPondOverride(
            ...     grob_name="Glissando",
            ...     property_path="style",
            ...     value="#'zigzag",
            ...     )
            >>> override.override_string
            "\\override Glissando.style = #'zigzag"

        """
        return "\n".join(self.override_format_pieces)

    @property
    def property_path(self) -> typing.Tuple[str, ...]:
        r"""
        Gets LilyPond grob override property path.

        ..  container:: example

            >>> override = abjad.LilyPondOverride(
            ...    lilypond_type="Staff",
            ...    grob_name="TextSpanner",
            ...    once=True,
            ...    property_path=(
            ...        "bound-details",
            ...        "left",
            ...        "text",
            ...        ),
            ...    value=abjad.Markup(r"\bold { over pressure }"),
            ...    )
            >>> override.property_path
            ('bound-details', 'left', 'text')

        """
        return self._property_path

    @property
    def revert_format_pieces(self) -> typing.Tuple[str, ...]:
        r"""
        Gets LilyPond grob override \revert format pieces.

        ..  container:: example

            >>> override = abjad.LilyPondOverride(
            ...     grob_name="Glissando",
            ...     property_path="style",
            ...     value="#'zigzag",
            ...     )
            >>> override.revert_format_pieces
            ('\\revert Glissando.style',)

        """
        result = rf"\revert {self._revert_property_path_string()}"
        return (result,)

    @property
    def revert_string(self) -> str:
        r"""
        Gets LilyPond grob override \revert string.

        ..  container:: example

            >>> override = abjad.LilyPondOverride(
            ...     grob_name="Glissando",
            ...     property_path="style",
            ...     value="#'zigzag",
            ...     )
            >>> override.revert_string
            '\\revert Glissando.style'

        """
        return "\n".join(self.revert_format_pieces)

    @property
    def value(self) -> typing.Any:
        r"""
        Gets value of LilyPond grob override.

        ..  container:: example

            >>> override = abjad.LilyPondOverride(
            ...    lilypond_type="Staff",
            ...    grob_name="TextSpanner",
            ...    once=True,
            ...    property_path=(
            ...        "bound-details",
            ...        "left",
            ...        "text",
            ...        ),
            ...    value=abjad.Markup(r"\markup \bold { over pressure }", literal=True),
            ...    )
            >>> override.value
            Markup(contents=['\\markup \\bold { over pressure }'], literal=True)

        """
        return self._value

    ### PUBLIC METHODS ###

    def tweak_string(self, directed=True, grob=False) -> str:
        r"""
        Gets LilyPond grob override \tweak string.

        ..  container:: example

            >>> override = abjad.LilyPondOverride(
            ...     grob_name="Glissando",
            ...     property_path="style",
            ...     value="#'zigzag",
            ...     )
            >>> override.tweak_string()
            "- \\tweak style #'zigzag"

        ..  container:: example

            >>> override = abjad.LilyPondOverride(
            ...     grob_name="RehearsalMark",
            ...     property_path="color",
            ...     value="#red",
            ...     )
            >>> override.tweak_string(directed=False)
            '\\tweak color #red'

        ..  container:: example

            LilyPond literals are allowed:

            >>> override = abjad.LilyPondOverride(
            ...     grob_name="TextSpann",
            ...     property_path=("bound-details", "left-broken", "text"),
            ...     value=abjad.LilyPondLiteral(r"\markup \upright pont."),
            ...     )
            >>> override.tweak_string(directed=False)
            '\\tweak bound-details.left-broken.text \\markup \\upright pont.'

        """
        if directed:
            result = [r"- \tweak"]
        else:
            result = [r"\tweak"]
        if grob:
            property_path = (self.grob_name,) + self.property_path
        else:
            property_path = self.property_path
        string = ".".join(property_path)
        result.append(string)
        if isinstance(self.value, LilyPondLiteral):
            assert isinstance(self.value.argument, str)
            string = self.value.argument
        else:
            string = format_embedded_scheme_value(self.value)
            # string = str(self.value)
        result.append(string)
        return " ".join(result)


class LilyPondSetting:
    r"""
    LilyPond context setting.

    ..  container:: example

        >>> context_setting = abjad.LilyPondSetting(
        ...    lilypond_type="Score",
        ...    context_property="autoBeaming",
        ...    value="##f",
        ...    )

        >>> print("\n".join(context_setting.format_pieces))
        \set Score.autoBeaming = ##f

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_context_property", "_lilypond_type", "_is_unset", "_value")

    _format_leaf_children = False

    ### INITIALIZER ###

    def __init__(
        self,
        lilypond_type: str = None,
        context_property: str = "autoBeaming",
        is_unset: bool = False,
        value: typing.Any = False,
    ) -> None:
        if lilypond_type is not None:
            lilypond_type = str(lilypond_type)
        self._lilypond_type = lilypond_type
        assert isinstance(context_property, str) and context_property
        self._context_property = context_property
        if is_unset is not None:
            is_unset = bool(is_unset)
        self._is_unset = is_unset
        self._value = value

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a LilyPond context setting with
        equivalent keyword values.
        """
        return super().__eq__(argument)

    def __hash__(self) -> int:
        """
        Hashes LilyPond context setting.

        Redefined in tandem with __eq__.
        """
        return super().__hash__()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        string = "\n".join(self.format_pieces)
        bundle.context_settings.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context_property(self) -> str:
        """
        Gets LilyPond context property name.
        """
        return self._context_property

    @property
    def format_pieces(self) -> typing.Tuple[str, ...]:
        r"""
        Gets LilyPond context setting ``\set`` or ``\unset`` format pieces.
        """
        result = []
        if not self.is_unset:
            result.append(r"\set")
        else:
            result.append(r"\unset")
        if self.lilypond_type is not None:
            string = f"{self.lilypond_type}.{self.context_property}"
            result.append(string)
        else:
            result.append(self.context_property)
        result.append("=")
        string = format_embedded_scheme_value(self.value)
        # assert string == str(self.value), repr((str(self.value), string))
        value_pieces = string.split("\n")
        result.append(value_pieces[0])
        result[:] = [" ".join(result)]
        result.extend(value_pieces[1:])
        return tuple(result)

    @property
    def is_unset(self) -> typing.Optional[bool]:
        """
        Is true if context setting unsets its value.
        """
        return self._is_unset

    @property
    def lilypond_type(self) -> typing.Optional[str]:
        """
        Gets LilyPond type.
        """
        return self._lilypond_type

    @property
    def value(self) -> typing.Any:
        """
        Gets value of LilyPond context setting.
        """
        return self._value


class OverrideInterface(Interface):
    """
    LilyPond grob name manager.

    ..  container:: example

        OverrideInterface instances are created by the
        ``abjad.override()`` factory function:

        >>> note = abjad.Note("c'4")
        >>> abjad.override(note)
        OverrideInterface()

    """

    ### SPECIAL METHODS ###

    def __getattr__(self, name) -> typing.Union[Interface, "OverrideInterface"]:
        r"""
        Gets Interface (or OverrideInterface) keyed to ``name``.

        ..  container:: example

            Somewhat confusingly, getting a grob name returns a
            Interface:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.override(staff[0]).NoteHead
            Interface()

            While getting a context name returns an override interface:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.override(staff[0]).Staff
            OverrideInterface()

            Which can then be deferenced to get an interface:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.override(staff[0]).Staff.NoteHead
            Interface()

        Note that the dot-chained user syntax is unproblematic. But the class of each
        manager returned in the chain is likely to be surprising at first encounter.
        """
        camel_name = String(name).to_upper_camel_case()
        # assert name == camel_name, repr((name, camel_name))
        if name.startswith("_"):
            try:
                return vars(self)[name]
            except KeyError:
                type_name = type(self).__name__
                raise AttributeError("{type_name!r} object has no attribute: {name!r}.")
        elif camel_name in contexts:
            try:
                return vars(self)["_" + name]
            except KeyError:
                context = OverrideInterface()
                vars(self)["_" + name] = context
                return context
        elif camel_name in grob_interfaces:
            try:
                return vars(self)[name]
            except KeyError:
                vars(self)[name] = Interface()
                return vars(self)[name]
        else:
            try:
                return vars(self)[name]
            except KeyError:
                type_name = type(self).__name__
                raise AttributeError(
                    f"{type_name!r} object has no attribute: {name!r}."
                )

    def __setattr__(self, attribute, value) -> None:
        """
        Sets attribute ``attribute`` of grob name manager to ``value``.
        """
        object.__setattr__(self, attribute, value)

    ### PRIVATE METHODS ###

    def _get_attribute_tuples(self):
        result = []
        for name, value in vars(self).items():
            if type(value) is Interface:
                grob, grob_proxy = name, value
                pairs = iter(vars(grob_proxy).items())
                for attribute, value in pairs:
                    triple = (grob, attribute, value)
                    result.append(triple)
            else:
                context, context_proxy = name.strip("_"), value
                for grob, grob_proxy in vars(context_proxy).items():
                    pairs = iter(vars(grob_proxy).items())
                    for attribute, value in pairs:
                        quadruple = (context, grob, attribute, value)
                        result.append(quadruple)
        return tuple(result)

    def _list_format_contributions(self, contribution_type, once=False):
        assert contribution_type in ("override", "revert")
        result = []
        for attribute_tuple in self._get_attribute_tuples():
            if len(attribute_tuple) == 3:
                context = None
                grob = attribute_tuple[0]
                attribute = attribute_tuple[1]
                value = attribute_tuple[2]
            elif len(attribute_tuple) == 4:
                context = attribute_tuple[0]
                grob = attribute_tuple[1]
                attribute = attribute_tuple[2]
                value = attribute_tuple[3]
            else:
                raise ValueError(f"invalid attribute tuple: {attribute_tuple!r}.")
            if contribution_type == "override":
                override_string = make_lilypond_override_string(
                    grob, attribute, value, context=context, once=once
                )
                result.append(override_string)
            else:
                revert_string = make_lilypond_revert_string(
                    grob, attribute, context=context
                )
                result.append(revert_string)
        result.sort()
        return result


### FUNCTIONS ###


def override(argument):
    r"""
    Makes LilyPond grob name manager.

    ..  container:: example

        Overrides staff symbol color:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.override(staff).StaffSymbol.color = "#red"
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override StaffSymbol.color = #red
            }
            {
                c'4
                e'4
                d'4
                f'4
            }

    ..  container:: example

        Specify grob context like this:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.override(staff[0]).Staff.StaffSymbol.color = "#blue"
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \once \override Staff.StaffSymbol.color = #blue
                c'4
                e'4
                d'4
                f'4
            }

    ..  container:: example

        Returns LilyPond grob name manager:

        >>> staff = abjad.Staff("c'4 e' d' f'")
        >>> abjad.override(staff)
        OverrideInterface()

    """
    if getattr(argument, "_overrides", None) is None:
        argument._overrides = OverrideInterface()
    return argument._overrides


class SettingInterface(Interface):
    """
    LilyPond setting name manager.

    ..  container:: example

        >>> note = abjad.Note("c'4")
        >>> abjad.setting(note)
        SettingInterface()

    """

    ### SPECIAL METHODS ###

    def __getattr__(self, name: str) -> typing.Any:
        r"""
        Gets arbitrary object keyed to ``name``.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.setting(staff).instrumentName = abjad.Markup("Vn. I")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    instrumentName = \markup { Vn. I }
                }
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }

        ..  container:: example

            Returns arbitrary object keyed to ``name``:

            >>> abjad.setting(staff).instrumentName
            Markup(contents=['Vn. I'])

        """
        camel_name = String(name).to_upper_camel_case()
        # assert name == camel_name, repr((name, camel_name))
        if name.startswith("_"):
            try:
                return vars(self)[name]
            except KeyError:
                message = "{type(self).__name__!r} object has no attribute: {name!r}."
                raise AttributeError(message)
        elif camel_name in contexts:
            try:
                return vars(self)["_" + name]
            except KeyError:
                context = Interface()
                vars(self)["_" + name] = context
                return context
        else:
            try:
                return vars(self)[name]
            except KeyError:
                message = "{type(self).__name__!r} object has no attribute: {name!r}."
                raise AttributeError(message)

    ### PRIVATE METHODS ###

    def _format_in_with_block(self) -> typing.List[str]:
        strings = []
        for key, value in vars(self).items():
            assert isinstance(key, str), repr(key)
            name = key.split("_")
            first = name[0:1]
            rest = name[1:]
            rest = [x.title() for x in rest]
            name = first + rest
            string = "".join(name)
            # assert key == string, repr((key, string))
            value = format_lilypond_value(value)
            value_parts = value.split("\n")
            result = rf"{string!s} = {value_parts[0]!s}"
            pieces = [result]
            for part in value_parts[1:]:
                pieces.append(LilyPondFormatBundle.indent + part)
            string = "\n".join(pieces)
            strings.append(string)
        return strings

    def _format_inline(self, context=None) -> typing.List[str]:
        result = []
        for name, value in vars(self).items():
            # if we've found a leaf context namespace
            if name.startswith("_"):
                for x, y in vars(value).items():
                    if not x.startswith("_"):
                        string = self._format_inline_helper(x, y, name)
                        result.append(string)
            # otherwise we've found a default leaf context setting
            else:
                # parse default context setting
                string = self._format_inline_helper(name, value)
                result.append(string)
        return result

    def _format_inline_helper(self, name, value, context=None):
        name = name.split("_")
        first = name[0:1]
        rest = name[1:]
        rest = [x.title() for x in rest]
        name = first + rest
        name = "".join(name)
        value = format_lilypond_value(value)
        if context is not None:
            context_string = context[1:]
            context_string = context_string.split("_")
            context_string = [x.title() for x in context_string]
            context_string = "".join(context_string)
            context_string += "."
        else:
            context_string = ""
        result = rf"\set {context_string}{name} = {value}"
        return result

    def _get_attribute_tuples(self):
        result = []
        for name, value in vars(self).items():
            if type(value) is Interface:
                prefixed_context_name = name
                lilypond_type = prefixed_context_name.strip("_")
                context_proxy = value
                attribute_pairs = context_proxy._get_attribute_pairs()
                for attribute_name, attribute_value in attribute_pairs:
                    triple = (lilypond_type, attribute_name, attribute_value)
                    result.append(triple)
            else:
                attribute_name, attribute_value = name, value
                result.append((attribute_name, attribute_value))
        return result


### FUNCTIONS ###


def setting(argument):
    r"""
    Makes LilyPond setting name manager.

    ..  container:: example

        Sets instrument name:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.setting(staff).instrumentName = abjad.Markup("Vn. I")
        >>> abjad.show(staff) # doctest: +SKIP


        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                instrumentName = \markup { Vn. I }
            }
            {
                c'4
                e'4
                d'4
                f'4
            }

    ..  container:: example

        Returns LilyPond setting name manager:

        >>> abjad.setting(staff)
        SettingInterface(('instrumentName', Markup(contents=['Vn. I'])))

    """
    if getattr(argument, "_lilypond_setting_name_manager", None) is None:
        argument._lilypond_setting_name_manager = SettingInterface()
    return argument._lilypond_setting_name_manager


class TweakInterface(Interface):
    """
    LilyPond tweak manager.

    ..  container:: example

        Tweak managers are created by the ``abjad.tweak()`` factory function:

        >>> markup = abjad.Markup("Allegro", direction=abjad.Up)
        >>> abjad.tweak(markup)
        TweakInterface(('_literal', None))

        Set an attribute like this:

        >>> abjad.tweak(markup).color = "#red"

        The state of the tweak manager has changed:

        >>> abjad.tweak(markup)
        TweakInterface(('_literal', None), ('color', '#red'))

        And the value of the attribute just set is available like this:

        >>> abjad.tweak(markup).color
        '#red'

        Trying to get an attribute that has not yet been set raises an
        attribute error:

        >>> abjad.tweak(markup).Foo
        Traceback (most recent call last):
            ...
        AttributeError: TweakInterface object has no attribute 'Foo'.

    """

    ### INITIALIZER ###

    def __init__(
        self, *, deactivate: bool = None, literal: bool = None, tag: _tag.Tag = None
    ) -> None:
        if deactivate is not None:
            self._currently_deactivated = deactivate
        if literal is not None:
            literal = bool(literal)
        self._literal = literal
        if tag is not None:
            self._currently_tagging = tag

    ### SPECIAL METHODS ###

    def __getattr__(self, name) -> typing.Union[Interface, typing.Any]:
        r"""
        Gets Interface (or OverrideInterface) keyed to ``name``.

        ..  container:: example

            Tweaks may be tagged:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> markup = abjad.Markup(r"\italic Allegro", direction=abjad.Up)
            >>> abjad.tweak(markup, tag=abjad.Tag("+PARTS")).color = "#red"
            >>> abjad.attach(markup, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> string = abjad.lilypond(staff, tags=True)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #red %! +PARTS
                ^ \markup {
                    \italic
                        Allegro
                    }
                d'4
                e'4
                f'4
            }

            Tweaks may be tagged with ``deactivate=True``:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> markup = abjad.Markup(r"\italic Allegro", direction=abjad.Up)
            >>> abjad.tweak(
            ...     markup, deactivate=True, tag=abjad.Tag("+PARTS")
            ... ).color = "#red"
            >>> abjad.attach(markup, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> string = abjad.lilypond(staff, tags=True)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #red %! +PARTS
                ^ \markup {
                    \italic
                        Allegro
                    }
                d'4
                e'4
                f'4
            }

            Tweak tags and indicator tags may be set together:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> markup = abjad.Markup(r"\italic Allegro", direction=abjad.Up)
            >>> abjad.tweak(markup, tag=abjad.Tag("+PARTS")).color = "#red"
            >>> abjad.attach(markup, staff[0], tag=abjad.Tag("RED:M1"))
            >>> abjad.show(staff) # doctest: +SKIP

            >>> string = abjad.lilypond(staff, tags=True)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #red                 %! +PARTS
                ^ \markup {                         %! RED:M1
                    \italic                         %! RED:M1
                        Allegro                     %! RED:M1
                    }                               %! RED:M1
                d'4
                e'4
                f'4
            }

        ..  container:: example

            Preloaded tweak managers can be made like this:

            >>> tweaks = abjad.TweakInterface()
            >>> tweaks.color = "#red"
            >>> tweaks.Y_offset = 6
            >>> tweaks
            TweakInterface(('Y_offset', 6), ('_literal', None), ('color', '#red'))

            Use the ``abjad.tweak()`` factory function for a shortcut:

            >>> tweaks = abjad.tweak("#red").color
            >>> tweaks
            TweakInterface(('_literal', None), ('color', '#red'))

            >>> tweaks.Y_offset = 6
            >>> tweaks
            TweakInterface(('Y_offset', 6), ('_literal', None), ('color', '#red'))

        ..  container:: example

            Set long LilyPond grob chains like this:

            >>> abjad.tweak(False).bound_details__left_broken__text
            TweakInterface(('_literal', None), ('bound_details__left_broken__text', False))

        """
        if name == "_currently_deactivated":
            return vars(self).get("_currently_deactivated")
        if name == "_currently_tagging":
            return vars(self).get("_currently_tagging")
        if name == "_literal":
            return vars(self).get("_literal")
        if "_pending_value" in vars(self):
            _pending_value = self._pending_value
            self.__setattr__(name, _pending_value)
            delattr(self, "_pending_value")
            return self
        camel_name = String(name).to_upper_camel_case()
        # assert name == camel_name, repr((name, camel_name))
        if name.startswith("_"):
            try:
                return vars(self)[name]
            except KeyError:
                type_name = type(self).__name__
                raise AttributeError(f"{type_name} object has no attribute {name!r}.")
        elif camel_name in grob_interfaces:
            try:
                return vars(self)[name]
            except KeyError:
                vars(self)[name] = Interface()
                return vars(self)[name]
        else:
            try:
                return vars(self)[name]
            except KeyError:
                type_name = type(self).__name__
                raise AttributeError(f"{type_name} object has no attribute {name!r}.")

    def __setattr__(self, name, value):
        """
        Sets attribute ``name`` equal to ``value``.

        ..  container:: example

            Allows LilyPond colors:

            >>> abjad.tweak("#blue").color
            TweakInterface(('_literal', None), ('color', '#blue'))

            >>> abjad.tweak("#(x11-color 'ForestGreen)").color
            TweakInterface(('_literal', None), ('color', "#(x11-color 'ForestGreen)"))

        """
        tag = getattr(self, "_currently_tagging", None)
        deactivate = getattr(self, "_currently_deactivated", None)
        if tag is not None:
            if deactivate is True:
                value = ("TAGGED", value, tag, True)
            else:
                value = ("TAGGED", value, tag)
        object.__setattr__(self, name, value)
        if name in ("_currently_deactivated", "_currently_tagging"):
            return
        try:
            delattr(self, "_currently_deactivated")
        except AttributeError:
            pass
        try:
            delattr(self, "_currently_tagging")
        except AttributeError:
            pass

    ### PRIVATE METHODS ###

    def _get_attribute_tuples(self) -> typing.List[typing.Tuple]:
        result: typing.List[typing.Tuple] = []
        for name, value in vars(self).items():
            if name == "_currently_tagging":
                continue
            if name == "_literal":
                continue
            if type(value) is Interface:
                grob_name = name
                grob_proxy = value
                pairs = iter(vars(grob_proxy).items())
                for attribute_name, attribute_value in pairs:
                    triple = (grob_name, attribute_name, attribute_value)
                    result.append(triple)
            else:
                attribute_name = name
                attribute_value = value
                pair = (attribute_name, attribute_value)
                result.append(pair)
        return result

    def _list_format_contributions(self, directed=True):
        result = []
        for attribute_tuple in self._get_attribute_tuples():
            if len(attribute_tuple) == 2:
                grob = None
                attribute = attribute_tuple[0]
                value = attribute_tuple[1]
            elif len(attribute_tuple) == 3:
                grob = attribute_tuple[0]
                attribute = attribute_tuple[1]
                value = attribute_tuple[2]
            else:
                raise ValueError(f"invalid attribute tuple: {attribute_tuple!r}.")
            deactivate = False
            if isinstance(value, tuple) and value[0] == "TAGGED":
                if len(value) == 4:
                    deactivate = value[3]
                tag = value[2]
                value = value[1]
            else:
                tag = None
            string = make_lilypond_tweak_string(
                attribute,
                value,
                directed=directed,
                grob=grob,
                literal=self._literal,
            )
            if tag is not None:
                strings = [string]
                strings = _tag.tag(strings, deactivate=deactivate, tag=tag)
                string = strings[0]
            result.append(string)
        result.sort()
        return result

    ### PUBLIC METHODS ###

    # TODO: move this somewhere clearer
    @staticmethod
    def set_tweaks(
        argument, manager: typing.Optional["TweakInterface"]
    ) -> typing.Optional["TweakInterface"]:
        r"""
        Sets tweaks on ``argument``.

        ..  container:: example

            >>> glissando = abjad.Glissando()
            >>> glissando.tweaks is None
            True

            >>> tweaks = abjad.tweak("blue").color
            >>> abjad.TweakInterface.set_tweaks(glissando, tweaks)
            TweakInterface(('_literal', None), ('color', 'blue'))

            >>> abjad.tweak(glissando)
            TweakInterface(('_literal', None), ('color', 'blue'))

        """
        if not hasattr(argument, "_tweaks"):
            try:
                argument._tweaks = None
            except AttributeError:
                name = type(argument).__name__
                raise NotImplementedError(f"{name} does not implement tweaks.")
        if manager is None:
            return None
        if not isinstance(manager, TweakInterface):
            raise Exception(f"must be tweak manager (not {manager!r}).")
        if argument._tweaks is None:
            argument._tweaks = TweakInterface(literal=manager._literal)
        existing_manager = argument._tweaks
        for tuple_ in manager._get_attribute_tuples():
            if len(tuple_) == 2:
                attribute, value = tuple_
                value = copy.copy(value)
                setattr(existing_manager, attribute, value)
            elif len(tuple_) == 3:
                grob, attribute, value = tuple_
                value = copy.copy(value)
                grob = getattr(existing_manager, grob)
                setattr(grob, attribute, value)
            else:
                message = "tweak tuple must have length 2 or 3"
                message += f" (not {tuple_!r})."
                raise ValueError(message)
        return existing_manager


IndexedTweakManager = typing.Union[TweakInterface, typing.Tuple[TweakInterface, int]]

IndexedTweakManagers = typing.Tuple[IndexedTweakManager, ...]


### FUNCTIONS ###


def tweak(argument, *, deactivate=None, expression=None, literal=None, tag=None):
    r"""
    Makes LilyPond tweak manager.

    ..  container:: example

        Tweaks markup:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup("Allegro assai", direction=abjad.Up)
        >>> abjad.tweak(markup).color = "#red"
        >>> abjad.attach(markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #red
                ^ \markup { Allegro assai }
                d'4
                e'4
                f'4
            }

        Survives copy:

        >>> import copy
        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup_1 = abjad.Markup("Allegro assai", direction=abjad.Up)
        >>> abjad.tweak(markup_1).color = "#red"
        >>> markup_2 = copy.copy(markup_1)
        >>> abjad.attach(markup_2, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #red
                ^ \markup { Allegro assai }
                d'4
                e'4
                f'4
            }

        Survives dot-chaining:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup(r'\italic "Allegro assai"', direction=abjad.Up)
        >>> abjad.tweak(markup).color = "#red"
        >>> abjad.attach(markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #red
                ^ \markup {
                    \italic
                        "Allegro assai"
                    }
                d'4
                e'4
                f'4
            }

        Works for opposite-directed coincident markup:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup_1 = abjad.Markup("Allegro assai ...", direction=abjad.Up)
        >>> abjad.tweak(markup_1).color = "#red"
        >>> abjad.attach(markup_1, staff[0])
        >>> markup_2 = abjad.Markup("... ma non troppo", direction=abjad.Down)
        >>> abjad.tweak(markup_2).color = "#blue"
        >>> abjad.tweak(markup_2).staff_padding = 4
        >>> abjad.attach(markup_2, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #red
                ^ \markup { Allegro assai ... }
                - \tweak color #blue
                - \tweak staff-padding 4
                _ \markup { ... ma non troppo }
                d'4
                e'4
                f'4
            }

        Ignored for same-directed coincident markup:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup_1 = abjad.Markup("Allegro assai ...", direction=abjad.Up)
        >>> abjad.tweak(markup_1).color = "#red"
        >>> abjad.attach(markup_1, staff[0])
        >>> markup_2 = abjad.Markup("... ma non troppo", direction=abjad.Up)
        >>> abjad.tweak(markup_2).color = "#blue"
        >>> abjad.tweak(markup_2).staff_padding = 4
        >>> abjad.attach(markup_2, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #red
                ^ \markup { Allegro assai ... }
                - \tweak color #blue
                - \tweak staff-padding 4
                ^ \markup { ... ma non troppo }
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Tweaks note-head:

        >>> staff = abjad.Staff("c'4 cs' d' ds'")
        >>> abjad.tweak(staff[1].note_head).color = "#red"
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                \tweak color #red
                cs'4
                d'4
                ds'4
            }

        Tweaks grob aggregated to note-head:

        >>> staff = abjad.Staff("c'4 cs' d' ds'")
        >>> abjad.tweak(staff[1].note_head).Accidental.color = "#red"
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                \tweak Accidental.color #red
                cs'4
                d'4
                ds'4
            }

    ..  container:: example

        Tweaks can be tagged:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> dynamic = abjad.Dynamic("f")
        >>> abjad.tweak(dynamic, tag=abjad.Tag("RED")).color = "#red"
        >>> abjad.attach(dynamic, staff[0])

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
        \new Staff
        {
            c'4
            - \tweak color #red %! RED
            \f
            d'4
            e'4
            f'4
        }

        >>> abjad.show(staff) # doctest: +SKIP

        REGRESSION. Tweaked tags can be set multiple times:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> dynamic = abjad.Dynamic("f")
        >>> abjad.tweak(dynamic, tag=abjad.Tag("RED")).color = "#red"
        >>> abjad.tweak(dynamic, tag=abjad.Tag("BLUE")).color = "#blue"
        >>> abjad.attach(dynamic, staff[0])

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
        \new Staff
        {
            c'4
            - \tweak color #blue %! BLUE
            \f
            d'4
            e'4
            f'4
        }

        >>> abjad.show(staff) # doctest: +SKIP

    ..  container:: example

        Returns LilyPond tweak manager:

        >>> abjad.tweak(markup_1)
        TweakInterface(('_literal', None), ('color', '#red'))

    ..  container:: example

        Tweak expressions work like this:

        >>> abjad.tweak("#red").color
        TweakInterface(('_literal', None), ('color', '#red'))

        >>> abjad.tweak(6).Y_offset
        TweakInterface(('Y_offset', 6), ('_literal', None))

        >>> abjad.tweak(False).bound_details__left_broken__text
        TweakInterface(('_literal', None), ('bound_details__left_broken__text', False))

    """
    if tag is not None and not isinstance(tag, _tag.Tag):
        raise Exception(f"must be be tag: {repr(tag)}")

    constants = (enums.Down, enums.Left, enums.Right, enums.Up)
    prototype = (bool, int, float, str, tuple)
    if expression is True or argument in constants or isinstance(argument, prototype):
        interface = TweakInterface(deactivate=deactivate, literal=literal, tag=tag)
        interface._pending_value = argument
        return interface
    if not hasattr(argument, "_tweaks"):
        name = type(argument).__name__
        raise NotImplementedError(f"{name} does not allow tweaks (yet).")
    if argument._tweaks is None:
        interface = TweakInterface(deactivate=deactivate, literal=literal, tag=tag)
        argument._tweaks = interface
    else:
        interface = argument._tweaks
        interface.__init__(deactivate=deactivate, literal=literal, tag=tag)
    return interface
