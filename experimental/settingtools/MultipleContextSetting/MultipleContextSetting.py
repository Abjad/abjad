from experimental.settingtools.Setting import Setting
import copy


class MultipleContextSetting(Setting):
    r'''.. versionadded:: 1.0

    Multiple-context setting::
    
        >>> from abjad.tools import *
        >>> from experimental import *

    Set `attribute` to `source` for multiple-context `target`:: 

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
                        index='red'
                        )
                    ),
                context_names=['Grouped Rhythmic Staves Score']
                ),
            persist=True,
            truncate=False
            )

    Composers create multiple-context settings at specification-time.

    Composers create mutliple-context settings with ``SegmentSpecification`` setter methods.

    Multiple-context settings capture composers' musical intent.
    '''

    ### INITIAILIZER ###

    def __init__(self, attribute, source, target, persist=True, truncate=False):
        Setting.__init__(self, attribute, source, target, persist=persist, truncate=truncate)

    ### PUBLIC METHODS ###

    def unpack(self):
        '''Unpack multiple-context setting.

        Return list of single-context settings.
        '''
        from experimental import selectortools
        from experimental import settingtools
        from experimental import specificationtools
        settings = []
        context_names = self.target.context_names or [None]
        assert isinstance(context_names, list), repr(context_names)
        for context_name in context_names:
            if isinstance(self.target, selectortools.RatioSelector):
                target = copy.deepcopy(self.target)
                target.reference._context_name = context_name
            else:
                target = selectortools.SingleContextTimespanSelector(context_name, 
                    timespan=copy.deepcopy(self.target.timespan))
            setting = settingtools.SingleContextSetting(self.attribute, self.source, target,
                persist=self.persist, truncate=self.truncate)
            settings.append(setting)
        return settings
