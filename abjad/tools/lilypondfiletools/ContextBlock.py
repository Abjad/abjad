from .Block import Block


class ContextBlock(Block):
    r"""
    A LilyPond file ``\context`` block.

    ..  container:: example

        >>> block = abjad.ContextBlock(
        ...     source_lilypond_type='Staff',
        ...     name='FluteStaff',
        ...     type_='Engraver_group',
        ...     alias='Staff',
        ...     )
        >>> block.remove_commands.append('Forbid_line_break_engraver')
        >>> block.consists_commands.append('Horizontal_bracket_engraver')
        >>> block.accepts_commands.append('FluteUpperVoice')
        >>> block.accepts_commands.append('FluteLowerVoice')
        >>> block.items.append(r'\accidentalStyle dodecaphonic')
        >>> abjad.override(block).beam.positions = (-4, -4)
        >>> abjad.override(block).stem.stem_end_position = -6
        >>> abjad.setting(block).auto_beaming = False
        >>> abjad.setting(block).tuplet_full_length = True
        >>> block
        <ContextBlock(source_lilypond_type='Staff', name='FluteStaff', type_='Engraver_group', alias='Staff')>

        >>> print(format(block))
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
            \override Stem.stem-end-position = #-6
            autoBeaming = ##f
            tupletFullLength = ##t
            \accidentalStyle dodecaphonic
        }

    """

    ### INITIALIZER ###

    def __init__(
        self,
        source_lilypond_type=None,
        name=None,
        type_=None,
        alias=None,
        ):
        Block.__init__(self, name='context')
        self._source_lilypond_type = source_lilypond_type
        self._name = name
        self._type_ = type_
        self._alias = alias
        self._accepts_commands = []
        self._consists_commands = []
        self._remove_commands = []

    ### PRIVATE METHODS ###

    def _get_format_pieces(self):
        import abjad
        indent = abjad.LilyPondFormatManager.indent
        result = []
        string = '{} {{'.format(self._escaped_name)
        result.append(string)
        manager = abjad.LilyPondFormatManager
        # CAUTION: source context name must come before type_ to allow
        # context redefinition.
        if self.source_lilypond_type is not None:
            string = indent + r'\{}'.format(self.source_lilypond_type)
            result.append(string)
        if self.name is not None:
            string = indent + r'\name {}'.format(self.name)
            result.append(string)
        if self.type_ is not None:
            string = indent + r'\type {}'.format(self.type_)
            result.append(string)
        if self.alias is not None:
            string = indent + r'\alias {}'.format(self.alias)
            result.append(string)
        for statement in self.remove_commands:
            string = indent + r'\remove {}'.format(statement)
            result.append(string)
        # CAUTION: LilyPond \consists statements are order-significant!
        for statement in self.consists_commands:
            string = indent + r'\consists {}'.format(statement)
            result.append(string)
        for statement in self.accepts_commands:
            string = indent + r'\accepts {}'.format(statement)
            result.append(string)
        overrides = abjad.override(self)._list_format_contributions('override')
        for statement in overrides:
            string = indent + statement
            result.append(string)
        setting_contributions = []
        for key, value in abjad.setting(self)._get_attribute_tuples():
            setting_contribution = \
                manager.format_lilypond_context_setting_in_with_block(
                    key, value)
            setting_contributions.append(setting_contribution)
        for setting_contribution in sorted(setting_contributions):
            string = indent + setting_contribution
            result.append(string)
        for item in self.items:
            if isinstance(item, str):
                string = indent + '{}'.format(item)
                result.append(string)
            elif '_get_format_pieces' in dir(item):
                pieces = item._get_format_pieces()
                pieces = [indent + item for item in pieces]
                result.extend(pieces)
            else:
                pass
        result.append('}')
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def accepts_commands(self):
        r"""
        Gets arguments of LilyPond ``\accepts`` commands.

        ..  container:: example

            >>> block = abjad.ContextBlock(
            ...     source_lilypond_type='Staff',
            ...     name='FluteStaff',
            ...     type_='Engraver_group',
            ...     alias='Staff',
            ...     )
            >>> block.remove_commands.append('Forbid_line_break_engraver')
            >>> block.consists_commands.append('Horizontal_bracket_engraver')
            >>> block.accepts_commands.append('FluteUpperVoice')
            >>> block.accepts_commands.append('FluteLowerVoice')
            >>> block.items.append(r'\accidentalStyle dodecaphonic')
            >>> abjad.override(block).beam.positions = (-4, -4)
            >>> abjad.override(block).stem.stem_end_position = -6
            >>> abjad.setting(block).auto_beaming = False
            >>> abjad.setting(block).tuplet_full_length = True

            >>> block.accepts_commands
            ['FluteUpperVoice', 'FluteLowerVoice']

        Returns list.
        """
        return self._accepts_commands

    @property
    def alias(self):
        r"""
        Gets and sets argument of LilyPond ``\alias`` command.

        ..  container:: example

            >>> block = abjad.ContextBlock(
            ...     source_lilypond_type='Staff',
            ...     name='FluteStaff',
            ...     type_='Engraver_group',
            ...     alias='Staff',
            ...     )
            >>> block.remove_commands.append('Forbid_line_break_engraver')
            >>> block.consists_commands.append('Horizontal_bracket_engraver')
            >>> block.accepts_commands.append('FluteUpperVoice')
            >>> block.accepts_commands.append('FluteLowerVoice')
            >>> block.items.append(r'\accidentalStyle dodecaphonic')
            >>> abjad.override(block).beam.positions = (-4, -4)
            >>> abjad.override(block).stem.stem_end_position = -6
            >>> abjad.setting(block).auto_beaming = False
            >>> abjad.setting(block).tuplet_full_length = True

            >>> block.alias
            'Staff'

        Returns string or none.
        """
        return self._alias

    @property
    def consists_commands(self):
        r"""
        Gets arguments of LilyPond ``\consists`` commands.

        ..  container:: example

            >>> block = abjad.ContextBlock(
            ...     source_lilypond_type='Staff',
            ...     name='FluteStaff',
            ...     type_='Engraver_group',
            ...     alias='Staff',
            ...     )
            >>> block.remove_commands.append('Forbid_line_break_engraver')
            >>> block.consists_commands.append('Horizontal_bracket_engraver')
            >>> block.accepts_commands.append('FluteUpperVoice')
            >>> block.accepts_commands.append('FluteLowerVoice')
            >>> block.items.append(r'\accidentalStyle dodecaphonic')
            >>> abjad.override(block).beam.positions = (-4, -4)
            >>> abjad.override(block).stem.stem_end_position = -6
            >>> abjad.setting(block).auto_beaming = False
            >>> abjad.setting(block).tuplet_full_length = True

            >>> block.consists_commands
            ['Horizontal_bracket_engraver']

        Returns list.
        """
        return self._consists_commands

    @property
    def items(self):
        r"""
        Gets items in context block.

        ..  container:: example

            >>> block = abjad.ContextBlock(
            ...     source_lilypond_type='Staff',
            ...     name='FluteStaff',
            ...     type_='Engraver_group',
            ...     alias='Staff',
            ...     )
            >>> block.remove_commands.append('Forbid_line_break_engraver')
            >>> block.consists_commands.append('Horizontal_bracket_engraver')
            >>> block.accepts_commands.append('FluteUpperVoice')
            >>> block.accepts_commands.append('FluteLowerVoice')
            >>> block.items.append(r'\accidentalStyle dodecaphonic')
            >>> abjad.override(block).beam.positions = (-4, -4)
            >>> abjad.override(block).stem.stem_end_position = -6
            >>> abjad.setting(block).auto_beaming = False
            >>> abjad.setting(block).tuplet_full_length = True

            >>> block.items
            ['\\accidentalStyle dodecaphonic']

        Returns list.
        """
        return self._items

    @property
    def name(self):
        r"""
        Gets and sets argument of LilyPond ``\name`` command.

        ..  container:: example

            >>> block = abjad.ContextBlock(
            ...     source_lilypond_type='Staff',
            ...     name='FluteStaff',
            ...     type_='Engraver_group',
            ...     alias='Staff',
            ...     )
            >>> block.remove_commands.append('Forbid_line_break_engraver')
            >>> block.consists_commands.append('Horizontal_bracket_engraver')
            >>> block.accepts_commands.append('FluteUpperVoice')
            >>> block.accepts_commands.append('FluteLowerVoice')
            >>> block.items.append(r'\accidentalStyle dodecaphonic')
            >>> abjad.override(block).beam.positions = (-4, -4)
            >>> abjad.override(block).stem.stem_end_position = -6
            >>> abjad.setting(block).auto_beaming = False
            >>> abjad.setting(block).tuplet_full_length = True

            >>> block.name
            'FluteStaff'

        Returns string or none.
        """
        return self._name

    @property
    def remove_commands(self):
        r"""
        Gets arguments of LilyPond ``\remove`` commands.

        ..  container:: example

            >>> block = abjad.ContextBlock(
            ...     source_lilypond_type='Staff',
            ...     name='FluteStaff',
            ...     type_='Engraver_group',
            ...     alias='Staff',
            ...     )
            >>> block.remove_commands.append('Forbid_line_break_engraver')
            >>> block.consists_commands.append('Horizontal_bracket_engraver')
            >>> block.accepts_commands.append('FluteUpperVoice')
            >>> block.accepts_commands.append('FluteLowerVoice')
            >>> block.items.append(r'\accidentalStyle dodecaphonic')
            >>> abjad.override(block).beam.positions = (-4, -4)
            >>> abjad.override(block).stem.stem_end_position = -6
            >>> abjad.setting(block).auto_beaming = False
            >>> abjad.setting(block).tuplet_full_length = True

            >>> block.remove_commands
            ['Forbid_line_break_engraver']

        Returns list.
        """
        return self._remove_commands

    @property
    def source_lilypond_type(self):
        r"""
        Gets and sets source context name.

        ..  container:: example

            >>> block = abjad.ContextBlock(
            ...     source_lilypond_type='Staff',
            ...     name='FluteStaff',
            ...     type_='Engraver_group',
            ...     alias='Staff',
            ...     )
            >>> block.remove_commands.append('Forbid_line_break_engraver')
            >>> block.consists_commands.append('Horizontal_bracket_engraver')
            >>> block.accepts_commands.append('FluteUpperVoice')
            >>> block.accepts_commands.append('FluteLowerVoice')
            >>> block.items.append(r'\accidentalStyle dodecaphonic')
            >>> abjad.override(block).beam.positions = (-4, -4)
            >>> abjad.override(block).stem.stem_end_position = -6
            >>> abjad.setting(block).auto_beaming = False
            >>> abjad.setting(block).tuplet_full_length = True

            >>> block.source_lilypond_type
            'Staff'

        Returns string or none.
        """
        return self._source_lilypond_type

    @property
    def type_(self):
        r"""
        Gets and sets argument of LilyPond ``\type`` command.

        ..  container:: example

            >>> block = abjad.ContextBlock(
            ...     source_lilypond_type='Staff',
            ...     name='FluteStaff',
            ...     type_='Engraver_group',
            ...     alias='Staff',
            ...     )
            >>> block.remove_commands.append('Forbid_line_break_engraver')
            >>> block.consists_commands.append('Horizontal_bracket_engraver')
            >>> block.accepts_commands.append('FluteUpperVoice')
            >>> block.accepts_commands.append('FluteLowerVoice')
            >>> block.items.append(r'\accidentalStyle dodecaphonic')
            >>> abjad.override(block).beam.positions = (-4, -4)
            >>> abjad.override(block).stem.stem_end_position = -6
            >>> abjad.setting(block).auto_beaming = False
            >>> abjad.setting(block).tuplet_full_length = True

            >>> block.type_
            'Engraver_group'

        Returns string or none.
        """
        return self._type_
