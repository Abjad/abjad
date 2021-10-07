import importlib
import inspect
import numbers
import os
import pathlib
import subprocess
import time
import typing

from . import bundle as _bundle
from . import configuration as _configuration
from . import contextmanagers as _contextmanagers
from . import format as _format
from . import iterate as iterate_
from . import lilypondformat as _lilypondformat
from . import markups as _markups
from . import overrides as _overrides
from . import score as _score
from . import tag as _tag
from .indicators.LilyPondComment import LilyPondComment

configuration = _configuration.Configuration()


class Block:
    r"""
    LilyPond file block.

    ..  container:: example

        REGRESSION. Blocks remember attribute assignment order.

        Here right margin precedes left margin even though left margin alphabetizes
        before right margin:

        >>> block = abjad.Block(name="paper")
        >>> block.right_margin = abjad.LilyPondDimension(2, "cm")
        >>> block.left_margin = abjad.LilyPondDimension(2, "cm")
        >>> block
        <Block(name='paper')>

        >>> string = abjad.lilypond(block)
        >>> print(string)
        \paper
        {
            right-margin = 2\cm
            left-margin = 2\cm
        }

    ..  container:: example

        >>> block = abjad.Block(name='score')
        >>> markup = abjad.Markup(r"\markup foo", literal=True)
        >>> block.items.append(markup)
        >>> block
        <Block(name='score')>

        >>> string = abjad.lilypond(block)
        >>> print(string)
        \score
        {
            {
                \markup foo
            }
        }

    """

    ### INITIALIZER ###

    def __init__(self, name="score"):
        assert isinstance(name, str), repr(name)
        self._name = name
        escaped_name = rf"\{name}"
        self._escaped_name = escaped_name
        self._items = []
        self._public_attribute_names = []

    ### SPECIAL METHODS ###

    def __delattr__(self, name) -> None:
        """
        Deletes block attribute with ``name``.

        ..  container:: example

            >>> header_block = abjad.Block(name="header")
            >>> header_block.tagline = False
            >>> header_block.tagline
            False

            >>> delattr(header_block, "tagline")
            >>> hasattr(header_block, "tagline")
            False

        """
        self._public_attribute_names.remove(name)
        object.__delattr__(self, name)

    def __getitem__(self, name):
        """
        Gets item with ``name``.

        ..  container:: example

            Gets score with name ``'Red Example Score'`` in score block:

            >>> block = abjad.Block(name="score")
            >>> score = abjad.Score(name="Red_Example_Score")
            >>> block.items.append(score)

            >>> block["Red_Example_Score"]
            Score(simultaneous=True, name='Red_Example_Score')

        Returns item.

        Raises key error when no item with ``name`` is found.
        """
        for item in self.items:
            if getattr(item, "name", None) == name:
                return item
        raise KeyError

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    def __setattr__(self, name, value):
        """
        Sets block ``name`` to ``value``.

        Returns none.
        """
        if not name.startswith("_") and name not in self._public_attribute_names:
            self._public_attribute_names.append(name)
        object.__setattr__(self, name, value)

    def __setstate__(self, state):
        """
        Sets state of block.

        Returns none.
        """
        if not hasattr(self, "_public_attribute_names"):
            self._public_attribute_names = []
        for key, value in state.items():
            setattr(self, key, value)

    ### PRIVATE METHODS ###

    def _format_item(self, item, depth=1):
        indent = _bundle.LilyPondFormatBundle.indent * depth
        result = []
        if isinstance(item, (list, tuple)):
            result.append(indent + "{")
            depth_ = depth + 1
            for x in item:
                pieces = self._format_item(x, depth=depth_)
                result.extend(pieces)
            result.append(indent + "}")
        elif isinstance(item, str):
            if item.isspace():
                string = ""
            else:
                string = indent + item
            result.append(string)
        elif "_get_format_pieces" in dir(item):
            try:
                pieces = item._get_format_pieces()
            except TypeError:
                pieces = item._get_format_pieces()
            for piece in pieces:
                if piece.isspace():
                    piece = ""
                else:
                    piece = indent + piece
                result.append(piece)
        return result

    def _formatted_context_blocks(self):
        result = []
        context_blocks = []
        for item in self.items:
            if isinstance(item, ContextBlock):
                context_blocks.append(item)
        for context_block in context_blocks:
            result.extend(context_block._get_format_pieces())
        return result

    def _get_format_pieces(self, tag=None):
        indent = _bundle.LilyPondFormatBundle.indent
        result = []
        if (
            not self._get_formatted_user_attributes()
            and not getattr(self, "contexts", None)
            and not getattr(self, "context_blocks", None)
            and not len(self.items)
        ):
            string = f"{self._escaped_name} {{}}"
            result.append(string)
            return result
        strings = [f"{self._escaped_name}", "{"]
        if tag is not None:
            strings = _tag.double_tag(strings, tag)
        result.extend(strings)
        for item in self.items:
            if isinstance(item, ContextBlock):
                continue
            if isinstance(item, (_score.Leaf, _markups.Markup)):
                item = [item]
            result.extend(self._format_item(item))
        formatted_attributes = self._get_formatted_user_attributes()
        formatted_attributes = [indent + _ for _ in formatted_attributes]
        result.extend(formatted_attributes)
        formatted_context_blocks = self._formatted_context_blocks()
        formatted_context_blocks = [indent + _ for _ in formatted_context_blocks]
        result.extend(formatted_context_blocks)
        string = "}"
        strings = [string]
        if tag is not None:
            strings = _tag.double_tag(strings, tag)
        result.extend(strings)

        return result

    def _get_format_specification(self):
        return _format.FormatSpecification(
            repr_is_bracketed=True,
        )

    def _get_formatted_user_attributes(self):
        result = []
        for key in self._public_attribute_names:
            assert not key.startswith("_"), repr(key)
            value = getattr(self, key)
            formatted_key = key.split("__")
            for i, k in enumerate(formatted_key):
                formatted_key[i] = k.replace("_", "-")
                if 0 < i:
                    string = f"#'{formatted_key[i]}"
                    formatted_key[i] = string
            formatted_key = " ".join(formatted_key)
            if isinstance(value, _markups.Markup):
                formatted_value = value._get_format_pieces()
            elif isinstance(value, LilyPondDimension):
                formatted_value = [_lilypondformat.lilypond(value)]
            else:
                assert isinstance(value, (int, str, float)), repr((self, key, value))
                formatted_value = [str(value)]
            setting = f"{formatted_key!s} = {formatted_value[0]!s}"
            result.append(setting)
            result.extend(formatted_value[1:])
        return result

    def _get_lilypond_format(self, tag=None):
        return "\n".join(self._get_format_pieces(tag=tag))

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r"""
        Gets items in block.

        ..  container:: example

            >>> block = abjad.Block(name="score")
            >>> markup = abjad.Markup(r"\markup foo", literal=True)
            >>> block.items.append(markup)

            >>> block.items
            [Markup(contents=['\\markup foo'], literal=True)]

        ..  container:: example

            Accepts strings:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> score_block = abjad.Block(name="score")
            >>> score_block.items.append("<<")
            >>> score_block.items.append(r'{ \include "layout.ly" }')
            >>> score_block.items.append(staff)
            >>> score_block.items.append(">>")
            >>> lilypond_file = abjad.LilyPondFile(
            ...     lilypond_language_token=False,
            ...     lilypond_version_token=False,
            ... )
            >>> lilypond_file.items.append(score_block)

            >>> string = abjad.lilypond(lilypond_file)
            >>> print(string)
            <BLANKLINE>
            \score
            {
                <<
                { \include "layout.ly" }
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }
                >>
            }

        Returns list.
        """
        return self._items

    @property
    def name(self) -> typing.Optional[str]:
        """
        Gets name of block.

        ..  container:: example

            >>> block = abjad.Block(name="score")
            >>> block.name
            'score'

        """
        return self._name

    ### PUBLIC METHODS ###

    def empty(self) -> bool:
        """
        Is true when block contains no items and has no user attributes.
        """
        if not self.items and not self._get_formatted_user_attributes():
            return True
        return False


class ContextBlock(Block):
    r"""
    LilyPond file ``\context`` block.

    ..  container:: example

        >>> block = abjad.ContextBlock(
        ...     source_lilypond_type="Staff",
        ...     name="FluteStaff",
        ...     type_="Engraver_group",
        ...     alias="Staff",
        ... )
        >>> block.remove_commands.append("Forbid_line_break_engraver")
        >>> block.consists_commands.append("Horizontal_bracket_engraver")
        >>> block.accepts_commands.append("FluteUpperVoice")
        >>> block.accepts_commands.append("FluteLowerVoice")
        >>> block.items.append(r"\accidentalStyle dodecaphonic")
        >>> abjad.override(block).Beam.positions = "#'(-4 . -4)"
        >>> abjad.override(block).Stem.stem_end_position = -6
        >>> abjad.setting(block).autoBeaming = False
        >>> abjad.setting(block).tupletFullLength = True
        >>> block
        <ContextBlock(source_lilypond_type='Staff', name='FluteStaff', type_='Engraver_group', alias='Staff')>

        >>> string = abjad.lilypond(block)
        >>> print(string)
        \context
        {
            \Staff
            \name FluteStaff
            \type Engraver_group
            \alias Staff
            \remove Forbid_line_break_engraver
            \consists Horizontal_bracket_engraver
            \accepts FluteUpperVoice
            \accepts FluteLowerVoice
            \override Beam.positions = #'(-4 . -4)
            \override Stem.stem-end-position = -6
            autoBeaming = ##f
            tupletFullLength = ##t
            \accidentalStyle dodecaphonic
        }

    """

    ### INITIALIZER ###

    def __init__(self, source_lilypond_type=None, name=None, type_=None, alias=None):
        Block.__init__(self, name="context")
        self._source_lilypond_type = source_lilypond_type
        self._name = name
        self._type_ = type_
        self._alias = alias
        self._accepts_commands = []
        self._consists_commands = []
        self._remove_commands = []

    ### PRIVATE METHODS ###

    def _get_format_pieces(self, tag=None):
        indent = _bundle.LilyPondFormatBundle.indent
        result = []
        result.extend([f"{self._escaped_name}", "{"])
        # CAUTION: source context name must come before type_ to allow
        # context redefinition.
        if self.source_lilypond_type is not None:
            string = indent + rf"\{self.source_lilypond_type}"
            result.append(string)
        if self.name is not None:
            string = indent + rf"\name {self.name}"
            result.append(string)
        if self.type_ is not None:
            string = indent + rf"\type {self.type_}"
            result.append(string)
        if self.alias is not None:
            string = indent + rf"\alias {self.alias}"
            result.append(string)
        for statement in self.remove_commands:
            string = indent + rf"\remove {statement}"
            result.append(string)
        # CAUTION: LilyPond \consists statements are order-significant!
        for statement in self.consists_commands:
            string = indent + rf"\consists {statement}"
            result.append(string)
        for statement in self.accepts_commands:
            string = indent + rf"\accepts {statement}"
            result.append(string)
        overrides = _overrides.override(self)._list_format_contributions("override")
        for statement in overrides:
            string = indent + statement
            result.append(string)
        setting_contributions = _overrides.setting(self)._format_in_with_block()
        for setting_contribution in sorted(setting_contributions):
            string = indent + setting_contribution
            result.append(string)
        for item in self.items:
            if isinstance(item, str):
                string = indent + f"{item}"
                result.append(string)
            elif "_get_format_pieces" in dir(item):
                for piece in item._get_format_pieces():
                    if piece.isspace():
                        piece = ""
                    else:
                        piece = indent + piece
                    result.append(piece)
            else:
                pass
        result.append("}")
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def accepts_commands(self) -> typing.List[str]:
        r"""
        Gets arguments of LilyPond ``\accepts`` commands.

        ..  container:: example

            >>> block = abjad.ContextBlock(
            ...     source_lilypond_type="Staff",
            ...     name="FluteStaff",
            ...     type_="Engraver_group",
            ...     alias="Staff",
            ... )
            >>> block.remove_commands.append("Forbid_line_break_engraver")
            >>> block.consists_commands.append("Horizontal_bracket_engraver")
            >>> block.accepts_commands.append("FluteUpperVoice")
            >>> block.accepts_commands.append("FluteLowerVoice")
            >>> block.items.append(r"\accidentalStyle dodecaphonic")
            >>> abjad.override(block).Beam.positions = "#'(-4 . -4)"
            >>> abjad.override(block).Stem.stem_end_position = -6
            >>> abjad.setting(block).autoBeaming = False
            >>> abjad.setting(block).tupletFullLength = True

            >>> block.accepts_commands
            ['FluteUpperVoice', 'FluteLowerVoice']

        """
        return self._accepts_commands

    @property
    def alias(self) -> typing.Optional[str]:
        r"""
        Gets and sets argument of LilyPond ``\alias`` command.

        ..  container:: example

            >>> block = abjad.ContextBlock(
            ...     source_lilypond_type="Staff",
            ...     name="FluteStaff",
            ...     type_="Engraver_group",
            ...     alias="Staff",
            ... )
            >>> block.remove_commands.append("Forbid_line_break_engraver")
            >>> block.consists_commands.append("Horizontal_bracket_engraver")
            >>> block.accepts_commands.append("FluteUpperVoice")
            >>> block.accepts_commands.append("FluteLowerVoice")
            >>> block.items.append(r"\accidentalStyle dodecaphonic")
            >>> abjad.override(block).Beam.positions = "#'(-4 . -4)"
            >>> abjad.override(block).Stem.stem_end_position = -6
            >>> abjad.setting(block).autoBeaming = False
            >>> abjad.setting(block).tupletFullLength = True

            >>> block.alias
            'Staff'

        """
        return self._alias

    @property
    def consists_commands(self) -> typing.List[str]:
        r"""
        Gets arguments of LilyPond ``\consists`` commands.

        ..  container:: example

            >>> block = abjad.ContextBlock(
            ...     source_lilypond_type="Staff",
            ...     name="FluteStaff",
            ...     type_="Engraver_group",
            ...     alias="Staff",
            ... )
            >>> block.remove_commands.append("Forbid_line_break_engraver")
            >>> block.consists_commands.append("Horizontal_bracket_engraver")
            >>> block.accepts_commands.append("FluteUpperVoice")
            >>> block.accepts_commands.append("FluteLowerVoice")
            >>> block.items.append(r"\accidentalStyle dodecaphonic")
            >>> abjad.override(block).Beam.positions = "#'(-4 . -4)"
            >>> abjad.override(block).Stem.stem_end_position = -6
            >>> abjad.setting(block).autoBeaming = False
            >>> abjad.setting(block).tupletFullLength = True

            >>> block.consists_commands
            ['Horizontal_bracket_engraver']

        """
        return self._consists_commands

    @property
    def items(self) -> typing.List[str]:
        r"""
        Gets items in context block.

        ..  container:: example

            >>> block = abjad.ContextBlock(
            ...     source_lilypond_type="Staff",
            ...     name="FluteStaff",
            ...     type_="Engraver_group",
            ...     alias="Staff",
            ... )
            >>> block.remove_commands.append("Forbid_line_break_engraver")
            >>> block.consists_commands.append("Horizontal_bracket_engraver")
            >>> block.accepts_commands.append("FluteUpperVoice")
            >>> block.accepts_commands.append("FluteLowerVoice")
            >>> block.items.append(r"\accidentalStyle dodecaphonic")
            >>> abjad.override(block).Beam.positions = "#'(-4 . -4)"
            >>> abjad.override(block).Stem.stem_end_position = -6
            >>> abjad.setting(block).autoBeaming = False
            >>> abjad.setting(block).tupletFullLength = True

            >>> block.items
            ['\\accidentalStyle dodecaphonic']

        """
        return self._items

    @property
    def name(self) -> typing.Optional[str]:
        r"""
        Gets and sets argument of LilyPond ``\name`` command.

        ..  container:: example

            >>> block = abjad.ContextBlock(
            ...     source_lilypond_type="Staff",
            ...     name="FluteStaff",
            ...     type_="Engraver_group",
            ...     alias="Staff",
            ... )
            >>> block.remove_commands.append("Forbid_line_break_engraver")
            >>> block.consists_commands.append("Horizontal_bracket_engraver")
            >>> block.accepts_commands.append("FluteUpperVoice")
            >>> block.accepts_commands.append("FluteLowerVoice")
            >>> block.items.append(r"\accidentalStyle dodecaphonic")
            >>> abjad.override(block).Beam.positions = "#'(-4 . -4)"
            >>> abjad.override(block).Stem.stem_end_position = -6
            >>> abjad.setting(block).autoBeaming = False
            >>> abjad.setting(block).tupletFullLength = True

            >>> block.name
            'FluteStaff'

        """
        return self._name

    @property
    def remove_commands(self) -> typing.List[str]:
        r"""
        Gets arguments of LilyPond ``\remove`` commands.

        ..  container:: example

            >>> block = abjad.ContextBlock(
            ...     source_lilypond_type="Staff",
            ...     name="FluteStaff",
            ...     type_="Engraver_group",
            ...     alias="Staff",
            ... )
            >>> block.remove_commands.append("Forbid_line_break_engraver")
            >>> block.consists_commands.append("Horizontal_bracket_engraver")
            >>> block.accepts_commands.append("FluteUpperVoice")
            >>> block.accepts_commands.append("FluteLowerVoice")
            >>> block.items.append(r"\accidentalStyle dodecaphonic")
            >>> abjad.override(block).Beam.positions = "#'(-4 . -4)"
            >>> abjad.override(block).Stem.stem_end_position = -6
            >>> abjad.setting(block).autoBeaming = False
            >>> abjad.setting(block).tupletFullLength = True

            >>> block.remove_commands
            ['Forbid_line_break_engraver']

        """
        return self._remove_commands

    @property
    def source_lilypond_type(self) -> typing.Optional[str]:
        r"""
        Gets and sets source context name.

        ..  container:: example

            >>> block = abjad.ContextBlock(
            ...     source_lilypond_type="Staff",
            ...     name="FluteStaff",
            ...     type_="Engraver_group",
            ...     alias="Staff",
            ... )
            >>> block.remove_commands.append("Forbid_line_break_engraver")
            >>> block.consists_commands.append("Horizontal_bracket_engraver")
            >>> block.accepts_commands.append("FluteUpperVoice")
            >>> block.accepts_commands.append("FluteLowerVoice")
            >>> block.items.append(r"\accidentalStyle dodecaphonic")
            >>> abjad.override(block).Beam.positions = "#'(-4 . -4)"
            >>> abjad.override(block).Stem.stem_end_position = -6
            >>> abjad.setting(block).autoBeaming = False
            >>> abjad.setting(block).tupletFullLength = True

            >>> block.source_lilypond_type
            'Staff'

        """
        return self._source_lilypond_type

    @property
    def type_(self) -> typing.Optional[str]:
        r"""
        Gets and sets argument of LilyPond ``\type`` command.

        ..  container:: example

            >>> block = abjad.ContextBlock(
            ...     source_lilypond_type="Staff",
            ...     name="FluteStaff",
            ...     type_="Engraver_group",
            ...     alias="Staff",
            ... )
            >>> block.remove_commands.append("Forbid_line_break_engraver")
            >>> block.consists_commands.append("Horizontal_bracket_engraver")
            >>> block.accepts_commands.append("FluteUpperVoice")
            >>> block.accepts_commands.append("FluteLowerVoice")
            >>> block.items.append(r"\accidentalStyle dodecaphonic")
            >>> abjad.override(block).Beam.positions = "#'(-4 . -4)"
            >>> abjad.override(block).Stem.stem_end_position = -6
            >>> abjad.setting(block).autoBeaming = False
            >>> abjad.setting(block).tupletFullLength = True

            >>> block.type_
            'Engraver_group'

        """
        return self._type_


class DateTimeToken:
    """
    LilyPond file date / time token.

    ..  container:: example

        >>> abjad.DateTimeToken()
        DateTimeToken()

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_date_string",)

    ### INITIALIZER ###

    def __init__(self, date_string=None):
        assert isinstance(date_string, (str, type(None)))
        self._date_string = date_string

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation of date / time token.

        ..  container:: example

            >>> abjad.DateTimeToken()
            DateTimeToken()

        """
        date_string = self._date_string or ""
        return f"{type(self).__name__}({date_string})"

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return self.date_string

    ### PUBLIC PROPERTIES ###

    @property
    def date_string(self) -> str:
        """
        Gets date string of date / time token.

        ..  container:: example

            >>> token = abjad.DateTimeToken()
            >>> token.date_string # doctest: +SKIP
            '2014-01-23 12:21'

        """
        date_string = self._date_string or time.strftime("%Y-%m-%d %H:%M")
        return date_string


class LilyPondDimension:
    r"""
    LilyPond file ``\paper`` block dimension.

    ..  container:: example

        >>> abjad.LilyPondDimension(2, "in")
        LilyPondDimension(value=2, unit='in')

    Use for LilyPond file ``\paper`` block attributes.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_unit", "_value")

    ### INITIALIZER ###

    def __init__(self, value=0, unit="cm"):
        assert isinstance(value, numbers.Number) and 0 <= value
        assert unit in ("cm", "in", "mm", "pt")
        self._value = value
        self._unit = unit

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    ### PRIVATE METHODS ###

    def _get_format_pieces(self, tag=None):
        return [rf"{self.value}\{self.unit}"]

    def _get_lilypond_format(self):
        return "\n".join(self._get_format_pieces())

    ### PUBLIC PROPERTIES ###

    @property
    def unit(self) -> str:
        """
        Gets unit of LilyPond dimension.

        ..  container:: example

            >>> dimension = abjad.LilyPondDimension(2, "in")
            >>> dimension.unit
            'in'

        Returns ``'cm'``, ``'in'``, ``'mm'`` or ``'pt'``.
        """
        return self._unit

    @property
    def value(self) -> typing.Union[int, float]:
        """
        Gets value of LilyPond dimension.

        ..  container:: example

            >>> dimension = abjad.LilyPondDimension(2, "in")
            >>> dimension.value
            2

        """
        return self._value


class LilyPondLanguageToken:
    r"""
    LilyPond file ``\language`` token.

    ..  container:: example

        >>> abjad.LilyPondLanguageToken()
        LilyPondLanguageToken()

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation of LilyPond language token.

        ..  container:: example

            >>> token = abjad.LilyPondLanguageToken()
            >>> token
            LilyPondLanguageToken()

        """
        return f"{type(self).__name__}()"

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        string = r'\language "english"'
        return string


class LilyPondVersionToken:
    r"""
    LilyPond file ``\version`` token.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_version_string",)

    ### INITIALIZER ###

    def __init__(self, version_string=None):
        assert isinstance(version_string, (str, type(None)))
        if version_string is None:
            version_string = configuration.get_lilypond_version_string()
        self._version_string = version_string

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation of LilyPond version_string token.

        ..  container:: example

            >>> token = abjad.LilyPondVersionToken()
            >>> token # doctest: +SKIP
            LilyPondVersionToken('2.19.84')

        """
        return f"{type(self).__name__}({self.version_string!r})"

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return rf'\version "{self.version_string}"'

    ### PUBLIC PROPERTIES ###

    @property
    def version_string(self) -> str:
        """
        Gets version string of LilyPond version token.

        ..  container:: example

            Gets version string from install environment:

            >>> token = abjad.LilyPondVersionToken(
            ...     version_string=None,
            ...     )
            >>> token.version_string # doctest: +SKIP
            '2.19.84'

        ..  container:: example

            Gets version string from explicit input:

            >>> token = abjad.LilyPondVersionToken(
            ...     version_string="2.19.84",
            ...     )
            >>> token.version_string
            '2.19.84'

        """
        return self._version_string


class PackageGitCommitToken:
    """
    Python package git commit token.

    ..  container:: example

        >>> token = abjad.PackageGitCommitToken("abjad")
        >>> token
        PackageGitCommitToken(package_name='abjad')

        >>> string = abjad.lilypond(token)
        >>> print(string)  # doctest: +SKIP
        package "abjad" @ b6a48a7 [implement-lpf-git-token] (2016-02-02 13:36:25)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_package_name",)

    ### INITIALIZER ###

    def __init__(self, package_name=None):
        self._package_name = package_name

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    ### PRIVATE METHODS ###

    def _get_commit_timestamp(self, commit_hash):
        command = f"git show -s --format=%ci {commit_hash}"
        return self._run_command(command)

    def _get_git_branch(self):
        command = "git rev-parse --abbrev-ref HEAD"
        return self._run_command(command)

    def _get_git_hash(self):
        command = "git rev-parse HEAD"
        return self._run_command(command)

    def _get_lilypond_format(self):
        path = self._get_package_path()
        with _contextmanagers.TemporaryDirectoryChange(path):
            git_branch = self._get_git_branch()
            git_hash = self._get_git_hash()
            timestamp = self._get_commit_timestamp(git_hash)
        date, time, _ = timestamp.split()
        return 'package "{}" @ {} [{}] ({} {})'.format(
            self._package_name, git_hash[:7], git_branch, date, time
        )

    def _get_package_path(self):
        module = importlib.import_module(self._package_name)
        path = module.__path__[0]
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        path = os.path.abspath(path)
        return path

    def _run_command(self, command):
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        process.wait()
        if process.returncode:
            return None
        result = process.stdout.read().splitlines()[0]
        result = result.decode("utf-8")
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def package_name(self) -> str:
        """
        Gets package name of package git commit token.

        ..  container:: example

            >>> token = abjad.PackageGitCommitToken("abjad")
            >>> token.package_name
            'abjad'

        """
        return self._package_name


class LilyPondFile:
    r"""
    LilyPond file.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> comments = [
        ...     "File construct as an example.",
        ...     "Parts shown here for positioning.",
        ... ]
        >>> lilypond_file = abjad.LilyPondFile(
        ...     items=[staff],
        ...     default_paper_size=("a5", "portrait"),
        ...     comments=comments,
        ...     includes=["abjad.ily"],
        ...     global_staff_size=16,
        ... )

        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ::

            >>> string = abjad.lilypond(lilypond_file)
            >>> print(string) # doctest: +SKIP
            % File construct as an example.
            % Parts shown here for positioning.
            <BLANKLINE>
            \version "2.23.1"
            \language "english"
            <BLANKLINE>
            \include "abjad.ily"
            <BLANKLINE>
            #(set-default-paper-size "a5" 'portrait)
            #(set-global-staff-size 16)
            <BLANKLINE>
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_comments",
        "_date_time_token",
        "_default_paper_size",
        "_global_staff_size",
        "_includes",
        "_items",
        "_lilypond_language_token",
        "_lilypond_version_token",
        "_tag",
        "_use_relative_includes",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        *,
        comments=None,
        date_time_token=None,
        default_paper_size=None,
        global_staff_size=None,
        includes=None,
        lilypond_language_token=None,
        lilypond_version_token=None,
        tag: _tag.Tag = None,
        use_relative_includes=None,
    ) -> None:
        comments = comments or ()
        comments = tuple(comments)
        self._comments = comments
        self._date_time_token = None
        if bool(date_time_token):
            self._date_time_token = DateTimeToken()
        self._default_paper_size = default_paper_size
        self._global_staff_size = global_staff_size
        includes = list(includes or [])
        self._includes = includes
        self._items = list(items or [])
        self._lilypond_language_token = None
        if lilypond_language_token is not False:
            language = LilyPondLanguageToken()
            self._lilypond_language_token = language
        self._lilypond_version_token = None
        if lilypond_version_token is not False:
            version = LilyPondVersionToken()
            self._lilypond_version_token = version
        if tag is not None:
            assert isinstance(tag, _tag.Tag), repr(tag)
        self._tag = tag
        self._use_relative_includes = use_relative_includes

    ### SPECIAL METHODS ###

    def __contains__(self, argument) -> bool:
        """
        Is true when LilyPond file contains ``argument``.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> lilypond_file = abjad.LilyPondFile([staff])

            >>> staff in lilypond_file
            True

            >>> abjad.Staff in lilypond_file
            True

            >>> "Allegro" in lilypond_file
            False

            >>> 0 in lilypond_file
            False

        """
        try:
            self[argument]
            return True
        except (AssertionError, KeyError, ValueError, TypeError):
            return False

    def __getitem__(self, argument):
        r"""
        Gets item identified by ``argument``.

        ..  container:: example

            Searches score:

            >>> voice_1 = abjad.Voice("c''4 b' a' g'", name="Voice_1")
            >>> literal = abjad.LilyPondLiteral(r"\voiceOne", "opening")
            >>> abjad.attach(literal, voice_1)
            >>> voice_2 = abjad.Voice("c'4 d' e' f'", name="Voice_2")
            >>> literal = abjad.LilyPondLiteral(r"\voiceTwo", "opening")
            >>> abjad.attach(literal, voice_2)
            >>> staff = abjad.Staff(
            ...     [voice_1, voice_2],
            ...     simultaneous=True,
            ...     name="Staff",
            ... )
            >>> score = abjad.Score([staff], name="Score")
            >>> block = abjad.Block(name="score")
            >>> block.items.append(score)
            >>> lilypond_file = abjad.LilyPondFile([block])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            c''4
                            b'4
                            a'4
                            g'4
                        }
                        \context Voice = "Voice_2"
                        {
                            \voiceTwo
                            c'4
                            d'4
                            e'4
                            f'4
                        }
                    >>
                >>

            >>> lilypond_file["score"]
            <Block(name='score')>

            >>> lilypond_file["Score"]
            <Score-"Score"<<1>>>

            >>> lilypond_file[abjad.Score]
            <Score-"Score"<<1>>>

            >>> lilypond_file["Staff"]
            <Staff-"Staff"<<2>>>

            >>> lilypond_file[abjad.Staff]
            <Staff-"Staff"<<2>>>

            >>> lilypond_file["Voice_1"]
            Voice("c''4 b'4 a'4 g'4", name='Voice_1')

            >>> lilypond_file["Voice_2"]
            Voice("c'4 d'4 e'4 f'4", name='Voice_2')

            >>> lilypond_file[abjad.Voice]
            Voice("c''4 b'4 a'4 g'4", name='Voice_1')

        ..  container:: example

            Searches score:

            >>> voice_1 = abjad.Voice("c''4 b' a' g'", name="Voice_1")
            >>> literal = abjad.LilyPondLiteral(r"\voiceOne", "opening")
            >>> abjad.attach(literal, voice_1)
            >>> voice_2 = abjad.Voice("c'4 d' e' f'", name="Voice_2")
            >>> literal = abjad.LilyPondLiteral(r"\voiceTwo", "opening")
            >>> abjad.attach(literal, voice_2)
            >>> staff = abjad.Staff(
            ...     [voice_1, voice_2],
            ...     simultaneous=True,
            ...     name="Staff",
            ... )
            >>> score = abjad.Score([staff], name="Score")
            >>> lilypond_file = abjad.LilyPondFile([score])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            c''4
                            b'4
                            a'4
                            g'4
                        }
                        \context Voice = "Voice_2"
                        {
                            \voiceTwo
                            c'4
                            d'4
                            e'4
                            f'4
                        }
                    >>
                >>

            >>> lilypond_file["Score"]
            <Score-"Score"<<1>>>

            >>> lilypond_file[abjad.Score]
            <Score-"Score"<<1>>>

            >>> lilypond_file["Staff"]
            <Staff-"Staff"<<2>>>

            >>> lilypond_file[abjad.Staff]
            <Staff-"Staff"<<2>>>

            >>> lilypond_file["Voice_1"]
            Voice("c''4 b'4 a'4 g'4", name='Voice_1')

            >>> lilypond_file["Voice_2"]
            Voice("c'4 d'4 e'4 f'4", name='Voice_2')

            >>> lilypond_file[abjad.Voice]
            Voice("c''4 b'4 a'4 g'4", name='Voice_1')

        ..  container:: example

            REGRESSION. Works when score block contains parallel container:

            >>> include_container = abjad.Container()
            >>> string = r'\include "layout.ly"'
            >>> literal = abjad.LilyPondLiteral(string, "opening")
            >>> abjad.attach(literal, include_container)
            >>> staff = abjad.Staff("c'4 d' e' f'", name="Staff")
            >>> container = abjad.Container(
            ...     [include_container, staff],
            ...     simultaneous=True,
            ... )
            >>> block = abjad.Block(name="score")
            >>> block.items.append(container)
            >>> lilypond_file = abjad.LilyPondFile(
            ...     items=[block],
            ...     lilypond_language_token=False,
            ...     lilypond_version_token=False,
            ... )
            >>> string = abjad.lilypond(lilypond_file)
            >>> print(string)
            <BLANKLINE>
            \score
            {
                <<
                    {
                        \include "layout.ly"
                    }
                    \context Staff = "Staff"
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                >>
            }

            >>> lilypond_file[abjad.Staff]
            Staff("c'4 d'4 e'4 f'4", name='Staff')

            >>> lilypond_file['Staff']
            Staff("c'4 d'4 e'4 f'4", name='Staff')

        Returns item.

        Raises key error when ``argument`` identifies no item in LilyPond file.
        """
        if not isinstance(argument, str):
            if inspect.isclass(argument):
                assert issubclass(argument, _score.Component), repr(argument)
            else:
                assert isinstance(argument, _score.Component), repr(argument)
        for item in self.items:
            if isinstance(item, _score.Component):
                for context in iterate_.components(item, _score.Context):
                    if context.name == argument:
                        return context
                    if context is argument:
                        return context
                    if inspect.isclass(argument) and isinstance(context, argument):
                        return context
        score = None
        if self.score_block and self.score_block.items:
            items = self.score_block.items
            for container in iterate_.components(items, _score.Container):
                if isinstance(container, _score.Context):
                    score = container
                    break
        if isinstance(argument, str):
            for item in self.items:
                if getattr(item, "name", None) == argument:
                    return item
            if score is not None:
                if score.name == argument:
                    return score
                context = score[argument]
                return context
            raise KeyError(f"can not find item with name {argument!r}.")
        elif isinstance(argument, _score.Component):
            for item in self.items:
                if item is argument:
                    return item
            if score is not None:
                if score is argument:
                    return score
                prototype = _score.Context
                for context in iterate_.components(score, prototype):
                    if context is argument:
                        return context
            raise KeyError(f"can not find {argument}.")
        elif inspect.isclass(argument) and issubclass(argument, _score.Component):
            for item in self.items:
                if isinstance(item, argument):
                    return item
            if score is not None:
                if isinstance(score, argument):
                    return score
                prototype = _score.Context
                for context in iterate_.components(score, prototype):
                    if isinstance(context, argument):
                        return context
            raise KeyError(f"can not find item of class {argument}.")
        else:
            raise TypeError(argument)

    def __illustrate__(self) -> "LilyPondFile":
        """
        Illustrates LilyPond file.

        Returns LilyPond file unchanged.
        """
        return self

    def __repr__(self) -> str:
        """
        Gets interpreter representation of LilyPond file.
        """
        return _format.get_repr(self)

    ### PRIVATE METHODS ###

    def _get_format_pieces(self, tag=None):
        result = []
        if self.date_time_token is not None:
            string = f"% {self.date_time_token}"
            result.append(string)
        result.extend(self._get_formatted_comments())
        includes = []
        if self.lilypond_version_token is not None:
            string = f"{self.lilypond_version_token._get_lilypond_format()}"
            includes.append(string)
        if self.lilypond_language_token is not None:
            string = f"{self.lilypond_language_token._get_lilypond_format()}"
            includes.append(string)
        tag = _tag.Tag("abjad.LilyPondFile._get_format_pieces()")
        includes = _tag.double_tag(includes, self.get_tag(tag))
        includes = "\n".join(includes)
        if includes:
            result.append(includes)
        postincludes = []
        if self.use_relative_includes:
            string = "#(ly:set-option 'relative-includes #t)"
            postincludes.append(string)
        postincludes.extend(self._get_formatted_includes())
        postincludes.extend(self._get_formatted_scheme_settings())
        result.extend(postincludes)
        strings = self._get_formatted_blocks()
        if strings:
            result.append("")
        result.extend(strings)
        return result

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return _format.FormatSpecification()

    def _get_formatted_blocks(self):
        result = []
        tag = _tag.Tag("abjad.LilyPondFile._get_formatted_blocks()")
        tag = self.get_tag(tag)
        for item in self.items:
            if "_get_lilypond_format" in dir(item) and not isinstance(item, str):
                try:
                    string = item._get_lilypond_format(tag=tag)
                except TypeError:
                    string = item._get_lilypond_format()
                if string:
                    result.append(string)
            else:
                result.append(str(item))
        return result

    def _get_formatted_comments(self):
        result = []
        for comment in self.comments:
            if "_get_lilypond_format" in dir(comment) and not isinstance(comment, str):
                lilypond_format = comment._get_lilypond_format()
                if lilypond_format:
                    string = f"% {comment}"
                    result.append(string)
            else:
                string = f"% {comment!s}"
                result.append(string)
        if result:
            result = ["\n".join(result)]
        return result

    def _get_formatted_includes(self):
        result = []
        tag = _tag.Tag("abjad.LilyPondFile._get_formatted_includes()")
        tag = self.get_tag(tag)
        for include in self.includes:
            if isinstance(include, str):
                string = rf'\include "{include}"'
                result.append(string)
            elif isinstance(include, pathlib.Path):
                string = rf'\include "{include!s}"'
                result.append(string)
            elif isinstance(include, _overrides.LilyPondLiteral):
                string = str(include.argument)
                result.append(string)
            else:
                result.append(include._get_lilypond_format())
        if result:
            result = _tag.double_tag(result, tag)
            result = ["\n".join(result)]
        return result

    def _get_formatted_scheme_settings(self):
        result = []
        tag = _tag.Tag("abjad.LilyPondFile._get_formatted_scheme_settings()")
        tag = self.get_tag(tag)
        default_paper_size = self.default_paper_size
        if default_paper_size is not None:
            dimension, orientation = default_paper_size
            string = f'#(set-default-paper-size "{dimension}" \'{orientation})'
            result.append(string)
        global_staff_size = self.global_staff_size
        if global_staff_size is not None:
            string = f"#(set-global-staff-size {global_staff_size})"
            result.append(string)
        if result:
            result = _tag.double_tag(result, tag)
            result = ["\n".join(result)]
        return result

    def _get_lilypond_format(self):
        strings = self._get_format_pieces()
        string = "\n".join(strings)
        lines = []
        for line in string.split("\n"):
            if line.isspace():
                lines.append("")
            else:
                lines.append(line)
        return "\n".join(lines)

    ### PUBLIC PROPERTIES ###

    @property
    def comments(self) -> typing.List[LilyPondComment]:
        """
        Gets comments of Lilypond file.

        ..  container:: example

            >>> lilypond_file = abjad.LilyPondFile()
            >>> lilypond_file.comments
            []

        """
        return list(self._comments)

    @property
    def date_time_token(self) -> typing.Optional[DateTimeToken]:
        """
        Gets date-time token.

        ..  container:: example

            >>> lilypond_file = abjad.LilyPondFile(date_time_token=True)
            >>> lilypond_file.date_time_token
            DateTimeToken()

        """
        return self._date_time_token

    @property
    def default_paper_size(self):
        """
        Gets default paper size of LilyPond file.

        ..  container:: example

            >>> lilypond_file = abjad.LilyPondFile()
            >>> lilypond_file.default_paper_size is None
            True

        Returns pair or none.
        """
        return self._default_paper_size

    @property
    def global_staff_size(self) -> typing.Union[int, float]:
        """
        Gets global staff size of LilyPond file.

        ..  container:: example

            >>> lilypond_file = abjad.LilyPondFile()
            >>> lilypond_file.global_staff_size is None
            True

        """
        return self._global_staff_size

    @property
    def header_block(self) -> typing.Optional[Block]:
        """
        Gets header block.

        ..  container:: example

            >>> block = abjad.Block(name="header")
            >>> lilypond_file = abjad.LilyPondFile([block])
            >>> lilypond_file.header_block
            <Block(name='header')>

        """
        for item in self.items:
            if isinstance(item, Block):
                if item.name == "header":
                    return item
        return None

    @property
    def includes(self) -> typing.List[str]:
        """
        Gets includes of LilyPond file.

        ..  container:: example

            >>> lilypond_file = abjad.LilyPondFile()
            >>> lilypond_file.includes
            []

        """
        return self._includes

    @property
    def items(self) -> typing.List:
        r"""
        Gets items in LilyPond file.

        ..  container:: example

            >>> lilypond_file = abjad.LilyPondFile()
            >>> lilypond_file.items
            []

        ..  container:: example

            Accepts strings:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> score_block = abjad.Block(name="score")
            >>> score_block.items.append(staff)
            >>> lilypond_file = abjad.LilyPondFile(
            ...     lilypond_language_token=False,
            ...     lilypond_version_token=False,
            ... )
            >>> string = r"\customCommand"
            >>> lilypond_file.items.append(string)
            >>> lilypond_file.items.append(score_block)

            >>> string = abjad.lilypond(lilypond_file)
            >>> print(string)
            <BLANKLINE>
            \customCommand
            \score
            {
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }
            }

        """
        return self._items

    @property
    def layout_block(self) -> typing.Optional[Block]:
        """
        Gets layout block.

        ..  container:: example

            >>> block = abjad.Block(name="layout")
            >>> lilypond_file = abjad.LilyPondFile([block])
            >>> lilypond_file.layout_block
            <Block(name='layout')>

        """
        for item in self.items:
            if isinstance(item, Block):
                if item.name == "layout":
                    return item
        return None

    @property
    def lilypond_language_token(self) -> typing.Optional[LilyPondLanguageToken]:
        """
        Gets LilyPond language token.

        ..  container:: example

            >>> lilypond_file = abjad.LilyPondFile()
            >>> lilypond_file.lilypond_language_token
            LilyPondLanguageToken()

        """
        return self._lilypond_language_token

    @property
    def lilypond_version_token(self) -> typing.Optional[LilyPondVersionToken]:
        """
        Gets LilyPond version token.

        ..  container:: example

            >>> lilypond_file = abjad.LilyPondFile()
            >>> lilypond_file.lilypond_version_token # doctest: +SKIP
            LilyPondVersionToken('2.19.35')

        """
        return self._lilypond_version_token

    @property
    def paper_block(self) -> typing.Optional[Block]:
        """
        Gets paper block.

        ..  container:: example

            Gets paper block:

            >>> block = abjad.Block(name="paper")
            >>> lilypond_file = abjad.LilyPondFile([block])
            >>> lilypond_file.paper_block
            <Block(name='paper')>

        """
        for item in self.items:
            if isinstance(item, Block):
                if item.name == "paper":
                    return item
        return None

    @property
    def score_block(self) -> typing.Optional[Block]:
        """
        Gets score block.

        ..  container:: example

            >>> block = abjad.Block(name="score")
            >>> lilypond_file = abjad.LilyPondFile([block])
            >>> lilypond_file.score_block
            <Block(name='score')>

        """
        for item in self.items:
            if isinstance(item, Block):
                if item.name == "score":
                    return item
        return None

    @property
    def use_relative_includes(self) -> typing.Optional[bool]:
        """
        Is true when LilyPond file should use relative includes.

        ..  container:: example

            >>> lilypond_file = abjad.LilyPondFile()
            >>> lilypond_file.use_relative_includes is None
            True

        """
        return self._use_relative_includes

    ### PUBLIC METHODS ###

    def get_tag(self, site=None):
        """
        Gets tag.
        """
        tag = _tag.Tag(self._tag)
        tag = tag.append(site)
        return tag
