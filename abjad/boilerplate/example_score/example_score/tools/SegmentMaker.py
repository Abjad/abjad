# -*- coding: utf-8 -*-
import abjad
import {score_package_name}


class SegmentMaker(abjad.abctools.AbjadObject):
    r'''Segment-maker.
    '''

    ### INITIALIZER ###

    def __init__(self):
        self.score_template = {score_package_name}.tools.ScoreTemplate()

    ### SPECIAL METHODS ###

    def __call__(
        self,
        segment_metadata=None,
        previous_segment_metadata=None,
        ):
        score = self.score_template()
        score['Example Voice'].extend("c'4 ( d'4 e'4 f'4 )")
        lilypond_file = abjad.lilypondfiletools.LilyPondFile.new(
            score,
            includes=['../../stylesheets/stylesheet.ily'],
            )
        return lilypond_file, segment_metadata
