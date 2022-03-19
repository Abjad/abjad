import copy
import dataclasses
import typing

from . import _indent
from . import bundle as _bundle
from . import enums as _enums
from . import lyenv as _lyenv
from . import string as _string
from . import tag as _tag


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

    _format_leaf_children: typing.ClassVar[bool] = False

    def __post_init__(self):
        if self.lilypond_type is not None:
            assert isinstance(self.lilypond_type, str)
        assert isinstance(self.grob_name, str)
        assert isinstance(self.once, bool), repr(self.once)
        assert isinstance(self.is_revert, bool)
        property_path_: tuple[str, ...]
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

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
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

    _format_leaf_children: typing.ClassVar[bool] = False

    def __post_init__(self):
        if self.lilypond_type is not None:
            assert isinstance(self.lilypond_type, str)
        assert isinstance(self.context_property, str)
        assert isinstance(self.is_unset, bool)
        assert isinstance(self.value, bool | int | float | str), repr(self.value)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        string = "\n".join(self.format_pieces)
        bundle.context_settings.append(string)
        return bundle

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
                pieces.append(_indent.INDENT + part)
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


class TweakInterface(Interface):
    r"""
    LilyPond tweak interface.

    ..  container:: example

        Tweak interfaces are created by the ``abjad.tweak()`` factory function:

        >>> markup = abjad.Markup(r"\markup Allegro")
        >>> abjad.tweak(markup)
        TweakInterface()

        Set an attribute like this:

        >>> abjad.tweak(markup).color = "#red"

        The state of the tweak interface has changed:

        >>> abjad.tweak(markup)
        TweakInterface(('color', '#red'))

        And the value of the attribute just set is available like this:

        >>> abjad.tweak(markup).color
        '#red'

        Trying to get an attribute that has not yet been set raises an attribute error:

        >>> abjad.tweak(markup).Foo
        Traceback (most recent call last):
            ...
        AttributeError: TweakInterface object has no attribute 'Foo'.

    """

    def __init__(self, *, deactivate: bool = False, tag: _tag.Tag = None) -> None:
        assert isinstance(deactivate, bool), repr(bool)
        if tag is not None:
            assert isinstance(tag, _tag.Tag), repr(tag)
        self._currently_deactivated = bool(deactivate)
        self._foo = "bar"
        del self._foo
        if tag is not None:
            self._currently_tagging = tag

    def __getattr__(self, name):
        r"""
        Gets interface (or override interface) keyed to ``name``.

        ..  container:: example

            Tweaks may be tagged:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> markup = abjad.Markup(r"\markup \italic Allegro")
            >>> abjad.tweak(markup, tag=abjad.Tag("+PARTS")).color = "#red"
            >>> abjad.attach(markup, staff[0], direction=abjad.UP)
            >>> abjad.show(staff) # doctest: +SKIP

            >>> string = abjad.lilypond(staff, tags=True)
            >>> print(string)
            \new Staff
            {
                c'4
                %! +PARTS
                - \tweak color #red
                ^ \markup \italic Allegro
                d'4
                e'4
                f'4
            }

            Tweaks may be tagged with ``deactivate=True``:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> markup = abjad.Markup(r"\markup \italic Allegro")
            >>> abjad.tweak(
            ...     markup, deactivate=True, tag=abjad.Tag("+PARTS")
            ... ).color = "#red"
            >>> abjad.attach(markup, staff[0], direction=abjad.UP)
            >>> abjad.show(staff) # doctest: +SKIP

            >>> string = abjad.lilypond(staff, tags=True)
            >>> print(string)
            \new Staff
            {
                c'4
                %! +PARTS
                - \tweak color #red
                ^ \markup \italic Allegro
                d'4
                e'4
                f'4
            }

            Tweak tags and indicator tags may be set together:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> markup = abjad.Markup(r"\markup \italic Allegro")
            >>> abjad.tweak(markup, tag=abjad.Tag("+PARTS")).color = "#red"
            >>> abjad.attach(
            ...     markup, staff[0], direction=abjad.UP, tag=abjad.Tag("RED:M1")
            ... )
            >>> abjad.show(staff) # doctest: +SKIP

            >>> string = abjad.lilypond(staff, tags=True)
            >>> print(string)
            \new Staff
            {
                c'4
                %! +PARTS
                %! RED
                %! M1
                - \tweak color #red
                %! RED
                %! M1
                ^ \markup \italic Allegro
                d'4
                e'4
                f'4
            }

        ..  container:: example

            Preloaded tweak interfaces can be made like this:

            >>> tweaks = abjad.TweakInterface()
            >>> tweaks.color = "#red"
            >>> tweaks.Y_offset = 6
            >>> tweaks
            TweakInterface(('Y_offset', 6), ('color', '#red'))

            Use the ``abjad.tweak()`` factory function for a shortcut:

            >>> tweaks = abjad.tweak("#red").color
            >>> tweaks
            TweakInterface(('color', '#red'))

            >>> tweaks.Y_offset = 6
            >>> tweaks
            TweakInterface(('Y_offset', 6), ('color', '#red'))

        ..  container:: example

            Set long LilyPond grob chains like this:

            >>> abjad.tweak(False).bound_details__left_broken__text
            TweakInterface(('bound_details__left_broken__text', False))

        """
        if name == "_currently_deactivated":
            return vars(self).get("_currently_deactivated")
        if name == "_currently_tagging":
            return vars(self).get("_currently_tagging")
        if "_pending_value" in vars(self):
            _pending_value = self._pending_value
            self.__setattr__(name, _pending_value)
            delattr(self, "_pending_value")
            return self
        camel_name = _string.to_upper_camel_case(name)
        if name.startswith("_"):
            try:
                return vars(self)[name]
            except KeyError:
                type_name = type(self).__name__
                raise AttributeError(f"{type_name} object has no attribute {name!r}.")
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
                raise AttributeError(f"{type_name} object has no attribute {name!r}.")

    def __setattr__(self, name, value):
        """
        Sets attribute ``name`` equal to ``value``.

        ..  container:: example

            >>> abjad.tweak("#blue").color
            TweakInterface(('color', '#blue'))

            >>> abjad.tweak("#(x11-color 'ForestGreen)").color
            TweakInterface(('color', "#(x11-color 'ForestGreen)"))

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

    def _get_attribute_tuples(self):
        result = []
        for name, value in vars(self).items():
            if name == "_currently_tagging":
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
        result.sort()
        return result

    def _list_contributions(self, directed=True):
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
            string = _make_lilypond_tweak_string(
                attribute,
                value,
                directed=directed,
                grob=grob,
            )
            strings = [string]
            if tag is not None:
                strings = _tag.double_tag(strings, tag, deactivate=deactivate)
            result.extend(strings)
        return result


IndexedTweakInterface: typing.TypeAlias = typing.Union[
    TweakInterface | tuple[TweakInterface, int]
]

IndexedTweakInterfaces: typing.TypeAlias = tuple[IndexedTweakInterface, ...]


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


def set_tweaks(argument, interface: TweakInterface) -> TweakInterface:
    """
    Sets tweaks on ``argument``.

    ..  container:: example

        >>> glissando = abjad.Glissando()
        >>> glissando.tweaks is None
        True

        >>> tweaks = abjad.tweak("blue").color
        >>> abjad.overrides.set_tweaks(glissando, tweaks)
        TweakInterface(('color', 'blue'))

        >>> abjad.tweak(glissando)
        TweakInterface(('color', 'blue'))

    """
    assert isinstance(interface, TweakInterface), repr(interface)
    if argument.tweaks is None:
        argument.tweaks = TweakInterface()
    existing_interface = argument.tweaks
    for tuple_ in interface._get_attribute_tuples():
        if len(tuple_) == 2:
            attribute, value = tuple_
            value = copy.copy(value)
            setattr(existing_interface, attribute, value)
        elif len(tuple_) == 3:
            grob, attribute, value = tuple_
            value = copy.copy(value)
            grob = getattr(existing_interface, grob)
            setattr(grob, attribute, value)
        else:
            raise Exception("tweak tuple must have length 2 or 3 (not {tuple_!r}).")
    return existing_interface


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


def tweak(argument, *, deactivate=False, tag=None):
    r"""
    Makes LilyPond tweak interface.

    ..  container:: example

        Tweaks markup:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup(r'\markup "Allegro assai"')
        >>> abjad.tweak(markup).color = "#red"
        >>> abjad.attach(markup, staff[0], direction=abjad.UP)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #red
                ^ \markup "Allegro assai"
                d'4
                e'4
                f'4
            }

        Survives copy:

        >>> import copy
        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup_1 = abjad.Markup(r'\markup "Allegro assai"')
        >>> abjad.tweak(markup_1).color = "#red"
        >>> markup_2 = copy.copy(markup_1)
        >>> abjad.attach(markup_2, staff[0], direction=abjad.UP)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #red
                ^ \markup "Allegro assai"
                d'4
                e'4
                f'4
            }

        Survives dot-chaining:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup(r'\markup \italic "Allegro assai"')
        >>> abjad.tweak(markup).color = "#red"
        >>> abjad.attach(markup, staff[0], direction=abjad.UP)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #red
                ^ \markup \italic "Allegro assai"
                d'4
                e'4
                f'4
            }

        Works for opposite-directed coincident markup:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup_1 = abjad.Markup(r'\markup "Allegro assai ..."')
        >>> abjad.tweak(markup_1).color = "#red"
        >>> abjad.attach(markup_1, staff[0], direction=abjad.UP)
        >>> markup_2 = abjad.Markup(r'\markup "... ma non troppo"')
        >>> abjad.tweak(markup_2).color = "#blue"
        >>> abjad.tweak(markup_2).staff_padding = 4
        >>> abjad.attach(markup_2, staff[0], direction=abjad.DOWN)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #red
                ^ \markup "Allegro assai ..."
                - \tweak color #blue
                - \tweak staff-padding 4
                _ \markup "... ma non troppo"
                d'4
                e'4
                f'4
            }

        Ignored for same-directed coincident markup:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup_1 = abjad.Markup(r'\markup "Allegro assai ..."')
        >>> abjad.tweak(markup_1).color = "#red"
        >>> abjad.attach(markup_1, staff[0], direction=abjad.UP)
        >>> markup_2 = abjad.Markup(r'\markup "... ma non troppo"')
        >>> abjad.tweak(markup_2).color = "#blue"
        >>> abjad.tweak(markup_2).staff_padding = 4
        >>> abjad.attach(markup_2, staff[0], direction=abjad.UP)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #red
                ^ \markup "Allegro assai ..."
                - \tweak color #blue
                - \tweak staff-padding 4
                ^ \markup "... ma non troppo"
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
            %! RED
            - \tweak color #red
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
            %! BLUE
            - \tweak color #blue
            \f
            d'4
            e'4
            f'4
        }

        >>> abjad.show(staff) # doctest: +SKIP

    ..  container:: example

        Returns LilyPond tweak interface:

        >>> abjad.tweak(markup_1)
        TweakInterface(('color', '#red'))

    ..  container:: example

        Tweak expressions work like this:

        >>> abjad.tweak("#red").color
        TweakInterface(('color', '#red'))

        >>> abjad.tweak(6).Y_offset
        TweakInterface(('Y_offset', 6))

        >>> abjad.tweak(False).bound_details__left_broken__text
        TweakInterface(('bound_details__left_broken__text', False))

    """
    assert isinstance(deactivate, bool), repr(deactivate)
    if tag is not None:
        assert isinstance(tag, _tag.Tag), repr(tag)
    prototype = (bool, int, float, str, tuple, _enums.Horizontal, _enums.Vertical)
    if isinstance(argument, prototype):
        interface = TweakInterface(deactivate=deactivate, tag=tag)
        interface._pending_value = argument
    elif hasattr(argument, "tweaks"):
        if argument.tweaks is None:
            interface = TweakInterface(deactivate=deactivate, tag=tag)
            argument.tweaks = interface
        else:
            interface = argument.tweaks
            interface.__init__(deactivate=deactivate, tag=tag)
    else:
        name = type(argument).__name__
        raise NotImplementedError(f"{name} does not allow tweaks (yet).")
    return interface
