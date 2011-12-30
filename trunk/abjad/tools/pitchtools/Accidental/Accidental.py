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

    __slots__ = ('_alphabetic_string', '_is_adjusted', '_name', '_semitones', '_symbolic_string')

    def __new__(klass, arg = ''):
        self = object.__new__(klass)
        # initialize symbolic string from arg
        if arg in self._all_accidental_alphabetic_strings:
            _alphabetic_string = arg
        elif arg in self._all_accidental_symbolic_strings:
            _alphabetic_string = self._symbolic_string_to_alphabetic_string[arg]
        elif arg in self._all_accidental_names:
            _alphabetic_string = self._name_to_alphabetic_string[arg]
        elif arg in self._all_accidental_semitone_values:
            _alphabetic_string = self._semitones_to_alphabetic_string[arg]
        elif isinstance(arg, type(self)):
            _alphabetic_string = arg.alphabetic_string
        elif isinstance(arg, type(None)):
            _alphabetic_string = ''
        else:
            raise ValueError('can not initialize accidental from value: %s' % arg)
        object.__setattr__(self, '_alphabetic_string', _alphabetic_string)
        # initialize derived attributes
        _semitones = self._alphabetic_string_to_semitones[self.alphabetic_string]
        object.__setattr__(self, '_semitones', _semitones)
        _name = self._alphabetic_string_to_name[self.alphabetic_string]
        object.__setattr__(self, '_name', _name)
        _is_adjusted = not self.semitones == 0
        object.__setattr__(self, '_is_adjusted', _is_adjusted)
        _symbolic_string = self._alphabetic_string_to_symbolic_string[self.alphabetic_string]
        object.__setattr__(self, '_symbolic_string', _symbolic_string)
        return self

    def __getnewargs__(self):
        return (self.alphabetic_string,)

    ### OVERLOADS ###

    def __add__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError('can only add accidental to other accidental.')
        semitones = self.semitones + arg.semitones
        return type(self)(semitones)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.alphabetic_string == arg.alphabetic_string:
                return True
        return False

    def __ge__(self, arg):
        return self.semitones >= arg.semitones

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
        return "%s('%s')" % (type(self).__name__, self.alphabetic_string)

    def __str__(self):
        return self.alphabetic_string

    def __sub__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError('can only sub accidental from other accidental.')
        semitones = self.semitones - arg.semitones
        return type(self)(semitones)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _all_accidental_alphabetic_strings(self):
        return self._alphabetic_string_to_symbolic_string.keys()

    _alphabetic_string_to_name = {
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

    _alphabetic_string_to_semitones = {
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

    _alphabetic_string_to_symbolic_string = {
        'ff': 'bb',
        'tqf': 'b+',
        'f': 'b',
        'qf': 'b-',
        '': '',
        '!': '!',
        'qs': '#-',
        's': '#',
        'tqs': '#+',
        'ss': '##',
    }

    _name_to_alphabetic_string = {
        'double sharp'            : 'ss',
        'three-quarters sharp'  : 'tqs',
        'sharp'                     : 's',
        'quarter sharp'           : 'qs',
        'natural'                   : '',
        'forced natural'          : '!',
        'quarter flat'            : 'qf',
        'flat'                        : 'f',
        'three-quarters flat'   : 'tqf',
        'double flat'             :  'ff',
    }

    _semitones_to_alphabetic_string = {
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

    _symbolic_string_to_alphabetic_string = {
        ''   : '',
        '!'  : '!',
        'bb' : 'ff',
        'b+' : 'tqf',
        'b'  : 'f',
        'b-' : 'qf',
        '###' : 'ss',
        '#+' : 'tqs',
        '#'  : 's',
        '#-' : 'qs',
    }

    @property
    def _all_accidental_names(self):
        return self._name_to_alphabetic_string.keys()

    @property
    def _all_accidental_semitone_values(self):
        return self._semitones_to_alphabetic_string.keys()

    @property
    def _all_accidental_symbolic_strings(self):
        return self._symbolic_string_to_alphabetic_string.keys()

    ### PUBLIC ATTRIBUTES ###

    @property
    def alphabetic_string(self):
        '''Read-only alphabetic string::

            abjad> accidental = pitchtools.Accidental('s')
            abjad> accidental.alphabetic_string
            's'

        Return string.
        '''
        return self._alphabetic_string

    @property
    def format(self):
        '''Read-only LilyPond input format of accidental::

            abjad> accidental = pitchtools.Accidental('s')
            abjad> accidental.format
            's'

        Return string.
        '''
        return self._alphabetic_string

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
    def symbolic_string(self):
        '''Read-only symbolic string of accidental::

            abjad> accidental = pitchtools.Accidental('s')
            abjad> accidental.symbolic_string
            '#'

        Return string.
        '''
        return self._symbolic_string
