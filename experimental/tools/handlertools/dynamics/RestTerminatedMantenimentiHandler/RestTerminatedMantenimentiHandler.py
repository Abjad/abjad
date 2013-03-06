from abjad.tools import leaftools
from abjad.tools import marktools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from experimental.tools.handlertools.dynamics.DynamicHandler import DynamicHandler


class RestTerminatedMantenimentiHandler(DynamicHandler):
    '''Rest-terminated mantenimenti handler.
    '''

    ### INITIALIZER ###

    def __init__(self, dynamics_talea=None, minimum_duration=None):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        dynamics_talea = dynamics_talea or []
        self.dynamics_talea = dynamics_talea

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        assert self.dynamics_talea, repr(self.dynamics_talea)
        groups = []
        for i, group in enumerate(leaftools.yield_groups_of_mixed_notes_and_chords_in_sequence(expr)):
            mantenimento = spannertools.CrescendoSpanner(group)
            mantenimento.override.hairpin.height = 0
            dynamic = self.dynamics_talea[i]
            marktools.LilyPondCommandMark(dynamic, 'right')(mantenimento.leaves[0])
            marktools.LilyPondCommandMark('nib', 'right')(mantenimento.leaves[-1])
            groups.append(group)
        return groups

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def dynamics_talea():
        def fget(self):
            return self._dynamics_talea
        def fset(self, dynamics_talea):
            assert isinstance(dynamics_talea, (list, tuple)), repr(dynamics_talea)
            self._dynamics_talea = sequencetools.CyclicTuple(dynamics_talea)
        return property(**locals())
