from experimental.settingtools.Setting import Setting
import copy


class MultipleContextSetting(Setting):
    r'''.. versionadded:: 1.0

    ::
    
        >>> from abjad.tools import *
        >>> from experimental import *

    Multiple-context setting::

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
                contexts=['Grouped Rhythmic Staves Score'],
                timespan=timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                ),
            persist=True,
            truncate=False
            )

    Return multiple-context setting.
    '''

    ### INITIAILIZER ###

    def __init__(self, attribute, source, target, persist=True, truncate=False):
        Setting.__init__(self, attribute, source, target, persist=persist, truncate=truncate)

    ### PUBLIC METHODS ###

    # TODO: this method should implement on MultipleContextSetting and not on SingleContextSetting
    def unpack(self):
        '''Unpack multiple-context setting.

        Return list of single-context settings.
        '''
        from experimental import selectortools
        from experimental import settingtools
        from experimental import specificationtools
        settings = []
        contexts = self.target.contexts or [self.target.contexts]
        assert contexts, repr(contexts)
        for context in contexts:
            if isinstance(self.target, selectortools.RatioSelector):
                target = copy.deepcopy(self.target)
                target.reference._context = context
            else:
                target = selectortools.SingleContextTimespanSelector(context, 
                    timespan=copy.deepcopy(self.target.timespan))
            setting = settingtools.SingleContextSetting(self.attribute, self.source, target,
                persist=self.persist, truncate=self.truncate)
            settings.append(setting)
        return settings
