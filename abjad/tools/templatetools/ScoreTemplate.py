import abc
from abjad.tools import abctools


class ScoreTemplate(abctools.AbjadValueObject):
    r'''Abstract score template.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self):
        r'''Calls score template.

        Returns score.
        '''
        pass

    def __illustrate__(self):
        r'''Illustrates score template.

        Returns LilyPond file.
        '''
        import abjad
        score = self()
        for voice in abjad.iterate(score).by_class(abjad.Voice):
            voice.append(abjad.Skip(1))
        self.attach_defaults(score)
        lilypond_file = score.__illustrate__()
        return lilypond_file

    ### PUBLIC METHODS ###

    def attach_defaults(self, score):
        r'''Attaches defaults to `score`.

        Returns none.
        '''
        import abjad
        prototype = (abjad.Staff, abjad.StaffGroup)
        for context in abjad.iterate(score).by_class(prototype):
            leaf = abjad.inspect(context).get_leaf(0)
            if not abjad.inspect(leaf).get_indicator(abjad.Instrument):
                instrument = abjad.inspect(context).get_annotation(
                    'default_instrument')
                abjad.attach(instrument, leaf)
            if not abjad.inspect(leaf).get_indicator(abjad.Clef):
                clef = abjad.inspect(context).get_annotation('default_clef')
                abjad.attach(clef, leaf)
