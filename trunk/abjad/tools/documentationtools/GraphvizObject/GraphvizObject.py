import abc
import copy
from abjad.tools.abctools import AbjadObject


class GraphvizObject(AbjadObject):
    '''An attributed Graphviz object.'''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, attributes=None):
        self._verify_attributes(attributes, '_attributes')

    ### PRIVATE METHODS ###

    def _format_attribute(self, name, value):
        return '{}={}'.format(name, self._format_value(value))

    def _format_attribute_list(self, attributes):
        result = []
        for k, v in sorted(attributes.items()):
            result.append(self._format_attribute(k, v))
        result[0] = '[' + result[0]
        result[-1] = result[-1] + '];'
        if 1 < len(result):
            for i, x in enumerate(result):
                if i < len(result) - 1:
                    result[i] = result[i] + ','
                if 0 < i:
                    result[i] = '\t' + result[i]
        return result

    def _format_value(self, value):
        if isinstance(value, bool):
            return repr(value).lower()
        elif isinstance(value, (int, float)):
            return repr(value)
        elif isinstance(value, str):
            if ' ' in value or \
                ',' in value or \
                '\\' in value or \
                "." in value or \
                '/' in value:
                return '"{}"'.format(value)
            return value
        elif isinstance(value, (list, tuple)):
            return '"{}"'.format(', '.join(self._format_value(x) for x in value))
        raise ValueError

    def _verify_attributes(self, attributes, destination):
        assert isinstance(attributes, (dict, type(None)))
        if attributes is None:
            attributes = {}
        else:
            attributes = copy.copy(attributes)
        setattr(self, destination, attributes)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attributes(self):
        return self._attributes

