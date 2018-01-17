import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class JobHandler(AbjadObject):
    r'''Abstact job-handler.

    ``JobHandlers`` control how ``QuantizationJob`` instances are
    processed by the ``Quantizer``, either serially or in parallel.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, jobs):
        r'''Calls job handler.
        '''
        raise NotImplementedError
