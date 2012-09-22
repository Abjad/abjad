from abjad.tools import iterationtools
from abjad.tools import sequencetools
from abjad.tools.wellformednesstools.Check import Check


class DuplicateIdCheck(Check):

    def _run(self, expr):
        violators = []
        components = iterationtools.iterate_components_in_expr(expr)
        total_ids = [id(x) for x in components]
        unique_ids = sequencetools.truncate_runs_in_sequence(total_ids)
        if len(unique_ids) < len(total_ids):
            for cur_id in unique_ids:
                if 1 < total_ids.count(cur_id):
                    violators.extend([x for x in components if id(x) == cur_id])
        return violators, len(total_ids)
