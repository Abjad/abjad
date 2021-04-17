from quicktions import Fraction

from . import (
    deprecated,
    enumerate,
    get,
    illustrators,
    io,
    iterpitches,
    lyconst,
    lyenv,
    makers,
    mutate,
    persist,
    wf,
)
from ._version import __version__, __version_info__
from .attach import Wrapper, annotate, attach, detach
from .bundle import LilyPondFormatBundle, SlotContributions
from .configuration import (
    Configuration,
    list_all_classes,
    list_all_functions,
    yield_all_modules,
)
from .contextmanagers import (
    ContextManager,
    FilesystemState,
    ForbidUpdate,
    NullContextManager,
    ProgressIndicator,
    RedirectedStreams,
    TemporaryDirectory,
    TemporaryDirectoryChange,
    Timer,
)
from .cyclictuple import CyclicTuple
from .duration import Duration, Multiplier, NonreducedFraction, Offset
from .enums import (
    Center,
    Comparison,
    Down,
    Exact,
    HorizontalAlignment,
    Left,
    Less,
    Middle,
    More,
    Right,
    Up,
    VerticalAlignment,
)
from .exceptions import (
    AssignabilityError,
    ImpreciseMetronomeMarkError,
    LilyPondParserError,
    MissingMetronomeMarkError,
    ParentageError,
    PersistentIndicatorError,
    SchemeParserFinishedError,
    UnboundedTimeIntervalError,
    WellformednessError,
)
from .expression import Expression
from .format import LilyPondFormatManager
from .get import Descendants, Lineage
from .illustrators import illustrate
from .indicators.Arpeggio import Arpeggio
from .indicators.Articulation import Articulation
from .indicators.BarLine import BarLine
from .indicators.BeamCount import BeamCount
from .indicators.BendAfter import BendAfter
from .indicators.BowContactPoint import BowContactPoint
from .indicators.BowMotionTechnique import BowMotionTechnique
from .indicators.BowPressure import BowPressure
from .indicators.BreathMark import BreathMark
from .indicators.Clef import Clef, StaffPosition
from .indicators.ColorFingering import ColorFingering
from .indicators.Dynamic import Dynamic
from .indicators.Fermata import Fermata
from .indicators.Glissando import Glissando
from .indicators.KeyCluster import KeyCluster
from .indicators.KeySignature import KeySignature
from .indicators.LaissezVibrer import LaissezVibrer
from .indicators.LilyPondComment import LilyPondComment
from .indicators.MarginMarkup import MarginMarkup
from .indicators.MetronomeMark import MetronomeMark
from .indicators.Mode import Mode
from .indicators.Ottava import Ottava
from .indicators.RehearsalMark import RehearsalMark
from .indicators.Repeat import Repeat
from .indicators.RepeatTie import RepeatTie
from .indicators.StaffChange import StaffChange
from .indicators.StartBeam import StartBeam
from .indicators.StartGroup import StartGroup
from .indicators.StartHairpin import StartHairpin
from .indicators.StartMarkup import StartMarkup
from .indicators.StartPhrasingSlur import StartPhrasingSlur
from .indicators.StartPianoPedal import StartPianoPedal
from .indicators.StartSlur import StartSlur
from .indicators.StartTextSpan import StartTextSpan
from .indicators.StartTrillSpan import StartTrillSpan
from .indicators.StemTremolo import StemTremolo
from .indicators.StopBeam import StopBeam
from .indicators.StopGroup import StopGroup
from .indicators.StopHairpin import StopHairpin
from .indicators.StopPhrasingSlur import StopPhrasingSlur
from .indicators.StopPianoPedal import StopPianoPedal
from .indicators.StopSlur import StopSlur
from .indicators.StopTextSpan import StopTextSpan
from .indicators.StopTrillSpan import StopTrillSpan
from .indicators.StringContactPoint import StringContactPoint
from .indicators.Tie import Tie
from .indicators.TimeSignature import TimeSignature
from .instruments import (
    Accordion,
    AltoFlute,
    AltoSaxophone,
    AltoTrombone,
    AltoVoice,
    BaritoneSaxophone,
    BaritoneVoice,
    BassClarinet,
    BassFlute,
    BassSaxophone,
    BassTrombone,
    BassVoice,
    Bassoon,
    Cello,
    ClarinetInA,
    ClarinetInBFlat,
    ClarinetInEFlat,
    Contrabass,
    ContrabassClarinet,
    ContrabassFlute,
    ContrabassSaxophone,
    Contrabassoon,
    EnglishHorn,
    Flute,
    FrenchHorn,
    Glockenspiel,
    Guitar,
    Harp,
    Harpsichord,
    Instrument,
    Marimba,
    MezzoSopranoVoice,
    Oboe,
    Percussion,
    Piano,
    Piccolo,
    SopraninoSaxophone,
    SopranoSaxophone,
    SopranoVoice,
    StringNumber,
    TenorSaxophone,
    TenorTrombone,
    TenorVoice,
    Trumpet,
    Tuba,
    Tuning,
    Vibraphone,
    Viola,
    Violin,
    Xylophone,
)
from .io import graph, play, show
from .iterate import Iteration, iterate
from .label import ColorMap, Label
from .lilypond import lilypond
from .lilypondfile import (
    Block,
    ContextBlock,
    DateTimeToken,
    LilyPondDimension,
    LilyPondFile,
    LilyPondLanguageToken,
    LilyPondVersionToken,
    PackageGitCommitToken,
)
from .lyproxy import (
    LilyPondContext,
    LilyPondEngraver,
    LilyPondGrob,
    LilyPondGrobInterface,
)
from .makers import LeafMaker, NoteMaker
from .markups import Markup, Postscript, PostscriptOperator
from .math import Infinity, NegativeInfinity
from .meter import Meter, MeterList, MetricAccentKernel, OffsetCounter
from .metricmodulation import MetricModulation
from .new import new
from .obgc import OnBeatGraceContainer, on_beat_grace_container
from .ordereddict import OrderedDict
from .overrides import (
    IndexedTweakManager,
    IndexedTweakManagers,
    Interface,
    LilyPondLiteral,
    LilyPondOverride,
    LilyPondSetting,
    OverrideInterface,
    SettingInterface,
    TweakInterface,
    override,
    setting,
    tweak,
)
from .parentage import Parentage
from .parsers import parser
from .parsers.base import Parser
from .parsers.parse import parse
from .pattern import Pattern, PatternTuple
from .pitch.Accidental import Accidental
from .pitch.Octave import Octave
from .pitch.PitchRange import PitchRange
from .pitch.SetClass import SetClass
from .pitch.intervalclasses import (
    IntervalClass,
    NamedIntervalClass,
    NamedInversionEquivalentIntervalClass,
    NumberedIntervalClass,
    NumberedInversionEquivalentIntervalClass,
)
from .pitch.intervals import Interval, NamedInterval, NumberedInterval
from .pitch.operators import (
    CompoundOperator,
    Duplication,
    Inversion,
    Multiplication,
    Retrograde,
    Rotation,
    Transposition,
)
from .pitch.pitchclasses import NamedPitchClass, NumberedPitchClass, PitchClass
from .pitch.pitches import NamedPitch, NumberedPitch, Pitch, PitchTyping
from .pitch.segments import (
    IntervalClassSegment,
    IntervalSegment,
    PitchClassSegment,
    PitchSegment,
    Segment,
    TwelveToneRow,
)
from .pitch.sets import IntervalClassSet, IntervalSet, PitchClassSet, PitchSet, Set
from .pitch.vectors import (
    IntervalClassVector,
    IntervalVector,
    PitchClassVector,
    PitchVector,
    Vector,
)
from .ratio import NonreducedRatio, Ratio
from .score import (
    AfterGraceContainer,
    BeforeGraceContainer,
    Chord,
    Cluster,
    Component,
    Container,
    Context,
    DrumNoteHead,
    Leaf,
    MultimeasureRest,
    Note,
    NoteHead,
    NoteHeadList,
    Rest,
    Score,
    Skip,
    Staff,
    StaffGroup,
    TremoloContainer,
    Tuplet,
    Voice,
)
from .segmentmaker import SegmentMaker
from .select import (
    DurationInequality,
    Inequality,
    LengthInequality,
    LogicalTie,
    PitchInequality,
    Selection,
    select,
)
from .sequence import Sequence
from .spanners import (
    beam,
    bow_contact_spanner,
    glissando,
    hairpin,
    horizontal_bracket,
    ottava,
    phrasing_slur,
    piano_pedal,
    slur,
    text_spanner,
    tie,
    trill_spanner,
)
from .storage import (
    FormatSpecification,
    StorageFormatManager,
    StorageFormatSpecification,
    storage,
)
from .string import String
from .tag import Line, Tag, activate, deactivate
from .templates import (
    GroupedRhythmicStavesScoreTemplate,
    GroupedStavesScoreTemplate,
    ScoreTemplate,
    StringOrchestraScoreTemplate,
    StringQuartetScoreTemplate,
    TwoStaffPianoScoreTemplate,
)
from .timespan import AnnotatedTimespan, Timespan, TimespanList
from .typedcollections import (
    TypedCollection,
    TypedCounter,
    TypedFrozenset,
    TypedList,
    TypedTuple,
)
from .typings import (
    DurationSequenceTyping,
    DurationTyping,
    IntegerPair,
    IntegerSequence,
    Number,
    NumberPair,
    PatternTyping,
    Prototype,
    RatioSequenceTyping,
    RatioTyping,
    Strings,
)
from .verticalmoment import (
    VerticalMoment,
    iterate_leaf_pairs,
    iterate_pitch_pairs,
    iterate_vertical_moments,
)

index = Pattern.index
index_all = Pattern.index_all
index_first = Pattern.index_first
index_last = Pattern.index_last


__all__ = [
    "Accidental",
    "Accordion",
    "AfterGraceContainer",
    "AltoFlute",
    "AltoSaxophone",
    "AltoTrombone",
    "AltoVoice",
    "AnnotatedTimespan",
    "Arpeggio",
    "Articulation",
    "AssignabilityError",
    "BarLine",
    "BaritoneSaxophone",
    "BaritoneVoice",
    "BassClarinet",
    "BassFlute",
    "BassSaxophone",
    "BassTrombone",
    "BassVoice",
    "Bassoon",
    "BeamCount",
    "BeforeGraceContainer",
    "BendAfter",
    "Block",
    "BowContactPoint",
    "BowMotionTechnique",
    "BowPressure",
    "BreathMark",
    "Cello",
    "Center",
    "Chord",
    "ClarinetInA",
    "ClarinetInBFlat",
    "ClarinetInEFlat",
    "Clef",
    "Cluster",
    "ColorFingering",
    "ColorMap",
    "Comparison",
    "Component",
    "CompoundOperator",
    "Configuration",
    "Container",
    "Context",
    "ContextBlock",
    "ContextManager",
    "Contrabass",
    "ContrabassClarinet",
    "ContrabassFlute",
    "ContrabassSaxophone",
    "Contrabassoon",
    "CyclicTuple",
    "DateTimeToken",
    "Descendants",
    "Down",
    "DrumNoteHead",
    "Duplication",
    "Duration",
    "DurationInequality",
    "DurationSequenceTyping",
    "DurationTyping",
    "Dynamic",
    "EnglishHorn",
    "Exact",
    "Expression",
    "Fermata",
    "FilesystemState",
    "Flute",
    "ForbidUpdate",
    "FormatSpecification",
    "Fraction",
    "FrenchHorn",
    "Glissando",
    "Glockenspiel",
    "GroupedRhythmicStavesScoreTemplate",
    "GroupedStavesScoreTemplate",
    "Guitar",
    "Harp",
    "Harpsichord",
    "HorizontalAlignment",
    "ImpreciseMetronomeMarkError",
    "IndexedTweakManager",
    "IndexedTweakManagers",
    "Inequality",
    "Infinity",
    "Instrument",
    "IntegerPair",
    "IntegerSequence",
    "Interface",
    "Interval",
    "IntervalClass",
    "IntervalClassSegment",
    "IntervalClassSet",
    "IntervalClassVector",
    "IntervalSegment",
    "IntervalSet",
    "IntervalVector",
    "Inversion",
    "Iteration",
    "KeyCluster",
    "KeySignature",
    "Label",
    "LaissezVibrer",
    "Leaf",
    "LeafMaker",
    "Left",
    "LengthInequality",
    "Less",
    "LilyPondComment",
    "LilyPondContext",
    "LilyPondDimension",
    "LilyPondEngraver",
    "LilyPondFile",
    "LilyPondFormatBundle",
    "LilyPondFormatManager",
    "LilyPondGrob",
    "LilyPondGrobInterface",
    "LilyPondLanguageToken",
    "LilyPondLiteral",
    "LilyPondOverride",
    "LilyPondParserError",
    "LilyPondSetting",
    "LilyPondVersionToken",
    "Line",
    "Lineage",
    "LogicalTie",
    "MarginMarkup",
    "Marimba",
    "Markup",
    "Meter",
    "MeterList",
    "MetricAccentKernel",
    "MetricModulation",
    "MetronomeMark",
    "MezzoSopranoVoice",
    "Middle",
    "MissingMetronomeMarkError",
    "Mode",
    "More",
    "MultimeasureRest",
    "Multiplication",
    "Multiplier",
    "NamedInterval",
    "NamedIntervalClass",
    "NamedInversionEquivalentIntervalClass",
    "NamedPitch",
    "NamedPitchClass",
    "NegativeInfinity",
    "NonreducedFraction",
    "NonreducedRatio",
    "Note",
    "NoteHead",
    "NoteHeadList",
    "NoteMaker",
    "NullContextManager",
    "Number",
    "NumberPair",
    "NumberedInterval",
    "NumberedIntervalClass",
    "NumberedInversionEquivalentIntervalClass",
    "NumberedPitch",
    "NumberedPitchClass",
    "Oboe",
    "Octave",
    "Offset",
    "OffsetCounter",
    "OnBeatGraceContainer",
    "OrderedDict",
    "Ottava",
    "OverrideInterface",
    "PackageGitCommitToken",
    "Parentage",
    "ParentageError",
    "Parser",
    "Pattern",
    "PatternTuple",
    "PatternTyping",
    "Percussion",
    "PersistentIndicatorError",
    "Piano",
    "Piccolo",
    "Pitch",
    "PitchClass",
    "PitchClassSegment",
    "PitchClassSet",
    "PitchClassVector",
    "PitchInequality",
    "PitchRange",
    "PitchSegment",
    "PitchSet",
    "PitchTyping",
    "PitchVector",
    "Postscript",
    "PostscriptOperator",
    "ProgressIndicator",
    "Prototype",
    "Ratio",
    "RatioSequenceTyping",
    "RatioTyping",
    "RedirectedStreams",
    "RehearsalMark",
    "Repeat",
    "RepeatTie",
    "Rest",
    "Retrograde",
    "Right",
    "Rotation",
    "SchemeParserFinishedError",
    "Score",
    "ScoreTemplate",
    "Segment",
    "SegmentMaker",
    "Selection",
    "Sequence",
    "Set",
    "SetClass",
    "SettingInterface",
    "Skip",
    "SlotContributions",
    "SopraninoSaxophone",
    "SopranoSaxophone",
    "SopranoVoice",
    "Staff",
    "StaffChange",
    "StaffGroup",
    "StaffPosition",
    "StartBeam",
    "StartGroup",
    "StartHairpin",
    "StartMarkup",
    "StartPhrasingSlur",
    "StartPianoPedal",
    "StartSlur",
    "StartTextSpan",
    "StartTrillSpan",
    "StemTremolo",
    "StopBeam",
    "StopGroup",
    "StopHairpin",
    "StopPhrasingSlur",
    "StopPianoPedal",
    "StopSlur",
    "StopTextSpan",
    "StopTrillSpan",
    "StorageFormatManager",
    "StorageFormatSpecification",
    "String",
    "StringContactPoint",
    "StringNumber",
    "StringOrchestraScoreTemplate",
    "StringQuartetScoreTemplate",
    "Strings",
    "Tag",
    "TemporaryDirectory",
    "TemporaryDirectoryChange",
    "TenorSaxophone",
    "TenorTrombone",
    "TenorVoice",
    "Tie",
    "TimeSignature",
    "Timer",
    "Timespan",
    "TimespanList",
    "Transposition",
    "TremoloContainer",
    "Trumpet",
    "Tuba",
    "Tuning",
    "Tuplet",
    "TweakInterface",
    "TwelveToneRow",
    "TwoStaffPianoScoreTemplate",
    "TypedCollection",
    "TypedCounter",
    "TypedFrozenset",
    "TypedList",
    "TypedTuple",
    "UnboundedTimeIntervalError",
    "Up",
    "Vector",
    "VerticalAlignment",
    "VerticalMoment",
    "Vibraphone",
    "Viola",
    "Violin",
    "Voice",
    "WellformednessError",
    "Wrapper",
    "Xylophone",
    "__version__",
    "__version_info__",
    "activate",
    "annotate",
    "attach",
    "beam",
    "bow_contact_spanner",
    "deactivate",
    "deprecated",
    "detach",
    "enumerate",
    "glissando",
    "graph",
    "hairpin",
    "horizontal_bracket",
    "illustrate",
    "illustrators",
    "index",
    "index_all",
    "index_first",
    "index_last",
    "get",
    "io",
    "iterate",
    "iterate_leaf_pairs",
    "iterate_pitch_pairs",
    "iterate_vertical_moments",
    "iterpitches",
    "lilypond",
    "list_all_classes",
    "list_all_functions",
    "lyconst",
    "lyenv",
    "makers",
    "mutate",
    "new",
    "on_beat_grace_container",
    "ottava",
    "override",
    "parse",
    "parser",
    "persist",
    "phrasing_slur",
    "piano_pedal",
    "pitch_class_segment",
    "play",
    "select",
    "setting",
    "show",
    "slur",
    "storage",
    "text_spanner",
    "tie",
    "trill_spanner",
    "tweak",
    "wf",
    "yield_all_modules",
]
