import functools
import numbers
from abjad import enums
from abjad import mathtools
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.FormatSpecification import FormatSpecification
from . import constants


@functools.total_ordering
class Accidental(AbjadValueObject):
    """
    Accidental.

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

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_arrow',
        '_semitones',
        )

    ### INITIALIZER ##

    def __init__(self, name='', *, arrow=None):
        import abjad
        semitones = 0
        _arrow = None
        if name is None:
            pass
        elif isinstance(name, str):
            if name in constants._accidental_name_to_abbreviation:
                name = constants._accidental_name_to_abbreviation[name]
                semitones = constants._accidental_abbreviation_to_semitones[name]
            else:
                match = constants._comprehensive_accidental_regex.match(name)
                if not match:
                    try:
                        pitch = abjad.NamedPitch(name)
                        semitones = pitch.accidental.semitones
                        _arrow = pitch.accidental.arrow
                    except Exception:
                        message = 'can not instantiate {} from {!r}.'
                        message = message.format(type(self).__name__, name)
                        raise TypeError(message)
                else:
                    group_dict = match.groupdict()
                    if group_dict['alphabetic_accidental']:
                        prefix, _, suffix = name.partition('q')
                        if prefix.startswith('s'):
                            semitones += len(prefix)
                        elif prefix.startswith('f'):
                            semitones -= len(prefix)
                        if suffix == 's':
                            semitones += 0.5
                            if prefix == 't':
                                semitones += 1
                        elif suffix == 'f':
                            semitones -= 0.5
                            if prefix == 't':
                                semitones -= 1
                    elif group_dict['symbolic_accidental']:
                        semitones += name.count('#')
                        semitones -= name.count('b')
                        if name.endswith('+'):
                            semitones += 0.5
                        elif name.endswith('~'):
                            semitones -= 0.5
        elif isinstance(name, numbers.Number):
            semitones = float(name)
            assert (semitones % 1.) in (0., 0.5)
        elif hasattr(name, 'accidental'):
            _arrow = name.accidental.arrow
            semitones = name.accidental.semitones
        elif isinstance(name, type(self)):
            _arrow = name.arrow
            semitones = name.semitones
        else:
            try:
                pitch = abjad.NamedPitch(name)
                semitones = pitch.accidental.semitones
                _arrow = pitch.accidental.arrow
            except Exception:
                message = 'can not initialize accidental from value: {!r}'
                message = message.format(name)
                raise ValueError(message)
        semitones = mathtools.integer_equivalent_number_to_integer(semitones)
        self._semitones = semitones
        self._arrow = _arrow
        if arrow is not None:
            arrow = enums.VerticalAlignment.from_expr(arrow)
            if arrow is enums.Center:
                arrow = None
            self._arrow = arrow

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        """
        Adds `argument` to accidental.

        ..  container:: example

            >>> accidental = abjad.Accidental('qs')

            >>> accidental + accidental
            Accidental('sharp')

            >>> accidental + accidental + accidental
            Accidental('three-quarters sharp')

        Returns new accidental.
        """
        if not isinstance(argument, type(self)):
            message = 'can only add accidental to other accidental.'
            raise TypeError(message)
        semitones = self.semitones + argument.semitones
        return type(self)(semitones)

    def __call__(self, argument):
        """
        Calls accidental on `argument`.

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
        """
        if not hasattr(argument, '_apply_accidental'):
            message = 'do not know how to apply accidental to {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        return argument._apply_accidental(self)

    def __lt__(self, argument):
        """
        Is true when `argument` is an accidental with semitones greater
        than those of this accidental.

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
        """
        return self.semitones < argument.semitones

    def __neg__(self):
        """
        Negates accidental.

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
        """
        return type(self)(-self.semitones)

    def __radd__(self, argument):
        """
        Raises not implemented error on accidental.
        """
        raise NotImplementedError

    def __str__(self):
        """
        Gets string representation of accidental.

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
        """
        if self.semitones in constants._accidental_semitones_to_abbreviation:
            return constants._accidental_semitones_to_abbreviation[self.semitones]
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
        """
        Subtracts `argument` from accidental.

        ..  container:: example

            >>> accidental = abjad.Accidental('qs')

            >>> accidental - accidental
            Accidental('natural')

            >>> accidental - accidental - accidental
            Accidental('quarter flat')

        Returns new accidental.
        """
        if not isinstance(argument, type(self)):
            message = 'can only subtract accidental from other accidental.'
            raise TypeError(message)
        semitones = self.semitones - argument.semitones
        return type(self)(semitones)

    ### PRIVATE METHODS ###

    @classmethod
    def _get_all_accidental_abbreviations(class_):
        return list(constants._accidental_abbreviation_to_symbol.keys())

    @classmethod
    def _get_all_accidental_names(class_):
        return list(constants._accidental_name_to_abbreviation.keys())

    @classmethod
    def _get_all_accidental_semitone_values(class_):
        return list(constants._accidental_semitones_to_abbreviation.keys())

    def _get_format_specification(self):
        return FormatSpecification(
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
        return bool(constants._alphabetic_accidental_regex.match(argument))

    @classmethod
    def _is_symbol(class_, argument):
        if not isinstance(argument, str):
            return False
        return bool(constants._symbolic_accidental_regex.match(argument))

    ### PUBLIC PROPERTIES ###

    @property
    def arrow(self):
        """
        Gets arrow of accidental.

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

        Arrow property is currently a stub in the object model. You can set the
        property but accidental math and formatting currently ignore the
        setting.

        Returns up, down or none.
        """
        return self._arrow

    @property
    def name(self):
        """
        Gets name of accidental.

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
        """
        try:
            abbreviation = constants._accidental_semitones_to_abbreviation[self.semitones]
            name = constants._accidental_abbreviation_to_name[abbreviation]
        except KeyError:
            name = str(self)
        return name

    @property
    def semitones(self):
        """
        Gets semitones of accidental.

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
        """
        return self._semitones

    @property
    def symbol(self):
        """
        Gets symbol of accidental.

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
        """
        abbreviation = constants._accidental_semitones_to_abbreviation[self.semitones]
        symbol = constants._accidental_abbreviation_to_symbol[abbreviation]
        return symbol

    ### PUBLIC METHODS ###

    # TODO: move somewhere else; remove late imports
    @staticmethod
    def respell_with_flats(selection):
        r"""
        Respells `selection` with flats.

        ..  container:: example

            Respells notes in staff:

            >>> staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
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
                \new Staff
                {
                    c'8
                    df'8
                    d'8
                    ef'8
                    e'8
                    f'8
                }

        Returns none.
        """
        import abjad
        for leaf in abjad.iterate(selection).leaves():
            if isinstance(leaf, abjad.Note):
                leaf.written_pitch = leaf.written_pitch._respell_with_flats()
            elif isinstance(leaf, abjad.Chord):
                for note_head in leaf.note_heads:
                    pitch = note_head.written_pitch._respell_with_flats()
                    note_head.written_pitch = pitch

    # TODO: move somewhere else; remove late imports
    @staticmethod
    def respell_with_sharps(selection):
        r"""
        Respells `selection` with sharps.

        ..  container:: example

            Respells notes in staff:

            >>> staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
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
                \new Staff
                {
                    c'8
                    cs'8
                    d'8
                    ds'8
                    e'8
                    f'8
                }

        Returns none.
        """
        import abjad
        for leaf in abjad.iterate(selection).leaves():
            if isinstance(leaf, abjad.Note):
                leaf.written_pitch = leaf.written_pitch._respell_with_sharps()
            elif isinstance(leaf, abjad.Chord):
                for note_head in leaf.note_heads:
                    pitch = note_head.written_pitch._respell_with_sharps()
                    note_head.written_pitch = pitch
