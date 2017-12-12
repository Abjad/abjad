def select(items=None):
    r'''Selects `items` or makes select expression.

    ..  container:: example

        Selects first two notes in staff:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> selection = abjad.select(staff[:2]).by_leaf(pitched=True)
            >>> for note in selection:
            ...     abjad.override(note).note_head.color = 'red'

        ::

            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \once \override NoteHead.color = #red
                c'4
                \once \override NoteHead.color = #red
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Returns selection agent:

        ::

            >>> abjad.select(staff)
            Selection([Staff("c'4 d'4 e'4 f'4")])

        ::

            >>> abjad.f(abjad.select())
            abjad.Expression(
                callbacks=[
                    abjad.Expression(
                        evaluation_template='abjad.Selection',
                        is_initializer=True,
                        ),
                    ],
                proxy_class=abjad.Selection,
                )

    '''
    import abjad
    if items is None:
        return abjad.Expression().select()
    return abjad.Selection(items=items)
