import os
import types
from abjad.tools import abctools
from abjad.tools.documentationtools.ModuleCrawler import ModuleCrawler


class ClassCrawler(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_code_root', '_include_private_objects', '_module_crawler',
        '_root_package_name')

    ### INITIALIZER ###

    def __init__(self, code_root, include_private_objects=False, root_package_name=None):
        self._module_crawler = ModuleCrawler(code_root, root_package_name=root_package_name)
        self._code_root = code_root
        self._include_private_objects = include_private_objects
        if root_package_name is None:
            self._root_package_name = self._module_crawler.root_package_name
        else:
            self._root_package_name = root_package_name

    ### SPECIAL METHODS ###

    def __call__(self):
        objects = []
        for module in self.module_crawler:
            name = module.__name__.split('.')[-1]
            if not self.include_private_objects and name.startswith('_'):
                continue
            if not hasattr(module, name):
                continue
            obj = getattr(module, name)
            if isinstance(obj, types.TypeType):
                objects.append(obj)
        return tuple(sorted(objects))

    ### PUBLIC PROPERTIES ###

    @property
    def code_root(self):
        return self._code_root

    @property
    def include_private_objects(self):
        return self._include_private_objects

    @property
    def module_crawler(self):
        return self._module_crawler

    @property
    def root_package_name(self):
        return self._root_package_name
