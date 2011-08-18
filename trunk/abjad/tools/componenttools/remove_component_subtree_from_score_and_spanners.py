def remove_component_subtree_from_score_and_spanners(components):
    r'''.. versionadded:: 1.1

    Remove arbitrary `components` and children of `components` from score and spanners::

        abjad> score = Voice(notetools.make_repeated_notes(2))
        abjad> score.insert(1, Container(notetools.make_repeated_notes(2)))
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(score)
        abjad> spannertools.BeamSpanner(score.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8)
        abjad> spannertools.GlissandoSpanner(score.leaves)
        GlissandoSpanner(c'8, d'8, e'8, f'8)

    ::

        abjad> f(score)
        \new Voice {
            c'8 [ \glissando
            {
                d'8 \glissando
                e'8 \glissando
            }
            f'8 ]
        }

    Examples refer to the score above.

    Remove one leaf from score::

        abjad> componenttools.remove_component_subtree_from_score_and_spanners(score.leaves[1:2]) # doctest: +SKIP
        (Note(d', 8),)

    ::

        abjad> f(score) # doctest: +SKIP
        \new Voice {
            c'8 [ \glissando
            {
                e'8 \glissando
            }
            f'8 ]
        }

    Remove contiguous leaves from score::

        abjad> result = componenttools.remove_component_subtree_from_score_and_spanners(score.leaves[:2]) # doctest: +SKIP
        (Note(c', 8), Note(d', 8))

    ::

        abjad> f(score) # doctest: +SKIP
        \new Voice {
            {
                e'8 [ \glissando
            }
            f'8 ]
        }

    Remove noncontiguous leaves from score::

        abjad> componenttools.remove_component_subtree_from_score_and_spanners([score.leaves[0], score.leaves[2]]) # doctest: +SKIP
        [Note(c', 8), Note(e', 8)]

    ::

        abjad> f(score) # doctest: +SKIP
        \new Voice {
            {
                d'8 [ \glissando
            }
            f'8 ]
        }

    Remove container from score::

        abjad> result = componenttools.remove_component_subtree_from_score_and_spanners(score[1:2])
        abjad> result # doctest: +SKIP
        [{d'8, e'8}]

    ::

        abjad> f(score) # doctest: +SKIP
        \new Voice {
            c'8 [ \glissando
            f'8 ]
        }

    Withdraw `components` and children of `components` from spanners.

    Return either tuple or list of `components` and children of `components`.

    .. todo:: regularize return value of function.

    .. note:: rename to ``componenttools.remove_components_from_score_deep()``.

    .. versionchanged:: 2.0
        renamed ``componenttools.detach()`` to
        ``componenttools.remove_component_subtree_from_score_and_spanners()``.
    '''
    from abjad.tools.spannertools._withdraw_components_in_expr_from_attached_spanners import _withdraw_components_in_expr_from_attached_spanners
    from abjad.tools import componenttools

    assert componenttools.all_are_components(components)

    for component in components:
        component._parentage._cut()
        _withdraw_components_in_expr_from_attached_spanners([component])
    return components
