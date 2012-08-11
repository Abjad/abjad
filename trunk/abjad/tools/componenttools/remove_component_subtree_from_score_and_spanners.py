def remove_component_subtree_from_score_and_spanners(components):
    r'''.. versionadded:: 1.1

    Example 1. Remove one leaf from score::

        >>> voice = Voice("c'8 [ { d'8 e'8 } f'8 ]")
        >>> spannertools.GlissandoSpanner(voice.leaves)
        GlissandoSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(voice)
        \new Voice {
            c'8 [ \glissando
            {
                d'8 \glissando
                e'8 \glissando
            }
            f'8 ]
        }

    ::

        >>> componenttools.remove_component_subtree_from_score_and_spanners(voice.leaves[1:2])
        (Note("d'8"),)

    ::

        >>> f(voice)
        \new Voice {
            c'8 [ \glissando
            {
                e'8 \glissando
            }
            f'8 ]
        }

    Example 2. Remove contiguous leaves from score::

        >>> voice = Voice("c'8 [ { d'8 e'8 } f'8 ]")
        >>> spannertools.GlissandoSpanner(voice.leaves)
        GlissandoSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(voice)
        \new Voice {
            c'8 [ \glissando
            {
                d'8 \glissando
                e'8 \glissando
            }
            f'8 ]
        }

    ::

        >>> componenttools.remove_component_subtree_from_score_and_spanners(voice.leaves[:2])
        (Note("c'8"), Note("d'8"))

    ::

        >>> f(voice)
        \new Voice {
            {
                e'8 [ \glissando
            }
            f'8 ]
        }

    Example 3. Remove noncontiguous leaves from score::

        >>> voice = Voice("c'8 [ { d'8 e'8 } f'8 ]")
        >>> spannertools.GlissandoSpanner(voice.leaves)
        GlissandoSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(voice)
        \new Voice {
            c'8 [ \glissando
            {
                d'8 \glissando
                e'8 \glissando
            }
            f'8 ]
        }

    ::

        >>> componenttools.remove_component_subtree_from_score_and_spanners(
        ... [voice.leaves[0], voice.leaves[2]])
        [Note("c'8"), Note("e'8")]

    ::

        >>> f(voice)
        \new Voice {
            { d'8 [ \glissando
            }
            f'8 ]
        }

    Example 4. Remove container from score::

        >>> voice = Voice("c'8 [ { d'8 e'8 } f'8 ]")
        >>> spannertools.GlissandoSpanner(voice.leaves)
        GlissandoSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(voice)
        \new Voice {
            c'8 [ \glissando
            {
                d'8 \glissando
                e'8 \glissando
            }
            f'8 ]
        }

    ::

        >>> componenttools.remove_component_subtree_from_score_and_spanners(voice[1:2])
        [{d'8, e'8}]

    ::

        >>> f(voice)
        \new Voice {
            c'8 [ \glissando
            f'8 ]
        }

    Withdraw `components` and children of `components` from spanners.

    Return either tuple or list of `components` and children of `components`.

    .. todo:: regularize return value of function.

    .. versionchanged:: 2.0
        renamed ``componenttools.detach()`` to
        ``componenttools.remove_component_subtree_from_score_and_spanners()``.
    '''
    from abjad.tools import componenttools
    from abjad.tools.spannertools._withdraw_components_in_expr_from_attached_spanners import \
        _withdraw_components_in_expr_from_attached_spanners

    assert componenttools.all_are_components(components)

    for component in components:
        component._cut()
        _withdraw_components_in_expr_from_attached_spanners([component])
    return components
