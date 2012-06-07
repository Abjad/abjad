from abjad.tools.abctools.AbjadObject import AbjadObject
from specificationtools.AttributeNameEnumeration import AttributeNameEnumeration
from specificationtools.Scope import Scope
from specificationtools.Selection import Selection


class AttributeRetrievalIndicator(AbjadObject):

    ### CLASS ATTRIBUTES ###

    attribute_names = AttributeNameEnumeration()

    ### INITIALIZER ###

    def __init__(self, attribute_name, segment_name, context_name=None, scope=None):
        assert isinstance(segment_name, str), segment_name
        assert attribute_name in self.attribute_names, attribute_name
        assert isinstance(context_name, (str, type(None))), context_name
        assert isinstance(scope, (Scope, type(None))), scope
        self.attribute_name = attribute_name
        self.segment_name = segment_name
        self.context_name = context_name
        self.scope = scope
