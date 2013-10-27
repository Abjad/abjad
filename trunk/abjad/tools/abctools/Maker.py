# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class Maker(AbjadObject):
    r'''Abstract base class for all maker classers.
    '''

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self):
        raise NotImplemented

    ### PUBLIC PROPERTIES ###

    @property
    def storage_format(self):
        r'''Storage format of maker.

        Returns string.
        '''
        return self._tools_package_qualified_indented_repr

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def new(self):
        raise NotImplemented
