import abc
import typing
from abjad.tools import abctools
from abjad.tools.datastructuretools.OrderedDict import OrderedDict
from abjad.tools.datastructuretools.String import String
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
from abjad.tools.systemtools.Tag import Tag
from abjad.tools.systemtools.Wrapper import Wrapper
from abjad.tools.topleveltools.attach import attach
from abjad.tools.topleveltools.inspect import inspect
from abjad.tools.topleveltools.iterate import iterate
from abjad.tools.topleveltools.new import new
from abjad.tools.topleveltools.select import select
from .PartAssignment import PartAssignment
from .PartManifest import PartManifest
from .Tags import Tags


class ScoreTemplate(abctools.AbjadValueObject):
    """
    Abstract score template.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Score templates'

    __slots__ = (
        '_voice_abbreviations',
        )

    _always_make_global_rests = False

    _do_not_require_margin_markup = False

    _part_manifest: PartManifest = PartManifest()

    ### INITIALIZER ###

    def __init__(self):
        self._voice_abbreviations = OrderedDict()

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self) -> Score:
        """
        Calls score template.
        """
        pass

    def __illustrate__(
        self,
        default_paper_size=None,
        global_staff_size=None,
        includes=None,
        ):
        """
        Illustrates score template.
        """
        score: Score = self()
        for voice in iterate(score).components(Voice):
            voice.append(Skip(1))
        self.attach_defaults(score)
        lilypond_file: LilyPondFile = score.__illustrate__()
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
    def always_make_global_rests(self) -> bool:
        """
        Is true when score template always makes global rests.
        """
        return self._always_make_global_rests

    @property
    def do_not_require_margin_markup(self) -> bool:
        """
        Is true when score template does not require margin markup.

        Conventionally, solos do not require margin markup.
        """
        return self._do_not_require_margin_markup

    @property
    def part_manifest(self) -> typing.Optional[PartManifest]:
        """
        Gets part manifest.
        """
        if self._part_manifest is not None:
            assert isinstance(self._part_manifest, PartManifest)
        return self._part_manifest

    ### PUBLIC METHODS ###

    def allows_instrument(
        self,
        staff_name: str,
        instrument: Instrument,
        ) -> bool:
        """
        Is true when ``staff_name`` allows ``instrument``.

        To be implemented by concrete score template classes.
        """
        return True

    def allows_part_assignment(
        self,
        voice_name: str,
        part_assignment: PartAssignment,
        ) -> bool:
        """
        Is true when ``voice_name`` allows ``part_assignment``.
        """
        section = part_assignment.section or 'ZZZ'
        if voice_name.startswith(section):
            return True
        return False

    def attach_defaults(self, argument) -> typing.List:
        """
        Attaches defaults to all staff and staff group contexts in
        ``argument`` when ``argument`` is a score.

        Attaches defaults to ``argument`` (without iterating ``argument``) when
        ``argument`` is a staff or staff group.

        Returns list of one wrapper for every indicator attached.
        """
        assert isinstance(argument, (Score, Staff, StaffGroup)), repr(argument)
        wrappers: typing.List[Wrapper] = []
        tag = Tags().REMOVE_ALL_EMPTY_STAVES
        empty_prototype = (MultimeasureRest, Skip)
        prototype = (Staff, StaffGroup)
        if isinstance(argument, Score):
            staff__groups = select(argument).components(prototype)
            staves = select(argument).components(Staff)
        elif isinstance(argument, Staff):
            staff__groups = [argument]
            staves = [argument]
        else:
            assert isinstance(argument, StaffGroup), repr(argument)
            staff__groups = [argument]
            staves = []
        for staff__group in staff__groups:
            leaf = None
            voices = select(staff__group).components(Voice)
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
                instrument = inspect(staff__group).get_annotation(string)
                if instrument is not None:
                    wrapper = attach(instrument, leaf, tag='ST1', wrapper=True)
                    wrappers.append(wrapper)
            margin_markup = inspect(leaf).get_indicator(MarginMarkup)
            if margin_markup is None:
                string = 'default_margin_markup'
                margin_markup = inspect(staff__group).get_annotation(string)
                if margin_markup is not None:
                    wrapper = attach(
                        margin_markup,
                        leaf,
                        tag=Tag('-PARTS').prepend('ST2'),
                        wrapper=True,
                        )
                    wrappers.append(wrapper)
        for staff in staves:
            leaf = inspect(staff).get_leaf(0)
            clef = inspect(leaf).get_indicator(Clef)
            if clef is not None:
                continue
            clef = inspect(staff).get_annotation('default_clef')
            if clef is not None:
                wrapper = attach(clef, leaf, tag='ST3', wrapper=True)
                wrappers.append(wrapper)
        return wrappers

    ### PUBLIC PROPERTIES ###

    @property
    def voice_abbreviations(self) -> OrderedDict:
        """
        Gets voice abbreviations.
        """
        return self._voice_abbreviations
