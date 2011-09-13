from abjad.tools.leaftools._Leaf import _Leaf
from abjad.tools import componenttools


def label_leaves_in_expr_with_melodic_chromatic_interval_classes(expr, markup_direction = 'up'):
    r""".. versionadded:: 2.0

    Label leaves in `expr` with melodic chromatic interval classes::

        abjad> staff = Staff(notetools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Duration(1, 8)]))
        abjad> leaftools.label_leaves_in_expr_with_melodic_chromatic_interval_classes(staff)
        abjad> f(staff)
        \new Staff {
            c'8 ^ \markup { +1 }
            cs'''8 ^ \markup { -2 }
            b'8 ^ \markup { -2 }
            af8 ^ \markup { -10 }
            bf,8 ^ \markup { +1 }
            b,8 ^ \markup { +10 }
            a'8 ^ \markup { +1 }
            bf'8 ^ \markup { -4 }
            fs'8 ^ \markup { -1 }
            f'8
        }

    Return none.
    """
    from abjad.tools import markuptools
    from abjad.tools import threadtools
    from abjad.tools.notetools.Note import Note

    for note in componenttools.iterate_components_forward_in_expr(expr, Note):
        thread_iterator = threadtools.iterate_thread_forward_from_component(note, _Leaf)
        try:
            thread_iterator.next()
            next_leaf = thread_iterator.next()
            if isinstance(next_leaf, Note):
                mdi = note.written_pitch - next_leaf.written_pitch
                mci = mdi.melodic_chromatic_interval
                mcic = mci.melodic_chromatic_interval_class
                markuptools.Markup(mcic, markup_direction)(note)
        except StopIteration:
            pass
