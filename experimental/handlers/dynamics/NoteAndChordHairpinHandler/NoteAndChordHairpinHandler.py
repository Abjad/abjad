from abjad.tools import componenttools
from abjad.tools import leaftools
from abjad.tools import marktools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from handlers.dynamics.DynamicHandler import DynamicHandler


class NoteAndChordHairpinHandler(DynamicHandler):

    def __init__(self, hairpin_token=None, minimum_prolated_duration=None):
        DynamicHandler.__init__(self, minimum_prolated_duration=minimum_prolated_duration)
        self.hairpin_token = hairpin_token

    ### SPECIAL METHODS ###

    def __call__(self, hairpin_token=None):
        new = type(self)(hairpin_token=hairpin_token)
        return new

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def hairpin_token():
        def fget(self):
            return self._hairpin_token
        def fset(self, hairpin_token):
            if hairpin_token is None:
                self._hairpin_token = hairpin_token
            elif spannertools.HairpinSpanner.is_hairpin_token(hairpin_token):
                self._hairpin_token = hairpin_token
            else:
                raise TypeError(hairpin_token)
        return property(**locals())

    ### PUBLIC METHODS ###

    def apply(self, expr, offset=0):
        leaves = list(leaftools.iterate_leaves_forward_in_expr(expr))
        leaves = leaftools.remove_outer_rests_from_sequence(leaves)
        group = leaves
        is_short_group = False
        if len(group) == 1:
            is_short_group = True
        elif self.minimum_prolated_duration is not None:
            prolated_duration = componenttools.sum_prolated_duration_of_components(group)
            if prolated_duration < self.minimum_prolated_duration:
                is_short_group = True
        if is_short_group:
            start_dynamic = self.hairpin_token[0]
            marktools.LilyPondCommandMark(start_dynamic, 'right')(group[0])
        else:
            descriptor = ' '.join([x for x in self.hairpin_token if x])
            spannertools.HairpinSpanner(group, descriptor, include_rests = False)
        return expr
