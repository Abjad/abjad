import abc
import functools
import uqbar.objects
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


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

    def __eq__(self, argument):
        """
        Check equality.
        """
        return uqbar.objects.compare_objects(self, argument, coerce=True)

    def __hash__(self):
        r'''Hashes interval-class.

        Returns integer.
        '''
        return uqbar.objects.get_hash(self)

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
