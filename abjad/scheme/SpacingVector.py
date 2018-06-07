from abjad.typings import Number
from .SchemeVector import SchemeVector
from .SchemePair import SchemePair


class SpacingVector(SchemeVector):
    r"""
    Abjad model of Scheme spacing vector.

    ..  container:: example

        >>> vector = abjad.SpacingVector(0, 0, 12, 0)

        >>> abjad.f(vector)
        abjad.SpacingVector(
            abjad.SchemePair(('basic-distance', 0)),
            abjad.SchemePair(('minimum-distance', 0)),
            abjad.SchemePair(('padding', 12)),
            abjad.SchemePair(('stretchability', 0))
            )

        Use to set paper block spacing attributes:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> lilypond_file = abjad.LilyPondFile.new(staff)
        >>> vector = abjad.SpacingVector(0, 0, 12, 0)
        >>> lilypond_file.paper_block.system_system_spacing = vector

        ..  docs::

            >>> abjad.f(lilypond_file.paper_block)
            \paper {
                system-system-spacing = #'((basic-distance . 0) (minimum-distance . 0) (padding . 12) (stretchability . 0))
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        basic_distance: Number = 0,
        minimum_distance: Number = 0,
        padding: Number = 12,
        stretchability: Number = 0,
        ) -> None:
        pairs = [
            SchemePair(('basic-distance', basic_distance)),
            SchemePair(('minimum-distance', minimum_distance)),
            SchemePair(('padding', padding)),
            SchemePair(('stretchability', stretchability)),
            ]
        return SchemeVector.__init__(self, pairs)
