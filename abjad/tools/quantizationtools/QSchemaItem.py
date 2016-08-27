# -*- coding: utf-8 -*-
import abc
import collections
from abjad.tools import indicatortools
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
    def __init__(
        self,
        search_tree=None,
        tempo=None,
        ):
        from abjad.tools import quantizationtools
        if search_tree is not None:
            assert isinstance(search_tree, quantizationtools.SearchTree)
        self._search_tree = search_tree
        #if tempo is not None:
        #    tempo = indicatortools.Tempo(tempo)
        #    assert not tempo.is_imprecise
        if tempo is not None:
            if isinstance(tempo, tuple):
                tempo = indicatortools.Tempo(*tempo)
            assert not tempo.is_imprecise
        self._tempo = tempo

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats q schema item.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
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
        r'''The optionally defined tempo.

        Returns tempo or none.
        '''
        return self._tempo
