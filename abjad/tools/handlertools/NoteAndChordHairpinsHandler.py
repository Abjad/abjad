# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate
from abjad.tools.handlertools.DynamicHandler import DynamicHandler


class NoteAndChordHairpinsHandler(DynamicHandler):
    r'''Note and chord hairpins handler.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_hairpin_tokens',
        )

    ### INTIIALIZER ###

    def __init__(
        self, 
        hairpin_tokens=None, 
        minimum_duration=None,
        ):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        if hairpin_tokens is not None:
            for hairpin_token in hairpin_tokens:
                if not spannertools.Hairpin._is_hairpin_token(hairpin_token):
                    message = 'not hairpin token: {!r}'.format(hairpin_token)
                    raise ValueError(message)
        self._hairpin_tokens = hairpin_tokens

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties, timespan=None, offset=0):
        r'''Calls handler on `logical_ties` with `offset`.

        Returns none.
        '''
        hairpin_tokens = datastructuretools.CyclicTuple(self.hairpin_tokens)
        logical_tie_groups = self._group_contiguous_logical_ties(logical_ties)
        for logical_tie_group in logical_tie_groups:
            pairs = sequencetools.iterate_sequence_nwise(
                logical_tie_group,
                n=2,
                )
            for i, pair in enumerate(pairs):
                hairpin_token = hairpin_tokens[i]
                descriptor = ' '.join([_ for _ in hairpin_token if _])
                hairpin = spannertools.Hairpin(
                    descriptor=descriptor,
                    include_rests=False,
                    )
                first_logical_tie, second_logical_tie = pair
                notes = []
                notes.extend(first_logical_tie)
                notes.append(second_logical_tie.head)
                attach(hairpin, notes)

    ### PUBLIC PROPERTIES ###

    @property
    def hairpin_tokens(self):
        r'''Gets hairpin tokens of handler.

        Returns tuple or none.
        '''
        return self._hairpin_tokens