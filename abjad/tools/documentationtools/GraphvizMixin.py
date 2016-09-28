# -*- coding: utf-8 -*-
import abc
import copy
import re
from abjad.tools.abctools import AbjadObject
from abjad.tools.topleveltools import new


class GraphvizMixin(AbjadObject):
    r'''An attributed Graphviz mixin.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Graphviz'

    __slots__ = ()

    _word_pattern = re.compile('^\w[\w\-:]*$')

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, attributes=None):
        self._verify_attributes(attributes, '_attributes')

    ### PRIVATE METHODS ###

    @staticmethod
    def _copy_with_memo(node):
        from abjad.tools import systemtools
        agent = systemtools.StorageFormatAgent(node)
        edges = set(getattr(node, '_edges', ()))
        mapping = dict()
        args = agent.get_template_dict()
        if 'children' not in args:
            copied_node = new(node)
            mapping[node] = copied_node
        else:
            copied_node = new(node, children=None)
            mapping[node] = copied_node
            for child in args['children']:
                (
                    copied_child,
                    child_edges,
                    child_mapping,
                    ) = GraphvizMixin._copy_with_memo(child)
                copied_node.append(copied_child)
                edges.update(child_edges)
                mapping.update(child_mapping)
        return copied_node, edges, mapping

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
            should_quote = False
            if not self._word_pattern.match(value):
                should_quote = True
            elif value and value[0].isdigit():
                should_quote = True
            elif value.lower() in (
                'digraph',
                'graph',
                'node',
                'subgraph',
                ) and quote_keywords:
                should_quote = True
            if should_quote:
                value = value.replace('"', r'\"')
                value = '"{}"'.format(value)
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
