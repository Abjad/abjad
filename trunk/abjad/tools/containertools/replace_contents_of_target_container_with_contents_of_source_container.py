def replace_contents_of_target_container_with_contents_of_source_container(target_container, source_container):
    r'''.. versionadded:: 2.0

    Replace contents of `target_container` with contents of `source_container`::

        >>> staff = Staff(Tuplet(Fraction(2, 3), "c'8 d'8 e'8") * 3)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        ...     staff)
        >>> beamtools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8, ... [5] ..., c''8, d''8)

    ::

        >>> f(staff)
        \new Staff {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                f'8
                g'8
                a'8
            }
            \times 2/3 {
                b'8
                c''8
                d''8 ]
            }
        }

    ::

        >>> container = Container("c'8 d'8 e'8")
        >>> spannertools.SlurSpanner(container.leaves)
        SlurSpanner(c'8, d'8, e'8)

    ::

        >>> f(container)
        {
            c'8 (
            d'8
            e'8 )
        }

    ::

        >>> containertools.replace_contents_of_target_container_with_contents_of_source_container(
        ...     staff[1], container)
        Tuplet(2/3, [c'8, d'8, e'8])

    ::

        >>> f(staff)
        \new Staff {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                c'8 (
                d'8
                e'8 )
            }
            \times 2/3 {
                b'8
                c''8
                d''8 ]
            }
        }

    Leave `source_container` empty::

        >>> container
        {}

    Return `target_container`.
    '''

    # to avoid pychecker slice assignment error
    #target_container[:] = source_container[:]
    target_container.__setitem__(
        slice(0, len(target_container)), 
        source_container.__getitem__(slice(0, len(source_container))))

    return target_container
