from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.AttributeNameEnumeration import AttributeNameEnumeration
#from experimental.timespantools.Timespan import Timespan


class AttributeRetrievalIndicator(AbjadObject):
    r'''.. versionadded:: 1.0

    Frozen request to retrieve the attribute specified against an arbitrary object in score.

    (Object-oriented delayed evaluation.)

    .. note:: class needs to be reworked to center around ComponentSelector objects.
    '''

    ### CLASS ATTRIBUTES ###

    attributes = AttributeNameEnumeration()

    ### INITIALIZER ###

    def __init__(self, attribute, segment_name, context_name=None, timespan=None):
        assert isinstance(segment_name, str), repr(segment_name)
        assert attribute in self.attributes, repr(attribute)
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        #assert isinstance(timespan, (Timespan, type(None))), repr(timespan)
        self.attribute = attribute
        self.segment_name = segment_name
        self.context_name = context_name
        self.timespan = timespan
