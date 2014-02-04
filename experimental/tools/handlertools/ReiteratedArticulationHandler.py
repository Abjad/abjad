# -*- encoding: utf-8 -*-
import copy
from abjad.tools import datastructuretools
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import select
from experimental.tools.handlertools.ArticulationHandler \
    import ArticulationHandler


class ReiteratedArticulationHandler(ArticulationHandler):

    def __init__(
        self,
        articulation_list=None,
        minimum_duration=None,
        maximum_duration=None,
        minimum_written_pitch=None,
        maximum_written_pitch=None,
        ):
        ArticulationHandler.__init__(
            self,
            minimum_duration=minimum_duration,
            maximum_duration=maximum_duration,
            minimum_written_pitch=minimum_written_pitch,
            maximum_written_pitch=maximum_written_pitch,
            )
        if articulation_list is None:
            articulation_list = []
        if isinstance(articulation_list, str):
            articulation_list = [articulation_list]
        self.articulation_list = articulation_list

    ### SPECIAL METHODS ###

    def __call__(self, expr, offset=0, skip_first=0, skip_last=0):
        articulation_list = datastructuretools.CyclicTuple(
            self.articulation_list)
        notes_and_chords = \
            list(iterate(expr).by_class((scoretools.Note, scoretools.Chord)))
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
                if isinstance(note_or_chord, scoretools.Note):
                    minimum_written_pitch = note_or_chord.pitch
                else:
                    minimum_written_pitch = note_or_chord.pitches[0]
                if minimum_written_pitch < self.minimum_written_pitch:
                    continue
            if self.maximum_written_pitch is not None:
                if isinstance(note_or_chord, scoretools.Note):
                    maximum_written_pitch = note_or_chord.pitch
                else:
                    maximum_written_pitch = note_or_chord.pitches[-1]
                if self.maximum_written_pitch < maximum_written_pitch:
                    continue
            articulation_list = [
                indicatortools.Articulation(x)
                for x in self.articulation_list
                ]
            for articulation in articulation_list:
                new_articulation = copy.copy(articulation)
                attach(new_articulation, note_or_chord)
        return expr

    ### PUBLIC PROPERTIES ###

    @apply
    def articulation_list():
        def fget(self):
            return self._articulation_list
        def fset(self, articulation_list):
            if isinstance(articulation_list, list):
                if all(isinstance(x, str) for x in articulation_list):
                    self._articulation_list = articulation_list
            elif isinstance(articulation_list, str):
                self._articulation_list = [articulation_list]
            else:
                raise TypeError(articulation_list)
        return property(**locals())
