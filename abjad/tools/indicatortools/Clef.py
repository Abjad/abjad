# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class Clef(AbjadObject):
    r'''A clef.

    ..  container:: example

        ::

            >>> clef = Clef('treble')
            >>> clef
            Clef(name='treble')

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
            >>> show(staff) # doctest: +SKIP

    ..  container:: example

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

    def __copy__(self, *args):
        r'''Copies clef.

        ..  container:: example

            ::

                >>> import copy
                >>> clef_1 = Clef('alto')
                >>> clef_2 = copy.copy(clef_1)

            ::

                >>> clef_1, clef_2
                (Clef(name='alto'), Clef(name='alto'))

            ::

                >>> clef_1 == clef_2
                True

            ::

                >>> clef_1 is clef_2
                False

        Returns new clef.
        '''
        return type(self)(self.name)

    def __eq__(self, expr):
        r'''Is true when `expr` is a clef with name equal to that of this clef.
        Otherwise false.

        ..  container:: example

            ::

                >>> clef_1 = Clef('treble')
                >>> clef_2 = Clef('alto')

            ::

                >>> clef_1 == clef_1
                True
                >>> clef_1 == clef_2
                False
                >>> clef_2 == clef_1
                False
                >>> clef_2 == clef_2
                True

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            return self._name == expr._name
        return False

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

        Returns string.
        '''
        if format_specification == 'lilypond':
            return self._lilypond_format
        superclass = super(Clef, self)
        return superclass.__format__(format_specification=format_specification)

    def __hash__(self):
        r'''Hashes clef.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(Clef, self).__hash__()

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

        Returns boolean.
        '''
        superclass = super(Clef, self)
        return superclass.__ne__(arg)

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='name',
                command='nm',
                editor=idetools.getters.get_string,
                ),
            )

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

    ### PUBLIC PROPERTIES ###

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

    def named_pitch_to_staff_position(self, named_pitch):
        r'''Changes `named_pitch` to staff position.

        ..  container:: example

            **Example 1.** Gets staff positions of fourth-octave pitches
            in treble clef:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
                >>> clef = Clef('treble')
                >>> for note in staff:
                ...     named_pitch = note.written_pitch
                ...     staff_position = clef.named_pitch_to_staff_position(named_pitch)
                ...     message = '{}\t{!s}'
                ...     message = message.format(named_pitch, staff_position) 
                ...     print(message)
                c'	StaffPosition(-6)
                d'	StaffPosition(-5)
                e'	StaffPosition(-4)
                f'	StaffPosition(-3)
                g'	StaffPosition(-2)
                a'	StaffPosition(-1)
                b'	StaffPosition(0)
                c''	StaffPosition(1)

        ..  container:: example

            **Example 2.** Gets staff positions of third-octave pitches
            in bass clef:

            ::

                >>> staff = Staff("c8 d8 e8 f8 g8 a8 b8 c'8")
                >>> clef = Clef('bass')
                >>> for note in staff:
                ...     named_pitch = note.written_pitch
                ...     staff_position = clef.named_pitch_to_staff_position(named_pitch)
                ...     message = '{}\t{!s}'
                ...     message = message.format(named_pitch, staff_position) 
                ...     print(message)

            .. todo:: Make this work.

        Returns staff position.
        '''
        from abjad.tools import pitchtools
        number = abs(named_pitch.diatonic_pitch_number)
        number += self.middle_c_position.number
        return pitchtools.StaffPosition(number)

    def staff_position_to_named_pitch(self, staff_position):
        r'''Changes `staff_position` to named pitch.

        ..  container:: example

            **Example 1.** Gets named pitches inside treble staff:

            ::

                >>> clef = Clef('treble')
                >>> for staff_position in range(-4, 5):
                ...     named_pitch = clef.staff_position_to_named_pitch(staff_position)
                ...     message = '{}\t{!s}'
                ...     message = message.format(staff_position, named_pitch) 
                ...     print(message)


        Returns named pitch.
        '''
        from abjad.tools import pitchtools
        if not isinstance(staff_position, pitchtools.StaffPosition):
            staff_position = pitchtools.StaffPosition(staff_position)
        center_pitch = self._clef_name_to_staff_position_zero(self.name)
        diatonic_pitch_number = center_pitch.diatonic_pitch_number
        diatonic_pitch_number += staff_position.number
        named_pitch = pitchtools.NamedPitch.from_diatonic_pitch_number(
            diatonic_pitch_number)
        return named_pitch