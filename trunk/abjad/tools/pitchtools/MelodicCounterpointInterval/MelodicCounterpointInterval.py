from abjad.tools.pitchtools._CounterpointInterval import _CounterpointInterval
from abjad.tools.pitchtools._MelodicInterval import _MelodicInterval


class MelodicCounterpointInterval(_CounterpointInterval, _MelodicInterval):
    '''.. versionadded:: 2.0

    Abjad model of melodic counterpoint interval::

        abjad> pitchtools.MelodicCounterpointInterval(-9)
        MelodicCounterpointInterval(-9)

    Melodic counterpoint intervals are immutable.
    '''

    def __new__(klass, number):
        self = object.__new__(klass)
        if not isinstance(number, int):
            raise TypeError('must be integer.')
        if number == 0:
            raise ValueError('must be nonzero integer.')
        if abs(number) == 1:
            number = 1
        object.__setattr__(self, '_number', number)
        return self

    ### OVERLOADS ###

    def __str__(self):
        return self._format_string

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return '%s%s' % (self._direction_symbol, abs(self.number))

    ### PUBLIC ATTRIBUTES ###

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
