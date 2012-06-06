from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.specificationtools.AttributeRetrievalIndicator import AttributeRetrievalIndicator


class AttributeRetrievalRequest(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, indicator, callback=None, count=None, offset=None):
        assert isinstance(indicator, AttributeRetrievalIndicator)
        self.indicator = indicator
        self.callback = callback
        self.count = count
        self.offset = offset

    ### SPECIAL METHODS ###

    def __call__(self):
        raise NotImplementedError

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _one_line_format(self):
        body = []
        for attribute_name in ('segment_name', 'context_name', 'scope'):
            attribute_value = getattr(self.indicator.selection, attribute_name, None)
            if attribute_value is not None:
                body.append(attribute_value)
        body.append(self.indicator.attribute_name)
        body = ', '.join(body)
        return '({}, count={}, offset={})'.format(body, self.count, self.offset)
