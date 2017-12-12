import functools
import re
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadValueObject


@functools.total_ordering
class Accidental(AbjadValueObject):
    '''Accidental.

    ..  container:: example

            >>> abjad.Accidental('ff')
            Accidental('double flat')

        >>> abjad.Accidental('tqf')
        Accidental('three-quarters flat')

        >>> abjad.Accidental('f')
        Accidental('flat')

        >>> abjad.Accidental('')
        Accidental('natural')

        >>> abjad.Accidental('qs')
        Accidental('quarter sharp')

        >>> abjad.Accidental('s')
        Accidental('sharp')

        >>> abjad.Accidental('tqs')
        Accidental('three-quarters sharp')

        >>> abjad.Accidental('ss')
        Accidental('double sharp')

    ..  container:: example

        Generalized accidentals are allowed:

        >>> abjad.Accidental('ssss')
        Accidental('ssss')

    '''

    ### CLASS VARIABLES ###

    _abbreviation_to_name = {
        'ss': 'double sharp',
        'tqs': 'three-quarters sharp',
        's': 'sharp',
        'qs': 'quarter sharp',
        '': 'natural',
        'qf': 'quarter flat',
        'f': 'flat',
        'tqf': 'three-quarters flat',
        'ff': 'double flat',
        }

    _abbreviation_to_semitones = {
        'ff': -2,
        'tqf': -1.5,
        'f': -1,
        'qf': -0.5,
        '': 0,
        'qs': 0.5,
        's': 1,
        'tqs': 1.5,
        'ss': 2,
        }

    _abbreviation_to_symbol = {
        'ff': 'bb',
        'tqf': 'b~',
        'f': 'b',
        'qf': '~',
        '': '',
        'qs': '+',
        's': '#',
        'tqs': '#+',
        'ss': '##',
        }

    _alphabetic_accidental_regex_body = """
        (?P<alphabetic_accidental>
        [s]*(qs)?
        |[f]*(qf)?
        |t?q?[fs]
        |)
        """

    _alphabetic_accidental_regex = re.compile(
        '^{}$'.format(_alphabetic_accidental_regex_body),
        re.VERBOSE,
        )

    _comprehensive_regex_body = """
        (?P<comprehensive_accidental>
        [s]*(qs)?
        |[f]*(qf)?
        |t?q?[fs]
        |[#]+[+]?
        |[b]+[~]?
        |[+]
        |[~]
        |
        )
        """

    _comprehensive_accidental_regex = re.compile(
        '^{}$'.format(_comprehensive_regex_body),
        re.VERBOSE,
        )

    _name_to_abbreviation = {
        'double sharp': 'ss',
        'three-quarters sharp': 'tqs',
        'sharp': 's',
        'quarter sharp': 'qs',
        'natural': '',
        'quarter flat': 'qf',
        'flat': 'f',
        'three-quarters flat': 'tqf',
        'double flat': 'ff',
        }

    _semitones_to_abbreviation = {
        -2: 'ff',
        -1.5: 'tqf',
        -1: 'f',
        -0.5: 'qf',
        0: '',
        0.5: 'qs',
        1: 's',
        1.5: 'tqs',
        2: 'ss',
        }

    _symbol_regex_body = '''
        (?P<symbol>
        [#]+[+]?
        |[b]+[~]?
        |[+]
        |[~]
        |
        )
        '''

    _symbol_regex = re.compile(
        '^{}$'.format(_symbol_regex_body),
        re.VERBOSE,
        )

    _symbol_to_abbreviation = {
        'bb': 'ff',
        'b~': 'tqf',
        'b': 'f',
        '~': 'qf',
        '': '',
        '!': '!',
        '+': 'qs',
        '#': 's',
        '#+': 'tqs',
        '##': 'ss',
        }

    _symbol_to_semitones = {
        'bb': -2,
        'b~': -1.5,
        'b': -1,
        '~': -0.5,
        '': 0,
        '+': 0.5,
        '#': 1,
        '#+': 1.5,
        '##': 2,
        'ff': -2,
        'tqf': 1.5,
        'f': -1,
        'qf': -0.5,
        'qs': 0.5,
        's': 1,
        'tqs': 1.5,
        'ss': 2,
        }

    __slots__ = (
        '_arrow',
        '_semitones',
        )

    ### INITIALIZER ##

    def __init__(self, name='', arrow=None):
        import abjad
        if name is None:
            semitones = 0
        elif isinstance(name, str):
            semitones = 0
            if self._is_abbreviation(name):
                if name in self._abbreviation_to_semitones:
                    semitones = self._abbreviation_to_semitones[name]
                else:
                    while name and name.startswith(('f', 's')):
                        if name[0] == 's':
                            semitones += 1
                        else:
                            semitones -= 1
                        name = name[1:]
                    if name == 'qs':
                        semitones += 0.5
                    elif name == 'qf':
                        semitones -= 0.5
            elif self._is_symbol(name):
                if name in self._symbol_to_semitones:
                    semitones = self._symbol_to_semitones[name]
                else:
                    while name and name.startswith(('b', '#')):
                        if name[0] == '#':
                            semitones += 1
                        else:
                            semitones -= 1
                        name = name[1:]
                    if name == '+':
                        semitones += 0.5
                    elif name == '~':
                        semitones -= 0.5
            elif name in self._name_to_abbreviation:
                name = self._name_to_abbreviation[name]
                semitones = self._abbreviation_to_semitones[name]
            else:
                message = 'can not initialize accidental from value: {!r}'
                message = message.format(name)
                raise ValueError(message)
        elif isinstance(name, type(self)):
            semitones = name.semitones
        elif isinstance(name, (int, float)):
            semitones = float(name)
            assert (semitones % 1.) in (0., 0.5)
        elif hasattr(name, 'accidental'):
            semitones = name.accidental.semitones
        else:
            message = 'can not initialize accidental from value: {!r}'
            message = message.format(name)
            raise ValueError(message)
        semitones = mathtools.integer_equivalent_number_to_integer(semitones)
        self._semitones = semitones
        if arrow not in (None, abjad.Up, abjad.Down):
            message = 'arrow must be none, up or down: {!r}.'
            message = message.format(arrow)
            raise TypeError(message)
        self._arrow = arrow

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r'''Adds `argument` to accidental.

        ..  container:: example

            >>> accidental = abjad.Accidental('qs')

            >>> accidental + accidental
            Accidental('sharp')

            >>> accidental + accidental + accidental
            Accidental('three-quarters sharp')

        Returns new accidental.
        '''
        if not isinstance(argument, type(self)):
            message = 'can only add accidental to other accidental.'
            raise TypeError(message)
        semitones = self.semitones + argument.semitones
        return type(self)(semitones)

    def __call__(self, argument):
        r'''Calls accidental on `argument`.

        >>> accidental = abjad.Accidental('s')

        ..  container:: example

            Calls accidental on pitches:

            >>> accidental(abjad.NamedPitch("c''"))
            NamedPitch("cs''")

            >>> accidental(abjad.NamedPitch("cqs''"))
            NamedPitch("ctqs''")

            >>> accidental(abjad.NumberedPitch(12))
            NumberedPitch(13)

            >>> accidental(abjad.NumberedPitch(12.5))
            NumberedPitch(13.5)

        ..  container:: example

            Calls accidental on pitch-classes:

            >>> accidental(abjad.NamedPitchClass('c'))
            NamedPitchClass('cs')

            >>> accidental(abjad.NamedPitchClass('cqs'))
            NamedPitchClass('ctqs')

            >>> accidental(abjad.NumberedPitchClass(0))
            NumberedPitchClass(1)

            >>> accidental(abjad.NumberedPitchClass(0.5))
            NumberedPitchClass(1.5)

        Returns new object of `argument` type.
        '''
        if not hasattr(argument, '_apply_accidental'):
            message = 'do not know how to apply accidental to {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        return argument._apply_accidental(self)

    def __lt__(self, argument):
        r'''Is true when `argument` is an accidental with semitones greater
        than those of this accidental. Otherwise false.

        ..  container:: example

            >>> accidental_1 = abjad.Accidental('f')
            >>> accidental_2 = abjad.Accidental('f')
            >>> accidental_3 = abjad.Accidental('s')

            >>> accidental_1 < accidental_1
            False
            >>> accidental_1 < accidental_2
            False
            >>> accidental_1 < accidental_3
            True

            >>> accidental_2 < accidental_1
            False
            >>> accidental_2 < accidental_2
            False
            >>> accidental_2 < accidental_3
            True

            >>> accidental_3 < accidental_1
            False
            >>> accidental_3 < accidental_2
            False
            >>> accidental_3 < accidental_3
            False

        Returns true or false.
        '''
        return self.semitones < argument.semitones

    def __neg__(self):
        r'''Negates accidental.

        ..  container:: example

            >>> -abjad.Accidental('ff')
            Accidental('double sharp')

            >>> -abjad.Accidental('tqf')
            Accidental('three-quarters sharp')

            >>> -abjad.Accidental('f')
            Accidental('sharp')

            >>> -abjad.Accidental('')
            Accidental('natural')

            >>> -abjad.Accidental('qs')
            Accidental('quarter flat')

            >>> -abjad.Accidental('s')
            Accidental('flat')

            >>> -abjad.Accidental('tqs')
            Accidental('three-quarters flat')

            >>> -abjad.Accidental('ss')
            Accidental('double flat')

        Returns new accidental.
        '''
        return type(self)(-self.semitones)

    def __radd__(self, argument):
        r'''Raises not implemented error on accidental.
        '''
        raise NotImplementedError

    def __str__(self):
        r'''Gets string representation of accidental.

        ..  container:: example

            >>> str(abjad.Accidental('ff'))
            'ff'

            >>> str(abjad.Accidental('tqf'))
            'tqf'

            >>> str(abjad.Accidental('f'))
            'f'

            >>> str(abjad.Accidental(''))
            ''

            >>> str(abjad.Accidental('qs'))
            'qs'

            >>> str(abjad.Accidental('s'))
            's'

            >>> str(abjad.Accidental('tqs'))
            'tqs'

            >>> str(abjad.Accidental('ss'))
            'ss'

        Returns string.
        '''
        if self.semitones in self._semitones_to_abbreviation:
            return self._semitones_to_abbreviation[self.semitones]
        character = 's'
        if self.semitones < 0:
            character = 'f'
        semitones = abs(self.semitones)
        semitones, remainder = divmod(semitones, 1.0)
        abbreviation = character * int(semitones)
        if remainder:
            abbreviation += 'q{}'.format(character)
        return abbreviation

    def __sub__(self, argument):
        r'''Subtracts `argument` from accidental.

        ..  container:: example

            >>> accidental = abjad.Accidental('qs')

            >>> accidental - accidental
            Accidental('natural')

            >>> accidental - accidental - accidental
            Accidental('quarter flat')

        Returns new accidental.
        '''
        if not isinstance(argument, type(self)):
            message = 'can only subtract accidental from other accidental.'
            raise TypeError(message)
        semitones = self.semitones - argument.semitones
        return type(self)(semitones)

    ### PRIVATE METHODS ###

    @classmethod
    def _get_all_accidental_abbreviations(class_):
        return list(class_._abbreviation_to_symbol.keys())

    @classmethod
    def _get_all_accidental_names(class_):
        return list(class_._name_to_abbreviation.keys())

    @classmethod
    def _get_all_accidental_semitone_values(class_):
        return list(class_._semitones_to_abbreviation.keys())

    def _get_format_specification(self):
        import abjad
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[self.name],
            storage_format_is_indented=False,
            storage_format_kwargs_names=['arrow'],
            )

    def _get_lilypond_format(self):
        return self._abbreviation

    @classmethod
    def _is_abbreviation(class_, argument):
        if not isinstance(argument, str):
            return False
        return bool(class_._alphabetic_accidental_regex.match(argument))

    @classmethod
    def _is_symbol(class_, argument):
        if not isinstance(argument, str):
            return False
        return bool(class_._symbol_regex.match(argument))

    ### PUBLIC PROPERTIES ###

    @property
    def arrow(self):
        r'''Gets arrow of accidental.

        ..  container:: example

            Most accidentals carry no arrow:

            >>> abjad.Accidental('sharp').arrow is None
            True

        ..  container:: example

            Sharp with up-arrow:

            >>> abjad.Accidental('sharp', arrow=abjad.Up).arrow
            Up

            Sharp with down-arrow:

            >>> abjad.Accidental('sharp', arrow=abjad.Down).arrow
            Down

        ArrowLineSegment property is currently a stub in the object model. You can set the
        property but accidental math and formatting currently ignore the
        setting.

        Returns up, down or none.
        '''
        return self._arrow

    @property
    def name(self):
        r'''Gets name of accidental.

        ..  container:: example

            >>> abjad.Accidental('ff').name
            'double flat'

            >>> abjad.Accidental('tqf').name
            'three-quarters flat'

            >>> abjad.Accidental('f').name
            'flat'

            >>> abjad.Accidental('').name
            'natural'

            >>> abjad.Accidental('qs').name
            'quarter sharp'

            >>> abjad.Accidental('s').name
            'sharp'

            >>> abjad.Accidental('tqs').name
            'three-quarters sharp'

            >>> abjad.Accidental('ss').name
            'double sharp'

        Returns string.
        '''
        try:
            abbreviation = self._semitones_to_abbreviation[self.semitones]
            name = self._abbreviation_to_name[abbreviation]
        except KeyError:
            name = str(self)
        return name

    @property
    def semitones(self):
        r'''Gets semitones of accidental.

        ..  container:: example

            >>> abjad.Accidental('ff').semitones
            -2

            >>> abjad.Accidental('tqf').semitones
            -1.5

            >>> abjad.Accidental('f').semitones
            -1

            >>> abjad.Accidental('').semitones
            0

            >>> abjad.Accidental('qs').semitones
            0.5

            >>> abjad.Accidental('s').semitones
            1

            >>> abjad.Accidental('tqs').semitones
            1.5

            >>> abjad.Accidental('ss').semitones
            2

        Returns number.
        '''
        return self._semitones

    @property
    def symbol(self):
        r'''Gets symbol of accidental.

        ..  container:: example

            >>> abjad.Accidental('ff').symbol
            'bb'

            >>> abjad.Accidental('tqf').symbol
            'b~'

            >>> abjad.Accidental('f').symbol
            'b'

            >>> abjad.Accidental('').symbol
            ''

            >>> abjad.Accidental('qs').symbol
            '+'

            >>> abjad.Accidental('s').symbol
            '#'

            >>> abjad.Accidental('tqs').symbol
            '#+'

            >>> abjad.Accidental('ss').symbol
            '##'

        Returns string.
        '''
        abbreviation = self._semitones_to_abbreviation[self.semitones]
        symbol = self._abbreviation_to_symbol[abbreviation]
        return symbol

    ### PUBLIC METHODS ###

    @staticmethod
    def respell_with_flats(selection):
        r'''Respells `selection` with flats.

        ..  container:: example

            Respells notes in staff:

            >>> staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                }

            >>> abjad.Accidental.respell_with_flats(staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    c'8
                    df'8
                    d'8
                    ef'8
                    e'8
                    f'8
                }

        Returns none.
        '''
        import abjad
        for leaf in abjad.iterate(selection).leaves():
            if isinstance(leaf, abjad.Note):
                leaf.written_pitch = leaf.written_pitch._respell_with_flats()
            elif isinstance(leaf, abjad.Chord):
                for note_head in leaf.note_heads:
                    pitch = note_head.written_pitch._respell_with_flats()
                    note_head.written_pitch = pitch

    @staticmethod
    def respell_with_sharps(selection):
        r'''Respells `selection` with sharps.

        ..  container:: example

            Respells notes in staff:

            >>> staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                }

            >>> abjad.Accidental.respell_with_sharps(staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    c'8
                    cs'8
                    d'8
                    ds'8
                    e'8
                    f'8
                }

        Returns none.
        '''
        import abjad
        for leaf in abjad.iterate(selection).leaves():
            if isinstance(leaf, abjad.Note):
                leaf.written_pitch = leaf.written_pitch._respell_with_sharps()
            elif isinstance(leaf, abjad.Chord):
                for note_head in leaf.note_heads:
                    pitch = note_head.written_pitch._respell_with_sharps()
                    note_head.written_pitch = pitch
