from abjad.tools import contexttools
from abjad.tools import leaftools
from abjad.tools import marktools
from handlers.dynamics.DynamicHandler import DynamicHandler


class ReiteratedDynamicHandler(DynamicHandler):

    ### INITIALIZER ###

    def __init__(self, dynamic_name=None, minimum_prolated_duration=None):
        DynamicHandler.__init__(self, minimum_prolated_duration=minimum_prolated_duration)
        self.dynamic_name = dynamic_name

    ### SPECIAL METHODS ###

    def __call__(self, dynamic_name):
        new = type(self)()
        new.dynamic_name = dynamic_name
        new.minimum_prolated_duration = self.minimum_prolated_duration
        return new

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def dynamic_name():
        def fget(self):
            return self._dynamic_name
        def fset(self, dynamic_name):
            if dynamic_name is None:
                self._dynamic_name = dynamic_name
            elif contexttools.DynamicMark.is_dynamic_name(dynamic_name):
                self._dynamic_name = dynamic_name
            else:
                raise TypeError(dynamic_name)
        return property(**locals())

    ### PUBLIC METHODS ###

    def apply(self, expr):
        for note_or_chord in leaftools.iterate_notes_and_chords_forward_in_expr(expr):
            marktools.LilyPondCommandMark(self.dynamic_name, 'right')(note_or_chord)
        return expr
