# -*- coding: utf-8 -*-
from abjad.tools.documentationtools.Documenter import Documenter


class FunctionDocumenter(Documenter):
    """
    A function documenter.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PUBLIC METHODS ###

    def build_rst(self):
        """
        Build ReST.
        """
        from abjad.tools import documentationtools
        document = documentationtools.ReSTDocument()
        tools_package_python_path = '.'.join(self.client.__module__.split('.')[:-1])
        module_directive = documentationtools.ReSTDirective(
            directive='currentmodule',
            argument=tools_package_python_path,
            )
        document.append(module_directive)
        heading = documentationtools.ReSTHeading(
            level=2,
            text=self.client.__name__,
            )
        document.append(heading)
        autodoc_directive = documentationtools.ReSTAutodocDirective(
            argument=self.client.__name__,
            directive='autofunction',
            )
        document.append(autodoc_directive)
        return document
