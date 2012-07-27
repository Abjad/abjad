from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental import helpertools


class AttributeIndicator(AbjadObject):
    r'''.. versionadded:: 1.0

    Request to select the attribute specified against an arbitrary score object.

    .. note:: maybe rename to AttributeSelector.

    .. note:: class needs to be reworked to center around some type of single-context selector.
        Probably also with the inclusion of a specific timepoint.
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
