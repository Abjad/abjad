from fractions import Fraction

from . import (
    _updatelib,
    configuration,
    contextmanagers,
    deprecated,
    enumerate,
    format,
    get,
    illustrators,
    io,
    iterate,
    iterpitches,
    lyconst,
    lyenv,
    makers,
    mutate,
    persist,
    string,
    wf,
    wrapper,
)
from ._version import __version__
from .bind import annotate, attach, detach
from .cyclictuple import CyclicTuple
from .duration import Duration, Offset, Ratio, durations
from .enums import (
    CENTER,
    DOWN,
    EXACT,
    LEFT,
    LESS,
    MIDDLE,
    MORE,
    RIGHT,
    UP,
    Comparison,
    Horizontal,
    Vertical,
)
from .exceptions import (
    AssignabilityError,
    ImpreciseMetronomeMarkError,
    LilyPondParserError,
    MissingContextError,
    MissingMetronomeMarkError,
    ParentageError,
    PersistentIndicatorError,
    SchemeParserFinishedError,
    UnboundedTimeIntervalError,
    WellformednessError,
)
from .get import Lineage
from .illustrators import illustrate, lilypond
from .indicators import (
    Arpeggio,
    Articulation,
    BarLine,
    BeamCount,
    BendAfter,
    BreathMark,
    Clef,
    ColorFingering,
    Dynamic,
    Fermata,
    Glissando,
    InstrumentName,
    KeyCluster,
    KeySignature,
    LaissezVibrer,
    LilyPondLiteral,
    Markup,
    MetronomeMark,
    Mode,
    Ottava,
    RehearsalMark,
    Repeat,
    RepeatTie,
    ShortInstrumentName,
    StaffChange,
    StartBeam,
    StartGroup,
    StartHairpin,
    StartPhrasingSlur,
    StartPianoPedal,
    StartSlur,
    StartTextSpan,
    StartTrillSpan,
    StemTremolo,
    StopBeam,
    StopGroup,
    StopHairpin,
    StopPhrasingSlur,
    StopPianoPedal,
    StopSlur,
    StopTextSpan,
    StopTrillSpan,
    TextMark,
    Tie,
    TimeSignature,
    VoiceNumber,
)
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
from .io import graph, show
from .label import ColorMap
from .lilypondfile import Block, LilyPondFile
from .lyproxy import (
    LilyPondContext,
    LilyPondEngraver,
    LilyPondGrob,
    LilyPondGrobInterface,
)
from .math import Infinity, NegativeInfinity
from .meter import Meter, MetricAccentKernel
from .metricmodulation import MetricModulation
from .obgc import OnBeatGraceContainer, on_beat_grace_container
from .overrides import (
    Interface,
    LilyPondOverride,
    LilyPondSetting,
    OverrideInterface,
    SettingInterface,
    override,
    setting,
)
from .parentage import Parentage
from .parsers import parser
from .parsers.base import Parser
from .parsers.parse import parse
from .pattern import Pattern, PatternTuple
from .pcollections import (
    PitchClassSegment,
    PitchClassSet,
    PitchRange,
    PitchSegment,
    PitchSet,
    TwelveToneRow,
)
from .pitch import (
    Accidental,
    Interval,
    IntervalClass,
    NamedInterval,
    NamedIntervalClass,
    NamedInversionEquivalentIntervalClass,
    NamedPitch,
    NamedPitchClass,
    NumberedInterval,
    NumberedIntervalClass,
    NumberedInversionEquivalentIntervalClass,
    NumberedPitch,
    NumberedPitchClass,
    Octave,
    Pitch,
    PitchClass,
    StaffPosition,
)
from .score import (
    AfterGraceContainer,
    BeforeGraceContainer,
    Chord,
    Cluster,
    Component,
    Container,
    Context,
    DrumNoteHead,
    IndependentAfterGraceContainer,
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
from .select import LogicalTie
from .setclass import SetClass
from .spanners import (
    beam,
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
from .tag import Tag, activate, deactivate
from .timespan import OffsetCounter, Timespan, TimespanList
from .tweaks import Bundle, Tweak, bundle, tweak
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
    "BreathMark",
    "Bundle",
    "Cello",
    "CENTER",
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
    "Container",
    "Context",
    "Contrabass",
    "ContrabassClarinet",
    "ContrabassFlute",
    "ContrabassSaxophone",
    "Contrabassoon",
    "CyclicTuple",
    "DOWN",
    "DrumNoteHead",
    "Duration",
    "Dynamic",
    "EnglishHorn",
    "EXACT",
    "Expression",
    "Fermata",
    "Flute",
    "Fraction",
    "FrenchHorn",
    "Glissando",
    "Glockenspiel",
    "Guitar",
    "Harp",
    "Harpsichord",
    "Horizontal",
    "ImpreciseMetronomeMarkError",
    "IndependentAfterGraceContainer",
    "Infinity",
    "Instrument",
    "InstrumentName",
    "IntegerPair",
    "Interface",
    "Interval",
    "IntervalClass",
    "KeyCluster",
    "KeySignature",
    "LaissezVibrer",
    "Leaf",
    "LEFT",
    "LESS",
    "LilyPondContext",
    "LilyPondEngraver",
    "LilyPondFile",
    "LilyPondGrob",
    "LilyPondGrobInterface",
    "LilyPondLiteral",
    "LilyPondOverride",
    "LilyPondParserError",
    "LilyPondSetting",
    "Lineage",
    "LogicalTie",
    "Marimba",
    "Markup",
    "Meter",
    "MetricAccentKernel",
    "MetricModulation",
    "MetronomeMark",
    "MezzoSopranoVoice",
    "MIDDLE",
    "MissingContextError",
    "MissingMetronomeMarkError",
    "Mode",
    "MORE",
    "MultimeasureRest",
    "NamedInterval",
    "NamedIntervalClass",
    "NamedInversionEquivalentIntervalClass",
    "NamedPitch",
    "NamedPitchClass",
    "NegativeInfinity",
    "Note",
    "NoteHead",
    "NoteHeadList",
    "Number",
    "NumberPair",
    "NumberedInterval",
    "NumberedIntervalClass",
    "NumberedInversionEquivalentIntervalClass",
    "NumberedPitch",
    "NumberedPitchClass",
    "PitchClassSegment",
    "PitchClassSet",
    "PitchSegment",
    "PitchSet",
    "Oboe",
    "Octave",
    "Offset",
    "OffsetCounter",
    "OnBeatGraceContainer",
    "Ottava",
    "OverrideInterface",
    "Parentage",
    "ParentageError",
    "Parser",
    "Pattern",
    "PatternTuple",
    "Percussion",
    "PersistentIndicatorError",
    "Piano",
    "Piccolo",
    "Pitch",
    "PitchClass",
    "PitchRange",
    "Ratio",
    "RehearsalMark",
    "Repeat",
    "RepeatTie",
    "Rest",
    "RIGHT",
    "SchemeParserFinishedError",
    "Score",
    "SetClass",
    "SettingInterface",
    "ShortInstrumentName",
    "Skip",
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
    "StringNumber",
    "Tag",
    "TenorSaxophone",
    "TenorTrombone",
    "TenorVoice",
    "TextMark",
    "Tie",
    "TimeSignature",
    "Timespan",
    "TimespanList",
    "TremoloContainer",
    "Trumpet",
    "Tuba",
    "Tuning",
    "Tuplet",
    "Tweak",
    "TwelveToneRow",
    "UnboundedTimeIntervalError",
    "UP",
    "Vertical",
    "VerticalMoment",
    "Vibraphone",
    "Viola",
    "Violin",
    "Voice",
    "VoiceNumber",
    "WellformednessError",
    "Wrapper",
    "Xylophone",
    "__version__",
    "__version_info__",
    "_updatelib",
    "activate",
    "annotate",
    "attach",
    "beam",
    "bundle",
    "configuration",
    "contextmanagers",
    "deactivate",
    "deprecated",
    "detach",
    "durations",
    "enumerate",
    "format",
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
    "label",
    "lilypond",
    "lyconst",
    "lyenv",
    "makers",
    "mutate",
    "on_beat_grace_container",
    "ottava",
    "override",
    "parse",
    "parser",
    "persist",
    "phrasing_slur",
    "piano_pedal",
    "select",
    "setting",
    "show",
    "slur",
    "string",
    "text_spanner",
    "tie",
    "trill_spanner",
    "tweak",
    "wf",
    "wrapper",
]
