import abc
from abjad.tools.pitchtools.DiatonicObject import DiatonicObject
from abjad.tools.pitchtools.IntervalObjectClass import IntervalObjectClass


class DiatonicIntervalClassObject(IntervalObjectClass, DiatonicObject):
    '''.. versionadded:: 2.0

    Diatonic interval-class base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __abs__(self):
        from abjad.tools.pitchtools.HarmonicDiatonicIntervalClass import HarmonicDiatonicIntervalClass
        return HarmonicDiatonicIntervalClass(str(self))

    def __float__(self):
        return float(self._number)

    def __int__(self):
        return self._number

    def __repr__(self):
        return "%s('%s')" % (type(self).__name__, str(self))

    def __str__(self):
        return self._format_string

    ### PRIVATE PROPERTIES ###

    _acceptable_quality_strings = ('perfect', 'major', 'minor', 'diminished', 'augmented')

    @property
    def _format_string(self):
        return '%s%s' % (self._quality_abbreviation, self.number)

    _interval_number_to_interval_string = {1: 'unison', 2: 'second',
            3: 'third', 4: 'fourth', 5: 'fifth', 6: 'sixth',
            7: 'seventh', 8: 'octave'}

    _quality_abbreviation_to_quality_string = {
        'M': 'major', 'm': 'minor', 'P': 'perfect', 'aug': 'augmented', 'dim': 'diminished'}

    _quality_string_to_quality_abbreviation = {
            'major': 'M', 'minor': 'm', 'perfect': 'P', 'augmented': 'aug', 'diminished': 'dim'}

    @property
    def _interval_string(self):
        return self._interval_number_to_interval_string[abs(self.number)]

    @property
    def _quality_abbreviation(self):
        return self._quality_string_to_quality_abbreviation[self._quality_string]

    ### PUBLIC PROPERTIES ###

    @property
    def quality_string(self):
        return self._quality_string
