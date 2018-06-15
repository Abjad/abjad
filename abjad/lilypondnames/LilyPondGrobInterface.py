import typing
from abjad.system.AbjadValueObject import AbjadValueObject


class LilyPondGrobInterface(AbjadValueObject):
    """
    LilyPond grob interface.

    ..  container:: example

        >>> interface = abjad.lilypondnames.LilyPondGrobInterface('beam-interface')
        >>> abjad.f(interface)
        LilyPondGrobInterface(name='beam-interface')

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        )

    _identity_map: typing.Dict[str, 'LilyPondGrobInterface'] = {}

    ### CONSTRUCTOR ###

    def __new__(class_, name='grob-interface'):
        if name in class_._identity_map:
            obj = class_._identity_map[name]
        else:
            obj = object.__new__(class_)
            class_._identity_map[name] = obj
        return obj

    ### INITIALIZER ###

    def __init__(self, name: str = 'grob-interface') -> None:
        from abjad.ly import interface_properties
        assert name in interface_properties
        self._name = name

    ### PUBLIC METHODS ###

    @staticmethod
    def list_all_interfaces() -> typing.Tuple['LilyPondGrobInterface', ...]:
        """
        Lists all interfaces.

        ..  container:: example

            >>> for grob_interface in abjad.lilypondnames.LilyPondGrobInterface.list_all_interfaces():
            ...     grob_interface
            ...
            LilyPondGrobInterface(name='accidental-interface')
            LilyPondGrobInterface(name='accidental-placement-interface')
            LilyPondGrobInterface(name='accidental-suggestion-interface')
            LilyPondGrobInterface(name='align-interface')
            LilyPondGrobInterface(name='ambitus-interface')
            LilyPondGrobInterface(name='arpeggio-interface')
            LilyPondGrobInterface(name='axis-group-interface')
            LilyPondGrobInterface(name='balloon-interface')
            LilyPondGrobInterface(name='bar-line-interface')
            LilyPondGrobInterface(name='bass-figure-alignment-interface')
            LilyPondGrobInterface(name='bass-figure-interface')
            LilyPondGrobInterface(name='beam-interface')
            LilyPondGrobInterface(name='bend-after-interface')
            LilyPondGrobInterface(name='break-alignable-interface')
            LilyPondGrobInterface(name='break-aligned-interface')
            LilyPondGrobInterface(name='break-alignment-interface')
            LilyPondGrobInterface(name='breathing-sign-interface')
            LilyPondGrobInterface(name='chord-name-interface')
            LilyPondGrobInterface(name='clef-interface')
            LilyPondGrobInterface(name='clef-modifier-interface')
            LilyPondGrobInterface(name='cluster-beacon-interface')
            LilyPondGrobInterface(name='cluster-interface')
            LilyPondGrobInterface(name='custos-interface')
            LilyPondGrobInterface(name='dot-column-interface')
            LilyPondGrobInterface(name='dots-interface')
            LilyPondGrobInterface(name='dynamic-interface')
            LilyPondGrobInterface(name='dynamic-line-spanner-interface')
            LilyPondGrobInterface(name='dynamic-text-interface')
            LilyPondGrobInterface(name='dynamic-text-spanner-interface')
            LilyPondGrobInterface(name='enclosing-bracket-interface')
            LilyPondGrobInterface(name='episema-interface')
            LilyPondGrobInterface(name='figured-bass-continuation-interface')
            LilyPondGrobInterface(name='finger-interface')
            LilyPondGrobInterface(name='fingering-column-interface')
            LilyPondGrobInterface(name='flag-interface')
            LilyPondGrobInterface(name='font-interface')
            LilyPondGrobInterface(name='footnote-interface')
            LilyPondGrobInterface(name='footnote-spanner-interface')
            LilyPondGrobInterface(name='fret-diagram-interface')
            LilyPondGrobInterface(name='glissando-interface')
            LilyPondGrobInterface(name='grace-spacing-interface')
            LilyPondGrobInterface(name='gregorian-ligature-interface')
            LilyPondGrobInterface(name='grid-line-interface')
            LilyPondGrobInterface(name='grid-point-interface')
            LilyPondGrobInterface(name='grob-interface')
            LilyPondGrobInterface(name='hairpin-interface')
            LilyPondGrobInterface(name='hara-kiri-group-spanner-interface')
            LilyPondGrobInterface(name='horizontal-bracket-interface')
            LilyPondGrobInterface(name='inline-accidental-interface')
            LilyPondGrobInterface(name='instrument-specific-markup-interface')
            LilyPondGrobInterface(name='item-interface')
            LilyPondGrobInterface(name='key-cancellation-interface')
            LilyPondGrobInterface(name='key-signature-interface')
            LilyPondGrobInterface(name='kievan-ligature-interface')
            LilyPondGrobInterface(name='ledger-line-spanner-interface')
            LilyPondGrobInterface(name='ledgered-interface')
            LilyPondGrobInterface(name='ligature-bracket-interface')
            LilyPondGrobInterface(name='ligature-head-interface')
            LilyPondGrobInterface(name='ligature-interface')
            LilyPondGrobInterface(name='line-interface')
            LilyPondGrobInterface(name='line-spanner-interface')
            LilyPondGrobInterface(name='lyric-extender-interface')
            LilyPondGrobInterface(name='lyric-hyphen-interface')
            LilyPondGrobInterface(name='lyric-interface')
            LilyPondGrobInterface(name='lyric-syllable-interface')
            LilyPondGrobInterface(name='mark-interface')
            LilyPondGrobInterface(name='measure-counter-interface')
            LilyPondGrobInterface(name='measure-grouping-interface')
            LilyPondGrobInterface(name='melody-spanner-interface')
            LilyPondGrobInterface(name='mensural-ligature-interface')
            LilyPondGrobInterface(name='metronome-mark-interface')
            LilyPondGrobInterface(name='multi-measure-interface')
            LilyPondGrobInterface(name='multi-measure-rest-interface')
            LilyPondGrobInterface(name='note-collision-interface')
            LilyPondGrobInterface(name='note-column-interface')
            LilyPondGrobInterface(name='note-head-interface')
            LilyPondGrobInterface(name='note-name-interface')
            LilyPondGrobInterface(name='note-spacing-interface')
            LilyPondGrobInterface(name='number-interface')
            LilyPondGrobInterface(name='only-prebreak-interface')
            LilyPondGrobInterface(name='ottava-bracket-interface')
            LilyPondGrobInterface(name='outside-staff-axis-group-interface')
            LilyPondGrobInterface(name='outside-staff-interface')
            LilyPondGrobInterface(name='paper-column-interface')
            LilyPondGrobInterface(name='parentheses-interface')
            LilyPondGrobInterface(name='percent-repeat-interface')
            LilyPondGrobInterface(name='percent-repeat-item-interface')
            LilyPondGrobInterface(name='piano-pedal-bracket-interface')
            LilyPondGrobInterface(name='piano-pedal-interface')
            LilyPondGrobInterface(name='piano-pedal-script-interface')
            LilyPondGrobInterface(name='pitched-trill-interface')
            LilyPondGrobInterface(name='pure-from-neighbor-interface')
            LilyPondGrobInterface(name='rest-collision-interface')
            LilyPondGrobInterface(name='rest-interface')
            LilyPondGrobInterface(name='rhythmic-grob-interface')
            LilyPondGrobInterface(name='rhythmic-head-interface')
            LilyPondGrobInterface(name='script-column-interface')
            LilyPondGrobInterface(name='script-interface')
            LilyPondGrobInterface(name='self-alignment-interface')
            LilyPondGrobInterface(name='semi-tie-column-interface')
            LilyPondGrobInterface(name='semi-tie-interface')
            LilyPondGrobInterface(name='separation-item-interface')
            LilyPondGrobInterface(name='side-position-interface')
            LilyPondGrobInterface(name='slur-interface')
            LilyPondGrobInterface(name='spaceable-grob-interface')
            LilyPondGrobInterface(name='spacing-interface')
            LilyPondGrobInterface(name='spacing-options-interface')
            LilyPondGrobInterface(name='spacing-spanner-interface')
            LilyPondGrobInterface(name='span-bar-interface')
            LilyPondGrobInterface(name='spanner-interface')
            LilyPondGrobInterface(name='staff-grouper-interface')
            LilyPondGrobInterface(name='staff-spacing-interface')
            LilyPondGrobInterface(name='staff-symbol-interface')
            LilyPondGrobInterface(name='staff-symbol-referencer-interface')
            LilyPondGrobInterface(name='stanza-number-interface')
            LilyPondGrobInterface(name='stem-interface')
            LilyPondGrobInterface(name='stem-tremolo-interface')
            LilyPondGrobInterface(name='string-number-interface')
            LilyPondGrobInterface(name='stroke-finger-interface')
            LilyPondGrobInterface(name='system-interface')
            LilyPondGrobInterface(name='system-start-delimiter-interface')
            LilyPondGrobInterface(name='system-start-text-interface')
            LilyPondGrobInterface(name='tab-note-head-interface')
            LilyPondGrobInterface(name='text-interface')
            LilyPondGrobInterface(name='text-script-interface')
            LilyPondGrobInterface(name='tie-column-interface')
            LilyPondGrobInterface(name='tie-interface')
            LilyPondGrobInterface(name='time-signature-interface')
            LilyPondGrobInterface(name='trill-pitch-accidental-interface')
            LilyPondGrobInterface(name='trill-spanner-interface')
            LilyPondGrobInterface(name='tuplet-bracket-interface')
            LilyPondGrobInterface(name='tuplet-number-interface')
            LilyPondGrobInterface(name='unbreakable-spanner-interface')
            LilyPondGrobInterface(name='vaticana-ligature-interface')
            LilyPondGrobInterface(name='volta-bracket-interface')
            LilyPondGrobInterface(name='volta-interface')

        """
        from abjad.ly import interface_properties
        return tuple(
            LilyPondGrobInterface(_)
            for _ in sorted(interface_properties)
            )

    ### PUBLIC PROPERTIES ###

    @property
    def name(self) -> str:
        """
        Gets name of LilyPond grob interface.

        ..  container:: example

            >>> interface = abjad.lilypondnames.LilyPondGrobInterface('beam-interface')
            >>> interface.name
            'beam-interface'

        """
        return self._name

    @property
    def property_names(self) -> typing.Tuple[str, ...]:
        """
        Gets property names of LilyPond grob interface.

        ..  container:: example

            >>> interface = abjad.lilypondnames.LilyPondGrobInterface('beam-interface')
            >>> for property_name in interface.property_names:
            ...     property_name
            ...
            'X-positions'
            'annotation'
            'auto-knee-gap'
            'beam-thickness'
            'beamed-stem-shorten'
            'beaming'
            'break-overshoot'
            'clip-edges'
            'collision-interfaces'
            'collision-voice-only'
            'concaveness'
            'damping'
            'details'
            'direction'
            'gap'
            'gap-count'
            'grow-direction'
            'inspect-quants'
            'knee'
            'length-fraction'
            'neutral-direction'
            'positions'
            'skip-quanting'

        """
        from abjad.ly import interface_properties
        names = interface_properties[self.name]
        assert isinstance(names, list), repr(names)
        assert all(isinstance(_, str) for _ in names), repr(names)
        return tuple(names)
