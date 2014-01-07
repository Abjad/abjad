# -*- encoding: utf-8 -*-
from abjad.tools import lilypondnametools
from abjad.tools.lilypondfiletools.Block import Block
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import set_


class ContextBlock(Block):
    r'''A LilyPond file context block.

    ..  container:: example

        ::

            >>> block = lilypondfiletools.ContextBlock(
            ...     source_context_name='Staff',
            ...     name='FluteStaff',
            ...     type_='Engraver_group',
            ...     alias='Staff',
            ...     )
            >>> block.engraver_removals.append('Forbid_line_break_engraver')
            >>> block.engraver_consists.append('Horizontal_bracket_engraver')
            >>> block.accepts.append('FluteUpperVoice')
            >>> block.accepts.append('FluteLowerVoice')
            >>> override(block).beam.positions = (-4, -4)
            >>> override(block).stem.stem_end_position = -6
            >>> set_(block).auto_beaming = False
            >>> set_(block).tuplet_full_length = True

        ::

            >>> print format(block)
            \context {
                \Staff
                \name FluteStaff
                \type Engraver_group
                \alias Staff
                \remove Forbid_line_break_engraver
                \consists Horizontal_bracket_engraver
                \accepts FluteUpperVoice
                \accepts FluteLowerVoice
                \override Beam #'positions = #'(-4 . -4)
                \override Stem #'stem-end-position = #-6
                autoBeaming = ##f
                tupletFullLength = ##t
            }

    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        source_context_name=None,
        name=None,
        type_=None,
        alias=None,
        ):
        Block.__init__(self, name='context')
        self._source_context_name = source_context_name
        self._name = name
        self._type_ = type_
        self._alias = alias
        self._accepts = []
        self._engraver_consists = []
        self._engraver_removals = []

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        from abjad.tools import systemtools
        result = []
        string = '{} {{'.format(self._escaped_name)
        result.append(string)
        manager = systemtools.LilyPondFormatManager
        # CAUTION: source context name must come before type_ to allow 
        # context redefinition.
        if self.source_context_name is not None:
            string = '\t' + r'\{}'.format(self.source_context_name)
            result.append(string)
        if self.name is not None:
            string = '\t' + r'\name {}'.format(self.name)
            result.append(string)
        if self.type_ is not None:
            string = '\t' + r'\type {}'.format(self.type_)
            result.append(string)
        if self.alias is not None:
            string = '\t' + r'\alias {}'.format(self.alias)
            result.append(string)
        for statement in self.engraver_removals:
            string = '\t' + r'\remove {}'.format(statement)
            result.append(string)
        # CAUTION: LilyPond \consists statements are order-significant!
        for statement in self.engraver_consists:
            string = '\t' + r'\consists {}'.format(statement)
            result.append(string)
        for statement in self.accepts:
            string = '\t' + r'\accepts {}'.format(statement)
            result.append(string)
        overrides = override(self)._list_format_contributions('override')
        for statement in overrides:
            string = '\t' + statement
            result.append(string)
        setting_contributions = []
        for key, value in set_(self)._get_attribute_tuples():
            setting_contribution = \
                manager.format_lilypond_context_setting_in_with_block(
                    key, value)
            setting_contributions.append(setting_contribution)
        for setting_contribution in sorted(setting_contributions):
            string = '\t' + setting_contribution
            result.append(string)
        result.append('}')
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def accepts(self):
        r'''Gets arguments of LilyPond ``\accepts`` commands.

        ..  container:: example

            >>> block.accepts
            ['FluteUpperVoice', 'FluteLowerVoice']

        Returns list.
        '''
        return self._accepts

    @property
    def engraver_consists(self):
        r'''Gets arguments of LilyPond ``\consists`` commands.

        ..  container:: example

            >>> block.engraver_consists
            ['Horizontal_bracket_engraver']

        Returns list.
        '''
        return self._engraver_consists

    @property
    def engraver_removals(self):
        r'''Gets arguments of LilyPond ``\remove`` commands.

        ..  container:: example

            >>> block.engraver_removals
            ['Forbid_line_break_engraver']

        Returns list.
        '''
        return self._engraver_removals

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        r'''Gets and sets argument of LilyPond ``\alias`` command.

        ..  container:: example

            >>> block.alias
            'Staff'

        Returns string or none.
        '''
        return self._alias

    @property
    def items(self):
        r'''Gets items in context block.

        ::

            >>> block.items
            []

        Returns list.
        '''
        return self._items

    @property
    def name(self):
        r'''Gets and sets argument of LilyPond ``\name`` command.

        ..  container:: example

            >>> block.name
            'FluteStaff'

        Returns string or none.
        '''
        return self._name

    @property
    def source_context_name(self):
        r'''Gets and sets source context name.

        ..  container:: example

            >>> block.source_context_name
            'Staff'

        Returns string or none.
        '''
        return self._source_context_name

    @property
    def type_(self):
        r'''Gets and sets argument of LilyPond ``\type`` command.

        ..  container:: example

            >>> block.type_
            'Engraver_group'

        Returns string or none.
        '''
        return self._type_
