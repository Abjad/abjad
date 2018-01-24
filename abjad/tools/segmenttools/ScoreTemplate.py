import abc
from abjad.tools import abctools


class ScoreTemplate(abctools.AbjadValueObject):
    r'''Abstract score template.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Score templates'

    __slots__ = (
        )

    _parts = (
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

    ### PUBLIC PROPERTIES ###

    @property
    def parts(self):
        r'''Gets list of part names defined as class variable.

        Returns list of valid LilyPond identifiers or none.
        '''
        import abjad
        parts = self._parts
        if parts is not None:
            assert not isinstance(parts, str), parts
            assert all(isinstance(part, str) for part in parts)
            for part in parts:
                if not abjad.String(part).is_lilypond_identifier():
                    message = 'invalid LilyPond identifier: {!r}.'
                    message = message.format(part)
                    raise Exception(message)
        return self._parts

    ### PUBLIC METHODS ###

    def attach_defaults(self, score):
        r'''Attaches defaults to `score`.

        Returns one leaf / indicator pair for every indicator attached.
        '''
        import abjad
        assert isinstance(score, abjad.Score), repr(score)
        pairs = []
        prototype = (abjad.Staff, abjad.StaffGroup)
        empty_prototype = (abjad.MultimeasureRest, abjad.Skip)
        for context in abjad.iterate(score).components(prototype):
            leaf = None
            voices = abjad.select(context).components(abjad.Voice)
            # find first leaf in first nonempty voice
            for voice in voices:
                leaves = abjad.select(voice).leaves()
                if not all(isinstance(_, empty_prototype) for _ in leaves):
                    leaf = abjad.inspect(voice).get_leaf(0)
            # otherwise, find first leaf in voice in non-removable staff
            if leaf is None:
                for voice in voices:
                    voice_might_vanish = False
                    for component in abjad.inspect(voice).get_parentage():
                        if abjad.inspect(component).get_annotation(
                            abjad.tags.REMOVE_ALL_EMPTY_STAVES
                            ) is True:
                            voice_might_vanish = True
                    if not voice_might_vanish:
                        leaf = abjad.inspect(voice).get_leaf(0)
                        if leaf is not None:    
                            break
            # otherwise, as last resort find first leaf in first voice
            if leaf is None:
                leaf = abjad.inspect(voices[0]).get_leaf(0)
            if leaf is None:
                continue
            instrument = abjad.inspect(leaf).get_indicator(abjad.Instrument)
            if instrument is None:
                string = 'default_instrument'
                instrument = abjad.inspect(context).get_annotation(string)
                if instrument is not None:
                    abjad.attach(instrument, leaf, site='ST1')
                    pairs.append((leaf, instrument))
            # simplify after adding abjad.MarginMarkup
            indicators = abjad.inspect(leaf).get_indicators()
            if all(type(_).__name__ != 'MarginMarkup' for _ in indicators):
                string = 'default_margin_markup'
                margin_markup = abjad.inspect(context).get_annotation(string)
                if margin_markup is not None:
                    abjad.attach(margin_markup, leaf, site='ST2')
                    pairs.append((leaf, margin_markup))
        for staff in abjad.iterate(score).components(abjad.Staff):
            leaf = abjad.inspect(staff).get_leaf(0)
            clef = abjad.inspect(leaf).get_indicator(abjad.Clef)
            if clef is not None:
                continue
            clef = abjad.inspect(staff).get_annotation('default_clef')
            if clef is not None:
                abjad.attach(clef, leaf, site='ST3')
                pairs.append((leaf, clef))
        return pairs
