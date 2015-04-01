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
        if isinstance(value, documentationtools.GraphvizTable):
            result = []
            lines = str(value).splitlines()
            result.append('{}={}'.format(name, lines[0]))
            for line in lines[1:]:
                result.append('    ' + line)
            result = '\n'.join(result)
            return result
        return '{}={}'.format(
            name,
            self._format_value(value, quote_keywords=True),
            )

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