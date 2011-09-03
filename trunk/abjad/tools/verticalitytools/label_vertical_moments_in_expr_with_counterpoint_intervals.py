from abjad.tools.notetools.Note import Note
from abjad.tools import markuptools
from abjad.tools.verticalitytools.iterate_vertical_moments_forward_in_expr import iterate_vertical_moments_forward_in_expr


def label_vertical_moments_in_expr_with_counterpoint_intervals(expr, markup_direction = 'down'):
    r'''.. versionadded:: 2.0

    Label counterpoint interval of every vertical moment in `expr`::

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
        abjad> verticalitytools.label_vertical_moments_in_expr_with_counterpoint_intervals(score)
        abjad> f(score)
        \new Score <<
            \new Staff {
                c'8
                d'8 _ \markup { \small { \column { 2 5 } } }
                e'8
                f'8 _ \markup { \small { \column { 4 4 } } }
            }
            \new Staff {
                \clef "alto"
                g4
                f4 _ \markup { \small { \column { 3 4 } } }
            }
            \new Staff {
                \clef "bass"
                c,2 _ \markup { \small { \column { 8 5 } } }
            }
        >>

    .. versionchanged:: 2.0
        renamed ``label.vertical_moment_counterpoint_intervals()`` to
        ``verticalitytools.label_vertical_moments_in_expr_with_counterpoint_intervals()``.
    '''
    from abjad.tools import pitchtools

    for vertical_moment in iterate_vertical_moments_forward_in_expr(expr):
        leaves = vertical_moment.leaves
        notes = [leaf for leaf in leaves if isinstance(leaf, Note)]
        if not notes:
            continue
        notes.sort(lambda x, y: cmp(x.written_pitch.numbered_chromatic_pitch,
            y.written_pitch.numbered_chromatic_pitch))
        notes.reverse()
        bass_note = notes[-1]
        upper_notes = notes[:-1]
        melodic_diatonic_intervals = []
        for upper_note in upper_notes:
            diatonic_interval = pitchtools.calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
                bass_note.written_pitch, upper_note.written_pitch)
            melodic_diatonic_intervals.append(diatonic_interval)
        intervals = melodic_diatonic_intervals
        hcpics = []
        for mdi in melodic_diatonic_intervals:
            hcpic = pitchtools.HarmonicCounterpointIntervalClass(mdi)
            hcpics.append(hcpic)
        intervals = ' '.join([str(x) for x in hcpics])
        intervals = r'\small { \column { %s } }' % intervals
        markuptools.Markup(intervals, markup_direction)(vertical_moment.start_leaves[-1])
