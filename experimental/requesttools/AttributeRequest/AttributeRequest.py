from experimental import helpertools
from experimental.requesttools.Request import Request
#from experimental.requesttools.AttributeIndicator import AttributeIndicator


class AttributeRequest(Request):

    ### CLASS ATTRIBUTES ###

    attributes = helpertools.AttributeNameEnumeration()

    ### INITIALIZER ###

    #def __init__(self, indicator, callback=None, count=None, offset=None):
    def __init__(self, attribute, segment_name, context_name=None, callback=None, count=None, offset=None):
        #assert isinstance(indicator, AttributeIndicator)
        #self.indicator = indicator
        self.callback = callback
        self.count = count
        self.offset = offset
        assert isinstance(segment_name, str), repr(segment_name)
        assert attribute in self.attributes, repr(attribute)
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        self.attribute = attribute
        self.segment_name = segment_name
        self.context_name = context_name

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
