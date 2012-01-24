from abjad.tools.chordtools.Chord import Chord
from abjad.decorators import requires


@requires(lambda x: hasattr(x, '__contains__'))
def yield_groups_of_chords_in_sequence(sequence):
    r'''.. versionadded:: 2.0

    Yield groups of chords in `sequence`::

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

        abjad> for chord in chordtools.yield_groups_of_chords_in_sequence(staff):
        ...     chord
        ... 
        (Chord("<e' g'>8"), Chord("<f' a'>8"))
        (Chord("<b' d''>8"), Chord("<c'' e''>8"))

    Return generator.
    '''
    from abjad.tools import componenttools

    return componenttools.yield_topmost_components_of_klass_grouped_by_type(sequence, Chord)
