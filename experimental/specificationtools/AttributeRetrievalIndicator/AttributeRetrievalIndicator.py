from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.AttributeNameEnumeration import AttributeNameEnumeration
#from experimental.specificationtools.TemporalScope import TemporalScope


class AttributeRetrievalIndicator(AbjadObject):
    r'''.. versionadded:: 1.0

    Frozen request to retrieve the attribute specified against an arbitrary object in score.

    (Object-oriented delayed evaluation.)

    .. note:: class needs to be reworked to center around ScoreObjectIndicator objects.
    '''

    ### CLASS ATTRIBUTES ###

    attribute_names = AttributeNameEnumeration()

    ### INITIALIZER ###

    def __init__(self, attribute_name, segment_name, context_name=None, scope=None):
        assert isinstance(segment_name, str), repr(segment_name)
        assert attribute_name in self.attribute_names, repr(attribute_name)
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        #assert isinstance(scope, (TemporalScope, type(None))), repr(scope)
        self.attribute_name = attribute_name
        self.segment_name = segment_name
        self.context_name = context_name
        self.scope = scope
