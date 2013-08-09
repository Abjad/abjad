# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class Flageolet(AbjadObject):
    r'''Abjad model of both natural and artificial harmonics.
    Abstract base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### PUBLIC PROPERTIES ###

    @property
    def suono_reale(self):
        r'''Actual sound of the harmonic when played.
        '''
        raise Exception('Not Implemented')
