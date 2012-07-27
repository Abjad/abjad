from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental import helpertools


class AttributeIndicator(AbjadObject):
    r'''.. versionadded:: 1.0

    Frozen request to retrieve the attribute specified against an arbitrary object in score.

    .. note:: class needs to be reworked to center around SingleContextCounttimeComponentSelector objects.
    '''

    ### CLASS ATTRIBUTES ###

    attributes = helpertools.AttributeNameEnumeration()

    ### INITIALIZER ###

    def __init__(self, attribute, segment_name, context_name=None):
        assert isinstance(segment_name, str), repr(segment_name)
        assert attribute in self.attributes, repr(attribute)
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        self.attribute = attribute
        self.segment_name = segment_name
        self.context_name = context_name
