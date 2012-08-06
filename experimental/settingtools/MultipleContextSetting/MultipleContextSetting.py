from experimental.settingtools.Setting import Setting
import copy


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
            selectortools.MultipleContextTimespanSelector(
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentItemSelector(
                        identifier='red'
                        )
                    ),
                context_names=['Grouped Rhythmic Staves Score']
                ),
            context_names=['Grouped Rhythmic Staves Score'],
            persist=True,
            truncate=False
            )

    Composers create multiple-context settings at specification-time.

    Composers create mutliple-context settings with ``SegmentSpecification`` setter methods.

    Multiple-context settings capture composers' musical intent.
    '''

    ### INITIAILIZER ###

    def __init__(self, attribute, source, selector, context_names=None, persist=True, truncate=False):
        Setting.__init__(self, attribute, source, selector, persist=persist, truncate=truncate)
        assert isinstance(context_names, (list, type(None))), repr(context_names)
        assert self.selector.context_names == context_names, repr((self.selector.context_names, context_names))
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
        '''Unpack multiple-context setting.

        Return list of single-context settings.
        '''
        from experimental import selectortools
        from experimental import settingtools
        settings = []
        context_names = self.context_names
        assert isinstance(context_names, list), repr(context_names)
        for context_name in context_names:
            if isinstance(self.selector, selectortools.RatioPartSelector):
                selector = copy.deepcopy(self.selector)
                selector.reference._context_name = context_name
            else:
                selector = selectortools.SingleContextTimespanSelector(context_name, 
                    timespan=copy.deepcopy(self.selector.timespan))
            setting = settingtools.SingleContextSetting(self.attribute, self.source, selector,
                context_name=context_name,
                persist=self.persist, truncate=self.truncate)
            settings.append(setting)
        return settings
