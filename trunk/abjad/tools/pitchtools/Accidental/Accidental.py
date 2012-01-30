from abjad.core import _Immutable
from abjad.core import _StrictComparator


class Accidental(_StrictComparator, _Immutable):
    '''.. versionadded:: 2.0

    Abjad model of the accidental:

    ::

        abjad> pitchtools.Accidental('s')
        Accidental('s')

    Accidentals are immutable.
    '''

    __slots__ = ('_alphabetic_accidental_abbreviation', '_is_adjusted', '_name', 
        '_semitones', '_symbolic_accidental_string')

    def __new__(klass, arg = ''):
        from abjad.tools import pitchtools
        self = object.__new__(klass)
        # initialize symbolic string from arg
        if pitchtools.is_alphabetic_accidental_abbreviation(arg):
            _alphabetic_accidental_abbreviation = arg
        elif pitchtools.is_symbolic_accidental_string(arg):
            _alphabetic_accidental_abbreviation = \
            pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation(arg)
        elif arg in self._all_accidental_names:
            _alphabetic_accidental_abbreviation = self._name_to_alphabetic_accidental_abbreviation[arg]
        elif arg in self._all_accidental_semitone_values:
            _alphabetic_accidental_abbreviation = self._semitones_to_alphabetic_accidental_abbreviation[arg]
        elif isinstance(arg, type(self)):
            _alphabetic_accidental_abbreviation = arg.alphabetic_accidental_abbreviation
        elif isinstance(arg, type(None)):
            _alphabetic_accidental_abbreviation = ''
        else:
            raise ValueError('can not initialize accidental from value: %s' % arg)
        object.__setattr__(self, '_alphabetic_accidental_abbreviation', _alphabetic_accidental_abbreviation)
        # initialize derived attributes
        _semitones = self._alphabetic_accidental_abbreviation_to_semitones[self.alphabetic_accidental_abbreviation]
        object.__setattr__(self, '_semitones', _semitones)
        _name = self._alphabetic_accidental_abbreviation_to_name[self.alphabetic_accidental_abbreviation]
        object.__setattr__(self, '_name', _name)
        _is_adjusted = not self.semitones == 0
        object.__setattr__(self, '_is_adjusted', _is_adjusted)
        _symbolic_accidental_string = \
            pitchtools.alphabetic_accidental_abbreviation_to_symbolic_accidental_string(
            self.alphabetic_accidental_abbreviation)
        object.__setattr__(self, '_symbolic_accidental_string', _symbolic_accidental_string)
        return self

    ### OVERLOADS ###

    def __add__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError('can only add accidental to other accidental.')
        semitones = self.semitones + arg.semitones
        return type(self)(semitones)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.alphabetic_accidental_abbreviation == arg.alphabetic_accidental_abbreviation:
                return True
        return False

    def __ge__(self, arg):
        return self.semitones >= arg.semitones

    def __getnewargs__(self):
        return (self.alphabetic_accidental_abbreviation,)

    def __gt__(self, arg):
        return self.semitones > arg.semitones

    def __le__(self, arg):
        return self.semitones <= arg.semitones

    def __lt__(self, arg):
        return self.semitones < arg.semitones

    def __ne__(self, arg):
        return not self == arg

    def __neg__(self):
        return type(self)(-self.semitones)

    def __nonzero__(self):
        return True

    def __repr__(self):
        return "%s('%s')" % (type(self).__name__, self.alphabetic_accidental_abbreviation)

    def __str__(self):
        return self.alphabetic_accidental_abbreviation

    def __sub__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError('can only sub accidental from other accidental.')
        semitones = self.semitones - arg.semitones
        return type(self)(semitones)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _all_accidental_alphabetic_accidental_abbreviations(self):
        return self._alphabetic_accidental_abbreviation_to_symbolic_accidental_string.keys()

    _alphabetic_accidental_abbreviation_to_name = {
        'ss'  : 'double sharp',
        'tqs' : 'three-quarters sharp',
        's'   : 'sharp',
        'qs'  : 'quarter-sharp',
        ''    : 'natural',
        '!'   : 'forced natural',
        'qf'  : 'quarter-flat',
        'f'   : 'flat',
        'tqf' : 'three-quarters flat',
        'ff'  : 'double flat',
    }

    _alphabetic_accidental_abbreviation_to_semitones = {
        'ff'  : -2,
        'tqf' : -1.5,
        'f'   : -1,
        'qf'  : -0.5,
        ''    : 0,
        '!'   : 0,
        'qs'  : 0.5,
        's'   : 1,
        'tqs' : 1.5,
        'ss'  : 2,
    }

    _name_to_alphabetic_accidental_abbreviation = {
        'double sharp'            : 'ss',
        'three-quarters sharp'    : 'tqs',
        'sharp'                   : 's',
        'quarter sharp'           : 'qs',
        'natural'                 : '',
        'forced natural'          : '!',
        'quarter flat'            : 'qf',
        'flat'                    : 'f',
        'three-quarters flat'     : 'tqf',
        'double flat'             :  'ff',
    }

    _semitones_to_alphabetic_accidental_abbreviation = {
        -2   : 'ff',
        -1.5 : 'tqf',
        -1   : 'f',
        -0.5 : 'qf',
        0    : '',
        0.5  : 'qs',
        1    : 's',
        1.5  : 'tqs',
        2    : 'ss',
    }

    @property
    def _all_accidental_names(self):
        return self._name_to_alphabetic_accidental_abbreviation.keys()

    @property
    def _all_accidental_semitone_values(self):
        return self._semitones_to_alphabetic_accidental_abbreviation.keys()

    ### PUBLIC ATTRIBUTES ###

    @property
    def alphabetic_accidental_abbreviation(self):
        '''Read-only alphabetic string::

            abjad> accidental = pitchtools.Accidental('s')
            abjad> accidental.alphabetic_accidental_abbreviation
            's'

        Return string.
        '''
        return self._alphabetic_accidental_abbreviation

    @property
    def format(self):
        '''Read-only LilyPond input format of accidental::

            abjad> accidental = pitchtools.Accidental('s')
            abjad> accidental.format
            's'

        Return string.
        '''
        return self._alphabetic_accidental_abbreviation

    @property
    def is_adjusted(self):
        '''True for all accidentals equal to a nonzero number of semitones. False otherwise::

            abjad> accidental = pitchtools.Accidental('s')
            abjad> accidental.is_adjusted
            True

        Return boolean.
        '''
        return self._is_adjusted

    @property
    def name(self):
        '''Read-only name of accidental::

            abjad> accidental = pitchtools.Accidental('s')
            abjad> accidental.name
            'sharp'

        Return string.
        '''
        return self._name

    @property
    def semitones(self):
        '''Read-only semitones of accidental::

            abjad> accidental = pitchtools.Accidental('s')
            abjad> accidental.semitones
            1

        Return number.
        '''
        return self._semitones

    @property
    def symbolic_accidental_string(self):
        '''Read-only symbolic string of accidental::

            abjad> accidental = pitchtools.Accidental('s')
            abjad> accidental.symbolic_accidental_string
            '#'

        Return string.
        '''
        return self._symbolic_accidental_string
