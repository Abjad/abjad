from ._version import __version_info__, __version__

try:
    from quicktions import Fraction
except ImportError:
    from fractions import Fraction

from .enums import (
    Comparison,
    HorizontalAlignment,
    VerticalAlignment,
    Both,
    Center,
    Down,
    Exact,
    Left,
    Less,
    More,
    Right,
    Up,
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

from .parsers import parser
from .formatting import (
    FormatSpecification,
    StorageFormatSpecification,
    StorageFormatManager,
)
from .system.Configuration import Configuration
from .system.ContextManager import ContextManager
from .system.FilesystemState import FilesystemState
from .system.ForbidUpdate import ForbidUpdate
from .system.IOManager import IOManager
from .system.LilyPondFormatBundle import LilyPondFormatBundle
from .system.LilyPondFormatManager import LilyPondFormatManager
from .system.NullContextManager import NullContextManager
from .system.Parser import Parser
from .system.PersistenceManager import PersistenceManager
from .system.ProgressIndicator import ProgressIndicator
from .system.RedirectedStreams import RedirectedStreams
from .system.Signature import Signature
from .system.SlotContributions import SlotContributions
from .system.TemporaryDirectory import TemporaryDirectory
from .system.TemporaryDirectoryChange import TemporaryDirectoryChange
from .system.TestManager import TestManager
from .system.Timer import Timer
from .system.UpdateManager import UpdateManager
from .system.Wrapper import Wrapper
from .system.annotate import annotate
from .tags import Tag, Tags

from .utilities.CyclicTuple import CyclicTuple
from .utilities.Duration import Duration
from .utilities.DurationInequality import DurationInequality
from .utilities.Enumerator import Enumerator
from .utilities.Expression import Expression
from .utilities.Inequality import Inequality
from .utilities.LengthInequality import LengthInequality
from .utilities.Multiplier import Multiplier
from .utilities.Offset import Offset
from .utilities.OrderedDict import OrderedDict
from .utilities.Pattern import Pattern
from .utilities.PatternTuple import PatternTuple
from .utilities.Sequence import Sequence
from .utilities.SortedCollection import SortedCollection
from .utilities.String import String
from .utilities.TypedCollection import TypedCollection
from .utilities.TypedCounter import TypedCounter
from .utilities.TypedFrozenset import TypedFrozenset
from .utilities.TypedList import TypedList
from .utilities.TypedTuple import TypedTuple
from .utilities.list_all_classes import list_all_classes
from .utilities.list_all_functions import list_all_functions
from .utilities.yield_all_modules import yield_all_modules
from .utilities import (
    Infinity,
    NegativeInfinity,
)

# typings after utilities because of Expression
from .typings import (
    IntegerPair,
    IntegerSequence,
    DurationTyping,
    DurationSequenceTyping,
    Number,
    NumberPair,
    PatternTyping,
    Prototype,
    RatioTyping,
    RatioSequenceTyping,
    SelectorTyping,
    Strings,
)

from .indicators.Arpeggio import Arpeggio
from .indicators.Articulation import Articulation
from .indicators.BarLine import BarLine
from .indicators.BeamCount import BeamCount
from .indicators.BendAfter import BendAfter
from .indicators.BowContactPoint import BowContactPoint
from .indicators.BowMotionTechnique import BowMotionTechnique
from .indicators.BowPressure import BowPressure
from .indicators.BreathMark import BreathMark
from .indicators.Clef import Clef
from .indicators.Clef import StaffPosition
from .indicators.ColorFingering import ColorFingering
from .indicators.Dynamic import Dynamic
from .indicators.Fermata import Fermata
from .indicators.GlissandoIndicator import GlissandoIndicator
from .indicators.KeyCluster import KeyCluster
from .indicators.KeySignature import KeySignature
from .indicators.LaissezVibrer import LaissezVibrer
from .indicators.LilyPondComment import LilyPondComment
from .indicators.LilyPondLiteral import LilyPondLiteral
from .indicators.MarginMarkup import MarginMarkup
from .indicators.MetricModulation import MetricModulation
from .indicators.MetronomeMark import MetronomeMark
from .indicators.Mode import Mode
from .indicators.Ottava import Ottava
from .indicators.RehearsalMark import RehearsalMark
from .indicators.Repeat import Repeat
from .indicators.RepeatTie import RepeatTie
from .indicators.Staccatissimo import Staccatissimo
from .indicators.Staccato import Staccato
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
from .indicators.WoodwindFingering import WoodwindFingering

from .instruments import (
    Instrument,
    StringNumber,
    Tuning,
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
    Marimba,
    MezzoSopranoVoice,
    Oboe,
    Percussion,
    Piano,
    Piccolo,
    SopraninoSaxophone,
    SopranoSaxophone,
    SopranoVoice,
    TenorSaxophone,
    TenorTrombone,
    TenorVoice,
    Trumpet,
    Tuba,
    Vibraphone,
    Viola,
    Violin,
    Xylophone,
)

from .lilypondfile.Block import Block
from .lilypondfile.ContextBlock import ContextBlock
from .lilypondfile.DateTimeToken import DateTimeToken
from .lilypondfile.LilyPondDimension import LilyPondDimension
from .lilypondfile.LilyPondFile import LilyPondFile
from .lilypondfile.LilyPondLanguageToken import LilyPondLanguageToken
from .lilypondfile.LilyPondVersionToken import LilyPondVersionToken
from .lilypondfile.PackageGitCommitToken import PackageGitCommitToken

from .lilypondnames.LilyPondContext import LilyPondContext
from .lilypondnames.LilyPondContextSetting import LilyPondContextSetting
from .lilypondnames.LilyPondEngraver import LilyPondEngraver
from .lilypondnames.LilyPondGrob import LilyPondGrob
from .lilypondnames.LilyPondGrobInterface import LilyPondGrobInterface
from .lilypondnames.LilyPondGrobNameManager import LilyPondGrobNameManager
from .lilypondnames.LilyPondGrobOverride import LilyPondGrobOverride
from .lilypondnames.LilyPondNameManager import LilyPondNameManager
from .lilypondnames.LilyPondSettingNameManager import LilyPondSettingNameManager
from .lilypondnames.LilyPondTweakManager import IndexedTweakManager
from .lilypondnames.LilyPondTweakManager import IndexedTweakManagers
from .lilypondnames.LilyPondTweakManager import LilyPondTweakManager

from .markups import (
    Markup,
    MarkupCommand,
    MarkupList,
    Postscript,
    PostscriptOperator,
)
from .meter import (
    Meter,
    MeterList,
    MetricAccentKernel,
    OffsetCounter,
)
from .pitch.intervalclasses import (
    IntervalClass,
    NamedIntervalClass,
    NamedInversionEquivalentIntervalClass,
    NumberedIntervalClass,
    NumberedInversionEquivalentIntervalClass,
)
from .pitch.intervals import (
    NamedInterval,
    NumberedInterval,
    Interval,
)
from .pitch.pitchclasses import (
    PitchClass,
    NamedPitchClass,
    NumberedPitchClass,
)
from .pitch.pitches import (
    NamedPitch,
    NumberedPitch,
    Pitch,
    PitchTyping,
)
from .pitch.Accidental import Accidental
from .pitch.ColorMap import ColorMap
from .pitch.Octave import Octave
from .pitch.PitchInequality import PitchInequality
from .pitch.PitchRange import PitchRange
from .pitch.SetClass import SetClass
from .pitch.operators import (
    CompoundOperator,
    Duplication,
    Inversion,
    Multiplication,
    Retrograde,
    Rotation,
    Transposition,
)
from .pitch.segments import (
    IntervalClassSegment,
    IntervalSegment,
    PitchClassSegment,
    PitchSegment,
    Segment,
    TwelveToneRow,
)
from .pitch.sets import (
    IntervalClassSet,
    IntervalSet,
    PitchClassSet,
    PitchSet,
    Set,
)
from .pitch.vectors import (
    IntervalClassVector,
    IntervalVector,
    PitchClassVector,
    PitchVector,
    Vector,
)
from .scheme import (
    Scheme,
    SchemeAssociativeList,
    SchemeColor,
    SchemeMoment,
    SchemePair,
    SchemeSymbol,
    SchemeVector,
    SchemeVectorConstant,
    SpacingVector,
)

from .core.AfterGraceContainer import AfterGraceContainer
from .core.BeforeGraceContainer import BeforeGraceContainer
from .core.Chord import Chord
from .core.Cluster import Cluster
from .core.Component import Component
from .core.Container import Container
from .core.Context import Context
from .core.Descendants import Descendants
from .core.DrumNoteHead import DrumNoteHead
from .core.Inspection import Inspection
from .core.Iteration import Iteration
from .core.Label import Label
from .core.Leaf import Leaf
from .core.LeafMaker import LeafMaker
from .core.Lineage import Lineage
from .core.LogicalTie import LogicalTie
from .core.MultimeasureRest import MultimeasureRest
from .core.Mutation import Mutation
from .core.Note import Note
from .core.NoteHead import NoteHead
from .core.NoteHeadList import NoteHeadList
from .core.NoteMaker import NoteMaker
from .core.OnBeatGraceContainer import OnBeatGraceContainer
from .core.OnBeatGraceContainer import on_beat_grace_container
from .core.Parentage import Parentage
from .core.Rest import Rest
from .core.Score import Score
from .core.Selection import Selection
from .core.Skip import Skip
from .core.Staff import Staff
from .core.StaffGroup import StaffGroup
from .core.TremoloContainer import TremoloContainer
from .core.Tuplet import Tuplet
from .core.VerticalMoment import VerticalMoment
from .core.Voice import Voice
from .core.Wellformedness import Wellformedness

from .segments.Job import Job
from .segments.Line import Line
from .segments.Momento import Momento
from .segments.Part import Part
from .segments.PartAssignment import PartAssignment
from .segments.PartManifest import PartManifest
from .segments.Path import Path
from .segments.PersistentOverride import PersistentOverride
from .segments.Section import Section
from .segments.SegmentMaker import SegmentMaker
from .segments.activate import activate
from .segments.deactivate import deactivate

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
from .templates import (
    GroupedRhythmicStavesScoreTemplate,
    GroupedStavesScoreTemplate,
    ScoreTemplate,
    StringOrchestraScoreTemplate,
    StringQuartetScoreTemplate,
    TwoStaffPianoScoreTemplate,
)
from .top import (
    attach,
    detach,
    f,
    graph,
    inspect,
    iterate,
    label,
    mutate,
    new,
    override,
    parse,
    persist,
    play,
    select,
    sequence,
    setting,
    show,
    tweak,
)

from .mathtools import (
    NonreducedFraction,
    NonreducedRatio,
    Ratio,
)

from .respell import (
    respell_with_flats,
    respell_with_sharps,
)

from .timespans import (
    AnnotatedTimespan,
    Timespan,
    TimespanList,
    timespan,
)

from .illustrate import illustrate

from . import cli
from . import demos
from . import ly
from . import utilities

configuration = Configuration()
tags = Tags()
index = Pattern.index
index_all = Pattern.index_all
index_first = Pattern.index_first
index_last = Pattern.index_last


__all__ = [
    "__version_info__",
    "__version__",
    "Fraction",
    "Comparison",
    "HorizontalAlignment",
    "VerticalAlignment",
    "Both",
    "Center",
    "Down",
    "Exact",
    "Left",
    "Less",
    "More",
    "Right",
    "Up",
    "AssignabilityError",
    "ImpreciseMetronomeMarkError",
    "LilyPondParserError",
    "MissingMetronomeMarkError",
    "ParentageError",
    "PersistentIndicatorError",
    "SchemeParserFinishedError",
    "UnboundedTimeIntervalError",
    "WellformednessError",
    "configuration",
    "parser",
    "FormatSpecification",
    "StorageFormatSpecification",
    "StorageFormatManager",
    "Configuration",
    "ContextManager",
    "FilesystemState",
    "ForbidUpdate",
    "IOManager",
    "LilyPondFormatBundle",
    "LilyPondFormatManager",
    "NullContextManager",
    "Parser",
    "PersistenceManager",
    "ProgressIndicator",
    "RedirectedStreams",
    "Signature",
    "SlotContributions",
    "Tag",
    "Tags",
    "TemporaryDirectory",
    "TemporaryDirectoryChange",
    "TestManager",
    "Timer",
    "UpdateManager",
    "Wrapper",
    "CyclicTuple",
    "Duration",
    "DurationInequality",
    "Enumerator",
    "Expression",
    "Inequality",
    "LengthInequality",
    "Multiplier",
    "Offset",
    "OrderedDict",
    "Pattern",
    "PatternTuple",
    "Sequence",
    "SortedCollection",
    "String",
    "TypedCollection",
    "TypedCounter",
    "TypedFrozenset",
    "TypedList",
    "TypedTuple",
    "list_all_classes",
    "list_all_functions",
    "yield_all_modules",
    "Infinity",
    "NegativeInfinity",
    "IntegerPair",
    "IntegerSequence",
    "DurationTyping",
    "DurationSequenceTyping",
    "Number",
    "NumberPair",
    "PatternTyping",
    "Prototype",
    "RatioTyping",
    "RatioSequenceTyping",
    "SelectorTyping",
    "Strings",
    "index",
    "index_all",
    "index_first",
    "index_last",
    "Arpeggio",
    "Articulation",
    "BarLine",
    "BeamCount",
    "BendAfter",
    "BowContactPoint",
    "BowMotionTechnique",
    "BowPressure",
    "BreathMark",
    "Clef",
    "ColorFingering",
    "Dynamic",
    "Fermata",
    "GlissandoIndicator",
    "KeyCluster",
    "KeySignature",
    "LaissezVibrer",
    "LilyPondComment",
    "LilyPondLiteral",
    "MarginMarkup",
    "MetricModulation",
    "MetronomeMark",
    "Mode",
    "Ottava",
    "RehearsalMark",
    "Repeat",
    "RepeatTie",
    "Staccatissimo",
    "Staccato",
    "StaffChange",
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
    "StringContactPoint",
    "Tie",
    "TimeSignature",
    "WoodwindFingering",
    "Instrument",
    "StringNumber",
    "Tuning",
    "Accordion",
    "AltoFlute",
    "AltoSaxophone",
    "AltoTrombone",
    "AltoVoice",
    "BaritoneSaxophone",
    "BaritoneVoice",
    "BassClarinet",
    "BassFlute",
    "BassSaxophone",
    "BassTrombone",
    "BassVoice",
    "Bassoon",
    "Cello",
    "ClarinetInA",
    "ClarinetInBFlat",
    "ClarinetInEFlat",
    "Contrabass",
    "ContrabassClarinet",
    "ContrabassFlute",
    "ContrabassSaxophone",
    "Contrabassoon",
    "EnglishHorn",
    "Flute",
    "FrenchHorn",
    "Glockenspiel",
    "Guitar",
    "Harp",
    "Harpsichord",
    "Marimba",
    "MezzoSopranoVoice",
    "Oboe",
    "Percussion",
    "Piano",
    "Piccolo",
    "SopraninoSaxophone",
    "SopranoSaxophone",
    "SopranoVoice",
    "TenorSaxophone",
    "TenorTrombone",
    "TenorVoice",
    "Trumpet",
    "Tuba",
    "Vibraphone",
    "Viola",
    "Violin",
    "Xylophone",
    "Block",
    "ContextBlock",
    "DateTimeToken",
    "LilyPondDimension",
    "LilyPondFile",
    "LilyPondLanguageToken",
    "LilyPondVersionToken",
    "PackageGitCommitToken",
    "LilyPondContext",
    "LilyPondContextSetting",
    "LilyPondEngraver",
    "LilyPondGrob",
    "LilyPondGrobInterface",
    "LilyPondGrobNameManager",
    "LilyPondGrobOverride",
    "LilyPondNameManager",
    "LilyPondSettingNameManager",
    "IndexedTweakManager",
    "IndexedTweakManagers",
    "LilyPondTweakManager",
    "Markup",
    "MarkupCommand",
    "MarkupList",
    "Postscript",
    "PostscriptOperator",
    "Meter",
    "MeterList",
    "MetricAccentKernel",
    "OffsetCounter",
    "Accidental",
    "ColorMap",
    "CompoundOperator",
    "Duplication",
    "Interval",
    "IntervalClass",
    "IntervalClassSegment",
    "IntervalClassSet",
    "IntervalClassVector",
    "IntervalSegment",
    "IntervalSet",
    "IntervalVector",
    "Inversion",
    "Multiplication",
    "NamedInterval",
    "NamedIntervalClass",
    "NamedInversionEquivalentIntervalClass",
    "NamedPitch",
    "NamedPitchClass",
    "NumberedInterval",
    "NumberedIntervalClass",
    "NumberedInversionEquivalentIntervalClass",
    "NumberedPitch",
    "NumberedPitchClass",
    "Octave",
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
    "Retrograde",
    "Rotation",
    "Segment",
    "Set",
    "SetClass",
    "StaffPosition",
    "Transposition",
    "TwelveToneRow",
    "Vector",
    "Scheme",
    "SchemeAssociativeList",
    "SchemeColor",
    "SchemeMoment",
    "SchemePair",
    "SchemeSymbol",
    "SchemeVector",
    "SchemeVectorConstant",
    "SpacingVector",
    "AfterGraceContainer",
    "BeforeGraceContainer",
    "Chord",
    "Cluster",
    "Component",
    "Container",
    "Context",
    "Descendants",
    "DrumNoteHead",
    "Inspection",
    "Iteration",
    "Label",
    "Leaf",
    "LeafMaker",
    "Lineage",
    "LogicalTie",
    "MultimeasureRest",
    "Mutation",
    "Note",
    "NoteHead",
    "NoteHeadList",
    "NoteMaker",
    "OnBeatGraceContainer",
    "on_beat_grace_container",
    "Parentage",
    "Rest",
    "Score",
    "Selection",
    "Skip",
    "Staff",
    "StaffGroup",
    "TremoloContainer",
    "Tuplet",
    "VerticalMoment",
    "Voice",
    "Wellformedness",
    "GroupedRhythmicStavesScoreTemplate",
    "GroupedStavesScoreTemplate",
    "Job",
    "Line",
    "Momento",
    "Part",
    "PartAssignment",
    "PartManifest",
    "Path",
    "PersistentOverride",
    "ScoreTemplate",
    "Section",
    "SegmentMaker",
    "StringOrchestraScoreTemplate",
    "StringQuartetScoreTemplate",
    "TwoStaffPianoScoreTemplate",
    "activate",
    "beam",
    "bow_contact_spanner",
    "glissando",
    "hairpin",
    "horizontal_bracket",
    "ottava",
    "phrasing_slur",
    "piano_pedal",
    "slur",
    "text_spanner",
    "tie",
    "trill_spanner",
    "annotate",
    "attach",
    "deactivate",
    "detach",
    "f",
    "graph",
    "inspect",
    "iterate",
    "label",
    "mutate",
    "new",
    "override",
    "parse",
    "persist",
    "play",
    "select",
    "sequence",
    "setting",
    "show",
    "tweak",
    "NonreducedFraction",
    "NonreducedRatio",
    "Ratio",
    "AnnotatedTimespan",
    "Timespan",
    "TimespanList",
    "timespan",
    "cli",
    "demos",
    "ly",
    "utilities",
    "tags",
    "respell_with_flats",
    "respell_with_sharps",
    "illustrate",
]
