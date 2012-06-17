from experimental.specificationtools.Setting import Setting
import copy


class ContextSetting(Setting):
    r'''.. versionadded:: 1.0

    Frozen request to set one attribute against one context-specified selection.

    Initialize with mandatory `target`, `attribute`, `source`
    and optional `persistent`, `truncate`, `fresh`.

    Initialize from other context setting.
    '''

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        return Setting._keyword_argument_names.fget(self) + ('fresh', )

    ### PRIVATE METHODS ###

    def _check_input_arguments(self, mandatory_argument_values, keyword_argument_values):
        from experimental import specificationtools
        target, attribute, source, = mandatory_argument_values
        persistent, truncate, fresh = keyword_argument_values
        assert isinstance(target, specificationtools.ContextSelection), repr(target)
        assert isinstance(attribute, str), repr(attribute)
        assert isinstance(persistent, bool), repr(persistent)
        assert isinstance(truncate, bool), repr(truncate)
        assert isinstance(fresh, type(True)), repr(fresh)

    def _get_input_argument_values(self, *args, **kwargs):
        if len(args) == 1:
            assert isinstance(args[0], type(self)), repr(args[0])
            mandatory_argument_values = args[0]._mandatory_argument_values
            keyword_argument_values = args[0]._keyword_argument_values
            if kwargs.get('persistent') is not None:
                keyword_argment_values[0] = kwargs.get('persistent')
            if kwargs.get('truncate') is not None:
                keyword_argment_values[0] = kwargs.get('truncate')
            if kwargs.get('fresh') is not None:
                keyword_argment_values[0] = kwargs.get('fresh')
        else:
            assert len(args) == 3, repr(args)
            mandatory_argument_values = args
            keyword_argument_values = []
            keyword_argument_values.append(kwargs.get('persistent', True))
            keyword_argument_values.append(kwargs.get('truncate', False))
            keyword_argument_values.append(kwargs.get('fresh', True))
        return mandatory_argument_values, keyword_argument_values

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def fresh(self):
        return self._fresh

    ### PUBLIC METHODS ###

    def copy_to_segment(self, segment):
        '''Only works when target timespan encompasses one segment exactly.

        Create new setting. Set new setting `fresh` to false.

        Return new setting.
        '''
        assert self.target.timespan.encompasses_one_segment_exactly, repr(self)
        new = copy.deepcopy(self)
        new.set_to_segment(segment)
        new._fresh = False
        return new

    def set_to_segment(self, segment):
        '''Only works when target timespan encompasses one segment exactly.

        Return none.
        '''
        from experimental import specificationtools
        assert self.target.timespan.encompasses_one_segment_exactly, repr(self)
        segment = specificationtools.expr_to_segment_name(segment)
        self.target.timespan.start.anchor._segment = segment
        self.target.timespan.stop.anchor._segment = segment
