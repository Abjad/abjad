import collections
import copy
import importlib
import inspect
import numbers
import os
import pathlib
import subprocess
import time
import typing

from . import _inspect
from . import tag as _tag
from .attach import attach
from .bundle import LilyPondFormatBundle
from .configuration import Configuration
from .contextmanagers import TemporaryDirectoryChange
from .indicators.LilyPondComment import LilyPondComment
from .indicators.TimeSignature import TimeSignature
from .iterate import Iteration
from .lilypond import lilypond
from .markups import Markup
from .overrides import LilyPondLiteral, override, setting
from .pitch.pitches import NamedPitch
from .score import Component, Container, Context, Leaf, Score, Skip, Staff, Voice
from .select import Selection
from .sequence import Sequence
from .storage import FormatSpecification, StorageFormatManager

configuration = Configuration()


class Block:
    r"""
    LilyPond file block.

    ..  container:: example

        REGRESSION. Blocks remember attribute assignment order.

        Here right margin precedes left margin even though left margin
        alphabetizes before right margin:

        >>> block = abjad.Block(name="paper")
        >>> block.right_margin = abjad.LilyPondDimension(2, "cm")
        >>> block.left_margin = abjad.LilyPondDimension(2, "cm")
        >>> block
        <Block(name='paper')>

        >>> string = abjad.lilypond(block)
        >>> print(string)
        \paper {
            right-margin = 2\cm
            left-margin = 2\cm
        }

    ..  container:: example

        >>> block = abjad.Block(name='score')
        >>> markup = abjad.Markup('foo')
        >>> block.items.append(markup)
        >>> block
        <Block(name='score')>

        >>> string = abjad.lilypond(block)
        >>> print(string)
        \score {
            {
                \markup { foo }
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
        return StorageFormatManager(self).get_repr_format()

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
        indent = LilyPondFormatBundle.indent * depth
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
        indent = LilyPondFormatBundle.indent
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
        string = f"{self._escaped_name} {{"
        if tag is not None:
            strings = _tag.tag([string], tag=tag)
            string = strings[0]
        result.append(string)
        for item in self.items:
            if isinstance(item, ContextBlock):
                continue
            if isinstance(item, (Leaf, Markup)):
                item = [item]
            result.extend(self._format_item(item))
        formatted_attributes = self._get_formatted_user_attributes()
        formatted_attributes = [indent + _ for _ in formatted_attributes]
        result.extend(formatted_attributes)
        formatted_context_blocks = self._formatted_context_blocks()
        formatted_context_blocks = [indent + _ for _ in formatted_context_blocks]
        result.extend(formatted_context_blocks)
        string = "}"
        if tag is not None:
            strings = _tag.tag([string], tag=tag)
            string = strings[0]
        result.append(string)

        return result

    def _get_format_specification(self):
        return FormatSpecification(
            client=self, repr_is_bracketed=True, repr_is_indented=False
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
            if isinstance(value, Markup):
                formatted_value = value._get_format_pieces()
            elif isinstance(value, LilyPondDimension):
                formatted_value = [lilypond(value)]
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
            >>> markup = abjad.Markup("foo")
            >>> block.items.append(markup)

            >>> block.items
            [Markup(contents=['foo'])]

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
            \score {
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
            >>> markup = abjad.Markup("foo")
            >>> block.items.append(markup)

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

        >>> print(abjad.lilypond(block))
        \context {
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
        indent = LilyPondFormatBundle.indent
        result = []
        string = f"{self._escaped_name} {{"
        result.append(string)
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
        overrides = override(self)._list_format_contributions("override")
        for statement in overrides:
            string = indent + statement
            result.append(string)
        setting_contributions = setting(self)._format_in_with_block()
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
        return StorageFormatManager(self).get_repr_format()

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

        >>> print(abjad.lilypond(token))  # doctest: +SKIP
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
        return StorageFormatManager(self).get_repr_format()

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
        with TemporaryDirectoryChange(path):
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
        >>> includes = [
        ...     "external-settings-file-1.ily",
        ...     "external-settings-file-2.ily",
        ... ]
        >>> lilypond_file = abjad.LilyPondFile(
        ...     items=[staff],
        ...     default_paper_size=("a5", "portrait"),
        ...     comments=comments,
        ...     includes=includes,
        ...     global_staff_size=16,
        ... )

        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ::

            >>> print(abjad.lilypond(lilypond_file)) # doctest: +SKIP
            % File construct as an example.
            % Parts shown here for positioning.
            <BLANKLINE>
            \version "2.23.0"
            \language "english"
            <BLANKLINE>
            \include "external-settings-file-1.ily"
            \include "external-settings-file-2.ily"
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
        comments=None,
        date_time_token=None,
        default_paper_size=None,
        global_staff_size=None,
        includes=None,
        items=None,
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
            >>> lilypond_file = abjad.LilyPondFile(items=[staff])

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

    def __getitem__(self, name):
        r"""
        Gets item with ``name``.

        ..  container:: example

            Searches score:

            >>> voice_1 = abjad.Voice("c''4 b' a' g'", name="Custom_Voice_1")
            >>> literal = abjad.LilyPondLiteral(r"\voiceOne", "opening")
            >>> abjad.attach(literal, voice_1)
            >>> voice_2 = abjad.Voice("c'4 d' e' f'", name="Custom_Voice_2")
            >>> literal = abjad.LilyPondLiteral(r"\voiceTwo", "opening")
            >>> abjad.attach(literal, voice_2)
            >>> staff = abjad.Staff(
            ...     [voice_1, voice_2],
            ...     simultaneous=True,
            ...     name="Custom_Staff",
            ... )
            >>> score = abjad.Score([staff], name="Custom_Score")
            >>> block = abjad.Block(name="score")
            >>> block.items.append(score)
            >>> lilypond_file = abjad.LilyPondFile(items=[block])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Custom_Score"
                <<
                    \context Staff = "Custom_Staff"
                    <<
                        \context Voice = "Custom_Voice_1"
                        {
                            \voiceOne
                            c''4
                            b'4
                            a'4
                            g'4
                        }
                        \context Voice = "Custom_Voice_2"
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

            >>> lilypond_file["Custom_Score"]
            <Score-"Custom_Score"<<1>>>

            >>> lilypond_file[abjad.Score]
            <Score-"Custom_Score"<<1>>>

            >>> lilypond_file["Custom_Staff"]
            <Staff-"Custom_Staff"<<2>>>

            >>> lilypond_file[abjad.Staff]
            <Staff-"Custom_Staff"<<2>>>

            >>> lilypond_file["Custom_Voice_1"]
            Voice("c''4 b'4 a'4 g'4", name='Custom_Voice_1')

            >>> lilypond_file["Custom_Voice_2"]
            Voice("c'4 d'4 e'4 f'4", name='Custom_Voice_2')

            >>> lilypond_file[abjad.Voice]
            Voice("c''4 b'4 a'4 g'4", name='Custom_Voice_1')

        ..  container:: example

            REGRESSION. Works when score block contains parallel container:

                >>> include_container = abjad.Container()
                >>> string = r'\include "layout.ly"'
                >>> literal = abjad.LilyPondLiteral(string, "opening")
                >>> abjad.attach(literal, include_container)
                >>> staff = abjad.Staff("c'4 d' e' f'", name="Custom_Staff")
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
                \score {
                    <<
                        {
                            \include "layout.ly"
                        }
                        \context Staff = "Custom_Staff"
                        {
                            c'4
                            d'4
                            e'4
                            f'4
                        }
                    >>
                }

                >>> lilypond_file[abjad.Staff]
                Staff("c'4 d'4 e'4 f'4", name='Custom_Staff')

                >>> lilypond_file['Custom_Staff']
                Staff("c'4 d'4 e'4 f'4", name='Custom_Staff')

        Returns item.

        Raises key error when no item with ``name`` is found.
        """
        if not isinstance(name, str):
            if inspect.isclass(name):
                assert issubclass(name, Component), repr(name)
            else:
                assert isinstance(name, Component), repr(name)
        score = None
        if self.score_block and self.score_block.items:
            items = self.score_block.items
            for container in Iteration(items).components(Container):
                if isinstance(container, Context):
                    score = container
                    break
        if isinstance(name, str):
            for item in self.items:
                if getattr(item, "name", None) == name:
                    return item
            if score is not None:
                if score.name == name:
                    return score
                context = score[name]
                return context
            raise KeyError(f"can not find item with name {name!r}.")
        elif isinstance(name, Component):
            for item in self.items:
                if item is name:
                    return item
            if score is not None:
                if score is name:
                    return score
                prototype = Context
                for context in Iteration(score).components(prototype):
                    if context is name:
                        return context
            raise KeyError(f"can not find {name}.")
        elif inspect.isclass(name) and issubclass(name, Component):
            for item in self.items:
                if isinstance(item, name):
                    return item
            if score is not None:
                if isinstance(score, name):
                    return score
                prototype = Context
                for context in Iteration(score).components(prototype):
                    if isinstance(context, name):
                        return context
            raise KeyError(f"can not find item of class {name}.")
        else:
            raise TypeError(name)

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
        return StorageFormatManager(self).get_repr_format()

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
        includes = _tag.tag(includes, tag=self.get_tag(tag))
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
        result.extend(self._get_formatted_blocks())
        return result

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return FormatSpecification(client=self)

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
            elif isinstance(include, LilyPondLiteral):
                string = str(include.argument)
                result.append(string)
            else:
                result.append(include._get_lilypond_format())
        if result:
            result = _tag.tag(result, tag=tag)
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
            result = _tag.tag(result, tag=tag)
            result = ["\n".join(result)]
        return result

    def _get_lilypond_format(self):
        string = "\n\n".join(self._get_format_pieces())
        lines = []
        for line in string.split("\n"):
            if line.isspace():
                lines.append("")
            else:
                lines.append(line)
        return "\n".join(lines)

    @staticmethod
    def _make_global_context_block(font_size=3, minimum_distance=10, padding=4):
        assert isinstance(font_size, (int, float))
        assert isinstance(padding, (int, float))
        block = ContextBlock(name="Global_Context", type_="Engraver_group")
        block.consists_commands.append("Axis_group_engraver")
        block.consists_commands.append("Time_signature_engraver")
        time_signature_grob = override(block).time_signature
        time_signature_grob.X_extent = (0, 0)
        time_signature_grob.X_offset = "#ly:self-alignment-interface::x-aligned-on-self"
        time_signature_grob.Y_extent = (0, 0)
        time_signature_grob.break_align_symbol = False
        time_signature_grob.break_visibility = "#end-of-line-invisible"
        time_signature_grob.font_size = font_size
        time_signature_grob.self_alignment_X = "#center"
        grob = override(block).vertical_axis_group
        string = "#'((basic-distance . 0) (minimum-distance . {minimum_distance}) (padding . {padding}) (stretchability . 0))"
        grob.default_staff_staff_spacing = string
        return block

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
            >>> lilypond_file = abjad.LilyPondFile(items=[block])
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
            \customCommand
            <BLANKLINE>
            \score {
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
            >>> lilypond_file = abjad.LilyPondFile(items=[block])
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
            >>> lilypond_file = abjad.LilyPondFile(items=[block])
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
            >>> lilypond_file = abjad.LilyPondFile(items=[block])
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

    @classmethod
    def rhythm(
        class_,
        selections,
        divisions=None,
        attach_lilypond_voice_commands=None,
        implicit_scaling=None,
        pitched_staff=None,
        simultaneous_selections=None,
        time_signatures=None,
    ) -> "LilyPondFile":
        r"""
        Makes rhythm-styled LilyPond file.

        ..  container:: example

            Makes rhythmic staff:

            >>> divisions = [(3, 4), (4, 8), (1, 4)]
            >>> maker = abjad.NoteMaker()
            >>> selections = [
            ...     maker(6 * [0], [(1, 8)]),
            ...     maker(8 * [0], [(1, 16)]),
            ...     maker(2 * [0], [(1, 8)]),
            ... ]
            >>> for selection in selections:
            ...     abjad.beam(selection[:])
            ...
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file[abjad.Score]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 3/4
                        s1 * 3/4
                        \time 4/8
                        s1 * 1/2
                        \time 1/4
                        s1 * 1/4
                    }
                    \new RhythmicStaff
                    {
                        c'8
                        [
                        c'8
                        c'8
                        c'8
                        c'8
                        c'8
                        ]
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                        c'8
                        [
                        c'8
                        ]
                    }
                >>

        ..  container:: example

            Set time signatures explicitly:

            >>> divisions = [(3, 4), (4, 8), (1, 4)]
            >>> maker = abjad.NoteMaker()
            >>> selections = [
            ...     maker(6 * [0], [(1, 8)]),
            ...     maker(8 * [0], [(1, 16)]),
            ...     maker(2 * [0], [(1, 8)]),
            ... ]
            >>> for selection in selections:
            ...     abjad.beam(selection[:])
            ...
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     [(6, 8), (4, 8), (2, 8)],
            ... )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file[abjad.Score]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 6/8
                        s1 * 3/4
                        \time 4/8
                        s1 * 1/2
                        \time 2/8
                        s1 * 1/4
                    }
                    \new RhythmicStaff
                    {
                        c'8
                        [
                        c'8
                        c'8
                        c'8
                        c'8
                        c'8
                        ]
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                        c'8
                        [
                        c'8
                        ]
                    }
                >>

        ..  container:: example

            Makes pitched staff:

            >>> divisions = [(3, 4), (4, 8), (1, 4)]
            >>> maker = abjad.NoteMaker()
            >>> selections = [
            ...     maker(6 * [0], [(1, 8)]),
            ...     maker(8 * [0], [(1, 16)]),
            ...     maker(2 * [0], [(1, 8)]),
            ... ]
            >>> for selection in selections:
            ...     abjad.beam(selection[:])
            ...
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     pitched_staff=True,
            ... )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 3/4
                        s1 * 3/4
                        \time 4/8
                        s1 * 1/2
                        \time 1/4
                        s1 * 1/4
                    }
                    \new Staff
                    {
                        c'8
                        [
                        c'8
                        c'8
                        c'8
                        c'8
                        c'8
                        ]
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                        c'8
                        [
                        c'8
                        ]
                    }
                >>

        ..  container:: example

            Makes simultaneous voices:

            >>> divisions = [(3, 4), (4, 8), (1, 4)]
            >>> maker = abjad.NoteMaker()
            >>> selections = [
            ...     maker(6 * [0], [(1, 8)]),
            ...     maker(8 * [0], [(1, 16)]),
            ...     maker(2 * [0], [(1, 8)]),
            ... ]
            >>> for selection in selections:
            ...     abjad.beam(selection[:])
            ...
            >>> for note in abjad.iterate(selections).components(abjad.Note):
            ...     note.written_pitch = abjad.NamedPitch("e'")
            ...
            >>> selection_1 = selections[0] + selections[1] + selections[2]
            >>> selections = [
            ...     maker(12 * [0], [(1, 16)]),
            ...     maker(16 * [0], [(1, 32)]),
            ...     maker(4 * [0], [(1, 16)]),
            ... ]
            >>> for selection in selections:
            ...     abjad.beam(selection[:])
            ...
            >>> selection_2 = selections[0] + selections[1] + selections[2]
            >>> selections = {
            ...     "Voice_1": selection_1,
            ...     "Voice_2": selection_2,
            ... }
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ... )
            >>> voice_1 = lilypond_file["Voice_1"]
            >>> literal = abjad.LilyPondLiteral(r"\voiceOne", "opening")
            >>> abjad.attach(literal, voice_1)
            >>> voice_2 = lilypond_file["Voice_2"]
            >>> literal = abjad.LilyPondLiteral(r"\voiceTwo", "opening")
            >>> abjad.attach(literal, voice_2)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 3/4
                        s1 * 1/2
                        s1 * 1/4
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            e'8
                            [
                            e'8
                            e'8
                            e'8
                            e'8
                            e'8
                            ]
                            e'16
                            [
                            e'16
                            e'16
                            e'16
                            e'16
                            e'16
                            e'16
                            e'16
                            ]
                            e'8
                            [
                            e'8
                            ]
                        }
                        \context Voice = "Voice_2"
                        {
                            \voiceTwo
                            c'16
                            [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            ]
                            c'32
                            [
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            ]
                            c'16
                            [
                            c'16
                            c'16
                            c'16
                            ]
                        }
                    >>
                >>

        """
        if isinstance(selections, Selection):
            pass
        elif isinstance(selections, list):
            for selection in selections:
                if not isinstance(selection, Selection):
                    raise TypeError(f"must be selection: {selection!r}.")
        elif isinstance(selections, dict):
            for selection in selections.values():
                if not isinstance(selection, Selection):
                    raise TypeError(f"must be selection: {selection!r}.")
        else:
            raise TypeError(f"must be list or dictionary: {selections!r}.")
        score = Score()
        lilypond_file = class_(
            includes=["default.ily", "rhythm-maker-docs.ily"],
            items=[
                Block(name="header"),
                Block(name="layout"),
                Block(name="paper"),
                Block(name="score"),
            ],
        )
        assert lilypond_file.header_block is not None
        lilypond_file.header_block.tagline = "##f"
        assert lilypond_file.score_block is not None
        lilypond_file.score_block.items.append(score)
        if pitched_staff is None:
            if isinstance(selections, (list, Selection)):
                selections_ = selections
            elif isinstance(selections, dict):
                selections_ = list(selections.values())
            else:
                raise TypeError(selections)
            notes = Selection(selections_).notes()
            assert isinstance(notes, Selection)
            for note in notes:
                if note.written_pitch != NamedPitch("c'"):
                    pitched_staff = True
                    break
            chords = Selection(selections_).chords()
            if chords:
                pitched_staff = True
        if isinstance(selections, (list, Selection)):
            if divisions is None:
                duration = _inspect._get_duration(selections)
                divisions = [duration]
            time_signatures = time_signatures or divisions
            time_signatures = [TimeSignature(_) for _ in time_signatures]
            if pitched_staff:
                staff = Staff()
            else:
                staff = Staff(lilypond_type="RhythmicStaff")
            staff.extend(selections)
        elif isinstance(selections, dict):
            voices = []
            for voice_name in sorted(selections):
                selections_ = selections[voice_name]
                selections_ = Sequence(selections_).flatten(depth=-1)
                selections_ = copy.deepcopy(selections_)
                voice = Voice(selections_, name=voice_name)
                if attach_lilypond_voice_commands:
                    voice_name_to_command_string = {
                        "Voice_1": "voiceOne",
                        "Voice_2": "voiceTwo",
                        "Voice_3": "voiceThree",
                        "Voice_4": "voiceFour",
                    }
                    command_string = voice_name_to_command_string.get(voice_name)
                    if command_string:
                        command = LilyPondLiteral("\\" + command_string)
                        attach(command, voice)
                voices.append(voice)
            staff = Staff(voices, simultaneous=True)
            if divisions is None:
                duration = staff._get_duration()
                divisions = [duration]
        else:
            message = "must be list or dictionary of selections:"
            message += f" {selections!r}."
            raise TypeError(message)
        score.append(staff)
        assert isinstance(divisions, collections.abc.Sequence), repr(divisions)
        time_signatures = time_signatures or divisions
        context = Context(lilypond_type="GlobalContext")
        skips = []
        for time_signature in time_signatures:
            skip = Skip(1)
            skip.multiplier = time_signature
            attach(time_signature, skip, context="Score")
            skips.append(skip)
        context.extend(skips)
        score.insert(0, context)
        return lilypond_file
