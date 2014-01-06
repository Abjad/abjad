# -*- encoding: utf-8 -*-
from abjad.tools import lilypondnametools
from abjad.tools.lilypondfiletools.Block import Block
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import contextualize


class ContextBlock(Block):
    r'''A LilyPond input file context block.

    ::

        >>> context_block = lilypondfiletools.ContextBlock()

    ::

        >>> context_block
        ContextBlock()

    ::

        >>> context_block.context_name = 'Score'
        >>> override(context_block).bar_number.transparent = True
        >>> scheme = schemetools.Scheme('end-of-line-invisible')
        >>> override(context_block).time_signature.break_visibility = scheme
        >>> moment = schemetools.SchemeMoment((1, 45))
        >>> contextualize(context_block).proportionalNotationDuration = moment

    ..  doctest::

        >>> print format(context_block)
        \context {
            \Score
            \override BarNumber #'transparent = ##t
            \override TimeSignature #'break-visibility = #end-of-line-invisible
            proportionalNotationDuration = #(ly:make-moment 1 45)
        }

    '''

    ### INITIALIZER ###

    def __init__(self, context_name=None):
        Block.__init__(self, name='context')
        self._accepts = []
        self._engraver_consists = []
        self._engraver_removals = []
        #self._escaped_name = r'\context'
        self.alias = None
        self.context_name = context_name
        self.name = None
        self.type = None

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        from abjad.tools import systemtools
        result = []
        result.append('%s {' % self._escaped_name)
        manager = systemtools.LilyPondFormatManager
        # CAUTION: source context name must come before type to allow 
        # context redefinition.
        # TODO: rename self.context_name to self.source_context_name
        if self.context_name is not None:
            result.append('\t' + r'\%s' % self.context_name)
        if self.name is not None:
            result.append('\t' + r'\name %s' % self.name)
        if self.type is not None:
            result.append('\t' + r'\type %s' % self.type)
        if self.alias is not None:
            result.append('\t' + r'\alias %s' % self.alias)
        for string in self.engraver_removals:
            result.append('\t' + r'\remove %s' % string)
        # CAUTION: LilyPond consist statements are order-significant!
        for string in self.engraver_consists:
            result.append('\t' + r'\consists %s' % string)
        for string in self.accepts:
            result.append('\t' + r'\accepts %s' % string)
        for string in override(self)._list_format_contributions('override'):
            result.append('\t' + string)
        setting_contributions = []
        for key, value in contextualize(self)._get_attribute_tuples():
            setting_contribution = \
                manager.format_lilypond_context_setting_in_with_block(
                    key, value)
            setting_contributions.append(setting_contribution)
        for setting_contribution in sorted(setting_contributions):
            result.append('\t' + setting_contribution)
        result.append('}')
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def accepts(self):
        r'''Context accepts commands.

        Returns sets.
        '''
        return self._accepts

    @property
    def engraver_consists(self):
        r'''Engraver consists commands.

        Returns set.
        '''
        return self._engraver_consists

    @property
    def engraver_removals(self):
        r'''Engraver removal commands.

        Returns set.
        '''
        return self._engraver_removals

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        r'''Gets and sets alias of context block.

        Returns string or none.
        '''
        return self._alias

    @alias.setter
    def alias(self, alias):
        assert isinstance(alias, (str, type(None)))
        self._alias = alias

    @property
    def context_name(self):
        r'''Gets and sets context name of context block.

        Returns string or none.
        '''
        return self._context_name

    @context_name.setter
    def context_name(self, context_name):
        assert isinstance(context_name, (str, type(None)))
        self._context_name = context_name

    @property
    def name(self):
        r'''Gets and sets name of context block.

        Returns string or none.
        '''
        return self._name

    @name.setter
    def name(self, name):
        assert isinstance(name, (str, type(None)))
        self._name = name

    @property
    def type(self):
        r'''Gets and sets LilyPond type of context block.

        Returns string or none.
        '''
        return self._type

    @type.setter
    def type(self, expr):
        assert isinstance(expr, (str, type(None)))
        self._type = expr
