# -*- encoding: utf-8 -*-
from abjad.tools import abctools


class ClassCrawler(abctools.AbjadObject):
    r'''Class crawler.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Code discovery'

    __slots__ = (
        '_code_root',
        '_include_private_objects',
        '_root_package_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        code_root=None,
        include_private_objects=False,
        root_package_name=None,
        ):
        self._code_root = code_root
        self._include_private_objects = include_private_objects
        self._root_package_name = root_package_name

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls class crawler.

        Returns tuple of classes.
        '''
        from abjad.tools import documentationtools
        generator = documentationtools.yield_all_classes(
            code_root=self.code_root,
            include_private_objects=self.include_private_objects,
            root_package_name=self.root_package_name,
            )
        return tuple(sorted(generator, key=lambda x: x.__name__))

    ### PUBLIC PROPERTIES ###

    @property
    def code_root(self):
        r'''Code root of class crawler.
        '''
        return self._code_root

    @property
    def include_private_objects(self):
        r'''Include private objects.
        '''
        return self._include_private_objects

    @property
    def root_package_name(self):
        r'''Root package name.
        '''
        return self._root_package_name