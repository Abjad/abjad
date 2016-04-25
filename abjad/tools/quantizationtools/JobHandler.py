# -*- coding: utf-8 -*-
import abc
from abjad.tools.abctools import AbjadObject


class JobHandler(AbjadObject):
    r'''Abstact job handler class from which concrete job handlers inherit.

    ``JobHandlers`` control how ``QuantizationJob`` instances are
    processed by the ``Quantizer``, either serially or in parallel.
    '''

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, jobs):
        r'''Calls job handler.
        '''
        raise NotImplementedError
