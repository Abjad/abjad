import abjad
import {score_package_name}


class SegmentMaker(abjad.AbjadObject):
    """
    Segment-maker.
    """

    ### INITIALIZER ###

    def __init__(self):
        self.score_template = {score_package_name}.ScoreTemplate()

    ### PUBLIC METHODS ###

    def run(
        self,
        metadata=None,
        midi=None,
        previous_metadata=None,
        ):
        """
        Runs segment-maker.

        Returns LilyPond file.
        """
        self.metadata = metadata
        self.midi = midi
        self.previous_metadata = previous_metadata
        score = self.score_template()
        score['Example Voice'].extend("c'4 ( d'4 e'4 f'4 )")
        lilypond_file = abjad.LilyPondFile.new(
            score,
            includes=['../../stylesheets/stylesheet.ily'],
            )
        return lilypond_file
