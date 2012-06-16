from abjad.tools.abctools.AbjadObject import AbjadObject
import copy


# TODO: make immutable
class Setting(AbjadObject):
    r'''.. versionadded:: 1.0

    Frozen request to set one attribute against one context-specified selection.

    Initialize with mandatory `target`, `attribute`, `source`
    and optional `persistent`, `truncate`, `fresh`.

    Initialize from other setting.
    '''

    ### CLASS ATTRIBUTES ###

#    __slots__ = (
#        '_attribute',
#        '_fresh',
#        '_persistent',
#        '_source',
#        '_target', 
#        '_truncate',
#        )
    
    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        mandatory_argument_values, keyword_argument_values = self._get_input_argument_values(*args, **kwargs)
        self._check_input_arguments(mandatory_argument_values, keyword_argument_values)
        target, attribute, source = mandatory_argument_values
        persistent, truncate, fresh = keyword_argument_values
        self._target = target
        self._attribute = attribute
        self._source = source
        self._persistent = persistent
        self._truncate = truncate
        self._fresh = fresh

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
            'persistent',
            'truncate',
            'fresh',
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
            self._one_line_target_format,
            self._get_one_line_source_format(self.source),
            ]
        if not self.persistent:
            body.append(self.persistent)
        body = ', '.join([str(x) for x in body])
        return '{}: {}'.format(self.attribute, body)

    # TODO: redo me to accommodate target selection
    @property
    def _one_line_target_format(self):
        body = []
        for attribute in ('segment_name', 'context_name', 'timespan'):
            attribute_value = getattr(self, attribute, None)
            if attribute_value is not None:
                body.append(attribute_value)
        body = ', '.join(body)
        return '({})'.format(body)

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
            keyword_argument_values.append(kwargs.get('truncate', False)) # <== i think that's right
            keyword_argument_values.append(kwargs.get('fresh', True))
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
    def fresh(self):
        return self._fresh

    @property
    def persistent(self):
        return self._persistent
    
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
        assert self.target.timespan.encompasses_one_segment_exactly, repr(self)
        segment = self.to_segment_name(segment)
        self.target.timespan.start.anchor._segment = segment
        self.target.timespan.stop.anchor._segment = segment

    def to_segment_name(self, segment):
        '''Change `segment` to segment name. Return string unchanged.

        Return string.
        '''
        from experimental import specificationtools
        if isinstance(segment, specificationtools.SegmentSpecification):
            return segment.name
        elif isinstance(segment, str):
            return segment
        else:
            raise Exception('{!r} is neither segment nor string.'.format(segment))
