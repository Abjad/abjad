from abjad.tools import mathtools
from abjad.tools.pitchtools._DiatonicIntervalClass import _DiatonicIntervalClass
from abjad.tools.pitchtools._MelodicIntervalClass import _MelodicIntervalClass


class MelodicDiatonicIntervalClass(_DiatonicIntervalClass, _MelodicIntervalClass):
    '''.. versionadded:: 2.0

    Abjad model of melodic diatonic interval-class::

        abjad> pitchtools.MelodicDiatonicIntervalClass('-M9')
        MelodicDiatonicIntervalClass('-M2')

    Melodic diatonic interval-classes are immutable.
    '''

    def __new__(klass, *args):
        from abjad.tools import pitchtools
        from abjad.tools.pitchtools.is_melodic_diatonic_interval_abbreviation import melodic_diatonic_interval_abbreviation_regex
        self = object.__new__(klass)
        if len(args) == 1:
            if isinstance(args[0], pitchtools.MelodicDiatonicInterval):
                quality_string = args[0]._quality_string
                number = args[0].number
            elif isinstance(args[0], str):
                match = melodic_diatonic_interval_abbreviation_regex.match(args[0])
                if match is None:
                    raise ValueError('"%s" does not have the form of an abbreviation.' % args[0])
                direction_string, quality_abbreviation, number_string = match.groups()
                quality_string = _DiatonicIntervalClass._quality_abbreviation_to_quality_string[quality_abbreviation]
                number = int(direction_string + number_string)
            else:
                raise TypeError('what type of instance is this?')
        else:
            quality_string, number = args
        if quality_string not in _DiatonicIntervalClass._acceptable_quality_strings:
            raise ValueError('not acceptable quality string.')
        if not isinstance(number, int):
            raise TypeError('must be integer.')
        if number == 0:
            raise ValueError('must be nonzero.')
        sign = mathtools.sign(number)
        abs_number = abs(number)
        if abs_number % 7 == 1 and 8 <= abs_number:
            number = 8
        else:
            number = abs_number % 7
            if number == 0:
                number = 7
        if not number == 1:
            number *= sign
        object.__setattr__(self, '_number', number)
        object.__setattr__(self, '_quality_string', quality_string)
        return self

    ### OVERLOADS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.direction_number == arg.direction_number:
                if self._quality_string == arg._quality_string:
                    if self.number == arg.number:
                        return True
        return False

    def __hash__(self):
        return hash(repr(self))

    def __ne__(self, arg):
        return not self == arg

    def __str__(self):
        return '%s%s%s' % (self.direction_symbol,
            self._quality_abbreviation, abs(self.number))

    ### PRIVATE ATTRIBUTES ###

    @property
    def _full_name(self):
        strings = []
        if self.direction_word:
            strings.append(self.direction_word)
        strings.extend([self._quality_string, self._interval_string])
        return ' '.join(strings)

    ### PUBLIC ATTRIBUTES ###

    @property
    def direction_number(self):
        if self.number < 1:
            return -1
        elif self.number == 1:
            return 0
        else:
            return 1

    @property
    def direction_symbol(self):
        if self.number < 1:
            return '-'
        elif self.number == 1:
            return ''
        else:
            return '+'

    @property
    def direction_word(self):
        if self.number < 1:
            return 'descending'
        elif self.number == 1:
            return ''
        else:
            return 'ascending'
