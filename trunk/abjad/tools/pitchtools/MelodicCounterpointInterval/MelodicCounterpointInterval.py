from abjad.tools.pitchtools.CounterpointIntervalObject import CounterpointIntervalObject
from abjad.tools.pitchtools.MelodicIntervalObject import MelodicIntervalObject


class MelodicCounterpointInterval(CounterpointIntervalObject, MelodicIntervalObject):
    '''.. versionadded:: 2.0

    Abjad model of melodic counterpoint interval::

        >>> pitchtools.MelodicCounterpointInterval(-9)
        MelodicCounterpointInterval(-9)

    Melodic counterpoint intervals are immutable.
    '''

    def __init__(self, number):
        if not isinstance(number, int):
            raise TypeError('must be integer.')
        if number == 0:
            raise ValueError('must be nonzero integer.')
        if abs(number) == 1:
            number = 1
        object.__setattr__(self, '_number', number)

    ### SPECIAL METHODS ###

    def __str__(self):
        return self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return '%s%s' % (self._direction_symbol, abs(self.number))

    ### PUBLIC PROPERTIES ###

    @property
    def direction_number(self):
        if self.number < 0:
            return -1
        elif self.number == 1:
            return 0
        elif 1 < self.number:
            return 1
        else:
            raise ValueError

    @property
    #def interval_class(self):
    def melodic_counterpoint_interval_class(self):
        from abjad.tools import pitchtools
        return pitchtools.MelodicCounterpointIntervalClass(self)
