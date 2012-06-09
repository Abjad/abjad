from abjad.tools import leaftools
from abjad.tools import marktools
from abjad.tools import sequencetools
from abjad.tools.notetools.Note import Note
from handlers.articulations.ArticulationHandler import ArticulationHandler


class PatternedArticulationsHandler(ArticulationHandler):

    def __init__(self, 
        articulation_lists=None,
        minimum_prolated_duration=None, 
        maximum_prolated_duration=None,
        minimum_written_pitch=None, 
        maximum_written_pitch=None):
        ArticulationHandler.__init__(self,
            minimum_prolated_duration=minimum_prolated_duration,
            maximum_prolated_duration=maximum_prolated_duration,
            minimum_written_pitch=minimum_written_pitch,
            maximum_written_pitch=maximum_written_pitch)
        if articulation_lists is None:
            articulation_lists = []
        self.articulation_lists = articulation_lists

    ### SPECIAL METHODS ###

    def __call__(self, articulation_lists):
        new = type(self)()
        new.articulation_lists = articulation_lists
        return new

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def articulation_lists():
        def fget(self):
            return self._articulation_lists
        def fset(self, articulation_lists):
            if all([isinstance(x, (tuple, list)) for x in articulation_lists]):
                self._articulation_lists = articulation_lists
            else:
                raise TypeError(articulation_lists)
        return property(**locals())

    ### PUBLIC METHODS ###

    def apply(self, expr, offset = 0, skip_first = 0, skip_last = 0):
        articulation_lists = sequencetools.CyclicList(self.articulation_lists)
        notes_and_chords = list(leaftools.iterate_notes_and_chords_forward_in_expr(expr))
        notes_and_chords = notes_and_chords[skip_first:]
        if skip_last:
            notes_and_chords = notes_and_chords[:-skip_last]
        for i, note_or_chord in enumerate(notes_and_chords):
            articulation_list = articulation_lists[offset+i]
            if self.minimum_prolated_duration is not None:
                if note_or_chord.duration.prolated < self.minimum_prolated_duration:
                    continue
            if self.maximum_prolated_duration is not None:
                if self.maximum_prolated_duration < note_or_chord.duration.prolated:
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
            marktools.attach_articulations_to_notes_and_chords_in_expr(note_or_chord, articulation_list)
        return expr
