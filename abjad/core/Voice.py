import typing
from .Context import Context


class Voice(Context):
    r"""
    Voice.

    ..  container:: example

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8")
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'8
                d'8
                e'8
                f'8
            }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Contexts'

    __slots__ = ()

    _default_lilypond_type = 'Voice'

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        lilypond_type: str = 'Voice',
        is_simultaneous: bool = None,
        name: str = None,
        tag: str = None,
        ) -> None:
        Context.__init__(
            self,
            components=components,
            lilypond_type=lilypond_type,
            is_simultaneous=is_simultaneous,
            name=name,
            tag=tag,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def tag(self) -> typing.Optional[str]:
        r"""
        Gets tag.

        ..  container:: example

            >>> voice = abjad.Voice("c'4 d' e' f'", tag='RED')
            >>> abjad.show(voice) # doctest: +SKIP

            >>> abjad.f(voice, strict=20)
            \new Voice          %! RED
            {                   %! RED
                c'4
                d'4
                e'4
                f'4
            }                   %! RED

        """
        return super().tag
