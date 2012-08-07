from experimental.requesttools.Request import Request


class AttributeRequest(Request):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Request `attribute` for `selector` in `context_name`.
    Apply any of `callback`, `count`, `offset` that are not none::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> segment = score_specification.append_segment('red')

    ::

        >>> request = segment.request_time_signatures()

    ::

        >>> z(request)
        requesttools.AttributeRequest(
            'time_signatures',
            selectortools.SegmentItemSelector(
                identifier='red'
                )
            )

    The purpose of an attribute request is to function as the source of a setting.
    '''
    
    ### INITIALIZER ###

    def __init__(self, attribute, selector, context_name=None, callback=None, count=None, offset=None):
        from experimental import selectortools
        assert attribute in self.attributes, repr(attribute)
        assert isinstance(selector, selectortools.Selector)
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        Request.__init__(self, callback=callback, count=count, offset=offset)
        self._attribute = attribute
        self._selector = selector
        self._context_name = context_name

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.attribute)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        return self._attribute

    @property
    def context_name(self):
        return self._context_name

    @property
    def segment_identifier(self):
        '''Delegate to ``self.selector.segment_identifier``.
        '''
        return self.selector.segment_identifier

    @property
    def selector(self):
        return self._selector
