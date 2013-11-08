# -*- encoding: utf-8 -*-
import abc
import collections
from abjad.tools import marktools
from abjad.tools.abctools import AbjadObject


class QSchemaItem(AbjadObject):
    '''`QSchemaItem` represents a change of state in the timeline of a 
    quantization process.

    `QSchemaItem` is abstract and immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_search_tree',
        '_tempo',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self,
        search_tree=None,
        tempo=None,
        ):
        from abjad.tools import quantizationtools
        if search_tree is not None:
            assert isinstance(search_tree, quantizationtools.SearchTree)
        self._search_tree = search_tree
        if tempo is not None:
            tempo = marktools.Tempo(tempo)
            assert not tempo.is_imprecise
        self._tempo = tempo

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __getnewargs__(self):
        r'''Returns self as a plain tuple. Used by copy and pickle.
        '''
        raise NotImplementedError

    def __format__(self, format_specification=''):
        r'''Formats q schema item.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        if format_specification in ('', 'storage'):
            return self._tools_package_qualified_indented_repr
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def search_tree(self):
        r'''The optionally defined search tree.

        Returns search tree or none.
        '''
        return self._search_tree

    @property
    def tempo(self):
        r'''The optionally defined tempo mark.

        Returns tempo mark or none.
        '''
        return self._tempo
