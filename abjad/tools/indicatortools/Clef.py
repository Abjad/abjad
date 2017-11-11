from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Clef(AbjadValueObject):
    r'''Clef.

    ..  container:: example

        At the beginning of a staff:

        >>> clef = abjad.Clef('treble')
        >>> clef
        Clef('treble')

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> abjad.show(staff) # doctest: +SKIP

    ..  container:: example

        Some available clefs:

        >>> clef = abjad.Clef('treble')
        >>> abjad.attach(clef, staff[0])
        >>> clef = abjad.Clef('alto')
        >>> abjad.attach(clef, staff[1])
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[2])
        >>> clef = abjad.Clef('treble^8')
        >>> abjad.attach(clef, staff[3])
        >>> clef = abjad.Clef('bass_8')
        >>> abjad.attach(clef, staff[4])
        >>> clef = abjad.Clef('tenor')
        >>> abjad.attach(clef, staff[5])
        >>> clef = abjad.Clef('bass^15')
        >>> abjad.attach(clef, staff[6])
        >>> clef = abjad.Clef('percussion')
        >>> abjad.attach(clef, staff[7])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
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
        '_context',
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
        import abjad
        self._context = 'Staff'
        if isinstance(name, str):
            self._name = name
        elif isinstance(name, type(self)):
            self._name = name.name
        else:
            message = 'can not initialize clef: {!r}.'
            message = message.format(name)
            raise TypeError(message)
        middle_c_position = self._calculate_middle_c_position(self._name)
        middle_c_position = abjad.StaffPosition(middle_c_position)
        self._middle_c_position = middle_c_position

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats clef.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            >>> clef = abjad.Clef('treble')
            >>> print(format(clef))
            abjad.Clef('treble')

        ..  container:: example

            >>> clef = abjad.Clef('treble')
            >>> print(format(clef, 'lilypond'))
            \clef "treble"

        Returns string.
        '''
        if format_specification == 'lilypond':
            return self._get_lilypond_format()
        superclass = super(Clef, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE PROPERTIES ###

    @property
    def _clef_name_to_staff_position_zero(self, clef_name):
        import abjad
        return {
            'treble': abjad.NamedPitch('B4'),
            'alto': abjad.NamedPitch('C4'),
            'tenor': abjad.NamedPitch('A3'),
            'bass': abjad.NamedPitch('D3'),
            'french': abjad.NamedPitch('D5'),
            'soprano': abjad.NamedPitch('G4'),
            'mezzosoprano': abjad.NamedPitch('E4'),
            'baritone': abjad.NamedPitch('F3'),
            'varbaritone': abjad.NamedPitch('F3'),
            'percussion': None,
            'tab': None,
            }[clef_name]

    @property
    def _contents_repr_string(self):
        return repr(self._name)

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

    def _get_format_specification(self):
        import abjad
        return abjad.FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=[self.name],
            storage_format_is_indented=False,
            )

    def _get_lilypond_format(self):
        return r'\clef "{}"'.format(self._name)

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        bundle.opening.commands.append(self._get_lilypond_format())
        return bundle

    @classmethod
    def _list_clef_names(class_):
        return list(sorted(class_._clef_name_to_middle_c_position))

    ### PUBLIC METHODS ###

    @staticmethod
    def from_selection(selection):
        r'''Makes clef from `selection`.

        ..  container:: example

            >>> maker = abjad.NoteMaker()
            >>> notes = maker(range(-12, -6), [(1, 4)])
            >>> staff = abjad.Staff(notes)
            >>> abjad.Clef.from_selection(staff)
            Clef('bass')

            Choses between treble and bass based on minimal number of ledger
            lines.

        Returns new clef.
        '''
        import abjad
        pitches = abjad.iterate(selection).pitches()
        diatonic_pitch_numbers = [
            pitch._get_diatonic_pitch_number() for pitch in pitches
            ]
        max_diatonic_pitch_number = max(diatonic_pitch_numbers)
        min_diatonic_pitch_number = min(diatonic_pitch_numbers)
        lowest_treble_line_pitch = abjad.NamedPitch('E4')
        lowest_treble_line_diatonic_pitch_number = \
            lowest_treble_line_pitch._get_diatonic_pitch_number()
        candidate_steps_below_treble = \
            lowest_treble_line_diatonic_pitch_number - \
            min_diatonic_pitch_number
        highest_bass_line_pitch = abjad.NamedPitch('A3')
        highest_bass_line_diatonic_pitch_number = \
            highest_bass_line_pitch._get_diatonic_pitch_number()
        candidate_steps_above_bass = \
            max_diatonic_pitch_number - highest_bass_line_diatonic_pitch_number
        if candidate_steps_above_bass < candidate_steps_below_treble:
            return Clef('bass')
        else:
            return Clef('treble')

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        r'''Gets default context of clef.

        ..  container:: example

            >>> clef = abjad.Clef('treble')
            >>> clef.context
            'Staff'

        Returns context or string.
        '''
        return self._context

    @property
    def middle_c_position(self):
        r'''Gets middle C position of clef.

        ..  container:: example

            Gets staff position of middle C in treble clef:

            >>> abjad.Clef('treble').middle_c_position
            StaffPosition(-6)

        ..  container:: example

            Gets staff position of middle C in alto clef:

            >>> abjad.Clef('alto').middle_c_position
            StaffPosition(0)

        Returns nonnegative integer staff position.
        '''
        return self._middle_c_position

    @property
    def name(self):
        r'''Gets name of clef.

        ..  container:: example

            Gets name treble clef:

            >>> abjad.Clef('treble').name
            'treble'

        ..  container:: example

            Gets name of alto clef:

            >>> abjad.Clef('alto').name
            'alto'

        Returns string.
        '''
        return self._name
