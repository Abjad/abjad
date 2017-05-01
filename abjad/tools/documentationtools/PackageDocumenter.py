# -*- coding: utf-8 -*-
import enum
import importlib
import inspect
import types
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib
from abjad.tools.documentationtools.Documenter import Documenter


class PackageDocumenter(Documenter):
    """
    A module documenter.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_members',
        '_package_path',
        )

    ### INITIALIZER ###

    def __init__(self, manager, client):
        Documenter.__init__(self, manager, client)
        package_path = pathlib.Path(self.client.__file__)
        assert package_path.name == '__init__.py'
        self._package_path = package_path.parent
        self._members = self._collect_members()

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

    def _collect_members(self):
        members = {}
        ignored_classes = self.manager._get_ignored_classes()
        for name in dir(self.client):
            if name.startswith('_'):
                continue
            member = self.client.__dict__[name]
            if isinstance(member, type):
                if member in ignored_classes:
                    continue
                module = importlib.import_module(member.__module__)
                module_path = pathlib.Path(module.__file__)
                if self.package_path not in module_path.parents:
                    continue
                section = getattr(member, '__documentation_section__', None)
                if section is None:
                    if issubclass(member, enum.Enum):
                        section = 'Enumerations'
                    elif issubclass(member, Exception):
                        section = 'Errors'
                    else:
                        section = 'Classes'
                    if inspect.isabstract(member):
                        section = 'Abstract Classes'
                members.setdefault(section, []).append(member)
            elif isinstance(member, types.FunctionType):
                module = importlib.import_module(member.__module__)
                module_path = pathlib.Path(module.__file__)
                if self.package_path not in module_path.parents:
                    continue
                section = 'Functions'
                members.setdefault(section, []).append(member)
            elif isinstance(member, types.ModuleType):
                module_path = pathlib.Path(member.__file__)
                if self.package_path not in module_path.parents:
                    continue
                section = 'Submodules'
                members.setdefault(section, []).append(member)
            else:
                continue
        for key, value in members.items():
            members[key] = tuple(sorted(value, key=lambda x: x.__name__))
        return members

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

    ### PUBLIC PROPERTIES ###

    @property
    def members(self):
        """
        Gets sorted members of documenter's client.
        """
        return self._members

    @property
    def package_path(self):
        """
        Gets package path of documenter's client.
        """
        return self._package_path
