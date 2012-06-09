from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.Scope import Scope
import copy


class Setting(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        mandatory_argument_values, keyword_argument_values = self._get_input_argument_values(*args, **kwargs)
        self._check_input_arguments(mandatory_argument_values, keyword_argument_values)
        segment_name, context_name, scope, attribute_name, source, persistent, truncate = \
            mandatory_argument_values
        fresh = keyword_argument_values[0]
        self.segment_name = segment_name
        self.context_name = context_name
        self.scope = scope
        self.attribute_name = attribute_name
        self.source = source
        self.persistent = persistent
        self.truncate = truncate
        self.fresh = fresh

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
            self.segment_name,
            self.context_name,
            self.scope,
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
        segment_name, context_name, scope, attribute_name, source, persistent, truncate = \
            mandatory_argument_values
        fresh = keyword_argument_values[0]
        assert isinstance(segment_name, str), repr(segment_name)
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        assert isinstance(scope, (Scope, type(None))), repr(scope)
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
            assert len(args) == 7, repr(args)
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

    ### PUBLIC METHODS ###

    def copy_to_segment(self, segment_name):
        assert isinstance(segment_name, str), repr(segment_name)
        new = copy.deepcopy(self)
        new.segment_name = segment_name
        return new
