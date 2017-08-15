import abc
import functools
from abjad.tools.abctools import AbjadValueObject


@functools.total_ordering
class IntervalClass(AbjadValueObject):
    '''Abstract interval-class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Gets absolute value of interval-class.

        Returns new interval-class.
        '''
        return type(self)(abs(self._number))

    @abc.abstractmethod
    def __lt__(self, argument):
        r'''Is true when interval-class is less than `argument`.

        Returns true or false.
        '''
        raise NotImplementedError

    def __str__(self):
        r'''Gets string representation of interval-class.

        Returns string.
        '''
        return str(self.number)

    ### PUBLIC PROPERTIES ###

    @property
    def number(self):
        r'''Gets number of interval-class.

        Returns number.
        '''
        return self._number
