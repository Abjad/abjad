# -*- coding: utf-8 -*-
import inspect
from abjad.tools import abctools


class ClassDocumenter(abctools.AbjadObject):
    """
    A class documenter.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_attributes',
        '_class',
        '_manager',
        )

    ### INITIALIZER ###

    def __init__(self, manager, class_):
        self._manager = manager
        self._class = class_
        self._attributes = self._collect_class_attributes()

    ### PRIVATE METHODS ###

    def _collect_class_attributes(self):
        attributes = {}
        for attr in inspect.classify_class_attrs(self.class_):
            if attr.defining_class is object:
                continue
            elif attr.name in self.manager.ignored_special_methods:
                continue
            if attr.defining_class is not self.class_:
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
                attr.name not in getattr(self.class_, '__slots__', ())
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
        module_name, _, class_name = self.class_.__module__.rpartition('.')
        tools_package_python_path = '.'.join(self.class_.__module__.split('.')[:-1])
        document = documentationtools.ReSTDocument()
        module_directive = documentationtools.ReSTDirective(
            directive='currentmodule',
            argument=tools_package_python_path,
            )
        document.append(module_directive)
        heading = documentationtools.ReSTHeading(level=2, text=class_name)
        document.append(heading)
        autoclass_directive = documentationtools.ReSTAutodocDirective(
            argument=self.class_.__name__,
            directive='autoclass',
            )
        document.append(autoclass_directive)
        document.extend(manager._build_class_lineage_section_rst(self.class_))
        document.extend(manager._build_class_bases_section_rst(self.class_))
        document.extend(manager._build_class_enumeration_section_rst(self.class_))
        document.extend(manager._build_class_attributes_autosummary_rst(self.class_, self.attributes))
        document.extend(manager._build_class_readonly_properties_section_rst(self.class_, self.attributes))
        document.extend(manager._build_class_readwrite_properties_section_rst(self.class_, self.attributes))
        document.extend(manager._build_class_methods_section_rst(self.class_, self.attributes))
        document.extend(manager._build_class_classmethod_and_staticmethod_section_rst(self.class_, self.attributes))
        document.extend(manager._build_class_special_methods_section_rst(self.class_, self.attributes))
        return document

    ### PUBLIC PROPERTIES ###

    @property
    def attributes(self):
        """
        Gets sorted attributes of documenter's class.
        """
        return self._attributes

    @property
    def class_(self):
        """
        Gets class_ of documenter.
        """
        return self._class

    @property
    def manager(self):
        """
        Gets manager of documenter.
        """
        return self._manager
