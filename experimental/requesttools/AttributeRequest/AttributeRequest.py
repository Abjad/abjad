from experimental import helpertools
from experimental.requesttools.Request import Request


class AttributeRequest(Request):
    r'''.. versionadded:: 1.0

    Request `attribute` for `segment_name` in `context_name`.

    Apply any of `callback`, `count`, `offset` that are not none.

    The purpose of an attribute request object is to function as
    the source of a setting.
    '''
    
    ### CLASS ATTRIBUTES ###

    attributes = helpertools.AttributeNameEnumeration()

    ### INITIALIZER ###

    def __init__(self, attribute, segment_name, context_name=None, callback=None, count=None, offset=None):
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
