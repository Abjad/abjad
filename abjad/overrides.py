import copy
import dataclasses
import typing

from . import _indentlib
from . import contributions as _contributions
from . import enums as _enums
from . import lyenv as _lyenv
from . import string as _string


def _format_scheme_value(value):
    if value is True:
        result = "##t"
    elif value is False:
        result = "##f"
    elif isinstance(value, int | float):
        result = str(value)
    elif value is None:
        result = "##f"
    elif isinstance(value, _enums.Horizontal | _enums.Vertical):
        result = rf"#{value.name.lower()}"
    elif isinstance(value, tuple) and len(value) == 2:
        result = f"#'({value[0]} . {value[1]})"
    else:
        assert isinstance(value, str), repr(value)
        result = str(value)
    return result


def _format_lilypond_attribute(attribute):
    assert isinstance(attribute, str), repr(attribute)
    attribute = attribute.replace("__", ".")
    result = attribute.replace("_", "-")
    return result


def _make_lilypond_tweak_string(attribute, value, *, directed=True, grob=None) -> str:
    if grob is not None:
        grob = _string.to_upper_camel_case(grob)
        grob += "."
    else:
        grob = ""
    attribute = _format_lilypond_attribute(attribute)
    value = _format_scheme_value(value)
    string = rf"\tweak {grob}{attribute} {value}"
    if directed:
        string = "- " + string
    return string


@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
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
        ...    ),
        ...    value=r"\markup \bold { over pressure }",
        ... )
        >>> print(override.override_string)
        \once \override Staff.TextSpanner.bound-details.left.text = \markup \bold { over pressure }

        >>> override = abjad.LilyPondOverride(
        ...    lilypond_type="Staff",
        ...    grob_name="TextSpanner",
        ...    once=True,
        ...    property_path="bound_details__left__text",
        ...    value=r"\markup \bold { over pressure }",
        ... )
        >>> print(override.override_string)
        \once \override Staff.TextSpanner.bound-details.left.text = \markup \bold { over pressure }

    """

    lilypond_type: str | None = None
    grob_name: str = "NoteHead"
    once: bool = False
    is_revert: bool = False
    property_path: str | typing.Sequence[str] = "color"
    value: bool | int | float | str = "#red"

    format_leaf_children: typing.ClassVar[bool] = False

    def __post_init__(self):
        if self.lilypond_type is not None:
            assert isinstance(self.lilypond_type, str)
        assert isinstance(self.grob_name, str)
        assert isinstance(self.once, bool), repr(self.once)
        assert isinstance(self.is_revert, bool)
        if isinstance(self.property_path, str):
            property_path_ = (self.property_path,)
        else:
            property_path_ = tuple(self.property_path)
        assert all(isinstance(_, str) for _ in property_path_)
        self.property_path = property_path_
        prototype = (
            bool | int | float | str | _enums.Horizontal | _enums.Vertical | tuple
        )
        assert isinstance(self.value, prototype), repr(self.value)

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        if not self.once:
            revert_format = "\n".join(self.revert_format_pieces)
            contributions.grob_reverts.append(revert_format)
        if not self.is_revert:
            override_format = "\n".join(self.override_format_pieces)
            contributions.grob_overrides.append(override_format)
        return contributions

    def _override_property_path_string(self):
        parts = []
        if self.lilypond_type is not None:
            parts.append(self.lilypond_type)
        parts.append(self.grob_name)
        for part in self.property_path:
            part = _format_lilypond_attribute(part)
            parts.append(part)
        path = ".".join(parts)
        return path

    def _revert_property_path_string(self):
        parts = []
        if self.lilypond_type is not None:
            parts.append(self.lilypond_type)
        parts.append(self.grob_name)
        part = _format_lilypond_attribute(self.property_path[0])
        parts.append(part)
        path = ".".join(parts)
        return path

    @property
    def override_format_pieces(self) -> tuple[str, ...]:
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
            ...    ),
            ...    value=r"\markup \bold { over pressure }",
            ... )
            >>> for line in override.override_format_pieces:
            ...     line
            ...
            '\\once \\override Staff.TextSpanner.bound-details.left.text = \\markup \\bold { over pressure }'

        """
        result = []
        if self.once:
            result.append(r"\once")
        result.append(r"\override")
        result.append(self._override_property_path_string())
        result.append("=")
        string = _format_scheme_value(self.value)
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
            ... )
            >>> override.override_string
            "\\override Glissando.style = #'zigzag"

        """
        return "\n".join(self.override_format_pieces)

    @property
    def revert_format_pieces(self) -> tuple[str, ...]:
        r"""
        Gets LilyPond grob override \revert format pieces.

        ..  container:: example

            >>> override = abjad.LilyPondOverride(
            ...     grob_name="Glissando",
            ...     property_path="style",
            ...     value="#'zigzag",
            ... )
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
            ... )
            >>> override.revert_string
            '\\revert Glissando.style'

        """
        return "\n".join(self.revert_format_pieces)

    def tweak_string(self, directed=True, grob=False) -> str:
        r"""
        Gets LilyPond grob override \tweak string.

        ..  container:: example

            >>> override = abjad.LilyPondOverride(
            ...     grob_name="Glissando",
            ...     property_path="style",
            ...     value="#'zigzag",
            ... )
            >>> override.tweak_string()
            "- \\tweak style #'zigzag"

        ..  container:: example

            >>> override = abjad.LilyPondOverride(
            ...     grob_name="RehearsalMark",
            ...     property_path="color",
            ...     value="#red",
            ... )
            >>> override.tweak_string(directed=False)
            '\\tweak color #red'

        """
        if directed:
            result = [r"- \tweak"]
        else:
            result = [r"\tweak"]
        if grob:
            property_path = [self.grob_name] + list(self.property_path)
        else:
            property_path = list(self.property_path)
        string = ".".join(property_path)
        result.append(string)
        string = _format_scheme_value(self.value)
        result.append(string)
        return " ".join(result)


@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
class LilyPondSetting:
    r"""
    LilyPond context setting.

    ..  container:: example

        >>> context_setting = abjad.LilyPondSetting(
        ...    lilypond_type="Score",
        ...    context_property="autoBeaming",
        ...    value="##f",
        ... )

        >>> print("\n".join(context_setting.format_pieces))
        \set Score.autoBeaming = ##f

    """

    lilypond_type: str | None = None
    context_property: str = "autoBeaming"
    is_unset: bool = False
    value: typing.Any = False

    format_leaf_children: typing.ClassVar[bool] = False

    def __post_init__(self):
        if self.lilypond_type is not None:
            assert isinstance(self.lilypond_type, str)
        assert isinstance(self.context_property, str)
        assert isinstance(self.is_unset, bool)
        assert isinstance(self.value, bool | int | float | str), repr(self.value)

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        string = "\n".join(self.format_pieces)
        contributions.context_settings.append(string)
        return contributions

    @property
    def format_pieces(self) -> tuple[str, ...]:
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
        string = _format_scheme_value(self.value)
        value_pieces = string.split("\n")
        result.append(value_pieces[0])
        result[:] = [" ".join(result)]
        result.extend(value_pieces[1:])
        return tuple(result)


class Interface:
    """
    Base class from which grob, setting and tweak interfaces inherit.
    """

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is an interface with attribute pairs equal to those of
        this interface.

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
        Hashes interface.
        """
        return super().__hash__()

    def __repr__(self) -> str:
        """
        Gets repr.
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

    def _get_attribute_pairs(self):
        return list(sorted(vars(self).items()))


class OverrideInterface(Interface):
    """
    Override interface.

    ..  container:: example

        Override interfaces are created by the ``abjad.override()`` factory function:

        >>> note = abjad.Note("c'4")
        >>> abjad.override(note)
        OverrideInterface()

    """

    def __getattr__(self, name):
        r"""
        Gets Interface (or OverrideInterface) keyed to ``name``.

        ..  container:: example

            Somewhat confusingly, getting a grob name returns an interface:

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
        interface returned in the chain is likely to be surprising at first encounter.
        """
        camel_name = _string.to_upper_camel_case(name)
        if name.startswith("_"):
            try:
                return vars(self)[name]
            except KeyError:
                type_name = type(self).__name__
                raise AttributeError("{type_name!r} object has no attribute: {name!r}.")
        elif camel_name in _lyenv.contexts:
            try:
                return vars(self)["_" + name]
            except KeyError:
                context = OverrideInterface()
                vars(self)["_" + name] = context
                return context
        elif camel_name in _lyenv.grob_interfaces:
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

    def __setattr__(self, attribute, value):
        """
        Sets attribute ``attribute`` of override interface to ``value``.
        """
        object.__setattr__(self, attribute, value)

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
        result.sort()
        return tuple(result)

    def _list_contributions(self, contribution_type, once=False):
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
                override = LilyPondOverride(
                    lilypond_type=context,
                    grob_name=grob,
                    once=once,
                    is_revert=False,
                    property_path=attribute,
                    value=value,
                )
                override_string = override.override_string
                result.append(override_string)
            else:
                override = LilyPondOverride(
                    lilypond_type=context,
                    grob_name=grob,
                    is_revert=True,
                    property_path=attribute,
                )
                revert_string = override.revert_string
                result.append(revert_string)
        result.sort()
        return result


class SettingInterface(Interface):
    """
    LilyPond setting interface.

    ..  container:: example

        >>> note = abjad.Note("c'4")
        >>> abjad.setting(note)
        SettingInterface()

    """

    def __getattr__(self, name: str):
        r"""
        Gets arbitrary object keyed to ``name``.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> string = r'\markup "Vn. I"'
            >>> abjad.setting(staff).instrumentName = string
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    instrumentName = \markup "Vn. I"
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
            '\\markup "Vn. I"'

        """
        camel_name = _string.to_upper_camel_case(name)
        if name.startswith("_"):
            try:
                return vars(self)[name]
            except KeyError:
                message = "{type(self).__name__!r} object has no attribute: {name!r}."
                raise AttributeError(message)
        elif camel_name in _lyenv.contexts:
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

    def _format_in_with_block(self) -> list[str]:
        strings = []
        for key, value in vars(self).items():
            assert isinstance(key, str), repr(key)
            name = key.split("_")
            first = name[0:1]
            rest = name[1:]
            rest = [_.title() for _ in rest]
            name = first + rest
            string = "".join(name)
            value = _format_scheme_value(value)
            value_parts = value.split("\n")
            result = rf"{string!s} = {value_parts[0]!s}"
            pieces = [result]
            for part in value_parts[1:]:
                pieces.append(_indentlib.INDENT + part)
            string = "\n".join(pieces)
            strings.append(string)
        return strings

    def _format_inline(self, context=None) -> list[str]:
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
        rest = [_.title() for _ in rest]
        name = first + rest
        name = "".join(name)
        value = _format_scheme_value(value)
        if context is not None:
            context_string = context[1:]
            context_string = context_string.split("_")
            context_string = [_.title() for _ in context_string]
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
        result.sort()
        return result


def override(argument):
    r"""
    Makes LilyPond grob override interface.

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

        Returns LilyPond grob override interface.

        >>> staff = abjad.Staff("c'4 e' d' f'")
        >>> abjad.override(staff)
        OverrideInterface()

    """
    if getattr(argument, "_overrides", None) is None:
        argument._overrides = OverrideInterface()
    return argument._overrides


def setting(argument):
    r"""
    Makes LilyPond setting name interface.

    ..  container:: example

        Sets instrument name:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> string = r'\markup "Vn. I"'
        >>> abjad.setting(staff).instrumentName = string
        >>> abjad.show(staff) # doctest: +SKIP


        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                instrumentName = \markup "Vn. I"
            }
            {
                c'4
                e'4
                d'4
                f'4
            }

    ..  container:: example

        Returns LilyPond setting name interface:

        >>> abjad.setting(staff)
        SettingInterface(('instrumentName', '\\markup "Vn. I"'))

    """
    if getattr(argument, "_lilypond_setting_name_manager", None) is None:
        argument._lilypond_setting_name_manager = SettingInterface()
    return argument._lilypond_setting_name_manager
