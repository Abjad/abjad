from abjad.tools import iterationtools
from abjad.tools import spannertools
from abjad.tools.wellformednesstools.Check import Check


class OverlappingGlissandoCheck(Check):
    '''Glissandi must not overlap.
    Dove-tailed glissandi are OK.
    '''

    def _run(self, expr):
        violators = []
        for leaf in iterationtools.iterate_leaves_in_expr(expr):
            glissandi = spannertools.get_spanners_attached_to_component(
                leaf, spannertools.GlissandoSpanner)
            if 1 < len(glissandi):
                if len(glissandi) == 2:
                    common_leaves = set(glissandi[0].leaves) & \
                        set(glissandi[1].leaves)
                    if len(common_leaves) == 1:
                        x = list(common_leaves)[0]
                        if (glissandi[0]._is_my_first_leaf(x) and
                            glissandi[1]._is_my_last_leaf(x)) or \
                            (glissandi[1]._is_my_first_leaf(x) and
                            glissandi[0]._is_my_last_leaf(x)):
                            break

                for glissando in glissandi:
                    if glissando not in violators:
                        violators.append(glissando)
        total = spannertools.get_spanners_attached_to_any_improper_child_of_component(
            expr, spannertools.GlissandoSpanner)
        return violators, len(total)
