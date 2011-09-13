from abjad.tools import mathtools
from abjad.tools.pitchtools._Chromatic import _Chromatic
from abjad.tools.pitchtools._Interval import _Interval


class _ChromaticInterval(_Interval, _Chromatic):
    '''.. versionadded:: 2.0

    Chromatic interval base class.
    '''

    __slots__ = ('_number', )

    def __new__(klass, arg):
        self = object.__new__(klass)
        if isinstance(arg, (int, float, long)):
            _number = arg
        elif isinstance(arg, _Interval):
            _number = arg.semitones
        else:
            raise TypeError('%s must be number or interval.' % arg)
        object.__setattr__(self, '_number', _number)
        return self

    ### OVERLOADS ###

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

    ### PUBLIC ATTRIBUTES ###

    @property
    def number(self):
        return self._number

    @property
    def semitones(self):
        return self.number
