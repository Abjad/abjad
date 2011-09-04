from abjad.checks._Check import _Check
from abjad.tools.componenttools._Component import _Component
from abjad.tools import sequencetools


class DuplicateIDCheck(_Check):

    def _run(self, expr):
        from abjad.tools import componenttools
        violators = [ ]
        components = componenttools.iterate_components_forward_in_expr(expr, _Component)
        total_ids = [id(x) for x in components]
        unique_ids = sequencetools.truncate_runs_in_sequence(total_ids)
        if len(unique_ids) < len(total_ids):
            for cur_id in unique_ids:
                if 1 < total_ids.count(cur_id):
                    violators.extend([x for x in components if id(x) == cur_id])
        return violators, len(total_ids)
