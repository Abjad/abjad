# -*- encoding: utf-8 -*-
import abc
import copy
from abjad.tools.abctools import AbjadObject


class GraphvizObject(AbjadObject):
    r'''An attributed Graphviz object.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, attributes=None):
        self._verify_attributes(attributes, '_attributes')

    ### SPECIAL METHODS ###

    def __getstate__(self):
        r'''Gets object state.
        '''
        return vars(self)

    ### PRIVATE METHODS ###

    def _format_attribute(self, name, value):
        from abjad.tools import documentationtools
        result = []
        if isinstance(value, documentationtools.GraphvizTable):
            result.extend(str(value).splitlines())
            result[0] = '{}={}'.format(name, result[0])
        else:
            result.append('{}={}'.format(
                name,
                self._format_value(value, quote_keywords=True),
                ))
        result = '\n'.join(result)
        return result

    def _format_attribute_list(self, attributes):
        formatted_attributes = []
        for k, v in sorted(attributes.items()):
            formatted_attributes.append(self._format_attribute(k, v))
        result = []
        for i, formatted_attribute in enumerate(formatted_attributes):
            if i < len(formatted_attributes) - 1:
                formatted_attribute = formatted_attribute + ','
            lines = formatted_attribute.splitlines()
            result.extend(lines)
        for i, line in enumerate(result):
            if 0 < i:
                result[i] = '    ' + line
        result[0] = '[' + result[0]
        result[-1] = result[-1] + '];'
        return result

    def _format_value(self, value, quote_keywords=False):
        if isinstance(value, bool):
            return repr(value).lower()
        elif isinstance(value, (int, float)):
            return repr(value)
        elif isinstance(value, str):
            if value.startswith('<') and value.endswith('>'):
                return value
            elif ' ' in value or \
                ',' in value or \
                '\\' in value or \
                "." in value or \
                '/' in value:
                return '"{}"'.format(value)
            elif value.lower() in (
                'digraph',
                'graph',
                'node',
                'subgraph',
                ) and quote_keywords:
                return '"{}"'.format(value)
            return value
        elif isinstance(value, (list, tuple)):
            return '"{}"'.format(', '.join(
                self._format_value(x, quote_keywords=quote_keywords)
                for x in value))
        raise ValueError

    def _verify_attributes(self, attributes, destination):
        assert isinstance(attributes, (dict, type(None)))
        if attributes is None:
            attributes = {}
        else:
            attributes = copy.copy(attributes)
        setattr(self, destination, attributes)

    ### PUBLIC PROPERTIES ###

    @property
    def attributes(self):
        r'''Attributes of Graphviz object.
        '''
        return self._attributes