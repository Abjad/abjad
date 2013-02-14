from abjad.tools import iterationtools
from abjad.tools import marktools
from abjad.tools import sequencetools
from abjad.tools.notetools.Note import Note
from experimental.tools.handlertools.articulations.ArticulationHandler import ArticulationHandler


class ReiteratedArticulationHandler(ArticulationHandler):

    def __init__(self, 
        articulation_list=None,
        minimum_duration=None, 
        maximum_duration=None,
        minimum_written_pitch=None, 
        maximum_written_pitch=None):
        ArticulationHandler.__init__(self,
            minimum_duration=minimum_duration,
            maximum_duration=maximum_duration,
            minimum_written_pitch=minimum_written_pitch,
            maximum_written_pitch=maximum_written_pitch)
        if articulation_list is None:
            articulation_list = []
        if isinstance(articulation_list, str):
            articulation_list = [articulation_list]
        self.articulation_list = articulation_list

    ### SPECIAL METHODS ###

    def __call__(self, articulation_list):
        new = type(self)()
        new.articulation_list = articulation_list
        return new

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def articulation_list():
        def fget(self):
            return self._articulation_list
        def fset(self, articulation_list):
            if isinstance(articulation_list, list):
                if all([isinstance(x, str) for x in articulation_list]):
                    self._articulation_list = articulation_list
            elif isinstance(articulation_list, str):
                self._articulation_list = [articulation_list]
            else:
                raise TypeError(articulation_list)
        return property(**locals())

    ### PUBLIC METHODS ###

    def apply(self, expr, offset = 0, skip_first = 0, skip_last = 0):
        articulation_list = sequencetools.CyclicList(self.articulation_list)
        notes_and_chords = list(iterationtools.iterate_notes_and_chords_in_expr(expr))
        notes_and_chords = notes_and_chords[skip_first:]
        if skip_last:
            notes_and_chords = notes_and_chords[:-skip_last]
        for i, note_or_chord in enumerate(notes_and_chords):
            if self.minimum_duration is not None:
                if note_or_chord.duration.prolated < self.minimum_duration:
                    continue
            if self.maximum_duration is not None:
                if self.maximum_duration < note_or_chord.duration.prolated:
                    continue
            if self.minimum_written_pitch is not None:
                if isinstance(note_or_chord, Note):
                    minimum_written_pitch = note_or_chord.pitch
                else:
                    minimum_written_pitch = note_or_chord.pitches[0]
                if minimum_written_pitch < self.minimum_written_pitch:
                    continue
            if self.maximum_written_pitch is not None:
                if isinstance(note_or_chord, Note):
                    maximum_written_pitch = note_or_chord.pitch
                else:
                    maximum_written_pitch = note_or_chord.pitches[-1]
                if self.maximum_written_pitch < maximum_written_pitch:
                    continue
            marktools.attach_articulations_to_notes_and_chords_in_expr(
                note_or_chord, self.articulation_list)
        return expr
