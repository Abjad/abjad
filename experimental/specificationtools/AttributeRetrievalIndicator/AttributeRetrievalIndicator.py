from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.AttributeNameEnumeration import AttributeNameEnumeration
from experimental.specificationtools.TemporalScope import TemporalScope
from experimental.specificationtools.Selection import Selection


class AttributeRetrievalIndicator(AbjadObject):

    ### CLASS ATTRIBUTES ###

    attribute_names = AttributeNameEnumeration()

    ### INITIALIZER ###

    def __init__(self, attribute_name, segment_name, context_name=None, scope=None):
        assert isinstance(segment_name, str), repr(segment_name)
        assert attribute_name in self.attribute_names, repr(attribute_name)
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        assert isinstance(scope, (TemporalScope, type(None))), repr(scope)
        self.attribute_name = attribute_name
        self.segment_name = segment_name
        self.context_name = context_name
        self.scope = scope
