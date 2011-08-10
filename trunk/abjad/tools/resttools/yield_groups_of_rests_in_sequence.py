from abjad.tools.resttools.Rest import Rest


def yield_groups_of_rests_in_sequence(sequence):
    r'''.. versionadded:: 2.0

    Yield groups of rests in `sequence`::

        abjad> staff = Staff("c'8 d'8 r8 r8 <e' g'>8 <f' a'>8 g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")

    ::

        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            r8
            r8
            <e' g'>8
            <f' a'>8
            g'8
            a'8
            r8
            r8
            <b' d''>8
            <c'' e''>8
        }

    ::

        abjad> for rest in resttools.yield_groups_of_rests_in_sequence(staff):
        ...     rest
        ...
        (Rest('r8'), Rest('r8'))
        (Rest('r8'), Rest('r8'))

    Return generator.
    '''
    from abjad.tools import componenttools

    return componenttools.yield_topmost_components_of_klass_grouped_by_type(sequence, Rest)
