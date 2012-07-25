from experimental.requesttools.Request import Request
from experimental.requesttools.AttributeIndicator import AttributeIndicator


class AttributeRequest(Request):

    ### INITIALIZER ###

    def __init__(self, indicator, callback=None, count=None, offset=None):
        assert isinstance(indicator, AttributeIndicator)
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
        for attribute in ('segment_name', 'context_name', 'timespan'):
            attribute_value = getattr(self.indicator.selection, attribute, None)
            if attribute_value is not None:
                body.append(attribute_value)
        body.append(self.indicator.attribute)
        body = ', '.join(body)
        return '({}, count={}, offset={})'.format(body, self.count, self.offset)
