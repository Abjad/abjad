import copy
from experimental.settingtools.Setting import Setting


class MultipleContextSetting(Setting):
    r'''.. versionadded:: 1.0

    Multiple-context setting::
    
        >>> from abjad.tools import *
        >>> from experimental import *

    Set `attribute` to `source` for multiple-context `selector`:: 

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template)
        >>> segment = score_specification.append_segment('red')

    ::

        >>> multiple_context_setting = segment.set_time_signatures([(4, 8), (3, 8)])

    ::

        >>> z(multiple_context_setting)
        settingtools.MultipleContextSetting(
            'time_signatures',
            [(4, 8), (3, 8)],
            selectortools.SingleSegmentSelector(
                identifier='red'
                ),
            context_names=['Grouped Rhythmic Staves Score'],
            persist=True
            )

    Composers create multiple-context settings at specification-time.

    Composers create mutliple-context settings with ``SegmentSpecification`` setter methods.

    Multiple-context settings capture composers' musical intent.
    '''

    ### INITIAILIZER ###

    #def __init__(self, attribute, source, selector, context_names=None, persist=True, truncate=False):
    def __init__(self, attribute, source, selector, context_names=None, persist=True, truncate=None):
        Setting.__init__(self, attribute, source, selector, persist=persist, truncate=truncate)
        assert isinstance(context_names, (list, type(None))), repr(context_names)
        self._context_names = context_names

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_names(self):
        '''Multiple-context setting context names.
    
        Return list of strings or none.
        '''
        return self._context_names

    ### PUBLIC METHODS ###

    def unpack(self):
        from experimental import settingtools
        single_context_settings = []
        for context_name in self.context_names:
            selector = copy.deepcopy(self.selector)
            single_context_setting = settingtools.SingleContextSetting(
                self.attribute, 
                self.source, 
                selector,
                context_name=context_name,
                persist=self.persist, 
                truncate=self.truncate)
            single_context_settings.append(single_context_setting)
        return single_context_settings
