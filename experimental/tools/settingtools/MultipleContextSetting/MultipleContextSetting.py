import copy
from experimental.tools.settingtools.Setting import Setting


class MultipleContextSetting(Setting):
    r'''Multiple-context setting.

    Set `attribute` to `request` for multiple-context `anchor`:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    ::

        >>> multiple_context_setting = red_segment.set_time_signatures([(4, 8), (3, 8)])

    ::

        >>> z(multiple_context_setting)
        settingtools.MultipleContextSetting(
            attribute='time_signatures',
            request=settingtools.AbsoluteExpression(
                ((4, 8), (3, 8))
                ),
            anchor='red',
            persist=True
            )

    Composers create multiple-context settings at specification-time.

    Composers create multiple-context settings with ``SegmentSpecification`` setter methods.

    Multiple-context settings capture composers' musical intent.
    '''

    ### CLASS ATTRIBUTES ###


    ### INITIAILIZER ###

    def __init__(self, attribute=None, request=None, anchor=None, context_names=None, 
            persist=True, truncate=None):
        Setting.__init__(self, attribute=attribute, request=request, anchor=anchor, 
            persist=persist, truncate=truncate)
        assert isinstance(context_names, (list, type(None))), repr(context_names)
        self._context_names = context_names

    ### PRIVATE METHODS ###
    
    def _attribute_to_single_context_setting_class(self, attribute):
        from experimental.tools import settingtools
        return {
            'time_signatures': settingtools.SingleContextTimeSignatureSetting,
            'divisions': settingtools.SingleContextDivisionSetting,
            'rhythm': settingtools.SingleContextRhythmSetting,
            }[attribute]
        
    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_names(self):
        '''Multiple-context setting context names.
    
        Return list of strings or none.
        '''
        return self._context_names

    ### PUBLIC METHODS ###

    def unpack(self):
        single_context_settings = []
        single_context_setting_class = \
            self._attribute_to_single_context_setting_class(self.attribute)
        if self.context_names is None:
            anchor = copy.deepcopy(self.anchor)
            single_context_setting = single_context_setting_class(
                self.request, 
                anchor,
                context_name=None,
                persist=self.persist)
            single_context_settings.append(single_context_setting)
        else:
            for context_name in self.context_names:
                anchor = copy.deepcopy(self.anchor)
                single_context_setting = single_context_setting_class(
                    self.request, 
                    anchor,
                    context_name=context_name,
                    persist=self.persist)
                single_context_settings.append(single_context_setting)
        if self.attribute == 'divisions':
            for single_context_setting in single_context_settings:
                single_context_setting._truncate = self.truncate
        return single_context_settings
