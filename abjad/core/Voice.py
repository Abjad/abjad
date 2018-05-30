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
        lilypond_type='Voice',
        is_simultaneous=None,
        name=None,
        ):
        Context.__init__(
            self,
            components=components,
            lilypond_type=lilypond_type,
            is_simultaneous=is_simultaneous,
            name=name,
            )
