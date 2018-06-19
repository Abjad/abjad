import collections
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
        operator_string='&',
        pitches=None,
        ):
        import abjad
        assert operator_string in self._set_theoretic_operator_strings
        self._operator_string = operator_string
        # only intersection is currently implemented
        if not isinstance(pitches, collections.Iterable):
            pitches = [pitches]
        pitches = abjad.PitchSet(
            items=pitches,
            item_class=abjad.NumberedPitch,
            )
        self._pitches = pitches

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        """
        Calls inequality on ``argument``.

        Returns true or false.
        """
        import abjad
        if not self.pitches:
            return False
        pitch_set = abjad.PitchSet.from_selection(
            argument,
            item_class=abjad.NumberedPitch,
            )
        if self.operator_string == '&':
            return bool(self.pitches.intersection(pitch_set))
        else:
            message = 'implement {!r}.'
            message = message.format(self.operator_string)
            raise NotImplementedError(message)

    ### PUBLIC PROPERTIES ###

    @property
    def operator_string(self):
        """
        Gets operator string.

        Returns string.
        """
        return self._operator_string

    @property
    def pitches(self):
        """
        Gets pitches.

        Returns numbered pitch set.
        """
        return self._pitches
