from abjad.tools import markuptools
from abjad.tools.verticalitytools.iterate_vertical_moments_forward_in_expr import iterate_vertical_moments_forward_in_expr


def label_vertical_moments_in_expr_with_numbered_chromatic_pitch_classes(expr, markup_direction = 'down'):
    r'''.. versionadded:: 2.0

    Label pitch-classes of every vertical moment in `expr`::

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
        abjad> verticalitytools.label_vertical_moments_in_expr_with_numbered_chromatic_pitch_classes(score)
        abjad> f(score)
        \new Score <<
            \new Staff {
                c'8
                d'8 _ \markup { \small { \column { 7 2 0 } } }
                e'8
                f'8 _ \markup { \small { \column { 5 0 } } }
            }
            \new Staff {
                \clef "alto"
                g4
                f4 _ \markup { \small { \column { 5 4 0 } } }
            }
            \new Staff {
                \clef "bass"
                c,2 _ \markup { \small { \column { 7 0 } } }
            }
        >>

    .. versionchanged:: 2.0
        renamed ``label.vertical_moment_pitch_classes()`` to
        ``verticalitytools.label_vertical_moments_in_expr_with_numbered_chromatic_pitch_classes()``.
    '''
    from abjad.tools import pitchtools

    for vertical_moment in iterate_vertical_moments_forward_in_expr(expr):
        leaves = vertical_moment.leaves
        pitches = pitchtools.list_named_chromatic_pitches_in_expr(leaves)
        if not pitches:
            continue
        pitch_classes = [abs(pitch.numbered_chromatic_pitch_class) for pitch in pitches]
        pitch_classes = list(set(pitch_classes))
        pitch_classes.sort()
        pitch_classes.reverse()
        pitch_classes = ' '.join([str(x) for x in pitch_classes])
        pitch_classes = r'\small { \column { %s } }' % pitch_classes
        markuptools.Markup(pitch_classes, markup_direction)(vertical_moment.start_leaves[-1])
