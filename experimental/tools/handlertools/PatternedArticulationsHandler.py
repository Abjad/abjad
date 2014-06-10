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


class PatternedArticulationsHandler(ArticulationHandler):

    def __init__(
        self,
        articulation_lists=None,
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
        if articulation_lists is None:
            articulation_lists = []
        self.articulation_lists = articulation_lists

    ### SPECIAL METHODS ###

    def __call__(self, expr, offset=0, skip_first=0, skip_last=0):
        articulation_lists = datastructuretools.CyclicTuple(
            self.articulation_lists)
        notes_and_chords = \
            list(iterate(expr).by_class((scoretools.Note, scoretools.Chord)))
        notes_and_chords = notes_and_chords[skip_first:]
        if skip_last:
            notes_and_chords = notes_and_chords[:-skip_last]
        for i, note_or_chord in enumerate(notes_and_chords):
            articulation_list = articulation_lists[offset+i]
            articulation_list = [
                indicatortools.Articulation(x)
                for x in articulation_list
                ]
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
            for articulation in articulation_list:
                new_articulation = copy.copy(articulation)
                attach(new_articulation, note_or_chord)
        return expr

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='articulation_lists',
                menu_key='al',
                editor=idetools.getters.get_lists,
                ),
            systemtools.AttributeDetail(
                name='minimum_duration',
                menu_key='nd',
                editor=idetools.getters.get_duration,
                ),
            systemtools.AttributeDetail(
                name='maximum_duration',
                menu_key='xd',
                editor=idetools.getters.get_duration,
                ),
            systemtools.AttributeDetail(
                name='minimum_written_pitch',
                menu_key='np',
                editor=idetools.getters.get_named_pitch,
                ),
            systemtools.AttributeDetail(
                name='maximum_written_pitch',
                menu_key='xp',
                editor=idetools.getters.get_named_pitch,
                ),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def articulation_lists(self):
        return self._articulation_lists

    @articulation_lists.setter
    def articulation_lists(self, articulation_lists):
        if all(isinstance(x, (tuple, list)) for x in articulation_lists):
            self._articulation_lists = articulation_lists
        else:
            raise TypeError(articulation_lists)
