# -*- encoding: utf-8 -*-
import copy
from abjad.tools import datastructuretools
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import new
from abjad.tools.topleveltools import select
from abjad.tools.handlertools.ArticulationHandler import ArticulationHandler


class ReiteratedArticulationHandler(ArticulationHandler):
    r'''Reiterated articulation handler.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_articulation_list',
        )

    ### INITIALIZER ###

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
        articulation_list = articulation_list or ()
        if isinstance(articulation_list, str):
            articulation_list = [articulation_list]
        for articulation in articulation_list:
            if not isinstance(articulation, str):
                message = 'not articulation: {!r}'.format(articulation)
                raise TypeError(message)
        self._articulation_list = articulation_list

    ### SPECIAL METHODS ###

    def __call__(self, expr, offset=0, skip_first=0, skip_last=0):
        r'''Calls handler on `expr` with keywords.

        Returns none.
        '''
        prototype = (scoretools.Note, scoretools.Chord)
        notes_and_chords = list(iterate(expr).by_class(prototype))
        notes_and_chords = notes_and_chords[skip_first:]
        if skip_last:
            notes_and_chords = notes_and_chords[:-skip_last]
        for i, note_or_chord in enumerate(notes_and_chords):
            logical_tie = inspect_(note_or_chord).get_logical_tie()
            duration = logical_tie.get_duration()
            if self.minimum_duration is not None:
                if duration < self.minimum_duration:
                    continue
            if self.maximum_duration is not None:
                if self.maximum_duration <= duration:
                    continue
            if self.minimum_written_pitch is not None:
                if isinstance(note_or_chord, scoretools.Note):
                    minimum_written_pitch = note_or_chord.pitch
                else:
                    minimum_written_pitch = note_or_chord.written_pitches[0]
                if minimum_written_pitch < self.minimum_written_pitch:
                    continue
            if self.maximum_written_pitch is not None:
                if isinstance(note_or_chord, scoretools.Note):
                    maximum_written_pitch = note_or_chord.written_pitch
                else:
                    maximum_written_pitch = note_or_chord.written_pitches[-1]
                if self.maximum_written_pitch < maximum_written_pitch:
                    continue
            articulations = [
                indicatortools.Articulation(_)
                for _ in self.articulation_list
                ]
            for articulation in articulations:
                articulation = copy.deepcopy(articulation)
                attach(articulation, note_or_chord)
        return expr

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='articulation_list',
                command='al',
                editor=idetools.getters.get_articulations,
                ),
            systemtools.AttributeDetail(
                name='minimum_duration',
                command='nd',
                editor=idetools.getters.get_duration,
                ),
            systemtools.AttributeDetail(
                name='maximum_duration',
                command='xd',
                editor=idetools.getters.get_duration,
                ),
            systemtools.AttributeDetail(
                name='minimum_written_pitch',
                command='np',
                editor=idetools.getters.get_named_pitch,
                ),
            systemtools.AttributeDetail(
                name='maximum_written_pitch',
                command='xp',
                editor=idetools.getters.get_named_pitch,
                ),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def articulation_list(self):
        r'''Gets articulation list of handler.

        Returns list, tuple or none.
        '''
        return self._articulation_list