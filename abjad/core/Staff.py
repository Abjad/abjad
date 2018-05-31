from .Context import Context


class Staff(Context):
    r"""
    Staff.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
            }

    ..  container:: example

        Can initialize from collection of strings:

        >>> staff = abjad.Staff([
        ...     r"\times 9/10 { r8 c'16 c'16 bf'4~ bf'16 r16 }",
        ...     r"\times 9/10 { bf'16 e''16 e''4 ~ e''16 r16 fs''16 af''16 }",
        ...     r"\times 4/5 { a'16 r4 }",
        ...     ])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        r8
                        c'16
                        c'16
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        bf'16
                        e''16
                        e''4
                        ~
                        e''16
                        r16
                        fs''16
                        af''16
                    }
                }
                {
                    \times 4/5 {
                        a'16
                        r4
                    }
                }
            }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Contexts'

    __slots__ = ()

    _default_lilypond_type = 'Staff'

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        lilypond_type='Staff',
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
