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

    def __init__(self, *args, **kwargs):
        from experimental import selectortools
        mandatory_argument_values, keyword_argument_values = self._get_input_argument_values(*args, **kwargs)
        attribute, source, target = mandatory_argument_values
        assert isinstance(target, (selectortools.Selector, type(None)))
        assert isinstance(attribute, str)
        self._target = target
        self._attribute = attribute
        self._source = source
        for name, value in zip(self._keyword_argument_names, keyword_argument_values):
            setattr(self, '_' + name, value)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if not self._mandatory_argument_values == expr._mandatory_argument_values:
            return False
        return self._keyword_argument_values == expr._keyword_argument_values

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        return (
            'persist',
            'truncate',
            )

    @property
    def _mandatory_argument_values(self):
        return (
            #self.target,
            #self.attribute,
            #self.source,
            self.attribute,
            self.source,
            self.target,
            )

    ### PRIVATE METHODS ###

    def _get_input_argument_values(self, *args, **kwargs):
        if len(args) == 1:
            assert isinstance(args[0], type(self)), repr(args[0])
            mandatory_argument_values = args[0]._mandatory_argument_values
            keyword_argument_values = args[0]._keyword_argument_values
            if kwargs.get('persist') is not None:
                keyword_argment_values[0] = kwargs.get('persist')
            if kwargs.get('truncate') is not None:
                keyword_argument_values[1] = kwargs.get('truncate')
        else:
            assert len(args) == 3, repr(args)
            mandatory_argument_values = args
            keyword_argument_values = []
            keyword_argument_values.append(kwargs.get('persist', True))
            keyword_argument_values.append(kwargs.get('truncate', False))
        return mandatory_argument_values, keyword_argument_values

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

        Return selector (usually? always?)
        '''
        return self._target

    @property
    def truncate(self):
        '''True when setting should truncate.

        Return boolean.
        '''
        return self._truncate

    ### PUBLIC METHODS ###

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
