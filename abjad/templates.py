import abc
import collections
import typing

from . import _inspect, _iterate, instruments
from .attach import Wrapper, annotate, attach
from .illustrators import illustrate
from .indicators.Clef import Clef
from .instruments import Piano
from .iterate import Iteration
from .lilypondfile import LilyPondFile
from .new import new
from .ordereddict import OrderedDict
from .overrides import LilyPondLiteral
from .score import Context, Score, Skip, Staff, StaffGroup, Voice
from .select import Selection
from .storage import StorageFormatManager
from .tag import Tag


class ScoreTemplate:
    """
    Abstract score template.
    """

    ### CLASS VARIABLES ###

    __documentation_section__: typing.Optional[str] = "Score templates"

    __slots__ = ("_voice_abbreviations",)

    _always_make_global_rests = False

    _do_not_require_margin_markup = False

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
        self, default_paper_size=None, global_staff_size=None, includes=None
    ):
        """
        Illustrates score template.
        """
        score: Score = self()
        site = "abjad.ScoreTemplate.__illustrate__()"
        tag = Tag(site)
        for voice in Iteration(score).components(Voice):
            skip = Skip(1, tag=tag)
            voice.append(skip)
        self.attach_defaults(score)
        lilypond_file: LilyPondFile = illustrate(score)
        lilypond_file = new(
            lilypond_file,
            default_paper_size=default_paper_size,
            global_staff_size=global_staff_size,
            includes=includes,
        )
        return lilypond_file

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _make_global_context(self):
        site = "abjad.ScoreTemplate._make_global_context()"
        tag = Tag(site)
        global_rests = Context(
            lilypond_type="GlobalRests",
            name="Global_Rests",
            tag=tag,
        )
        global_skips = Context(
            lilypond_type="GlobalSkips",
            name="Global_Skips",
            tag=tag,
        )
        global_context = Context(
            [global_rests, global_skips],
            lilypond_type="GlobalContext",
            simultaneous=True,
            name="Global_Context",
            tag=tag,
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

    ### PUBLIC METHODS ###

    def allows_instrument(
        self, staff_name: str, instrument: instruments.Instrument
    ) -> bool:
        """
        Is true when ``staff_name`` allows ``instrument``.

        To be implemented by concrete score template classes.
        """
        return True

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
        prototype = (Staff, StaffGroup)
        staves = Selection(argument).components(prototype)
        assert isinstance(staves, Selection), repr(staves)
        for staff in staves:
            leaf = _iterate._get_leaf(staff, 0)
            clef = _inspect._get_indicator(leaf, Clef)
            if clef is not None:
                continue
            clef = _inspect._get_annotation(staff, "default_clef")
            if clef is not None:
                wrapper = attach(
                    clef,
                    leaf,
                    tag=Tag("abjad.ScoreTemplate.attach_defaults(3)"),
                    wrapper=True,
                )
                wrappers.append(wrapper)
        return wrappers

    ### PUBLIC PROPERTIES ###

    @property
    def voice_abbreviations(self) -> OrderedDict:
        """
        Gets voice abbreviations.
        """
        return self._voice_abbreviations


class GroupedRhythmicStavesScoreTemplate(ScoreTemplate):
    r"""
    Grouped rhythmic staves score template.

    ..  container:: example

        One voice per staff:

        >>> class_ = abjad.GroupedRhythmicStavesScoreTemplate
        >>> template_1 = class_(staff_count=4)
        >>> abjad.show(template_1) # doctest: +SKIP

        ..  docs::

            >>> score = template_1.__illustrate__()[abjad.Score]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Grouped_Rhythmic_Staves_Score"
            <<
                \context StaffGroup = "Grouped_Rhythmic_Staves_Staff_Group"
                <<
                    \context RhythmicStaff = "Staff_1"
                    {
                        \context Voice = "Voice_1"
                        {
                            \clef "percussion"
                            s1
                        }
                    }
                    \context RhythmicStaff = "Staff_2"
                    {
                        \context Voice = "Voice_2"
                        {
                            \clef "percussion"
                            s1
                        }
                    }
                    \context RhythmicStaff = "Staff_3"
                    {
                        \context Voice = "Voice_3"
                        {
                            \clef "percussion"
                            s1
                        }
                    }
                    \context RhythmicStaff = "Staff_4"
                    {
                        \context Voice = "Voice_4"
                        {
                            \clef "percussion"
                            s1
                        }
                    }
                >>
            >>

        >>> score = template_1()
        >>> abjad.show(score) # doctest: +SKIP

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Grouped_Rhythmic_Staves_Score"
        <<
            \context StaffGroup = "Grouped_Rhythmic_Staves_Staff_Group"
            <<
                \context RhythmicStaff = "Staff_1"
                {
                    \context Voice = "Voice_1"
                    {
                    }
                }
                \context RhythmicStaff = "Staff_2"
                {
                    \context Voice = "Voice_2"
                    {
                    }
                }
                \context RhythmicStaff = "Staff_3"
                {
                    \context Voice = "Voice_3"
                    {
                    }
                }
                \context RhythmicStaff = "Staff_4"
                {
                    \context Voice = "Voice_4"
                    {
                    }
                }
            >>
        >>

    ..  container:: example

        More than one voice per staff:

        >>> template_2 = class_(staff_count=[2, 1, 2])
        >>> abjad.show(template_2) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(template_2.__illustrate__()[abjad.Score])
            >>> print(string)
            \context Score = "Grouped_Rhythmic_Staves_Score"
            <<
                \context StaffGroup = "Grouped_Rhythmic_Staves_Staff_Group"
                <<
                    \context RhythmicStaff = "Staff_1"
                    <<
                        \context Voice = "Voice_1_1"
                        {
                            s1
                        }
                        \context Voice = "Voice_1_2"
                        {
                            s1
                        }
                    >>
                    \context RhythmicStaff = "Staff_2"
                    {
                        \context Voice = "Voice_2"
                        {
                            s1
                        }
                    }
                    \context RhythmicStaff = "Staff_3"
                    <<
                        \context Voice = "Voice_3_1"
                        {
                            s1
                        }
                        \context Voice = "Voice_3_2"
                        {
                            s1
                        }
                    >>
                >>
            >>

        >>> score = template_2()
        >>> abjad.show(score) # doctest: +SKIP

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Grouped_Rhythmic_Staves_Score"
        <<
            \context StaffGroup = "Grouped_Rhythmic_Staves_Staff_Group"
            <<
                \context RhythmicStaff = "Staff_1"
                <<
                    \context Voice = "Voice_1_1"
                    {
                    }
                    \context Voice = "Voice_1_2"
                    {
                    }
                >>
                \context RhythmicStaff = "Staff_2"
                {
                    \context Voice = "Voice_2"
                    {
                    }
                }
                \context RhythmicStaff = "Staff_3"
                <<
                    \context Voice = "Voice_3_1"
                    {
                    }
                    \context Voice = "Voice_3_2"
                    {
                    }
                >>
            >>
        >>

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_staff_count",)

    ### INITIALIZER ###

    def __init__(self, staff_count=2):
        super().__init__()
        assert isinstance(staff_count, (int, collections.abc.Iterable))
        if isinstance(staff_count, collections.abc.Iterable):
            staff_count = list(staff_count)
        self._staff_count = staff_count

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Calls score template.

        Returns score.
        """
        staves = []
        site = "abjad.GroupedRhythmicStavesScoreTemplate.__call__()"
        tag = Tag(site)
        if isinstance(self.staff_count, int):
            for index in range(self.staff_count):
                number = index + 1
                name = f"Voice_{number}"
                voice = Voice([], name=name, tag=tag)
                name = f"Staff_{number}"
                staff = Staff([voice], name=name, tag=tag)
                staff.lilypond_type = "RhythmicStaff"
                annotate(staff, "default_clef", Clef("percussion"))
                staves.append(staff)
                key = f"v{number}"
                self.voice_abbreviations[key] = voice.name
        elif isinstance(self.staff_count, list):
            for staff_index, voice_count in enumerate(self.staff_count):
                staff_number = staff_index + 1
                name = f"Staff_{staff_number}"
                staff = Staff(name=name, tag=tag)
                staff.lilypond_type = "RhythmicStaff"
                assert 1 <= voice_count
                for voice_index in range(voice_count):
                    voice_number = voice_index + 1
                    if voice_count == 1:
                        voice_identifier = str(staff_number)
                    else:
                        voice_identifier = f"{staff_number}_{voice_number}"
                        staff.simultaneous = True
                    name = f"Voice_{voice_identifier}"
                    voice = Voice([], name=name, tag=tag)
                    staff.append(voice)
                    key = f"v{voice_identifier}"
                    self.voice_abbreviations[key] = voice.name
                staves.append(staff)
        grouped_rhythmic_staves_staff_group = StaffGroup(
            staves, name="Grouped_Rhythmic_Staves_Staff_Group", tag=tag
        )
        grouped_rhythmic_staves_score = Score(
            [grouped_rhythmic_staves_staff_group],
            name="Grouped_Rhythmic_Staves_Score",
            tag=tag,
        )
        return grouped_rhythmic_staves_score

    ### PUBLIC PROPERTIES ###

    @property
    def staff_count(self):
        """
        Gets score template staff count.

        ..  container:: example

            >>> class_ = abjad.GroupedRhythmicStavesScoreTemplate
            >>> template = class_(staff_count=4)
            >>> template.staff_count
            4

        Returns nonnegative integer.
        """
        return self._staff_count

    @property
    def voice_abbreviations(self):
        """
        Gets context name abbreviations.

        ..  container:: example

            >>> class_ = abjad.GroupedRhythmicStavesScoreTemplate
            >>> template = class_(staff_count=4)
            >>> template.voice_abbreviations
            OrderedDict([])

        """
        return super(GroupedRhythmicStavesScoreTemplate, self).voice_abbreviations


class GroupedStavesScoreTemplate(ScoreTemplate):
    r"""
    Grouped staves score template.

    ..  container:: example

        >>> class_ = abjad.GroupedStavesScoreTemplate
        >>> template = class_(staff_count=4)
        >>> abjad.show(template) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(template.__illustrate__()[abjad.Score])
            >>> print(string)
            \context Score = "Grouped_Staves_Score"
            <<
                \context StaffGroup = "Grouped_Staves_Staff_Group"
                <<
                    \context Staff = "Staff_1"
                    {
                        \context Voice = "Voice_1"
                        {
                            s1
                        }
                    }
                    \context Staff = "Staff_2"
                    {
                        \context Voice = "Voice_2"
                        {
                            s1
                        }
                    }
                    \context Staff = "Staff_3"
                    {
                        \context Voice = "Voice_3"
                        {
                            s1
                        }
                    }
                    \context Staff = "Staff_4"
                    {
                        \context Voice = "Voice_4"
                        {
                            s1
                        }
                    }
                >>
            >>

        >>> score = template()
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Grouped_Staves_Score"
        <<
            \context StaffGroup = "Grouped_Staves_Staff_Group"
            <<
                \context Staff = "Staff_1"
                {
                    \context Voice = "Voice_1"
                    {
                    }
                }
                \context Staff = "Staff_2"
                {
                    \context Voice = "Voice_2"
                    {
                    }
                }
                \context Staff = "Staff_3"
                {
                    \context Voice = "Voice_3"
                    {
                    }
                }
                \context Staff = "Staff_4"
                {
                    \context Voice = "Voice_4"
                    {
                    }
                }
            >>
        >>

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_staff_count",)

    ### INITIALIZER ###

    def __init__(self, staff_count=2):
        super().__init__()
        self._staff_count = staff_count

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Calls score template.

        Returns score.
        """
        staves = []
        site = "abjad.GroupedStavesScoreTemplate.__call__()"
        tag = Tag(site)
        for index in range(self.staff_count):
            number = index + 1
            voice = Voice([], name=f"Voice_{number}", tag=tag)
            staff = Staff([voice], name=f"Staff_{number}", tag=tag)
            staves.append(staff)
            self.voice_abbreviations[f"v{number}"] = voice.name
        staff_group = StaffGroup(staves, name="Grouped_Staves_Staff_Group", tag=tag)
        score = Score([staff_group], name="Grouped_Staves_Score", tag=tag)
        return score

    ### PUBLIC PROPERTIES ###

    @property
    def staff_count(self):
        """
        Gets staff count.

        ..  container::

            >>> class_ = abjad.GroupedStavesScoreTemplate
            >>> template = class_(staff_count=4)
            >>> template.staff_count
            4

        """
        return self._staff_count

    @property
    def voice_abbreviations(self):
        """
        Gets context name abbreviations.

        ..  container::

            >>> class_ = abjad.GroupedStavesScoreTemplate
            >>> template = class_(staff_count=4)
            >>> template.voice_abbreviations
            OrderedDict([])

        """
        return super().voice_abbreviations


class StringOrchestraScoreTemplate(ScoreTemplate):
    r"""
    String orchestra score template.

    ..  container:: example

        >>> template = abjad.StringOrchestraScoreTemplate()
        >>> abjad.show(template) # doctest: +SKIP

        >>> string = abjad.lilypond(template.__illustrate__()[abjad.Score])
        >>> print(string)
        \context Score = "Score"
        <<
            \tag #'(Violin_1 Violin_2 Violin_3 Violin_4 Violin_5 Violin_6 Viola_1 Viola_2 Viola_3 Viola_4 Cello_1 Cello_2 Cello_3 Contrabass_1 Contrabass_2)
            \context GlobalContext = "Global_Context"
            {
            }
            \context StaffGroup = "Outer_Staff_Group"
            <<
                \context ViolinStaffGroup = "Violin_Staff_Group"
                <<
                    \tag #'Violin_1
                    \context StringPerformerStaffGroup = "Violin_1_Staff_Group"
                    <<
                        \context BowingStaff = "Violin_1_Bowing_Staff"
                        <<
                            \context BowingVoice = "Violin_1_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Violin_1_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Violin_1_Fingering_Voice"
                            {
                                \clef "treble"
                                s1
                            }
                        >>
                    >>
                    \tag #'Violin_2
                    \context StringPerformerStaffGroup = "Violin_2_Staff_Group"
                    <<
                        \context BowingStaff = "Violin_2_Bowing_Staff"
                        <<
                            \context BowingVoice = "Violin_2_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Violin_2_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Violin_2_Fingering_Voice"
                            {
                                \clef "treble"
                                s1
                            }
                        >>
                    >>
                    \tag #'Violin_3
                    \context StringPerformerStaffGroup = "Violin_3_Staff_Group"
                    <<
                        \context BowingStaff = "Violin_3_Bowing_Staff"
                        <<
                            \context BowingVoice = "Violin_3_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Violin_3_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Violin_3_Fingering_Voice"
                            {
                                \clef "treble"
                                s1
                            }
                        >>
                    >>
                    \tag #'Violin_4
                    \context StringPerformerStaffGroup = "Violin_4_Staff_Group"
                    <<
                        \context BowingStaff = "Violin_4_Bowing_Staff"
                        <<
                            \context BowingVoice = "Violin_4_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Violin_4_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Violin_4_Fingering_Voice"
                            {
                                \clef "treble"
                                s1
                            }
                        >>
                    >>
                    \tag #'Violin_5
                    \context StringPerformerStaffGroup = "Violin_5_Staff_Group"
                    <<
                        \context BowingStaff = "Violin_5_Bowing_Staff"
                        <<
                            \context BowingVoice = "Violin_5_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Violin_5_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Violin_5_Fingering_Voice"
                            {
                                \clef "treble"
                                s1
                            }
                        >>
                    >>
                    \tag #'Violin_6
                    \context StringPerformerStaffGroup = "Violin_6_Staff_Group"
                    <<
                        \context BowingStaff = "Violin_6_Bowing_Staff"
                        <<
                            \context BowingVoice = "Violin_6_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Violin_6_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Violin_6_Fingering_Voice"
                            {
                                \clef "treble"
                                s1
                            }
                        >>
                    >>
                >>
                \context ViolaStaffGroup = "Viola_Staff_Group"
                <<
                    \tag #'Viola_1
                    \context StringPerformerStaffGroup = "Viola_1_Staff_Group"
                    <<
                        \context BowingStaff = "Viola_1_Bowing_Staff"
                        <<
                            \context BowingVoice = "Viola_1_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Viola_1_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Viola_1_Fingering_Voice"
                            {
                                \clef "alto"
                                s1
                            }
                        >>
                    >>
                    \tag #'Viola_2
                    \context StringPerformerStaffGroup = "Viola_2_Staff_Group"
                    <<
                        \context BowingStaff = "Viola_2_Bowing_Staff"
                        <<
                            \context BowingVoice = "Viola_2_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Viola_2_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Viola_2_Fingering_Voice"
                            {
                                \clef "alto"
                                s1
                            }
                        >>
                    >>
                    \tag #'Viola_3
                    \context StringPerformerStaffGroup = "Viola_3_Staff_Group"
                    <<
                        \context BowingStaff = "Viola_3_Bowing_Staff"
                        <<
                            \context BowingVoice = "Viola_3_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Viola_3_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Viola_3_Fingering_Voice"
                            {
                                \clef "alto"
                                s1
                            }
                        >>
                    >>
                    \tag #'Viola_4
                    \context StringPerformerStaffGroup = "Viola_4_Staff_Group"
                    <<
                        \context BowingStaff = "Viola_4_Bowing_Staff"
                        <<
                            \context BowingVoice = "Viola_4_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Viola_4_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Viola_4_Fingering_Voice"
                            {
                                \clef "alto"
                                s1
                            }
                        >>
                    >>
                >>
                \context CelloStaffGroup = "Cello_Staff_Group"
                <<
                    \tag #'Cello_1
                    \context StringPerformerStaffGroup = "Cello_1_Staff_Group"
                    <<
                        \context BowingStaff = "Cello_1_Bowing_Staff"
                        <<
                            \context BowingVoice = "Cello_1_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Cello_1_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Cello_1_Fingering_Voice"
                            {
                                \clef "bass"
                                s1
                            }
                        >>
                    >>
                    \tag #'Cello_2
                    \context StringPerformerStaffGroup = "Cello_2_Staff_Group"
                    <<
                        \context BowingStaff = "Cello_2_Bowing_Staff"
                        <<
                            \context BowingVoice = "Cello_2_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Cello_2_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Cello_2_Fingering_Voice"
                            {
                                \clef "bass"
                                s1
                            }
                        >>
                    >>
                    \tag #'Cello_3
                    \context StringPerformerStaffGroup = "Cello_3_Staff_Group"
                    <<
                        \context BowingStaff = "Cello_3_Bowing_Staff"
                        <<
                            \context BowingVoice = "Cello_3_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Cello_3_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Cello_3_Fingering_Voice"
                            {
                                \clef "bass"
                                s1
                            }
                        >>
                    >>
                >>
                \context ContrabassStaffGroup = "Contrabass_Staff_Group"
                <<
                    \tag #'Contrabass_1
                    \context StringPerformerStaffGroup = "Contrabass_1_Staff_Group"
                    <<
                        \context BowingStaff = "Contrabass_1_Bowing_Staff"
                        <<
                            \context BowingVoice = "Contrabass_1_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Contrabass_1_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Contrabass_1_Fingering_Voice"
                            {
                                \clef "bass_8"
                                s1
                            }
                        >>
                    >>
                    \tag #'Contrabass_2
                    \context StringPerformerStaffGroup = "Contrabass_2_Staff_Group"
                    <<
                        \context BowingStaff = "Contrabass_2_Bowing_Staff"
                        <<
                            \context BowingVoice = "Contrabass_2_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Contrabass_2_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Contrabass_2_Fingering_Voice"
                            {
                                \clef "bass_8"
                                s1
                            }
                        >>
                    >>
                >>
            >>
        >>

    ..  container:: example

        As a string quartet:

        >>> template = abjad.StringOrchestraScoreTemplate(
        ...     violin_count=2,
        ...     viola_count=1,
        ...     cello_count=1,
        ...     contrabass_count=0,
        ...     )
        >>> abjad.show(template) # doctest: +SKIP

        >>> string = abjad.lilypond(template.__illustrate__()[abjad.Score])
        >>> print(string)
        \context Score = "Score"
        <<
            \tag #'(Violin_1 Violin_2 Viola Cello)
            \context GlobalContext = "Global_Context"
            {
            }
            \context StaffGroup = "Outer_Staff_Group"
            <<
                \context ViolinStaffGroup = "Violin_Staff_Group"
                <<
                    \tag #'Violin_1
                    \context StringPerformerStaffGroup = "Violin_1_Staff_Group"
                    <<
                        \context BowingStaff = "Violin_1_Bowing_Staff"
                        <<
                            \context BowingVoice = "Violin_1_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Violin_1_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Violin_1_Fingering_Voice"
                            {
                                \clef "treble"
                                s1
                            }
                        >>
                    >>
                    \tag #'Violin_2
                    \context StringPerformerStaffGroup = "Violin_2_Staff_Group"
                    <<
                        \context BowingStaff = "Violin_2_Bowing_Staff"
                        <<
                            \context BowingVoice = "Violin_2_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Violin_2_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Violin_2_Fingering_Voice"
                            {
                                \clef "treble"
                                s1
                            }
                        >>
                    >>
                >>
                \context ViolaStaffGroup = "Viola_Staff_Group"
                <<
                    \tag #'Viola
                    \context StringPerformerStaffGroup = "Viola_Staff_Group"
                    <<
                        \context BowingStaff = "Viola_Bowing_Staff"
                        <<
                            \context BowingVoice = "Viola_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Viola_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Viola_Fingering_Voice"
                            {
                                \clef "alto"
                                s1
                            }
                        >>
                    >>
                >>
                \context CelloStaffGroup = "Cello_Staff_Group"
                <<
                    \tag #'Cello
                    \context StringPerformerStaffGroup = "Cello_Staff_Group"
                    <<
                        \context BowingStaff = "Cello_Bowing_Staff"
                        <<
                            \context BowingVoice = "Cello_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Cello_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Cello_Fingering_Voice"
                            {
                                \clef "bass"
                                s1
                            }
                        >>
                    >>
                >>
            >>
        >>

    ..  container:: example

        As a cello solo:

        >>> template = abjad.StringOrchestraScoreTemplate(
        ...     violin_count=0,
        ...     viola_count=0,
        ...     cello_count=1,
        ...     contrabass_count=0,
        ...     )
        >>> abjad.show(template) # doctest: +SKIP

        >>> string = abjad.lilypond(template.__illustrate__()[abjad.Score])
        >>> print(string)
        \context Score = "Score"
        <<
            \tag #'(Cello)
            \context GlobalContext = "Global_Context"
            {
            }
            \context StaffGroup = "Outer_Staff_Group"
            <<
                \context CelloStaffGroup = "Cello_Staff_Group"
                <<
                    \tag #'Cello
                    \context StringPerformerStaffGroup = "Cello_Staff_Group"
                    <<
                        \context BowingStaff = "Cello_Bowing_Staff"
                        <<
                            \context BowingVoice = "Cello_Bowing_Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Cello_Fingering_Staff"
                        <<
                            \context FingeringVoice = "Cello_Fingering_Voice"
                            {
                                \clef "bass"
                                s1
                            }
                        >>
                    >>
                >>
            >>
        >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_cello_count",
        "_contrabass_count",
        "_split_hands",
        "_use_percussion_clefs",
        "_viola_count",
        "_violin_count",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        violin_count=6,
        viola_count=4,
        cello_count=3,
        contrabass_count=2,
        split_hands=True,
        use_percussion_clefs=False,
    ):
        assert 0 <= violin_count
        assert 0 <= viola_count
        assert 0 <= cello_count
        assert 0 <= contrabass_count
        super().__init__()
        self._violin_count = int(violin_count)
        self._viola_count = int(viola_count)
        self._cello_count = int(cello_count)
        self._contrabass_count = int(contrabass_count)
        self._split_hands = bool(split_hands)
        self._use_percussion_clefs = bool(use_percussion_clefs)

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Calls string orchestra template.

        Returns score.
        """
        site = "abjad.StringOrchestraScoreTemplate.__call__()"
        tag = Tag(site)

        ### TAGS ###

        tag_names = []

        ### SCORE ###

        staff_group = StaffGroup(name="Outer_Staff_Group", tag=tag)

        score = Score([staff_group], name="Score", tag=tag)

        ### VIOLINS ###

        if self.violin_count:
            clef_name = "treble"
            if self.use_percussion_clefs:
                clef_name = "percussion"
            instrument = instruments.Violin()
            instrument_count = self.violin_count
            (
                instrument_staff_group,
                instrument_tag_names,
            ) = self._make_instrument_staff_group(
                clef_name=clef_name,
                count=instrument_count,
                instrument=instrument,
            )
            staff_group.append(instrument_staff_group)
            tag_names.extend(instrument_tag_names)

        ### VIOLAS ###

        if self.viola_count:
            clef_name = "alto"
            if self.use_percussion_clefs:
                clef_name = "percussion"
            instrument = instruments.Viola()
            instrument_count = self.viola_count
            (
                instrument_staff_group,
                instrument_tag_names,
            ) = self._make_instrument_staff_group(
                clef_name=clef_name,
                count=instrument_count,
                instrument=instrument,
            )
            staff_group.append(instrument_staff_group)
            tag_names.extend(instrument_tag_names)

        ### CELLOS ###

        if self.cello_count:
            clef_name = "bass"
            if self.use_percussion_clefs:
                clef_name = "percussion"
            instrument = instruments.Cello()
            instrument_count = self.cello_count
            (
                instrument_staff_group,
                instrument_tag_names,
            ) = self._make_instrument_staff_group(
                clef_name=clef_name,
                count=instrument_count,
                instrument=instrument,
            )
            staff_group.append(instrument_staff_group)
            tag_names.extend(instrument_tag_names)

        ### BASSES ###

        if self.contrabass_count:
            clef_name = "bass_8"
            if self.use_percussion_clefs:
                clef_name = "percussion"
            instrument = instruments.Contrabass()
            instrument_count = self.contrabass_count
            (
                instrument_staff_group,
                instrument_tag_names,
            ) = self._make_instrument_staff_group(
                clef_name=clef_name,
                count=instrument_count,
                instrument=instrument,
            )
            staff_group.append(instrument_staff_group)
            tag_names.extend(instrument_tag_names)

        ### TIME SIGNATURE CONTEXT ###

        global_context = Context(
            lilypond_type="GlobalContext", name="Global_Context", tag=tag
        )
        instrument_tags = " ".join(tag_names)
        tag_string = rf"\tag #'({instrument_tags})"
        literal = LilyPondLiteral(tag_string, "before")
        attach(literal, global_context, tag=tag)
        score.insert(0, global_context)
        return score

    ### PRIVATE METHODS ###

    def _make_instrument_staff_group(self, clef_name=None, count=None, instrument=None):
        site = "abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()"
        tag = Tag(site)
        name = instrument.name.title()
        instrument_staff_group = StaffGroup(
            lilypond_type=f"{name}StaffGroup",
            name=f"{name}_Staff_Group",
            tag=tag,
        )
        tag_names = []
        if count == 1:
            performer_staff_group, tag_name = self._make_performer_staff_group(
                clef_name=clef_name, instrument=instrument, number=None
            )
            instrument_staff_group.append(performer_staff_group)
            tag_names.append(tag_name)
        else:
            for i in range(1, count + 1):
                performer_staff_group, tag_name = self._make_performer_staff_group(
                    clef_name=clef_name, instrument=instrument, number=i
                )
                instrument_staff_group.append(performer_staff_group)
                tag_names.append(tag_name)
        return instrument_staff_group, tag_names

    def _make_performer_staff_group(self, clef_name=None, instrument=None, number=None):
        site = "StringOrchestraScoreTemplate._make_performer_staff_group()"
        tag = Tag(site)
        if number is not None:
            name = f"{instrument.name.title()}_{number}"
        else:
            name = instrument.name.title()
        pitch_range = instrument.pitch_range
        staff_group = StaffGroup(
            lilypond_type="StringPerformerStaffGroup",
            name=f"{name}_Staff_Group",
            tag=tag,
        )
        tag_name = name.replace(" ", "")
        tag_string = rf"\tag #'{tag_name}"
        tag_command = LilyPondLiteral(tag_string, "before")
        attach(tag_command, staff_group, tag=tag)
        if self.split_hands:
            lh_voice = Voice(
                [],
                lilypond_type="FingeringVoice",
                name=f"{name}_Fingering_Voice",
                tag=tag,
            )
            abbreviation = lh_voice.name.lower().replace(" ", "_")
            self.voice_abbreviations[abbreviation] = lh_voice.name
            lh_staff = Staff(
                [lh_voice],
                lilypond_type="FingeringStaff",
                name=f"{name}_Fingering_Staff",
                tag=tag,
            )
            lh_staff.simultaneous = True
            annotate(lh_staff, "pitch_range", pitch_range)
            annotate(lh_staff, "default_clef", Clef(clef_name))
            rh_voice = Voice(
                [],
                lilypond_type="BowingVoice",
                name=f"{name}_Bowing_Voice",
                tag=tag,
            )
            abbreviation = rh_voice.name.lower().replace(" ", "_")
            self.voice_abbreviations[abbreviation] = rh_voice.name
            rh_staff = Staff(
                [rh_voice],
                lilypond_type="BowingStaff",
                name=f"{name}_Bowing_Staff",
                tag=tag,
            )
            rh_staff.simultaneous = True
            staff_group.extend([rh_staff, lh_staff])
        else:
            lh_voice = Voice(
                [],
                lilypond_type="FingeringVoice",
                name=f"{name}_Voice",
                tag=tag,
            )
            lh_staff = Staff(
                [lh_voice],
                lilypond_type="FingeringStaff",
                name=f"{name}_Staff",
                tag=tag,
            )
            lh_staff.simultaneous = True
            annotate(lh_staff, "pitch_range", pitch_range)
            annotate(lh_staff, "default_clef", Clef(clef_name))
            staff_group.append(lh_staff)
        return staff_group, tag_name

    ### PUBLIC PROPERTIES ###

    @property
    def cello_count(self):
        """
        Number of cellos in string orchestra.

        Returns nonnegative integer.
        """
        return self._cello_count

    @property
    def contrabass_count(self):
        """
        Number of contrabasses in string orchestra.

        Returns nonnegative integer.
        """
        return self._contrabass_count

    @property
    def split_hands(self):
        """
        Is true if each performer's hand receives a separate staff.
        """
        return self._split_hands

    @property
    def use_percussion_clefs(self):
        """
        Is true if each staff should use a percussion clef rather than the
        normal clef for that instrument.
        """
        return self._use_percussion_clefs

    @property
    def viola_count(self):
        """
        Number of violas in string orcestra.

        Returns nonnegative integer.
        """
        return self._viola_count

    @property
    def violin_count(self):
        """
        Number of violins in string orchestra.

        Returns nonnegative integer.
        """
        return self._violin_count


class StringQuartetScoreTemplate(ScoreTemplate):
    r"""
    String quartet score template.

    ..  container:: example

        >>> template = abjad.StringQuartetScoreTemplate()
        >>> abjad.show(template) # doctest: +SKIP

        >>> string = abjad.lilypond(template.__illustrate__()[abjad.Score])
        >>> print(string)
        \context Score = "String_Quartet_Score"
        <<
            \context StaffGroup = "String_Quartet_Staff_Group"
            <<
                \tag #'first-violin
                \context Staff = "First_Violin_Staff"
                {
                    \context Voice = "First_Violin_Voice"
                    {
                        \clef "treble"
                        s1
                    }
                }
                \tag #'second-violin
                \context Staff = "Second_Violin_Staff"
                {
                    \context Voice = "Second_Violin_Voice"
                    {
                        \clef "treble"
                        s1
                    }
                }
                \tag #'viola
                \context Staff = "Viola_Staff"
                {
                    \context Voice = "Viola_Voice"
                    {
                        \clef "alto"
                        s1
                    }
                }
                \tag #'cello
                \context Staff = "Cello_Staff"
                {
                    \context Voice = "Cello_Voice"
                    {
                        \clef "bass"
                        s1
                    }
                }
            >>
        >>

    Returns score template.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        super().__init__()
        self.voice_abbreviations.update(
            {
                "vn1": "First Violin Voice",
                "vn2": "Second Violin Voice",
                "va": "Viola Voice",
                "vc": "Cello Voice",
            }
        )

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Calls string quartet score template.

        Returns score.
        """
        site = "abjad.StringQuartetScoreTemplate.__call__()"
        tag = Tag(site)

        # make first violin voice and staff
        first_violin_voice = Voice([], name="First_Violin_Voice", tag=tag)
        first_violin_staff = Staff(
            [first_violin_voice], name="First_Violin_Staff", tag=tag
        )
        clef = Clef("treble")
        annotate(first_violin_staff, "default_clef", clef)
        violin = instruments.Violin()
        annotate(first_violin_staff, "default_instrument", violin)
        literal = LilyPondLiteral(r"\tag #'first-violin", "before")
        attach(literal, first_violin_staff)

        # make second violin voice and staff
        second_violin_voice = Voice([], name="Second_Violin_Voice", tag=tag)
        second_violin_staff = Staff(
            [second_violin_voice], name="Second_Violin_Staff", tag=tag
        )
        clef = Clef("treble")
        annotate(second_violin_staff, "default_clef", clef)
        violin = instruments.Violin()
        annotate(second_violin_staff, "default_instrument", violin)
        literal = LilyPondLiteral(r"\tag #'second-violin", "before")
        attach(literal, second_violin_staff)

        # make viola voice and staff
        viola_voice = Voice([], name="Viola_Voice", tag=tag)
        viola_staff = Staff([viola_voice], name="Viola_Staff", tag=tag)
        clef = Clef("alto")
        annotate(viola_staff, "default_clef", clef)
        viola = instruments.Viola()
        annotate(viola_staff, "default_instrument", viola)
        literal = LilyPondLiteral(r"\tag #'viola", "before")
        attach(literal, viola_staff)

        # make cello voice and staff
        cello_voice = Voice([], name="Cello_Voice", tag=tag)
        cello_staff = Staff([cello_voice], name="Cello_Staff", tag=tag)
        clef = Clef("bass")
        annotate(cello_staff, "default_clef", clef)
        cello = instruments.Cello()
        annotate(cello_staff, "default_instrument", cello)
        literal = LilyPondLiteral(r"\tag #'cello", "before")
        attach(literal, cello_staff)

        # make string quartet staff group
        string_quartet_staff_group = StaffGroup(
            [first_violin_staff, second_violin_staff, viola_staff, cello_staff],
            name="String_Quartet_Staff_Group",
            tag=tag,
        )

        # make string quartet score
        string_quartet_score = Score(
            [string_quartet_staff_group],
            name="String_Quartet_Score",
            tag=tag,
        )

        # return string quartet score
        return string_quartet_score


class TwoStaffPianoScoreTemplate(ScoreTemplate):
    r"""
    Two-staff piano score template.

    ..  container:: example

        >>> template = abjad.TwoStaffPianoScoreTemplate()
        >>> abjad.show(template) # doctest: +SKIP

        >>> string = abjad.lilypond(template.__illustrate__()[abjad.Score])
        >>> print(string)
        \context Score = "Two_Staff_Piano_Score"
        <<
            \context GlobalContext = "Global_Context"
            <<
                \context GlobalRests = "Global_Rests"
                {
                }
                \context GlobalSkips = "Global_Skips"
                {
                }
            >>
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "RH_Staff"
                {
                    \context Voice = "RH_Voice"
                    {
                        s1
                    }
                }
                \context Staff = "LH_Staff"
                {
                    \context Voice = "LH_Voice"
                    {
                        \clef "bass"
                        s1
                    }
                }
            >>
        >>

    Returns score template.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        super().__init__()
        self.voice_abbreviations.update({"rh": "RHVoice", "lh": "LHVoice"})

    ### SPECIAL METHODS ###

    def __call__(self) -> Score:
        r"""
        Calls two-staff piano score template.

        ..  container:: example

            REGRESSION. Attaches piano to piano group (rather than just staff):

            >>> template = abjad.TwoStaffPianoScoreTemplate()
            >>> score = template()
            >>> piano_staff = score['Piano_Staff']
            >>> rh_voice = score['RH_Voice']
            >>> lh_voice = score['LH_Voice']

            >>> rh_voice.append("g'4")
            >>> lh_voice.append("c4")

            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Two_Staff_Piano_Score"
                <<
                    \context GlobalContext = "Global_Context"
                    <<
                        \context GlobalRests = "Global_Rests"
                        {
                        }
                        \context GlobalSkips = "Global_Skips"
                        {
                        }
                    >>
                    \context PianoStaff = "Piano_Staff"
                    <<
                        \context Staff = "RH_Staff"
                        {
                            \context Voice = "RH_Voice"
                            {
                                g'4
                            }
                        }
                        \context Staff = "LH_Staff"
                        {
                            \context Voice = "LH_Voice"
                            {
                                c4
                            }
                        }
                    >>
                >>

        """
        site = "abjad.TwoStaffPianoScoreTemplate.__call__()"
        tag = Tag(site)
        # GLOBAL CONTEXT
        global_context = self._make_global_context()

        # RH STAFF
        rh_voice = Voice(name="RH_Voice", tag=tag)
        rh_staff = Staff([rh_voice], name="RH_Staff", tag=tag)

        # LH STAFF
        lh_voice = Voice(name="LH_Voice", tag=tag)
        lh_staff = Staff([lh_voice], name="LH_Staff", tag=tag)
        annotate(lh_staff, "default_clef", Clef("bass"))

        # PIANO STAFF
        staff_group = StaffGroup(
            [rh_staff, lh_staff],
            lilypond_type="PianoStaff",
            name="Piano_Staff",
            tag=tag,
        )
        annotate(staff_group, "default_instrument", Piano())

        # SCORE
        score = Score(
            [global_context, staff_group],
            name="Two_Staff_Piano_Score",
            tag=tag,
        )
        return score
