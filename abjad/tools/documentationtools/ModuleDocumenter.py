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


class ModuleDocumenter(Documenter):
    """
    A module documenter.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_members',
        '_path',
        )

    ### INITIALIZER ###

    def __init__(self, manager, client):
        Documenter.__init__(self, manager, client)
        path = pathlib.Path(self.client.__file__)
        if path.name == '__init__.py':
            path = path.parent
        self._path = path
        self._members = self._collect_members()

    ### PRIVATE METHODS ###

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
                if self.path not in module_path.parents:
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
                if self.path not in module_path.parents:
                    continue
                section = 'Functions'
                members.setdefault(section, []).append(member)
            elif isinstance(member, types.ModuleType):
                module_path = pathlib.Path(member.__file__)
                if self.path not in module_path.parents:
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
        pass
