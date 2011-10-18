from abjad.tools.lilypondfiletools._AttributedBlock import _AttributedBlock
from abjad.core import LilyPondContextSettingComponentPlugIn
from abjad.core import LilyPondGrobOverrideComponentPlugIn


class ContextBlock(_AttributedBlock):
    r'''.. versionadded:: 2.5

    Abjad model of LilyPond input file context block::

        abjad> context_block = lilypondfiletools.ContextBlock()

    ::

        abjad> context_block
        ContextBlock()

    ::

        abjad> context_block.context_name = 'Score'
        abjad> context_block.override.bar_number.transparent = True
        abjad> context_block.override.time_signature.break_visibility = schemetools.SchemeVariable('end-of-line-invisible')
        abjad> context_block.set.proportionalNotationDuration = schemetools.SchemeMoment((1, 45))

    ::

        abjad> f(context_block)
        \context {
            \Score
            \override BarNumber #'transparent = ##t
            \override TimeSignature #'break-visibility = #end-of-line-invisible
            proportionalNotationDuration = #(ly:make-moment 1 45)
        }

    Return context block.
    '''

    def __init__(self, context_name=None):
        _AttributedBlock.__init__(self)
        self._escaped_name = r'\context'
        self.context_name = context_name
        
    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_pieces(self):
        result = []
        result.append('%s {' % self._escaped_name)
        if self.context_name is not None:
            result.append('\t' + r'\%s' % self.context_name)
        for override in self.override._list_format_contributions('override'):
            result.append('\t' + override)
        for key, value in self.set._get_attribute_tuples():
            value_format = getattr(value, 'format', str(value))
            result.append('\t' + '%s = %s' % (key, value_format))
        result.append('}')
        return result

    ### PUBLIC ATTRIBUTES ###

    @apply
    def context_name():
        def fget(self):
            r'''Read / write context name.'''
            return self._context_name
        def fset(self, context_name):
            assert isinstance(context_name, (str, type(None)))
            self._context_name = context_name
        return property(**locals())

    @property
    def override(self):
        '''Read-only reference to LilyPond grob override component plug-in.
        '''
        if not hasattr(self, '_override'):
            self._override = LilyPondGrobOverrideComponentPlugIn()
        return self._override

    @property
    def set(self):
        '''Read-only reference LilyPond context setting component plug-in.
        '''
        if not hasattr(self, '_set'):
            self._set = LilyPondContextSettingComponentPlugIn()
        return self._set
