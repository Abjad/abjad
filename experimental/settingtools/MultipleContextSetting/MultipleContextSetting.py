from experimental.settingtools.Setting import Setting
import copy


class MultipleContextSetting(Setting):
    r'''.. versionadded:: 1.0
    
        >>> from abjad.tools import *
        >>> from experimental import specificationtools

    Multiple-context setting::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template)
        >>> segment = score_specification.append_segment('red')

    ::

        >>> multiple_context_setting = segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    ::

        >>> z(multiple_context_setting)
        settingtools.MultipleContextSetting(
            selectortools.MultipleContextTimespanSelector(
                contexts=['Grouped Rhythmic Staves Score'],
                timespan=timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                ),
            'time_signatures',
            [(4, 8), (3, 8)],
            persist=True,
            truncate=False
            )

    Return multiple-context setting.
    '''

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        mandatory_argument_values, keyword_argument_values = self._get_input_argument_values(*args, **kwargs)
        target, attribute, source = mandatory_argument_values
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
            self.target,
            self.attribute,
            self.source,
            )

    @property
    def _one_line_format(self):
        body = [
            self.target._one_line_format,
            self._get_one_line_source_format(self.source),
            ]
        if not self.persist:
            body.append(self.persist)
        body = ', '.join([str(x) for x in body])
        return '{}: {}'.format(self.attribute, body)

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

    def _get_one_line_source_format(self, source):
        if hasattr(source, '_one_line_format'):
            return source._one_line_format
        elif hasattr(source, 'name'):
            return source.name
        else:
            return str(source)
    
    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        return self._attribute

    @property
    def persist(self):
        return self._persist

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    @property
    def truncate(self):
        return self._truncate

    ### PUBLIC METHODS ###

    # TODO: implement Selector.unpack() to complement this method;
    #       multiple-context selectors should know how to unpack themselves into single-context selectors;
    def unpack(self):
        '''Unpacking a multiple-context setting means exploding the multiple-context
        setting into a list of single-context settings.

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
            setting = settingtools.SingleContextSetting(target, self.attribute, self.source, 
                persist=self.persist, truncate=self.truncate)
            settings.append(setting)
        return settings
