import abc
from abjad.tools.pitchtools.IntervalObjectClass import IntervalObjectClass
from abjad.tools.pitchtools.MelodicObject import MelodicObject


class MelodicIntervalClassObject(IntervalObjectClass, MelodicObject):
    '''.. versionadded:: 2.0

    Melodic interval-class base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta
    __slots__ = ()
    
    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return '%s%s' % (self.direction_symbol, abs(self.number))

    ### PUBLIC ATTRIUBTES ###

    @property
    def direction_number(self):
        number = self.number
        if number < 0:
            return -1
        elif number == 0:
            return 0
        else:
            return 1

    @property
    def direction_symbol(self):
        number = self.number
        if number < 0:
            return '-'
        elif number == 0:
            return ''
        else:
            return '+'

    @property
    def direction_word(self):
        number = self.number
        if number < 0:
            return 'descending'
        elif number == 0:
            return ''
        else:
            return 'ascending'
