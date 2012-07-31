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

    ### INITIALIZER ###

    def __init__(self, attribute, source, target, persist=True, truncate=False):
        from experimental import selectortools
        assert isinstance(attribute, str)
        assert isinstance(target, (selectortools.Selector, type(None)))
        assert isinstance(persist, bool)
        assert isinstance(truncate, bool)
        self._attribute = attribute
        self._source = source
        self._target = target
        self._persist = persist
        self._truncate = truncate
        
    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if not self._mandatory_argument_values == expr._mandatory_argument_values:
            return False
        return self._keyword_argument_values == expr._keyword_argument_values

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''Setting attribute.

        Return string.
        '''
        return self._attribute

    @property
    def persist(self):
        '''True when setting should persist.
         
        Return boolean.
        '''
        return self._persist

    @property
    def source(self):
        '''Setting source.

        Many different return types are possible.
        '''
        return self._source

    @property
    def target(self):
        '''Setting target.

        Return selector or none.
        '''
        return self._target

    @property
    def truncate(self):
        '''True when setting should truncate.

        Return boolean.
        '''
        return self._truncate

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
