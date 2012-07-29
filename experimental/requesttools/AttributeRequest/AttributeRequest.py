from experimental.requesttools.Request import Request


class AttributeRequest(Request):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import requesttools

    Request `attribute` for `segment_name` in `context_name`.
    Apply any of `callback`, `count`, `offset` that are not none::

        >>> requesttools.AttributeRequest('time_signatures', 'red')
        AttributeRequest('time_signatures', 'red')

    The purpose of an attribute request is to function as the source of a setting.
    '''
    
    ### INITIALIZER ###

    def __init__(self, attribute, segment_name, context_name=None, callback=None, count=None, offset=None):
        assert attribute in self.attributes, repr(attribute)
        assert isinstance(segment_name, str), repr(segment_name)
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        Request.__init__(self, callback=callback, count=count, offset=offset)
        self.attribute = attribute
        self.segment_name = segment_name
        self.context_name = context_name
