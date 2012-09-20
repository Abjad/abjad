from abjad.tools import iterationtools
from abjad.tools import markuptools
from abjad.tools import spannertools
from abjad.tools import tietools


def _label_leaves_in_expr_with_leaf_durations(expr, markup_direction=Down,
    show=['written', 'prolated'], ties='together'):
    r'''Label leaves in expr with written leaf duration, prolated leaf duration
    or both written and prolated leaf durations.

    .. versionchanged:: 2.0
        renamed ``label.leaf_durations()`` to
        ``leaftools.label_leaves_in_expr_with_leaf_duration()``.
    '''

    for leaf in iterationtools.iterate_leaves_in_expr(expr):
        if ties == 'together':
            tie_spanners = spannertools.get_spanners_attached_to_component(
                leaf, tietools.TieSpanner)
            if not tie_spanners:
                if leaf.duration_multiplier is not None:
                    multiplier = '* %s' % str(leaf.duration_multiplier)
                else:
                    multiplier = ''
                if 'written' in show:
                    #label = r'\small %s%s' % (leaf.written_duration, multiplier)
                    label = markuptools.MarkupCommand('small', '{}{}'.format(str(leaf.written_duration), multiplier))
                    markuptools.Markup(label, markup_direction)(leaf)
                if 'prolated' in show:
                    label = markuptools.MarkupCommand('small', str(leaf.prolated_duration))
                    markuptools.Markup(label, markup_direction)(leaf)
            elif tuple(tie_spanners)[0]._is_my_first_leaf(leaf):
                tie = tie_spanners.pop()
                if 'written' in show:
                    written = sum([x.written_duration for x in tie])
                    #label = r'\small %s' % written
                    label = markuptools.MarkupCommand('small', str(written))
                    markuptools.Markup(label, markup_direction)(leaf)
                if 'prolated' in show:
                    prolated = sum([x.prolated_duration for x in tie])
                    #label = r'\small %s' % prolated
                    label = markuptools.MarkupCommand('small', str(prolated))
                    markuptools.Markup(label, markup_direction)(leaf)
        else:
            raise ValueError('unknown value for tie treatment.')
