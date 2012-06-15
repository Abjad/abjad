from abjad.tools.abctools.AbjadObject import AbjadObject
import copy


# TODO: make immutable
# TODO: make persistent, truncate keyword arguments to facilitate debugging with repr
class Setting(AbjadObject):
    r'''.. versionadded:: 1.0

    Frozen request to set one attribute against one context-specified selection.

    Initialize with mandatory `target`, `attribute_name`, `source`, `persistent`, `truncate`
    and optional `fresh`.

    (Note that that soon `persistent`, `truncate`, `fresh` will all be optional.)

    Initialize from other setting.
    '''

    ### CLASS ATTRIBUTES ###

#    __slots__ = (
#        '_attribute_name',
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
        target, attribute_name, source, persistent, truncate = mandatory_argument_values
        fresh = keyword_argument_values[0]
        self._target = target
        self._attribute_name = attribute_name
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
            'fresh',
            )

    @property
    def _mandatory_argument_values(self):
        return (
            self.target,
            self.attribute_name,
            self.source,
            self.persistent,
            self.truncate,
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
        return '{}: {}'.format(self.attribute_name, body)

    @property
    def _one_line_target_format(self):
        body = []
        for attribute_name in ('segment_name', 'context_name', 'scope'):
            attribute_value = getattr(self, attribute_name, None)
            if attribute_value is not None:
                body.append(attribute_value)
        body = ', '.join(body)
        return '({})'.format(body)

    ### PRIVATE METHODS ###

    def _check_input_arguments(self, mandatory_argument_values, keyword_argument_values):
        from experimental import specificationtools
        target, attribute_name, source, persistent, truncate = mandatory_argument_values
        fresh = keyword_argument_values[0]
        assert isinstance(target, specificationtools.ContextSelection), repr(target)
        assert isinstance(attribute_name, str), repr(attribute_name)
        assert isinstance(persistent, bool), repr(persistent)
        assert isinstance(truncate, bool), repr(truncate)
        assert isinstance(fresh, type(True)), repr(fresh)

    def _get_input_argument_values(self, *args, **kwargs):
        if len(args) == 1:
            assert isinstance(args[0], type(self)), repr(args[0])
            mandatory_argument_values = args[0]._mandatory_argument_values
            keyword_argument_values = args[0]._keyword_argument_values
            if kwargs.get('fresh') is not None:
                keyword_argment_values[0] = kwargs.get('fresh')
        else:
            assert len(args) == 5, repr(args)
            mandatory_argument_values = args
            keyword_argument_values = []
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
    def attribute_name(self):
        return self._attribute_name

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
        '''Only works when target scope encompasses one segment exactly.

        Create new setting. Set new setting `fresh` to false.

        Return new setting.
        '''
        assert self.target.scope.encompasses_one_segment_exactly, repr(self)
        new = copy.deepcopy(self)
        new.set_to_segment(segment)
        new._fresh = False
        return new

    def set_to_segment(self, segment):
        '''Only works when target scope encompasses one segment exactly.

        Return none.
        '''
        assert self.target.scope.encompasses_one_segment_exactly, repr(self)
        segment = self.to_segment_name(segment)
        self.target.scope.start.anchor._segment = segment
        self.target.scope.stop.anchor._segment = segment

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
