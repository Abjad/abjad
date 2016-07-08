# -*- coding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import lilypondfiletools
from {score_package_name}.tools import ScoreTemplate


class SegmentMaker(abctools.AbjadObject):

    ### INITIALIZER ###

    def __init__(self):
        self.score_template = ScoreTemplate()

    ### SPECIAL METHODS ###

    def __call__(
        self,
        segment_metadata=None,
        previous_segment_metadata=None,
        ):
        score = self.score_template()
        score['Example Voice'].extend("c'4 ( d'4 e'4 f'4 )")
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(
            score,
            includes=['../../stylesheets/stylesheet.ily'],
            )
        return lilypond_file, segment_metadata
