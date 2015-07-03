# -*- encoding: utf-8 -*-
import copy
from abjad.tools import datastructuretools
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import select
from abjad.tools.handlertools.ArticulationHandler import ArticulationHandler


class PatternedArticulationsHandler(ArticulationHandler):
    r'''Patterned articulations handler.

    ..  container:: example

        **Example 1.** Accents first logic tie of every three logical ties:

        ::

            >>> handler = handlertools.PatternedArticulationsHandler(
            ...     articulation_lists=(['accent'], None, None),
            ...     )
            >>> staff = Staff("c'4 ~ c'8 d'8 ~ d'4 r4 e'4 g'4 fs'4 ~ fs'4")
            >>> logical_ties = iterate(staff).by_logical_tie(pitched=True)
            >>> logical_ties = list(logical_ties)
            >>> logical_ties = handler(logical_ties)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'4 -\accent ~
                c'8
                d'8 ~
                d'4
                r4
                e'4 -\accent
                g'4
                fs'4 ~
                fs'4
            }

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_articulation_lists',
        )

    ### INITIALIZER ###

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
        if articulation_lists is not None:
            for articulation_list in articulation_lists:
                prototype = (tuple, list, type(None))
                if not isinstance(articulation_list, prototype):
                    message = 'not articulation list: {!r}.'
                    message = message.format(articulation_list)
                    raise TypeError(message)
                if articulation_list is not None:
                    for articulation in articulation_list:
                        if not isinstance(articulation, str):
                            message = 'not articulation: {!r}.'
                            message = message.format(articulation)
                            raise TypeError(message)
        self._articulation_lists = articulation_lists

    ### SPECIAL METHODS ###

    def __call__(
        self, 
        expr, 
        timespan=None, 
        offset=0, 
        skip_first=0, 
        skip_last=0,
        ):
        r'''Calls handler on `expr` with keywords.

        Returns none.
        '''
        articulation_lists = datastructuretools.CyclicTuple(
            self.articulation_lists)
        prototype = (scoretools.Note, scoretools.Chord)
        notes_and_chords = list(iterate(expr).by_class(prototype))
        notes_and_chords = notes_and_chords[skip_first:]
        if skip_last:
            notes_and_chords = notes_and_chords[:-skip_last]
        i = 0
        for note_or_chord in notes_and_chords:
            logical_tie = inspect_(note_or_chord).get_logical_tie()
            duration = logical_tie.get_duration()
            articulation_list = articulation_lists[offset+i]
            if articulation_list is None:
                i += 1
                continue
            articulation_list = [
                indicatortools.Articulation(_)
                for _ in articulation_list
                ]
            if self.minimum_duration is not None:
                if duration <= self.minimum_duration:
                    continue
            if self.maximum_duration is not None:
                if self.maximum_duration < duration:
                    continue
            if self.minimum_written_pitch is not None:
                if isinstance(note_or_chord, scoretools.Note):
                    minimum_written_pitch = note_or_chord.written_pitch
                else:
                    minimum_written_pitch = note_or_chord.writen_pitches[0]
                if minimum_written_pitch < self.minimum_written_pitch:
                    continue
            if self.maximum_written_pitch is not None:
                if isinstance(note_or_chord, scoretools.Note):
                    maximum_written_pitch = note_or_chord.written_pitch
                else:
                    maximum_written_pitch = note_or_chord.written_pitches[-1]
                if self.maximum_written_pitch < maximum_written_pitch:
                    continue
            logical_tie = inspect_(note_or_chord).get_logical_tie()
            if note_or_chord is logical_tie.head:
                for articulation in articulation_list:
                    # TODO: make new(articulation) work
                    articulation = copy.copy(articulation)
                    attach(articulation, note_or_chord)
                i += 1
        return expr

    ### PUBLIC PROPERTIES ###

    @property
    def articulation_lists(self):
        r'''Gets articulation lists of handler.

        Returns tuple or none.
        '''
        return self._articulation_lists