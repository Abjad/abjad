from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle


class Repeat(AbjadValueObject):
    r"""
    Repeat.

    ..  container:: example

        Volta repeat:

        >>> container = abjad.Container("c'4 d'4 e'4 f'4")
        >>> repeat = abjad.Repeat()
        >>> abjad.attach(repeat, container)
        >>> staff = abjad.Staff([container])
        >>> score = abjad.Score([staff])
        >>> abjad.show(score)  # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    \repeat volta 2
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                }
            >>

    ..  container:: example

        Unfold repeat:

        >>> container = abjad.Container("c'4 d'4 e'4 f'4")
        >>> repeat = abjad.Repeat(repeat_type='unfold')
        >>> abjad.attach(repeat, container)
        >>> staff = abjad.Staff([container])
        >>> score = abjad.Score([staff])
        >>> abjad.show(score)  # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    \repeat unfold 2
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                }
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_repeat_count',
        '_repeat_type',
        )

    _can_attach_to_containers = True

    _context = 'Score'

    _format_leaf_children = False

    _format_slot = 'before'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        repeat_count: int = 2,
        repeat_type: str = 'volta',
        ) -> None:
        repeat_count = int(repeat_count)
        assert 1 < repeat_count
        self._repeat_count = repeat_count
        assert repeat_type in ('volta', 'unfold')
        self._repeat_type = repeat_type

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        r"""
        Gets string representation of repeat.

        ..  container:: example

            Volta repeat:

            >>> str(abjad.Repeat())
            '\\repeat volta 2'

        ..  container:: example

            Unfold repeat:

            >>> str(abjad.Repeat(repeat_type='unfold'))
            '\\repeat unfold 2'

        """
        return rf'\repeat {self.repeat_type} {self.repeat_count}'

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        bundle.before.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        """
        Gets (historically conventional) context.

        ..  container:: example

            Volta repeat:

            >>> repeat = abjad.Repeat()
            >>> repeat.context
            'Score'

        ..  container:: example

            Unfold repeat:

            >>> repeat = abjad.Repeat(repeat_type='unfold')
            >>> repeat.context
            'Score'

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def repeat_count(self) -> int:
        """
        Gets repeat count of repeat.

        ..  container:: example

            Volta repeat:

            >>> repeat = abjad.Repeat()
            >>> repeat.repeat_count
            2

        ..  container:: example

            Unfold repeat:

            >>> repeat = abjad.Repeat(repeat_type='unfold')
            >>> repeat.repeat_count
            2

        """
        return self._repeat_count

    @property
    def repeat_type(self) -> str:
        """
        Gets repeat type of repeat.

        ..  container:: example

            Volta repeat:

            >>> repeat = abjad.Repeat()
            >>> repeat.repeat_type
            'volta'

        ..  container:: example

            Unfold repeat:

            >>> repeat = abjad.Repeat(repeat_type='unfold')
            >>> repeat.repeat_type
            'unfold'

        """
        return self._repeat_type

    @property
    def tweaks(self) -> None:
        r"""
        Are not implemented on repeat.
        
        The LilyPond ``\repeat`` command refuses tweaks.

        Override the LilyPond ``BarLine`` grob instead.
        """
        pass
