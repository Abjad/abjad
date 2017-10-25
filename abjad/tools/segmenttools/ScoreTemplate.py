import abc
from abjad.tools import abctools


class ScoreTemplate(abctools.AbjadValueObject):
    r'''Abstract score template.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Score templates'

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self):
        r'''Calls score template.

        Returns score.
        '''
        pass

    def __illustrate__(
        self,
        default_paper_size=None,
        global_staff_size=None,
        includes=None,
        ):
        r'''Illustrates score template.

        Returns LilyPond file.
        '''
        import abjad
        score = self()
        for voice in abjad.iterate(score).components(abjad.Voice):
            voice.append(abjad.Skip(1))
        self.attach_defaults(score)
        lilypond_file = score.__illustrate__()
        lilypond_file = abjad.new(
            lilypond_file,
            default_paper_size=default_paper_size,
            global_staff_size=global_staff_size,
            includes=includes,
            )
        return lilypond_file

    ### PUBLIC METHODS ###

    def attach_defaults(self, score):
        r'''Attaches defaults to `score`.

        Returns none.
        '''
        import abjad
        assert isinstance(score, abjad.Score), repr(score)
        prototype = (abjad.Staff, abjad.StaffGroup)
        for context in abjad.iterate(score).components(prototype):
            leaf = abjad.inspect(context).get_leaf(0)
            if leaf is None:
                continue
            instrument = abjad.inspect(leaf).get_indicator(abjad.Instrument)
            if instrument is None:
                string = 'default_instrument'
                instrument = abjad.inspect(context).get_annotation(string)
                abjad.attach(instrument, leaf)
        for staff in abjad.iterate(score).components(abjad.Staff):
            leaf = abjad.inspect(staff).get_leaf(0)
            clef = abjad.inspect(leaf).get_indicator(abjad.Clef)
            if clef is not None:
                continue
            clef = abjad.inspect(staff).get_annotation('default_clef')
            instrument = abjad.inspect(leaf).get_effective(abjad.Instrument)
            if clef is None and instrument is not None:
                clef = abjad.Clef(instrument.allowable_clefs[0])
            abjad.attach(clef, leaf)
