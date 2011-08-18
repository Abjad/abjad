from abjad.tools.componenttools.yield_topmost_components_grouped_by_type import yield_topmost_components_grouped_by_type


def yield_groups_of_mixed_klasses_in_sequence(sequence, klasses):
    r'''.. versionadded:: 2.0

    Yield groups of mixed `klasses` in `sequence`::

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

        abjad> for group in componenttools.yield_groups_of_mixed_klasses_in_sequence(staff, (Note, Chord)):
        ...   group
        (Note("c'8"), Note("d'8"))
        (Chord("<e' g'>8"), Chord("<f' a'>8"), Note("g'8"), Note("a'8"))
        (Chord("<b' d''>8"), Chord("<c'' e''>8"))

    Return generator.
    '''

    cur_group = ()
    for group in yield_topmost_components_grouped_by_type(sequence):
        if type(group[0]) in klasses:
            cur_group = cur_group + group
        elif cur_group:
            yield cur_group
            cur_group = ()

    if cur_group:
        yield cur_group
