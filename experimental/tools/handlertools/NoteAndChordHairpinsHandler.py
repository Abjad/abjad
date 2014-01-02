# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import spannertools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate
from experimental.tools.handlertools.DynamicHandler import DynamicHandler


class NoteAndChordHairpinsHandler(DynamicHandler):

    def __init__(self, hairpin_tokens=None, minimum_duration=None):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        if hairpin_tokens is None:
            hairpin_tokens = []
        for hairpin_token in hairpin_tokens:
            if not spannertools.Hairpin._is_hairpin_token(hairpin_token):
                raise ValueError('not hairpin token: %s' % str(hairpin_token))
        self.hairpin_tokens = hairpin_tokens

    ### SPECIAL METHODS ###

    def __call__(self, expr, offset=0):
        leaves = list(iterate(expr).by_class(scoretools.Leaf))
        groups = list(iterate(leaves).by_run(
            (scoretools.Note, scoretools.Chord)))
        hairpin_tokens = datastructuretools.CyclicList(self.hairpin_tokens)
        for i, group in enumerate(groups):
            if not isinstance(group, selectiontools.SliceSelection):
                group = selectiontools.SliceSelection(group)
            is_short_group = False
            hairpin_token = hairpin_tokens[offset + i]
            if len(group) == 1:
                is_short_group = True
            elif self.minimum_duration is not None:
                if group.get_duration() < self.minimum_duration:
                    is_short_group = True
            if is_short_group:
                start_dynamic = hairpin_token[0]
                #indicatortools.Dynamic(start_dynamic)(group[0])
                command = indicatortools.LilyPondCommand(start_dynamic, 'right')
                attach(command, group[0])
            else:
                descriptor = ' '.join([x for x in hairpin_token if x])
                hairpin = spannertools.Hairpin(
                    descriptor=descriptor,
                    include_rests=False,
                    )
                attach(hairpin, group)
        return expr
