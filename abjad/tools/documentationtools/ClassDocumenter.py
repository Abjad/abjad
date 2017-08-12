# -*- coding: utf-8 -*-
import enum
import importlib
import inspect
from abjad.tools.documentationtools.Documenter import Documenter


class ClassDocumenter(Documenter):
    """
    A class documenter.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_members',
        )

    ### INITIALIZER ###

    def __init__(self, manager, client):
        Documenter.__init__(self, manager, client)
        self._members = self._collect_members()

    ### PRIVATE METHODS ###

    def _build_attributes_autosummary_rst(self):
        from abjad.tools import documentationtools
        result = []
        sorted_attributes = []
        for key, value in sorted(self.members.items()):
            if key in ('special_methods', 'inherited_attributes', 'data'):
                continue
            sorted_attributes.extend(value)
        sorted_attributes.sort(key=lambda x: x.name)
        if 'special_methods' in self.members:
            special_methods = self.members['special_methods']
            special_methods = sorted(special_methods, key=lambda x: x.name)
            sorted_attributes.extend(special_methods)
        if not sorted_attributes:
            return result
        autosummary = documentationtools.ReSTAutosummaryDirective()
        for attribute in sorted_attributes:
            autosummary.append('~{}.{}.{}'.format(
                self.client.__module__,
                self.client.__name__,
                attribute.name,
                ))
        html_only = documentationtools.ReSTOnlyDirective(argument='html')
        text = 'Attribute summary'
        heading = documentationtools.ReSTHeading(level=3, text=text)
        html_only.append(heading)
        html_only.append(autosummary)
        result.append(html_only)
        return result

    def _build_attribute_section_rst(self, attributes, directive, title):
        from abjad.tools import documentationtools
        result = []
        if not attributes:
            return result
        heading = documentationtools.ReSTHeading(level=3, text=title)
        result.append(heading)
        for attributes in attributes:
            autodoc = documentationtools.ReSTAutodocDirective(
                argument='{}.{}.{}'.format(
                    self.client.__module__,
                    self.client.__name__,
                    attributes.name,
                    ),
                directive=directive,
                )
            if self.client is attributes.defining_class:
                result.append(autodoc)
            else:
                container = documentationtools.ReSTDirective(
                    argument='inherited',
                    directive='container',
                    )
                container.append(autodoc)
                html_only = documentationtools.ReSTDirective(
                    argument='html',
                    directive='only',
                    )
                html_only.append(container)
                result.append(html_only)
        return result

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

    def _build_classmethod_and_staticmethod_section_rst(self):
        return self._build_attribute_section_rst(
            sorted(
                self.members.get('class_methods', ()) +
                self.members.get('static_methods', ()),
                key=lambda x: x.name
            ),
            'automethod',
            'Class & static methods',
            )

    def _build_methods_section_rst(self):
        return self._build_attribute_section_rst(
            self.members.get('methods'),
            'automethod',
            'Methods',
            )

    def _build_readonly_properties_section_rst(self):
        return self._build_attribute_section_rst(
            self.members.get('readonly_properties'),
            'autoattribute',
            'Read-only properties',
            )

    def _build_readwrite_properties_section_rst(self):
        return self._build_attribute_section_rst(
            self.members.get('readwrite_properties'),
            'autoattribute',
            'Read/write properties',
            )

    def _build_special_methods_section_rst(self):
        return self._build_attribute_section_rst(
            self.members.get('special_methods'),
            'automethod',
            'Special methods',
            )

    def _build_enumeration_section_rst(self):
        from abjad.tools import documentationtools
        result = []
        if not issubclass(self.client, enum.Enum):
            return result
        items = sorted(self.client, key=lambda x: x.name)
        if not items:
            return result
        text = 'Enumeration Items'
        heading = documentationtools.ReSTHeading(level=3, text=text)
        result.append(heading)
        for item in items:
            line = '- ``{}``: {}'.format(item.name, item.value)
            paragraph = documentationtools.ReSTParagraph(
                text=line,
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
        result.append(graphviz_container)
        return result

    def _collect_members(self):
        members = {}
        for attr in inspect.classify_class_attrs(self.client):
            if attr.defining_class is object:
                continue
            elif attr.name in self.manager.ignored_special_methods:
                continue
            elif attr.name.startswith('_') and not attr.name.startswith('__'):
                continue
            if attr.defining_class is not self.client:
                members.setdefault('inherited_attributes', []).append(attr)
            if attr.kind == 'method':
                if attr.name.startswith('__'):
                    members.setdefault('special_methods', []).append(attr)
                else:
                    members.setdefault('methods', []).append(attr)
            elif attr.kind == 'class method':
                if attr.name.startswith('__'):
                    members.setdefault('special_methods', []).append(attr)
                else:
                    members.setdefault('class_methods', []).append(attr)
            elif attr.kind == 'static method':
                if attr.name.startswith('__'):
                    members.setdefault('special_methods', []).append(attr)
                else:
                    members.setdefault('static_methods', []).append(attr)
            elif attr.kind == 'property' and not attr.name.startswith('_'):
                if attr.object.fset is None:
                    members.setdefault('readonly_properties', []).append(
                        attr)
                else:
                    members.setdefault('readwrite_properties', []).append(
                        attr)
            elif (
                attr.kind == 'data' and
                attr.name not in getattr(self.client, '__slots__', ())
                ):
                members.setdefault('data', []).append(attr)
        for key, value in members.items():
            members[key] = tuple(sorted(value))
        return members

    ### PUBLIC METHODS ###

    def build_rst(self):
        """
        Build ReST.
        """
        from abjad.tools import documentationtools
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
        document.extend(self._build_enumeration_section_rst())
        document.extend(self._build_attributes_autosummary_rst())
        document.extend(self._build_readonly_properties_section_rst())
        document.extend(self._build_readwrite_properties_section_rst())
        document.extend(self._build_methods_section_rst())
        document.extend(self._build_classmethod_and_staticmethod_section_rst())
        document.extend(self._build_special_methods_section_rst())
        return document

    ### PUBLIC PROPERTIES ###

    @property
    def members(self):
        """
        Gets sorted members of documenter's class.
        """
        return self._members
