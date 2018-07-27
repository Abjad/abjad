import typing
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.pitch.NamedPitch import NamedPitch
from abjad.pitch.StaffPosition import StaffPosition
from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.top.iterate import iterate


class Clef(AbjadValueObject):
    r"""
    Clef.

    ..  container:: example

        Some available clefs:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
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
            \new Staff
            {
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

    ..  container:: example

        Clefs can be tagged:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Clef('treble'), staff[0], tag='RED')
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff)
        \new Staff
        {
            \clef "treble" %! RED
            c'4
            d'4
            e'4
            f'4
        }

    ..  container:: example

        LilyPond can not handle simultaneous clefs:

        >>> voice_1 = abjad.Voice("e'8 g' f' a' g' b'")
        >>> abjad.attach(abjad.Clef('treble'), voice_1[0], context='Voice')
        >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
        >>> voice_1.consists_commands.append('Clef_engraver')
        >>> voice_2 = abjad.Voice("c'4. c,8 b,, a,,")
        >>> abjad.attach(abjad.Clef('treble'), voice_2[0], context='Voice')
        >>> abjad.attach(abjad.Clef('bass'), voice_2[1], context='Voice')
        >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
        >>> voice_2.consists_commands.append('Clef_engraver')
        >>> staff = abjad.Staff([voice_1, voice_2], is_simultaneous=True)
        >>> staff.remove_commands.append('Clef_engraver')
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \remove Clef_engraver
            }
            <<
                \new Voice
                \with
                {
                    \consists Clef_engraver
                }
                {
                    \voiceOne
                    \clef "treble"
                    e'8
                    g'8
                    f'8
                    a'8
                    g'8
                    b'8
                }
                \new Voice
                \with
                {
                    \consists Clef_engraver
                }
                {
                    \voiceTwo
                    \clef "treble"
                    c'4.
                    \clef "bass"
                    c,8
                    b,,8
                    a,,8
                }
            >>

        But Abjad components work fine:

        >>> for leaf in abjad.select(voice_1).leaves():
        ...     leaf, abjad.inspect(leaf).effective(abjad.Clef)
        ...
        (Note("e'8"), Clef('treble'))
        (Note("g'8"), Clef('treble'))
        (Note("f'8"), Clef('treble'))
        (Note("a'8"), Clef('treble'))
        (Note("g'8"), Clef('treble'))
        (Note("b'8"), Clef('treble'))

        >>> for leaf in abjad.select(voice_2).leaves():
        ...     leaf, abjad.inspect(leaf).effective(abjad.Clef)
        ...
        (Note("c'4."), Clef('treble'))
        (Note('c,8'), Clef('bass'))
        (Note('b,,8'), Clef('bass'))
        (Note('a,,8'), Clef('bass'))

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_hide',
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


    _context = 'Staff'

    _format_slot = 'opening'

    _parameter = True

    _redraw = True

    _to_width = {
        'alto': 2.75,
        'bass': 2.75,
        'percussion': 2.5,
        'tenor': 2.75,
        'treble': 2.5,
        }

    ### INITIALIZER ###

    def __init__(
        self,
        name: str = 'treble',
        *,
        hide: bool = None,
        ) -> None:
        if isinstance(name, str):
            self._name = name
        elif isinstance(name, type(self)):
            self._name = name.name
        else:
            raise TypeError('can not initialize clef: {name!r}.')
        if hide is not None:
            hide = bool(hide)
        self._hide = hide
        middle_c_position = self._calculate_middle_c_position(self._name)
        middle_c_position = StaffPosition(middle_c_position)
        self._middle_c_position = middle_c_position

    ### SPECIAL METHODS ###

    def __format__(self, format_specification='') -> str:
        r"""
        Formats clef.

        ..  container:: example

            >>> clef = abjad.Clef('treble')
            >>> print(format(clef))
            abjad.Clef('treble')

        ..  container:: example

            >>> clef = abjad.Clef('treble')
            >>> print(format(clef, 'lilypond'))
            \clef "treble"

        Returns string.
        """
        if format_specification == 'lilypond':
            return self._get_lilypond_format()
        return super().__format__(
            format_specification=format_specification,
            )

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

    def _clef_name_to_staff_position_zero(self, clef_name):
        return {
            'treble': NamedPitch('B4'),
            'alto': NamedPitch('C4'),
            'tenor': NamedPitch('A3'),
            'bass': NamedPitch('D3'),
            'french': NamedPitch('D5'),
            'soprano': NamedPitch('G4'),
            'mezzosoprano': NamedPitch('E4'),
            'baritone': NamedPitch('F3'),
            'varbaritone': NamedPitch('F3'),
            'percussion': None,
            'tab': None,
            }[clef_name]

    def _get_format_specification(self):
        return FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=[self.name],
            storage_format_is_indented=False,
            )

    def _get_lilypond_format(self):
        return rf'\clef "{self.name}"'

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if not self.hide:
            bundle.opening.commands.append(self._get_lilypond_format())
        return bundle

    @classmethod
    def _list_clef_names(class_):
        return list(sorted(class_._clef_name_to_middle_c_position))

    ### PUBLIC METHODS ###

    @staticmethod
    def from_selection(selection) -> 'Clef':
        """
        Makes clef from ``selection``.

        ..  container:: example

            >>> maker = abjad.NoteMaker()
            >>> notes = maker(range(-12, -6), [(1, 4)])
            >>> staff = abjad.Staff(notes)
            >>> abjad.Clef.from_selection(staff)
            Clef('bass')

            Choses between treble and bass based on minimal number of ledger
            lines.

        """
        pitches = iterate(selection).pitches()
        diatonic_pitch_numbers = [
            pitch._get_diatonic_pitch_number() for pitch in pitches
            ]
        max_diatonic_pitch_number = max(diatonic_pitch_numbers)
        min_diatonic_pitch_number = min(diatonic_pitch_numbers)
        lowest_treble_line_pitch = NamedPitch('E4')
        lowest_treble_line_diatonic_pitch_number = \
            lowest_treble_line_pitch._get_diatonic_pitch_number()
        candidate_steps_below_treble = \
            lowest_treble_line_diatonic_pitch_number - \
            min_diatonic_pitch_number
        highest_bass_line_pitch = NamedPitch('A3')
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
    def context(self) -> str:
        """
        Gets (historically conventional) context.

        ..  container:: example

            >>> clef = abjad.Clef('treble')
            >>> clef.context
            'Staff'

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def hide(self) -> typing.Optional[bool]:
        r"""
        Is true when clef should not appear in output (but should still
        determine effective clef).

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Clef('treble'), staff[0]) 
            >>> abjad.attach(abjad.Clef('alto', hide=True), staff[2]) 
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.f(staff)
            \new Staff
            {
                \clef "treble"
                c'4
                d'4
                e'4
                f'4
            }

            >>> for leaf in abjad.iterate(staff).leaves():
            ...     leaf, abjad.inspect(leaf).effective(abjad.Clef)
            ...
            (Note("c'4"), Clef('treble'))
            (Note("d'4"), Clef('treble'))
            (Note("e'4"), Clef('alto', hide=True))
            (Note("f'4"), Clef('alto', hide=True))

        """
        return self._hide

    @property
    def middle_c_position(self) -> int:
        """
        Gets middle C position of clef.

        ..  container:: example

            Gets staff position of middle C in treble clef:

            >>> abjad.Clef('treble').middle_c_position
            StaffPosition(-6)

        ..  container:: example

            Gets staff position of middle C in alto clef:

            >>> abjad.Clef('alto').middle_c_position
            StaffPosition(0)

        """
        return self._middle_c_position

    @property
    def name(self) -> str:
        """
        Gets name of clef.

        ..  container:: example

            Gets name treble clef:

            >>> abjad.Clef('treble').name
            'treble'

        ..  container:: example

            Gets name of alto clef:

            >>> abjad.Clef('alto').name
            'alto'

        """
        return self._name

    @property
    def parameter(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.Clef('treble').parameter
            True

        Class constant.
        """
        return self._parameter
        
    @property
    def redraw(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.Clef('treble').redraw
            True

        Class constant.
        """
        return self._redraw

    @property
    def tweaks(self) -> None:
        r"""
        Are not implemented on clef.
        
        The LilyPond ``\clef`` command refuses tweaks.

        Override the LilyPond ``Clef`` grob instead.
        """
        pass
