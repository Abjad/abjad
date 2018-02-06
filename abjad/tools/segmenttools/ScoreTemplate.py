import abc
from typing import List
from typing import Tuple
from abjad.tools import abctools
from abjad.tools.indicatortools.Clef import Clef
from abjad.tools.indicatortools.MarginMarkup import MarginMarkup
from abjad.tools.instrumenttools.Instrument import Instrument
from abjad.tools.lilypondfiletools.LilyPondFile import LilyPondFile
from abjad.tools.scoretools.Context import Context
from abjad.tools.scoretools.MultimeasureRest import MultimeasureRest
from abjad.tools.scoretools.Rest import Rest
from abjad.tools.scoretools.Score import Score
from abjad.tools.scoretools.Skip import Skip
from abjad.tools.scoretools.Staff import Staff
from abjad.tools.scoretools.StaffGroup import StaffGroup
from abjad.tools.scoretools.Voice import Voice
from abjad.tools.topleveltools.attach import attach
from abjad.tools.topleveltools.inspect import inspect
from abjad.tools.topleveltools.iterate import iterate
from abjad.tools.topleveltools.new import new
from abjad.tools.topleveltools.select import select
from .Tags import Tags


class ScoreTemplate(abctools.AbjadValueObject):
    r'''Abstract score template.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Score templates'

    __slots__ = (
        )

    _part_manifest: Tuple = (
        )

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self) -> Score:
        r'''Calls score template.
        '''
        pass

    def __illustrate__(
        self,
        default_paper_size: str = None,
        global_staff_size: int = None,
        includes: List = None,
        ) -> LilyPondFile:
        r'''Illustrates score template.
        '''
        score = self()
        for voice in iterate(score).components(Voice):
            voice.append(Skip(1))
        self.attach_defaults(score)
        lilypond_file = score.__illustrate__()
        lilypond_file = new(
            lilypond_file,
            default_paper_size=default_paper_size,
            global_staff_size=global_staff_size,
            includes=includes,
            )
        return lilypond_file

    ### PRIVATE METHODS ###

    def _make_global_context(self):
        global_rests = Context(
            lilypond_type='GlobalRests',
            name='GlobalRests',
            )
        global_skips = Context(
            lilypond_type='GlobalSkips',
            name='GlobalSkips',
            )
        global_context = Context(
            [global_rests, global_skips],
            lilypond_type='GlobalContext',
            is_simultaneous=True,
            name='GlobalContext',
            )
        return global_context

    ### PUBLIC PROPERTIES ###

    @property
    def part_manifest(self) -> Tuple:
        r'''Gets part manifest.
        '''
        return self._part_manifest

    ### PUBLIC METHODS ###

    def attach_defaults(self, argument) -> List:
        r'''Attaches defaults to staff and staff group contexts in
        ``argument``.

        Returns one leaf / indicator pair for every indicator attached.
        '''
        pairs = []
        prototype = (Staff, StaffGroup)
        empty_prototype = (MultimeasureRest, Skip)
        tag = Tags().REMOVE_ALL_EMPTY_STAVES
        for context in iterate(argument).components(prototype):
            leaf = None
            voices = select(context).components(Voice)
            # find first leaf in first nonempty voice
            for voice in voices:
                leaves = select(voice).leaves()
                if not all(isinstance(_, empty_prototype) for _ in leaves):
                    leaf = inspect(voice).get_leaf(0)
            # otherwise, find first leaf in voice in non-removable staff
            if leaf is None:
                for voice in voices:
                    voice_might_vanish = False
                    for component in inspect(voice).get_parentage():
                        if inspect(component).get_annotation(tag) is True:
                            voice_might_vanish = True
                    if not voice_might_vanish:
                        leaf = inspect(voice).get_leaf(0)
                        if leaf is not None:    
                            break
            # otherwise, as last resort find first leaf in first voice
            if leaf is None:
                leaf = inspect(voices[0]).get_leaf(0)
            if leaf is None:
                continue
            instrument = inspect(leaf).get_indicator(Instrument)
            if instrument is None:
                string = 'default_instrument'
                instrument = inspect(context).get_annotation(string)
                if instrument is not None:
                    attach(instrument, leaf, site='ST1')
                    pairs.append((leaf, instrument))
            margin_markup = inspect(leaf).get_indicator(MarginMarkup)
            if margin_markup is None:
                string = 'default_margin_markup'
                margin_markup = inspect(context).get_annotation(string)
                if margin_markup is not None:
                    attach(
                        margin_markup,
                        leaf,
                        site='ST2',
                        tag='+SCORE:+SEGMENT',
                        )
                    pairs.append((leaf, margin_markup))
        for staff in iterate(argument).components(Staff):
            leaf = inspect(staff).get_leaf(0)
            clef = inspect(leaf).get_indicator(Clef)
            if clef is not None:
                continue
            clef = inspect(staff).get_annotation('default_clef')
            if clef is not None:
                attach(clef, leaf, site='ST3')
                pairs.append((leaf, clef))
        return pairs

    def part_names(self) -> List[str]:
        r'''Gets part names.
        '''
        return [_[0] for _ in self.part_manifest]
