from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.abctools.AbjadObject import AbjadObject


class Segment(AbjadObject):
    r'''.. versionadded:: 1.0

    The current implementation of ``specificationtools`` directs
    user interaction towards the ``SegmentSpecification`` class.

    This ``Segment`` class is provided as a stub implementation
    to allow for type testing throughout the ``specificationtools`` package.

    The ``Segment`` class is not expected to be instantiated because
    segments are not instantiated the way that components (and divisions) are.
    
    But this class can be used if or when a need to instantiate segments arises.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = ABCMeta

    ### INITIALIZER ##

    @abstractmethod
    def __init__(self):
        pass
