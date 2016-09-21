# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Clef(AbjadValueObject):
    r'''A clef.

    ..  container:: example

        **Example 1.** At the beginning of a staff:

        ::

            >>> clef = Clef('treble')
            >>> clef
            Clef(name='treble')

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
            >>> show(staff) # doctest: +SKIP

    ..  container:: example

        **Example 2.** Some available clefs:

        ::

            >>> clef = Clef('treble')
            >>> attach(clef, staff)
            >>> clef = Clef('alto')
            >>> attach(clef, staff[1])
            >>> clef = Clef('bass')
            >>> attach(clef, staff[2])
            >>> clef = Clef('treble^8')
            >>> attach(clef, staff[3])
            >>> clef = Clef('bass_8')
            >>> attach(clef, staff[4])
            >>> clef = Clef('tenor')
            >>> attach(clef, staff[5])
            >>> clef = Clef('bass^15')
            >>> attach(clef, staff[6])
            >>> clef = Clef('percussion')
            >>> attach(clef, staff[7])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                \clef "treble"
                c'8
                \clef "alto"
                d'8
                \clef "bass"
                e'8
                \clef "treble^8"
                f'8
                \clef "bass_8"
                g'8
                \clef "tenor"
                a'8
                \clef "bass^15"
                b'8
                \clef "percussion"
                c''8
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_scope',
        '_middle_c_position',
        '_name',
        )

    _clef_name_to_middle_c_position = {
        'treble': -6,
        'alto': 0,
        'tenor': 2,
        'bass': 6,
        'french': -8,
        'soprano': -4,
        'mezzosoprano': -2,
        'baritone': 4,
        'varbaritone': 4,
        'percussion': 0,
        'tab': 0,
        }

    _format_slot = 'opening'

    ### INITIALIZER ###

    def __init__(self, name='treble'):
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        self._default_scope = scoretools.Staff
        if isinstance(name, str):
            self._name = name
        elif isinstance(name, type(self)):
            self._name = name.name
        else:
            message = 'can not initialize clef: {!r}.'
            message = message.format(name)
            raise TypeError(message)
        middle_c_position = self._calculate_middle_c_position(self._name)
        middle_c_position = pitchtools.StaffPosition(middle_c_position)
        self._middle_c_position = middle_c_position

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats clef.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            ::

                >>> clef = Clef('treble')
                >>> print(format(clef))
                indicatortools.Clef(
                    name='treble',
                    )

        ..  container:: example

            ::

                >>> clef = Clef('treble')
                >>> print(format(clef, 'lilypond'))
                \clef "treble"

        Returns string.
        '''
        if format_specification == 'lilypond':
            return self._lilypond_format
        superclass = super(Clef, self)
        return superclass.__format__(format_specification=format_specification)

    def __ne__(self, arg):
        r'''Is true when clef of `arg` does not equal clef name of clef.
        Otherwise false.

        ..  container:: example

            ::

                >>> clef_1 = Clef('treble')
                >>> clef_2 = Clef('alto')

            ::

                >>> clef_1 != clef_1
                False
                >>> clef_1 != clef_2
                True
                >>> clef_2 != clef_1
                True
                >>> clef_2 != clef_2
                False

        Returns true or false.
        '''
        superclass = super(Clef, self)
        return superclass.__ne__(arg)

    ### PRIVATE METHODS ###

    def _calculate_middle_c_position(self, clef_name):
        alteration = 0
        if '_' in self._name:
            base_name, part, suffix = clef_name.partition('_')
            if suffix == '8':
                alteration = 7
            elif suffix == '15':
                alteration = 13
            else:
                message = 'bad clef alteration suffix: {!r}.'
                message = message.format(suffix)
                raise Exception(message)
        elif '^' in self._name:
            base_name, part, suffix = clef_name.partition('^')
            if suffix == '8':
                alteration = -7
            elif suffix == '15':
                alteration = -13
            else:
                message = "bad clef alteration suffix: {!r}."
                message = message.format(suffix)
                raise Exception(message)
        else:
            base_name = clef_name
        return self._clef_name_to_middle_c_position[base_name] + alteration

    @classmethod
    def _list_clef_names(cls):
        return list(sorted(cls._clef_name_to_middle_c_position))

    ### PUBLIC METHODS ###

    @staticmethod
    def from_selection(selection):
        r'''Makes clef from `selection`.

        ..  container:: example

            ::

                >>> numbers = list(range(-12, -6))
                >>> notes = scoretools.make_notes(numbers, [Duration(1, 4)])
                >>> staff = Staff(notes)
                >>> Clef.from_selection(staff)
                Clef(name='bass')

            Choses between treble and bass based on minimal number of ledger
            lines.

        Returns new clef.
        '''
        from abjad.tools import pitchtools
        pitches = pitchtools.list_named_pitches_in_expr(selection)
        diatonic_pitch_numbers = [pitch.diatonic_pitch_number for pitch in pitches]
        max_diatonic_pitch_number = max(diatonic_pitch_numbers)
        min_diatonic_pitch_number = min(diatonic_pitch_numbers)
        lowest_treble_line_pitch = pitchtools.NamedPitch('e', 4)
        lowest_treble_line_diatonic_pitch_number = \
            lowest_treble_line_pitch.diatonic_pitch_number
        candidate_steps_below_treble = \
            lowest_treble_line_diatonic_pitch_number - min_diatonic_pitch_number
        highest_bass_line_pitch = pitchtools.NamedPitch('a', 3)
        highest_bass_line_diatonic_pitch_number = \
            highest_bass_line_pitch.diatonic_pitch_number
        candidate_steps_above_bass = max_diatonic_pitch_number - highest_bass_line_diatonic_pitch_number
        if candidate_steps_above_bass < candidate_steps_below_treble:
            return Clef('bass')
        else:
            return Clef('treble')

    ### PRIVATE PROPERTIES ###

    @property
    def _clef_name_to_staff_position_zero(self, clef_name):
        from abjad.tools import pitchtools
        return {
            'treble': pitchtools.NamedPitch('B4'),
            'alto': pitchtools.NamedPitch('C4'),
            'tenor': pitchtools.NamedPitch('A3'),
            'bass': pitchtools.NamedPitch('D3'),
            'french': pitchtools.NamedPitch('D5'),
            'soprano': pitchtools.NamedPitch('G4'),
            'mezzosoprano': pitchtools.NamedPitch('E4'),
            'baritone': pitchtools.NamedPitch('F3'),
            'varbaritone': pitchtools.NamedPitch('F3'),
            'percussion': None,
            'tab': None,
            }[clef_name]

    @property
    def _contents_repr_string(self):
        return repr(self._name)

    @property
    def _lilypond_format(self):
        return r'\clef "{}"'.format(self._name)

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of clef.

        ..  container:: example

            ::

                >>> clef = Clef('treble')
                >>> clef.default_scope
                <class 'abjad.tools.scoretools.Staff.Staff'>

        Clefs are staff-scoped by default.

        Returns staff.
        '''
        return self._default_scope

    @property
    def middle_c_position(self):
        r'''Gets middle C position of clef.

        ..  container:: example

            **Example 1.** Gets staff position of middle C in treble clef:

            ::

                >>> Clef('treble').middle_c_position
                StaffPosition(number=-6)

        ..  container:: example

            **Example 2.** Gets staff position of middle C in alto clef:

            ::

                >>> Clef('alto').middle_c_position
                StaffPosition(number=0)

        Returns nonnegative integer staff position.
        '''
        return self._middle_c_position

    @property
    def name(self):
        r'''Gets name of clef.

        ..  container:: example

            **Example 1.** Gets name treble clef:

            ::

                >>> Clef('treble').name
                'treble'

        ..  container:: example

            **Example 2.** Gets name of alto clef:

            ::

                >>> Clef('alto').name
                'alto'

        Returns string.
        '''
        return self._name
