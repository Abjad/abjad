import abc
from abjad.tools import mathtools
from abjad.tools.pitchtools.ChromaticObject import ChromaticObject
from abjad.tools.pitchtools.IntervalObject import IntervalObject


class ChromaticIntervalObject(IntervalObject, ChromaticObject):
    '''.. versionadded:: 2.0

    Chromatic interval base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ('_number', )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, arg):
        if isinstance(arg, (int, float, long)):
            _number = arg
        elif isinstance(arg, IntervalObject):
            _number = arg.semitones
        else:
            raise TypeError('%s must be number or interval.' % arg)
        object.__setattr__(self, '_number', _number)

    ### SPECIAL METHODS ###

    def __abs__(self):
        from abjad.tools.pitchtools.HarmonicChromaticInterval import HarmonicChromaticInterval
        return HarmonicChromaticInterval(abs(self._number))

    def __add__(self, arg):
        if isinstance(arg, type(self)):
            number = self.number + arg.number
            return type(self)(number)
        raise TypeError('must be %s.'% type(self))

    def __copy__(self):
        return type(self)(self.number)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __float__(self):
        return float(self._number)

    def __int__(self):
        return int(self._number)

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._number)

    def __str__(self):
        return '%s' % self.number

    def __sub__(self, arg):
        if isinstance(arg, type(self)):
            number = self.number - arg.number
            return type(self)(number)
        raise TypeError('must be %s' % type(self))

    ### PUBLIC PROPERTIES ###

    @property
    def number(self):
        return self._number

    @property
    def semitones(self):
        return self.number
