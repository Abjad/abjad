from abjad.tools.lilypondfiletools.AttributedBlock import AttributedBlock
from abjad.tools import lilypondproxytools


class ContextBlock(AttributedBlock):
    r'''.. versionadded:: 2.5

    Abjad model of LilyPond input file context block::

        >>> context_block = lilypondfiletools.ContextBlock()

    ::

        >>> context_block
        ContextBlock()

    ::

        >>> context_block.context_name = 'Score'
        >>> context_block.override.bar_number.transparent = True
        >>> scheme = schemetools.Scheme('end-of-line-invisible')
        >>> context_block.override.time_signature.break_visibility = scheme
        >>> context_block.set.proportionalNotationDuration = schemetools.SchemeMoment((1, 45))

    ::

        >>> f(context_block)
        \context {
            \Score
            \override BarNumber #'transparent = ##t
            \override TimeSignature #'break-visibility = #end-of-line-invisible
            proportionalNotationDuration = #(ly:make-moment 1 45)
        }

    Return context block.
    '''

    ### INITIALIZER ###

    def __init__(self, context_name=None):
        AttributedBlock.__init__(self)
        self._accepts = []
        self._engraver_consists = []
        self._engraver_removals = []
        self._escaped_name = r'\context'
        self.context_name = context_name
        self.name = None
        self.type = None
        
    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        from abjad.tools.lilypondfiletools._format_lilypond_context_setting_in_with_block import \
            _format_lilypond_context_setting_in_with_block
        result = []
        result.append('%s {' % self._escaped_name)
        if self.type is not None:
            result.append('\t' + r'\type %s' % self.type)
        if self.context_name is not None:
            result.append('\t' + r'\%s' % self.context_name)
        if self.name is not None:
            result.append('\t' + r'\name %s' % self.name)
        for string in self.engraver_removals:
            result.append('\t' + r'\remove %s' % string)
        # CAUTION: LilyPond consist statements are order-significant!
        for string in self.engraver_consists:
            result.append('\t' + r'\consists %s' % string)
        for string in self.accepts:
            result.append('\t' + r'\accepts %s' % string)
        for override in self.override._list_format_contributions('override'):
            result.append('\t' + override)
        setting_contributions = []
        for key, value in self.set._get_attribute_tuples():
            setting_contribution = _format_lilypond_context_setting_in_with_block(key, value)
            setting_contributions.append(setting_contribution)
        for setting_contribution in sorted(setting_contributions):
            result.append('\t' + setting_contribution)
        result.append('}')
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

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
        '''Read-only reference to LilyPond grob override component plug-in.
        '''
        if not hasattr(self, '_override'):
            self._override = lilypondproxytools.LilyPondGrobOverrideComponentPlugIn()
        return self._override

    @property
    def set(self):
        '''Read-only reference LilyPond context setting component plug-in.
        '''
        if not hasattr(self, '_set'):
            self._set = lilypondproxytools.LilyPondContextSettingComponentPlugIn()
        return self._set

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def context_name():
        def fget(self):
            r'''Read / write context name.'''
            return self._context_name
        def fset(self, context_name):
            assert isinstance(context_name, (str, type(None)))
            self._context_name = context_name
        return property(**locals())

    @apply
    def name():
        def fget(self):
            r'''Read / write name.'''
            return self._name
        def fset(self, name):
            assert isinstance(name, (str, type(None)))
            self._name = name
        return property(**locals())

    @apply
    def type():
        def fget(self):
            r'''Read / write type.'''
            return self._type
        def fset(self, expr):
            assert isinstance(expr, (str, type(None)))
            self._type = expr
        return property(**locals())
