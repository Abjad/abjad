import copy
from abjad.tools.abctools import AbjadObject


class GraphvizObject(AbjadObject):
    '''An attributed Graphviz object.'''

    ### INITIALIZER ###

    def __init__(self, attributes=None):
        assert isinstance(attributes, (dict, type(None)))
        if attributes is None:
            self._attributes = {}
        else:
            self._attributes = copy.copy(attributes)

    ### PRIVATE METHODS ###

    def _format_attribute(self, name, value):
        if isinstance(value, str):
            return '{}="{}"'.format(name, value)
        return '{}={}'.format(name, value)

    def _format_attribute_list(self, attributes):
        result = []
        for k, v in sorted(attributes.items()):
            result.append(self._format_attribute(k, v))
        return '[{}]'.format(', '.join(result))

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def attributes(self):
        return self._attributes

