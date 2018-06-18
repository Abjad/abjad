import collections
from abjad.pitch.NumberedPitch import NumberedPitch
from abjad.pitch.PitchSet import PitchSet
from abjad.system.AbjadValueObject import AbjadValueObject


class PitchInequality(AbjadValueObject):
    """
    Pitch inequality.

    ..  container:: example

        >>> inequality = abjad.PitchInequality('&', 'C4 E4')
        >>> abjad.f(inequality)
        abjad.PitchInequality(
            operator_string='&',
            pitches=abjad.PitchSet(
                [0, 4]
                ),
            )

        >>> inequality(abjad.Staff("d'8 e' f' g'"))
        True

        >>> inequality(abjad.Staff("e'8 f' g' a'"))
        True

        >>> inequality(abjad.Staff("f'8 g' a' b'"))
        False

    .. note:: only intersection currently implemented.

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Inequalities'

    __slots__ = (
        '_operator_string',
        '_pitches',
        )

    _set_theoretic_operator_strings = (
        '&',
        '|',
        '^',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        operator_string: str = '&',
        pitches=None,
        ) -> None:
        assert operator_string in self._set_theoretic_operator_strings
        self._operator_string = operator_string
        # only intersection is currently implemented
        if not isinstance(pitches, collections.Iterable):
            pitches = [pitches]
        pitches = PitchSet(
            items=pitches,
            item_class=NumberedPitch,
            )
        self._pitches = pitches

    ### SPECIAL METHODS ###

    def __call__(self, argument) -> bool:
        """
        Calls inequality on ``argument``.
        """
        if not self.pitches:
            return False
        pitch_set = PitchSet.from_selection(
            argument,
            item_class=NumberedPitch,
            )
        if self.operator_string == '&':
            return bool(self.pitches.intersection(pitch_set))
        else:
            raise NotImplementedError('implement {self.operator_string!r}.')

    ### PUBLIC PROPERTIES ###

    @property
    def operator_string(self) -> str:
        """
        Gets operator string.
        """
        return self._operator_string

    @property
    def pitches(self) -> PitchSet:
        """
        Gets pitches.
        """
        return self._pitches
