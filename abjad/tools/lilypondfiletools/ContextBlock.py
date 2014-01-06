# -*- encoding: utf-8 -*-
from abjad.tools import lilypondnametools
from abjad.tools.lilypondfiletools.Block import Block
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import contextualize


class ContextBlock(Block):
    r'''A LilyPond file context block.

    ..  container:: example

        ::

            >>> block = lilypondfiletools.ContextBlock()
            >>> block.source_context_name = 'Score'
            >>> override(block).bar_number.transparent = True
            >>> scheme = schemetools.Scheme('end-of-line-invisible')
            >>> override(block).time_signature.break_visibility = scheme
            >>> moment = schemetools.SchemeMoment((1, 45))
            >>> contextualize(block).proportionalNotationDuration = moment

        ::

            >>> print format(block)
            \context {
                \Score
                \override BarNumber #'transparent = ##t
                \override TimeSignature #'break-visibility = #end-of-line-invisible
                proportionalNotationDuration = #(ly:make-moment 1 45)
            }

    '''

    ### INITIALIZER ###

    def __init__(self, source_context_name=None):
        Block.__init__(self, name='context')
        self._accepts = []
        self._engraver_consists = []
        self._engraver_removals = []
        self.alias = None
        self.source_context_name = source_context_name
        self.name = None
        self.type = None

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        from abjad.tools import systemtools
        result = []
        string = '{} {{'.format(self._escaped_name)
        result.append(string)
        manager = systemtools.LilyPondFormatManager
        # CAUTION: source context name must come before type to allow 
        # context redefinition.
        # TODO: rename self.source_context_name to self.source_source_context_name
        if self.source_context_name is not None:
            string = '\t' + r'\{}'.format(self.source_context_name)
            result.append(string)
        if self.name is not None:
            string = '\t' + r'\name {}'.format(self.name)
            result.append(string)
        if self.type is not None:
            string = '\t' + r'\type {}'.format(self.type)
            result.append(string)
        if self.alias is not None:
            string = '\t' + r'\alias {}'.format(self.alias)
            result.append(string)
        for statement in self.engraver_removals:
            string = '\t' + r'\remove {}'.format(statement)
            result.append(string)
        # CAUTION: LilyPond consist-statements are order-significant!
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
        for key, value in contextualize(self)._get_attribute_tuples():
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
        r'''Gets LilyPond ``\accepts`` commands in context block.

        ..  container:: example

            >>> block.accepts
            []

        Returns list.
        '''
        return self._accepts

    @property
    def engraver_consists(self):
        r'''Engraver consists commands.

        ..  container:: example

            >>> block.engraver_consists
            []

        Returns list.
        '''
        return self._engraver_consists

    @property
    def engraver_removals(self):
        r'''Engraver removal commands.

        ..  container:: example

            >>> block.engraver_removals
            []

        Returns list.
        '''
        return self._engraver_removals

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        r'''Gets and sets alias of context block.

        ..  container:: example

            >>> block.alias is None
            True

        Returns string or none.
        '''
        return self._alias

    @alias.setter
    def alias(self, alias):
        assert isinstance(alias, (str, type(None)))
        self._alias = alias

    @property
    def name(self):
        r'''Gets and sets name of context block.

        ..  container:: example

            >>> block.name is None
            True

        Returns string or none.
        '''
        return self._name

    @name.setter
    def name(self, name):
        assert isinstance(name, (str, type(None)))
        self._name = name

    @property
    def source_context_name(self):
        r'''Gets and sets context name of context block.

        ..  container:: example

            >>> block.source_context_name
            'Score'

        Returns string or none.
        '''
        return self._source_context_name

    @source_context_name.setter
    def source_context_name(self, source_context_name):
        assert isinstance(source_context_name, (str, type(None)))
        self._source_context_name = source_context_name

    @property
    def type(self):
        r'''Gets and sets LilyPond type of context block.

        ..  container:: example

            >>> block.type is None
            True

        Returns string or none.
        '''
        return self._type

    @type.setter
    def type(self, expr):
        assert isinstance(expr, (str, type(None)))
        self._type = expr
