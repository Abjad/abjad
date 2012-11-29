from abjad.tools.chordtools import Chord
from abjad.tools.notetools.Note import Note
from abjad.tools import componenttools
from abjad.tools import iterationtools
from abjad.tools import marktools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from experimental.handlertools.dynamics.DynamicHandler import DynamicHandler


class NoteAndChordHairpinsHandler(DynamicHandler):

    def __init__(self, hairpin_tokens=None, minimum_prolated_duration=None):
        DynamicHandler.__init__(self, minimum_prolated_duration=minimum_prolated_duration)
        if hairpin_tokens is None:
            hairpin_tokens = []
        for hairpin_token in hairpin_tokens:
            if not spannertools.HairpinSpanner.is_hairpin_token(hairpin_token):
                raise ValueError('not hairpin token: %s' % str(hairpin_token))
        self.hairpin_tokens = hairpin_tokens

    ### SPECIAL METHODS ###

    def __call__(self):
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def apply(self, expr, offset = 0):
        leaves = list(iterationtools.iterate_leaves_in_expr(expr))
        groups = list(componenttools.yield_groups_of_mixed_klasses_in_sequence(leaves, (Note, Chord)))
        hairpin_tokens = sequencetools.CyclicList(self.hairpin_tokens)
        for i, group in enumerate(groups):
            is_short_group = False
            hairpin_token = hairpin_tokens[offset+i]
            if len(group) == 1:
                is_short_group = True
            elif self.minimum_prolated_duration is not None:
                prolated_duration = componenttools.sum_duration_of_components(group)
                if prolated_duration < self.minimum_prolated_duration:
                    is_short_group = True
            if is_short_group:
                start_dynamic = hairpin_token[0]
                ## TODO: fix dynamic mark and replace below with dynamic mark
                marktools.LilyPondCommandMark(start_dynamic, 'right')(group[0])
            else:
                descriptor = ' '.join([x for x in hairpin_token if x])
                spannertools.HairpinSpanner(group, descriptor, include_rests = False)
        return expr
