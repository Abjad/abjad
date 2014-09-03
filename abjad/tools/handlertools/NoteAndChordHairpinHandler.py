# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import spannertools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate
from abjad.tools.handlertools.DynamicHandler import DynamicHandler


class NoteAndChordHairpinHandler(DynamicHandler):
    r'''Note and chord hairpin handler.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_hairpin_token',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        hairpin_token=None, 
        minimum_duration=None,
        ):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        if hairpin_token is not None:
            assert spannertools.Hairpin._is_hairpin_token(hairpin_token)
        self._hairpin_token = hairpin_token

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties, timespan=None, offset=0):
        r'''Calls note and chord hairpin handler on `logical_ties` 
        with `offset`.

        Returns none.
        '''
        groups = self._group_contiguous_logical_ties(logical_ties)
        for group in groups:
            notes = []
            for logical_tie in group:
                for note in logical_tie:
                    notes.append(note)
            if len(notes) <= 1:
                continue
            descriptor = ' '.join([_ for _ in self.hairpin_token if _])
            hairpin = spannertools.Hairpin(
                descriptor=descriptor,
                include_rests=False,
                )
            attach(hairpin, notes)

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='hairpin_token',
                command='ht',
                editor=idetools.getters.get_hairpin_token,
                ),
            systemtools.AttributeDetail(
                name='minimum_duration',
                command='md',
                editor=idetools.getters.get_duration,
                ),
            )

    ### PRIVATE METHODS ###

    def _group_contiguous_logical_ties(self, logical_ties):
        result = []
        current_group = [logical_ties[0]]
        for logical_tie in logical_ties[1:]:
            last_timespan = current_group[-1].get_timespan()
            current_timespan = logical_tie.get_timespan()
            if last_timespan.stops_when_timespan_starts(current_timespan):
                current_group.append(logical_tie)
            else:
                result.append(current_group)
                current_group = [logical_tie]
        if current_group:
            result.append(current_group)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def hairpin_token(self):
        r'''Gets hairpin token of handler.

        Like ``('f', '>', 'p')``.

        Set to triple.
        '''
        return self._hairpin_token