from abjad.tools import durationtools
from experimental import selectortools
from experimental.requesttools.Request import Request


class MaterialRequest(Request):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Request `attribute` for `selector` in `context_name`.

    Apply any of `index`, `count`, `reverse`, `rotation`, `callback` that are not none::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> segment = score_specification.make_segment('red')

    ::

        >>> request = segment.request_time_signatures()

    ::

        >>> z(request)
        requesttools.MaterialRequest(
            'time_signatures',
            selectortools.SingleSegmentSelector(
                identifier='red'
                )
            )

    The purpose of a material request is to function as the source of a setting.
    '''
    
    ### INITIALIZER ###

    def __init__(self, attribute, selector, context_name=None, 
        start_offset=None, stop_offset=None,
        index=None, count=None, reverse=None, rotation=None, callback=None):
        assert attribute in self.attributes, repr(attribute)
        assert isinstance(selector, selectortools.Selector)
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        start_offset = self._initialize_offset(start_offset)
        stop_offset = self._initialize_offset(stop_offset)
        Request.__init__(
            self, index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)
        self._attribute = attribute
        self._selector = selector
        self._context_name = context_name
        self._start_offset = start_offset
        self._stop_offset = stop_offset

    ### PRIVATE METHODS ###

    def _initialize_offset(self, offset):
        if offset is not None:
            return durationtools.Offset(offset)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        return self._attribute

    @property
    def context_name(self):
        return self._context_name

    @property
    def selector(self):
        return self._selector

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def start_segment_identifier(self):
        '''Delegate to ``self.selector.start_segment_identifier``.
        '''
        return self.selector.start_segment_identifier

    @property
    def stop_offset(self):
        return self._stop_offset

    @property
    def stop_segment_identifier(self):
        '''Delegate to ``self.selector.stop_segment_identifier``.
        '''
        return self.selector.stop_segment_identifier

    @property
    def voice_name(self):
        '''Aliased to ``self.context_name``.
        '''
        return self.context_name

