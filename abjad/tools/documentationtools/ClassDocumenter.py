# -*- coding: utf-8 -*-
import importlib
import inspect
import traceback
from abjad.tools import abctools


class ClassDocumenter(abctools.AbjadObject):
    """
    A class documenter.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_attributes',
        '_client',
        '_manager',
        )

    ### INITIALIZER ###

    def __init__(self, manager, client):
        self._manager = manager
        self._client = client
        self._attributes = self._collect_class_attributes()

    ### PRIVATE METHODS ###

    def _build_bases_section_rst(self):
        from abjad.tools import documentationtools
        result = []
        heading = documentationtools.ReSTHeading(level=3, text='Bases')
        result.append(heading)
        mro = inspect.getmro(self.client)[1:]
        for base in mro:
            parts = base.__module__.split('.') + [base.__name__]
            while 1 < len(parts) and parts[-1] == parts[-2]:
                parts.pop()
            packagesystem_path = '.'.join(parts)
            text = '- :py:class:`{}`'.format(packagesystem_path)
            paragraph = documentationtools.ReSTParagraph(
                text=text,
                wrap=False,
                )
            result.append(paragraph)
        return result

    def _build_lineage_graph(self):
        def get_node_name(original_name):
            parts = original_name.split('.')
            name = [parts[0]]
            for part in parts[1:]:
                if part != name[-1]:
                    name.append(part)
            if name[0] in ('abjad', 'experimental', 'ide'):
                return str('.'.join(name[2:]))
            return str('.'.join(name))
        from abjad.tools import documentationtools
        module_name, _, class_name = self.client.__module__.rpartition('.')
        node_name = '{}.{}'.format(self.client.__module__, self.client.__name__)
        importlib.import_module(module_name)
        lineage_graph_addresses = self.manager._get_lineage_graph_addresses()
        lineage = documentationtools.InheritanceGraph(
            addresses=lineage_graph_addresses,
            lineage_addresses=((module_name, class_name),)
            )
        graph = lineage.__graph__()
        maximum_node_count = 30
        if maximum_node_count < len(graph.leaves):
            lineage = documentationtools.InheritanceGraph(
                addresses=lineage_graph_addresses,
                lineage_addresses=((module_name, class_name),),
                lineage_prune_distance=2,
                )
            graph = lineage.__graph__()
        if maximum_node_count < len(graph.leaves):
            lineage = documentationtools.InheritanceGraph(
                addresses=lineage_graph_addresses,
                lineage_addresses=((module_name, class_name),),
                lineage_prune_distance=1,
                )
            graph = lineage.__graph__()
        if maximum_node_count < len(graph.leaves):
            lineage = documentationtools.InheritanceGraph(
                addresses=((module_name, class_name),),
                )
            graph = lineage.__graph__()
            graph_node = graph[node_name]
            graph_node.attributes['color'] = 'black'
            graph_node.attributes['fontcolor'] = 'white'
            graph_node.attributes['style'] = ('filled', 'rounded')
        graph_node = graph[node_name]
        graph_node.attributes['label'] = \
            '<<B>{}</B>>'.format(graph_node.attributes['label'])
        return graph

    def _build_lineage_section_rst(self):
        from abjad.tools import documentationtools
        result = []
        try:
            lineage_heading = documentationtools.ReSTHeading(
                level=3,
                text='Lineage',
                )
            result.append(lineage_heading)
            lineage_graph = self._build_lineage_graph()
            lineage_graph.attributes['background'] = 'transparent'
            lineage_graph.attributes['rankdir'] = 'LR'
            graphviz_directive = \
                documentationtools.ReSTGraphvizDirective(
                    graph=lineage_graph,
                    )
            graphviz_container = documentationtools.ReSTDirective(
                directive='container',
                argument='graphviz',
                )
            graphviz_container.append(graphviz_directive)
        except:
            traceback.print_exc()
        return result

    def _collect_class_attributes(self):
        attributes = {}
        for attr in inspect.classify_class_attrs(self.client):
            if attr.defining_class is object:
                continue
            elif attr.name in self.manager.ignored_special_methods:
                continue
            if attr.defining_class is not self.client:
                attributes.setdefault('inherited_attributes', []).append(attr)
            if attr.kind == 'method':
                if attr.name.startswith('__'):
                    attributes.setdefault('special_methods', []).append(attr)
                elif not attr.name.startswith('_'):
                    attributes.setdefault('methods', []).append(attr)
            elif attr.kind == 'class method':
                if attr.name.startswith('__'):
                    attributes.setdefault('special_methods', []).append(attr)
                elif not attr.name.startswith('_'):
                    attributes.setdefault('class_methods', []).append(attr)
            elif attr.kind == 'static method':
                if attr.name.startswith('__'):
                    attributes.setdefault('special_methods', []).append(attr)
                elif not attr.name.startswith('_'):
                    attributes.setdefault('static_methods', []).append(attr)
            elif attr.kind == 'property' and not attr.name.startswith('_'):
                if attr.object.fset is None:
                    attributes.setdefault('readonly_properties', []).append(
                        attr)
                else:
                    attributes.setdefault('readwrite_properties', []).append(
                        attr)
            elif (
                attr.kind == 'data' and
                not attr.name.startswith('_') and
                attr.name not in getattr(self.client, '__slots__', ())
                ):
                attributes.setdefault('data', []).append(attr)
        for key, value in attributes.items():
            attributes[key] = tuple(sorted(value))
        return attributes

    ### PUBLIC METHODS ###

    def build_rst(self):
        """
        Build ReST.
        """
        from abjad.tools import documentationtools
        manager = documentationtools.DocumentationManager()
        module_name, _, class_name = self.client.__module__.rpartition('.')
        tools_package_python_path = '.'.join(self.client.__module__.split('.')[:-1])
        document = documentationtools.ReSTDocument()
        module_directive = documentationtools.ReSTDirective(
            directive='currentmodule',
            argument=tools_package_python_path,
            )
        document.append(module_directive)
        heading = documentationtools.ReSTHeading(level=2, text=class_name)
        document.append(heading)
        autoclass_directive = documentationtools.ReSTAutodocDirective(
            argument=self.client.__name__,
            directive='autoclass',
            )
        document.append(autoclass_directive)
        document.extend(self._build_lineage_section_rst())
        document.extend(self._build_bases_section_rst())
        document.extend(manager._build_class_enumeration_section_rst(self.client))
        document.extend(manager._build_class_attributes_autosummary_rst(self.client, self.attributes))
        document.extend(manager._build_class_readonly_properties_section_rst(self.client, self.attributes))
        document.extend(manager._build_class_readwrite_properties_section_rst(self.client, self.attributes))
        document.extend(manager._build_class_methods_section_rst(self.client, self.attributes))
        document.extend(manager._build_class_classmethod_and_staticmethod_section_rst(self.client, self.attributes))
        document.extend(manager._build_class_special_methods_section_rst(self.client, self.attributes))
        return document

    ### PUBLIC PROPERTIES ###

    @property
    def attributes(self):
        """
        Gets sorted attributes of documenter's class.
        """
        return self._attributes

    @property
    def client(self):
        """
        Gets client of documenter.
        """
        return self._client

    @property
    def manager(self):
        """
        Gets manager of documenter.
        """
        return self._manager
