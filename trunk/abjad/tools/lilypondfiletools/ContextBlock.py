# -*- encoding: utf-8 -*-
from abjad.tools import lilypondproxytools
from abjad.tools.functiontools import override
from abjad.tools.lilypondfiletools.AttributedBlock import AttributedBlock


class ContextBlock(AttributedBlock):
    r'''Abjad model of LilyPond input file context block:

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
        >>> context_block.set.proportionalNotationDuration = \
        ...     schemetools.SchemeMoment((1, 45))

    ..  doctest::

        >>> f(context_block)
        \context {
            \Score
            \override BarNumber #'transparent = ##t
            \override TimeSignature #'break-visibility = #end-of-line-invisible
            proportionalNotationDuration = #(ly:make-moment 1 45)
        }

    Returns context block.
    '''

    ### INITIALIZER ###

    def __init__(self, context_name=None):
        AttributedBlock.__init__(self)
        self._accepts = []
        self._engraver_consists = []
        self._engraver_removals = []
        self._escaped_name = r'\context'
        self.alias = None
        self.context_name = context_name
        self.name = None
        self.type = None

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        from abjad.tools.lilypondfiletools._format_lilypond_context_setting_in_with_block \
            import _format_lilypond_context_setting_in_with_block
        result = []
        result.append('%s {' % self._escaped_name)
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
        for key, value in self.set._get_attribute_tuples():
            setting_contribution = \
                _format_lilypond_context_setting_in_with_block(key, value)
            setting_contributions.append(setting_contribution)
        for setting_contribution in sorted(setting_contributions):
            result.append('\t' + setting_contribution)
        result.append('}')
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def accepts(self):
        return self._accepts

    @property
    def engraver_consists(self):
        return self._engraver_consists

    @property
    def engraver_removals(self):
        return self._engraver_removals

    @property
    def override(self):
        r'''Reference to LilyPond grob override component plug-in.
        '''
        if not hasattr(self, '_override'):
            self._override = \
                lilypondproxytools.LilyPondGrobManager()
        return self._override

    @property
    def set(self):
        r'''Reference LilyPond context setting component plug-in.
        '''
        if not hasattr(self, '_set'):
            self._set = \
                lilypondproxytools.LilyPondSettingManager()
        return self._set

    ### PUBLIC PROPERTIES ###

    @apply
    def alias():
        def fget(self):
            r'''Read / write alias.
            '''
            return self._alias
        def fset(self, alias):
            assert isinstance(alias, (str, type(None)))
            self._alias = alias
        return property(**locals())

    @apply
    def context_name():
        def fget(self):
            r'''Read / write context name.
            '''
            return self._context_name
        def fset(self, context_name):
            assert isinstance(context_name, (str, type(None)))
            self._context_name = context_name
        return property(**locals())

    @apply
    def name():
        def fget(self):
            r'''Read / write name.
            '''
            return self._name
        def fset(self, name):
            assert isinstance(name, (str, type(None)))
            self._name = name
        return property(**locals())

    @apply
    def type():
        def fget(self):
            r'''Read / write type.
            '''
            return self._type
        def fset(self, expr):
            assert isinstance(expr, (str, type(None)))
            self._type = expr
        return property(**locals())
