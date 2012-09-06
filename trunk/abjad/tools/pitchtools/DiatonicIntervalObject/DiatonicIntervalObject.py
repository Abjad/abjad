import abc
from abjad.tools import mathtools
from abjad.tools.pitchtools.DiatonicObject import DiatonicObject
from abjad.tools.pitchtools.IntervalObject import IntervalObject


class DiatonicIntervalObject(IntervalObject, DiatonicObject):
    '''.. versionadded:: 2.0

    Diatonic interval base class.
    '''

    ### INITIALIZER ##

    __metaclass__ = abc.ABCMeta

    __slots__ = ('_number', '_quality_string')

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, quality_string, number):
        if quality_string == 'diminished':
            if abs(number) == 1:
                raise IntervalError('diminished unison makes no sense.')
        if quality_string in self._acceptable_quality_strings:
            quality_string = quality_string
        else:
            raise ValueError("quality string '%s' must be in %s." % (
                quality_string, str(self._acceptable_quality_strings)))
        object.__setattr__(self, '_quality_string', quality_string)
        if isinstance(number, int):
            if int == 0:
                raise ValueError
            number = number
        else:
            raise ValueError('interval must be integer.')
        object.__setattr__(self, '_number', number)

    ### SPECIAL METHODS ###

    def __abs__(self):
        from abjad.tools.pitchtools.HarmonicDiatonicInterval import HarmonicDiatonicInterval
        return HarmonicDiatonicInterval(self.quality_string, self.number)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.quality_string == arg.quality_string:
                if self.number == arg.number:
                    return True
        return False

    def __float__(self):
        return float(self._number)

    def __int__(self):
        return self._number

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return "%s('%s')" % (type(self).__name__, self._format_string)

    def __str__(self):
        return self._format_string

    ### PRIVATE PROPERTIES ###

    _acceptable_quality_strings = ('perfect', 'major', 'minor', 'diminished', 'augmented')

    _quality_abbreviation_to_quality_string = {
        'M': 'major', 'm': 'minor', 'P': 'perfect', 'aug': 'augmented', 'dim': 'diminished'}

    @property
    def _format_string(self):
        return '%s%s' % (self._quality_abbreviation, self.number)

    @property
    def _interval_string(self):
        interval_to_string = {1: 'unison', 2: 'second', 3: 'third',
            4: 'fourth', 5: 'fifth', 6: 'sixth', 7: 'seventh', 8: 'octave',
            9: 'ninth', 10: 'tenth', 11: 'eleventh', 12: 'twelth',
            13: 'thirteenth', 14: 'fourteenth', 15: 'fifteenth'}
        try:
            interval_string = interval_to_string[abs(self.number)]
        except KeyError:
            abs_number = abs(self.number)
            residue = abs_number % 10
            if residue == 1:
                suffix = 'st'
            elif residue == 2:
                suffix = 'nd'
            elif residue == 3:
                suffix = 'rd'
            else:
                suffix = 'th'
            interval_string = '%s%s' % (abs_number, suffix)
        return interval_string

    @property
    def _quality_abbreviation(self):
        _quality_string_to_quality_abbreviation = {
            'major': 'M', 'minor': 'm', 'perfect': 'P',
            'augmented': 'aug', 'diminished': 'dim'}
        return _quality_string_to_quality_abbreviation[self.quality_string]

    ### PUBLIC PROPERTIES ###

    @property
    def diatonic_interval_class(self):
        from abjad.tools import pitchtools
        quality_string, number = self._quality_string, self.number
        return pitchtools.InversionEquivalentDiatonicIntervalClass(quality_string, number)

    @property
    def interval_class(self):
        return ((abs(self.number) - 1) % 7) + 1

    @property
    def interval_string(self):
        return self._interval_string

    @property
    def number(self):
        return self._number

    @property
    def quality_string(self):
        return self._quality_string

    @property
    def semitones(self):
        result = 0
        interval_class_number_to_semitones = {1: 0,  2: 1,  3: 3, 4: 5, 5: 7, 6: 8, 7: 10, 8:0}
        try:
            interval_class_number = abs(self.interval_class.number)
        except AttributeError:
            interval_class_number = self.number
        result += interval_class_number_to_semitones[interval_class_number]
        result += (abs(self.number) - 1) / 7 * 12
        quality_string_to_semitones = {
            'perfect': 0, 'major': 1, 'minor': 0, 'augmented': 1, 'diminished': -1}
        result += quality_string_to_semitones[self.quality_string]
        if self.number < 0:
            result *= -1
        return result

    @property
    def staff_spaces(self):
        return self.number - 1
