from .Context import Context


class Voice(Context):
    r'''Voice.

    ..  container:: example

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8")
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice {
                c'8
                d'8
                e'8
                f'8
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Contexts'

    __slots__ = ()

    _default_context_name = 'Voice'

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        context_name='Voice',
        is_simultaneous=None,
        name=None,
        ):
        Context.__init__(
            self,
            components=components,
            context_name=context_name,
            is_simultaneous=is_simultaneous,
            name=name,
            )
