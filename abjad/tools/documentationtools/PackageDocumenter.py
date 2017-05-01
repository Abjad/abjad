# -*- coding: utf-8 -*-
import enum
import inspect
import types
from abjad.tools.documentationtools.Documenter import Documenter


class PackageDocumenter(Documenter):
    """
    A module documenter.
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
                section = 'Functions'
                members.setdefault(section, []).append(member)
            elif isinstance(member, types.ModuleType):
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
        return document
