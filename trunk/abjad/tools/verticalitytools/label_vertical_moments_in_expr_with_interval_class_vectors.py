from abjad.tools import markuptools
from abjad.tools.verticalitytools.iterate_vertical_moments_forward_in_expr import iterate_vertical_moments_forward_in_expr


def label_vertical_moments_in_expr_with_interval_class_vectors(expr, markup_direction = 'down'):
    r'''.. versionadded:: 2.0

    Label interval-class vector of every vertical moment in `expr`::

        abjad> from abjad.tools import verticalitytools

    ::

        abjad> score = Score(Staff([]) * 3)
        abjad> notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
        abjad> score[0].extend(notes)
        abjad> contexttools.ClefMark('alto')(score[1])
        ClefMark('alto')(Staff{})
        abjad> score[1].extend([Note(-5, (1, 4)), Note(-7, (1, 4))])
        abjad> contexttools.ClefMark('bass')(score[2])
        ClefMark('bass')(Staff{})
        abjad> score[2].append(Note(-24, (1, 2)))
        abjad> verticalitytools.label_vertical_moments_in_expr_with_interval_class_vectors(score)
        abjad> f(score)
        \new Score <<
            \new Staff {
                c'8
                d'8 _ \markup { \tiny { 0010020 } }
                e'8
                f'8 _ \markup { \tiny { 1000020 } }
            }
            \new Staff {
                \clef "alto"
                g4
                f4 _ \markup { \tiny { 0100110 } }
            }
            \new Staff {
                \clef "bass"
                c,2 _ \markup { \tiny { 1000020 } }
            }
        >>

    .. versionchanged:: 2.0
        renamed ``label.vertical_moment_interval_class_vectors()`` to
        ``verticalitytools.label_vertical_moments_in_expr_with_interval_class_vectors()``.
    '''
    from abjad.tools import pitchtools

    for vertical_moment in iterate_vertical_moments_forward_in_expr(expr):
        leaves = vertical_moment.leaves
        pitches = pitchtools.list_named_chromatic_pitches_in_expr(leaves)
        if not pitches:
            continue
        interval_class_vector = pitchtools.named_chromatic_pitches_to_inversion_equivalent_chromatic_interval_class_number_dictionary(pitches)
        formatted = _format_interval_class_vector(interval_class_vector)
        markuptools.Markup(formatted, markup_direction)(vertical_moment.start_leaves[-1])


def _format_interval_class_vector(interval_class_vector):
    counts = []
    for i in range(7):
        counts.append(interval_class_vector[i])
    counts = ''.join([str(x) for x in counts])
    if len(interval_class_vector) == 13:
        quartertones = []
        for i in range(6):
            quartertones.append(interval_class_vector[i+0.5])
        quartertones = ''.join([str(x) for x in quartertones])
        return r'\tiny { \column { "%s" "%s" } }' % (counts, quartertones)
    else:
        return r'\tiny { %s }' % counts
