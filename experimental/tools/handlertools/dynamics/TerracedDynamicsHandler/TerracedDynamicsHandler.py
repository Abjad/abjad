from abjad.tools import contexttools
from abjad.tools import iterationtools
from abjad.tools import marktools
from abjad.tools import sequencetools
from experimental.tools.handlertools.dynamics.DynamicHandler import DynamicHandler


class TerracedDynamicsHandler(DynamicHandler):
    '''Terraced dynamics.
    '''

    def __init__(self, dynamics=None, minimum_prolated_duration=None):
        DynamicHandler.__init__(self, minimum_prolated_duration=minimum_prolated_duration)
        if dynamics is None:
            dynamics = []
        self.dynamics = dynamics

    ### SPECIAL METHODS ###

    def __call__(self, dynamics):
        new = type(self)()
        new.dynamics = dynamics
        new.minimum_prolated_duration = self.minimum_prolated_duration
        return new

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def dynamics():
        def fget(self):
            return self._dynamics
        def fset(self, dynamics):
            if dynamics is None:
                self._dynamics = dynamics
            elif all([contexttools.DynamicMark.is_dynamic_name(x) for x in dynamics]):
                self._dynamics = dynamics
            else:
                raise TypeError(dynamics)
        return property(**locals())

    ### PUBLIC METHODS ###

    def apply(self, expr, offset=0):
        dynamics = sequencetools.CyclicList(self.dynamics)
        for i, note_or_chord in enumerate(iterationtools.iterate_notes_and_chords_in_expr(expr)):
            dynamic_name = dynamics[offset+i]
            if self.minimum_prolated_duration <= note_or_chord.prolated_duration:
                marktools.LilyPondCommandMark(dynamic_name, 'right')(note_or_chord)
        return expr
