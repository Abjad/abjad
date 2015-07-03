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
        '_skip_ties',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        articulation_list=None,
        minimum_duration=None,
        maximum_duration=None,
        minimum_written_pitch=None,
        maximum_written_pitch=None,
        skip_ties=False,
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
        self._skip_ties = skip_ties

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
            if self.skip_ties and not logical_tie.is_trivial:
                continue
            if not note_or_chord is logical_tie.head:
                continue
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

    ### PUBLIC PROPERTIES ###

    @property
    def articulation_list(self):
        r'''Gets articulation list of handler.

        Returns list, tuple or none.
        '''
        return self._articulation_list

    @property
    def skip_ties(self):
        r'''Is true when handler should skip ties. Otherwise false.

        ..  container:: example

            **Example 1.** Doesn't skip ties:

            ::

                >>> handler = handlertools.ReiteratedArticulationHandler(
                ...     articulation_list=['>'],
                ...     skip_ties=False,
                ...     )
                >>> staff = Staff("c'4. ~ c'8 d'8 e'8 f'8 g'8")
                >>> logical_ties = iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> logical_ties = handler(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'4. -\accent ~
                    c'8 
                    d'8 -\accent
                    e'8 -\accent
                    f'8 -\accent
                    g'8 -\accent
                }

        ..  container:: example

            **Example 2.** Skips ties:

            ::

                >>> handler = handlertools.ReiteratedArticulationHandler(
                ...     articulation_list=['>'],
                ...     skip_ties=True,
                ...     )
                >>> staff = Staff("c'4. ~ c'8 d'8 e'8 f'8 g'8")
                >>> logical_ties = iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> logical_ties = handler(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'4. ~
                    c'8
                    d'8 -\accent
                    e'8 -\accent
                    f'8 -\accent
                    g'8 -\accent
                }

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._skip_ties