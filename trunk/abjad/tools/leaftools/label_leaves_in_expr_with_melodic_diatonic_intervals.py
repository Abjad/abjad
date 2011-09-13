from abjad.tools.leaftools._Leaf import _Leaf
from abjad.tools import componenttools


def label_leaves_in_expr_with_melodic_diatonic_intervals(expr, markup_direction = 'up'):
    r""".. versionadded:: 2.0

    Label leaves in `expr` with melodic diatonic intervals::

        abjad> staff = Staff(notetools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Duration(1, 8)]))
        abjad> leaftools.label_leaves_in_expr_with_melodic_diatonic_intervals(staff)
        abjad> f(staff)
        \new Staff {
            c'8 ^ \markup { +aug15 }
            cs'''8 ^ \markup { -M9 }
            b'8 ^ \markup { -aug9 }
            af8 ^ \markup { -m7 }
            bf,8 ^ \markup { +aug1 }
            b,8 ^ \markup { +m14 }
            a'8 ^ \markup { +m2 }
            bf'8 ^ \markup { -dim4 }
            fs'8 ^ \markup { -aug1 }
            f'8
        }

    Return none.
    """
    from abjad.tools import markuptools
    from abjad.tools import threadtools
    from abjad.tools.notetools.Note import Note
    from abjad.tools import pitchtools

    for note in componenttools.iterate_components_forward_in_expr(expr, Note):
        thread_iterator = threadtools.iterate_thread_forward_from_component(note, _Leaf)
        try:
            thread_iterator.next()
            next_leaf = thread_iterator.next()
            if isinstance(next_leaf, Note):
                mdi = pitchtools.calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
                    note, next_leaf)
                markuptools.Markup(mdi, markup_direction)(note)
        except StopIteration:
            pass
