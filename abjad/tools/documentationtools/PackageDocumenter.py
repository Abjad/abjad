# -*- coding: utf-8 -*-
import types
from abjad.tools.documentationtools.ModuleDocumenter import ModuleDocumenter


class PackageDocumenter(ModuleDocumenter):
    """
    A package documenter.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _build_submodule_section(self, title, members):
        from abjad.tools import documentationtools
        result = []
        rule = documentationtools.ReSTHorizontalRule()
        result.append(rule)
        heading = documentationtools.ReSTHeading(level=3, text=title)
        result.append(heading)
        result.extend(self._build_autosummary(members))
        return result

    def _build_standard_section(self, title, members):
        from abjad.tools import documentationtools
        result = []
        rule = documentationtools.ReSTHorizontalRule()
        result.append(rule)
        heading = documentationtools.ReSTHeading(level=3, text=title)
        result.append(heading)
        result.extend(self._build_autosummary(members))
        for member in members:
            if member.__module__ != self.client.__name__:
                continue
            if isinstance(member, type):
                documenter = documentationtools.ClassDocumenter(
                    self.manager, member)
            elif isinstance(member, types.FunctionType):
                documenter = documentationtools.FunctionDocumenter(
                    self.manager, member)
            else:
                continue
            result.extend(documenter.build_rst())
        return result

    def _build_autosummary(self, members):
        from abjad.tools import documentationtools
        autosummary = documentationtools.ReSTAutosummaryDirective(
            options={'nosignatures': True},
            )
        for member in members:
            text = '~{}.{}'.format(member.__module__, member.__name__)
            item = documentationtools.ReSTAutosummaryItem(text=text)
            autosummary.append(item)
        return [autosummary]

    def _build_package_graph(self):
        from abjad.tools import documentationtools
        lineage_graph_addresses = self.manager._get_lineage_graph_addresses()
        inheritance_graph = documentationtools.InheritanceGraph(
            addresses=lineage_graph_addresses,
            lineage_addresses=[self.client.__name__]
            )
        lineage_graph = inheritance_graph.__graph__()
        lineage_graph.attributes['bgcolor'] = 'transparent'
        lineage_graph.attributes['dpi'] = 72
        lineage_graph.attributes['rankdir'] = 'LR'
        graphviz_directive = documentationtools.ReSTGraphvizDirective(
            graph=lineage_graph,
            )
        graphviz_container = documentationtools.ReSTDirective(
            directive='container',
            argument='graphviz',
            )
        graphviz_container.append(graphviz_directive)
        return graphviz_container

    ### PUBLIC METHODS ###

    def build_rst(self):
        """
        Build ReST.
        """
        from abjad.tools import documentationtools
        document = documentationtools.ReSTDocument()
        automodule_directive = documentationtools.ReSTAutodocDirective(
            argument=self.client.__name__,
            directive='automodule',
            )
        document.append(automodule_directive)
        document.append(self._build_package_graph())
        members = self.members.copy()
        if 'Submodules' in members:
            section = self._build_submodule_section(
                'Submodules', members.pop('Submodules'))
            document.extend(section)
        for key in ('Abstract Classes', 'Main Classes'):
            if key in members:
                section = self._build_standard_section(key, members.pop(key))
                document.extend(section)
        closing_sections = ('Functions', 'Enumerations', 'Errors')
        for key in sorted(members):
            if key in closing_sections:
                continue
            section = self._build_standard_section(key, members.pop(key))
            document.extend(section)
        for key in closing_sections:
            if key in members:
                section = self._build_standard_section(key, members.pop(key))
                document.extend(section)
        return document
