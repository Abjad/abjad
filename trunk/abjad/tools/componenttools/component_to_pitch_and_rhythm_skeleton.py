from abjad.tools.componenttools._Component import _Component


def component_to_pitch_and_rhythm_skeleton(component):
    r'''.. versionadded:: 2.0

    Change `component` to pitch and rhythm skeleton::

        abjad> tuplet = Tuplet(Fraction(3, 4), "c'8 d'8 e'8 f'8")
        abjad> measure = Measure((6, 16), [tuplet])
        abjad> staff = Staff([measure])
        abjad> score = Score(staff * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(score)

    ::

        abjad> skeleton = componenttools.component_to_pitch_and_rhythm_skeleton(score)
        abjad> print skeleton
        Score([
            Staff([
                Measure((6, 16), [
                    Tuplet(Fraction(3, 4), [
                        Note(('c', 4), Duration(1, 8)),
                        Note(('d', 4), Duration(1, 8)),
                        Note(('e', 4), Duration(1, 8)),
                        Note(('f', 4), Duration(1, 8))
                    ])
                ])
            ]),
            Staff([
                Measure((6, 16), [
                    Tuplet(Fraction(3, 4), [
                        Note(('g', 4), Duration(1, 8)),
                        Note(('a', 4), Duration(1, 8)),
                        Note(('b', 4), Duration(1, 8)),
                        Note(('c', 5), Duration(1, 8))
                    ])
                ])
            ])
        ])

    ::

        abjad> new = eval(skeleton)
        abjad> new
        Score<<2>>

    ::

        abjad> f(new)
        \new Score <<
            \new Staff {
                {
                    \time 6/16
                    \fraction \times 3/4 {
                        c'8
                        d'8
                        e'8
                        f'8
                    }
                }
            }
            \new Staff {
                {
                    \time 6/16
                    \fraction \times 3/4 {
                        g'8
                        a'8
                        b'8
                        c''8
                    }
                }
            }
        >>

    Return string.
    '''
    from abjad.tools.leaftools._Leaf import _Leaf
    from abjad.tools.containertools._container_to_pitch_and_rhythm_skeleton import _container_to_pitch_and_rhythm_skeleton
    from abjad.tools.leaftools._leaf_to_pitch_and_rhythm_skeleton import _leaf_to_pitch_and_rhythm_skeleton

    if not isinstance(component, _Component):
        raise TypeError('must be Abjad component.')

    if isinstance(component, _Leaf):
        return _leaf_to_pitch_and_rhythm_skeleton(component)
    else:
        return _container_to_pitch_and_rhythm_skeleton(component)
