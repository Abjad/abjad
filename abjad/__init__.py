# -*- coding: utf-8 -*-
# warn on an outdated Python installation
import distutils.version
import platform
if not (
    distutils.version.LooseVersion('2.7.2') <
    distutils.version.LooseVersion(platform.python_version())
    ):
    print('WARNING: Abjad does not support Python versions less than 2.7.3.')
    print('WARNING: Upgrade your Python to 2.7.3 or higher.')
del platform
del distutils

# set up tab completion
try:
    import readline
    import rlcompleter
    if readline.__doc__ is not None and 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    del readline
    del rlcompleter
except ImportError:
    pass

try:
    from quicktions import Fraction
except ImportError:
    from fractions import Fraction

# ensure that the ~/.abjad directory and friends are setup,
# and instantiate Abjad's configuration singleton
from abjad.tools.systemtools.AbjadConfiguration import AbjadConfiguration
abjad_configuration = AbjadConfiguration()
del AbjadConfiguration

# import all tools packages
from abjad.tools import *

# import some frequently used classes for direct user access
from abjad.tools.durationtools import Duration
from abjad.tools.durationtools import Multiplier
from abjad.tools.durationtools import Offset
from abjad.tools.datastructuretools import CyclicTuple
from abjad.tools.datastructuretools import TypedOrderedDict
from abjad.tools.expressiontools import Expression
from abjad.tools.indicatortools import Accelerando
from abjad.tools.indicatortools import Annotation
from abjad.tools.indicatortools import Arpeggio
from abjad.tools.indicatortools import Arrow
from abjad.tools.indicatortools import Articulation
from abjad.tools.indicatortools import BarLine
from abjad.tools.indicatortools import BendAfter
from abjad.tools.indicatortools import BowContactPoint
from abjad.tools.indicatortools import BowMotionTechnique
from abjad.tools.indicatortools import BowPressure
from abjad.tools.indicatortools import BreathMark
from abjad.tools.indicatortools import Clef
from abjad.tools.indicatortools import ColorFingering
from abjad.tools.indicatortools import Dynamic
from abjad.tools.indicatortools import Fermata
from abjad.tools.indicatortools import KeyCluster
from abjad.tools.indicatortools import KeySignature
from abjad.tools.indicatortools import LaissezVibrer
from abjad.tools.indicatortools import LilyPondCommand
from abjad.tools.indicatortools import LilyPondComment
from abjad.tools.indicatortools import LilyPondLiteral
from abjad.tools.indicatortools import LineSegment
from abjad.tools.indicatortools import MetricModulation
from abjad.tools.indicatortools import PageBreak
from abjad.tools.indicatortools import RehearsalMark
from abjad.tools.indicatortools import Repeat
from abjad.tools.indicatortools import Ritardando
from abjad.tools.indicatortools import StaffChange
from abjad.tools.indicatortools import StemTremolo
from abjad.tools.indicatortools import StringContactPoint
from abjad.tools.indicatortools import StringNumber
from abjad.tools.indicatortools import SystemBreak
from abjad.tools.indicatortools import Tempo
from abjad.tools.indicatortools import TimeSignature
from abjad.tools.indicatortools import Tremolo
from abjad.tools.indicatortools import Tuning
from abjad.tools.lilypondfiletools import LilyPondFile
from abjad.tools.markuptools import Markup
from abjad.tools.markuptools import MarkupList
from abjad.tools.mathtools import Infinity
Infinity = Infinity()
from abjad.tools.mathtools import NonreducedFraction
from abjad.tools.mathtools import NonreducedRatio
from abjad.tools.mathtools import Ratio
from abjad.tools.metertools import Meter
from abjad.tools.patterntools import Pattern
from abjad.tools.pitchtools import Inversion
from abjad.tools.pitchtools import Multiplication
from abjad.tools.pitchtools import NamedInterval
from abjad.tools.pitchtools import NamedIntervalClass
from abjad.tools.pitchtools import NamedPitch
from abjad.tools.pitchtools import NamedPitchClass
from abjad.tools.pitchtools import NumberedInterval
from abjad.tools.pitchtools import NumberedIntervalClass
from abjad.tools.pitchtools import NumberedPitch
from abjad.tools.pitchtools import NumberedPitchClass
from abjad.tools.pitchtools import PitchClassSet
from abjad.tools.pitchtools import PitchClassSegment
from abjad.tools.pitchtools import PitchSegment
from abjad.tools.pitchtools import PitchSet
from abjad.tools.pitchtools import PitchRange
from abjad.tools.pitchtools import Registration
from abjad.tools.pitchtools import Retrograde
from abjad.tools.pitchtools import Rotation
from abjad.tools.pitchtools import SetClass
from abjad.tools.pitchtools import Transposition
from abjad.tools.pitchtools import TwelveToneRow
from abjad.tools.schemetools import Scheme
from abjad.tools.schemetools import SchemeMoment
from abjad.tools.schemetools import SchemePair
from abjad.tools.schemetools import SchemeSymbol
from abjad.tools.schemetools import SchemeVector
from abjad.tools.scoretools import Chord
from abjad.tools.scoretools import Cluster
from abjad.tools.scoretools import Component
from abjad.tools.scoretools import Container
from abjad.tools.scoretools import Context
from abjad.tools.scoretools import FixedDurationTuplet
from abjad.tools.scoretools import GraceContainer
from abjad.tools.scoretools import Leaf
from abjad.tools.scoretools import Measure
from abjad.tools.scoretools import Measure
from abjad.tools.scoretools import MultimeasureRest
from abjad.tools.scoretools import Note
from abjad.tools.scoretools import Rest
from abjad.tools.scoretools import Score
from abjad.tools.scoretools import Skip
from abjad.tools.scoretools import Staff
from abjad.tools.scoretools import StaffGroup
from abjad.tools.scoretools import Tuplet
from abjad.tools.scoretools import Voice
from abjad.tools.selectiontools import Selection
from abjad.tools.selectortools import Selector
from abjad.tools.sequencetools import Sequence
from abjad.tools.spannertools import Beam
from abjad.tools.spannertools import BowContactSpanner
from abjad.tools.spannertools import ClefSpanner
from abjad.tools.spannertools import ComplexBeam
from abjad.tools.spannertools import ComplexTrillSpanner
from abjad.tools.spannertools import Crescendo
from abjad.tools.spannertools import Decrescendo
from abjad.tools.spannertools import DuratedComplexBeam
from abjad.tools.spannertools import GeneralizedBeam
from abjad.tools.spannertools import Glissando
from abjad.tools.spannertools import Hairpin
from abjad.tools.spannertools import HiddenStaffSpanner
from abjad.tools.spannertools import HorizontalBracketSpanner
from abjad.tools.spannertools import MeasuredComplexBeam
from abjad.tools.spannertools import MultipartBeam
from abjad.tools.spannertools import OctavationSpanner
from abjad.tools.spannertools import PhrasingSlur
from abjad.tools.spannertools import PianoPedalSpanner
from abjad.tools.spannertools import Slur
from abjad.tools.spannertools import Spanner
from abjad.tools.spannertools import StaffLinesSpanner
from abjad.tools.spannertools import StemTremoloSpanner
from abjad.tools.spannertools import TempoSpanner
from abjad.tools.spannertools import TextSpanner
from abjad.tools.spannertools import Tie
from abjad.tools.spannertools import TrillSpanner
from abjad.tools.timespantools import Timespan

# import some frequently used functions for direct user access
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import graph
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import label
from abjad.tools.topleveltools import mutate
from abjad.tools.topleveltools import new
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import parse
from abjad.tools.topleveltools import play
from abjad.tools.topleveltools import persist
from abjad.tools.topleveltools import select
from abjad.tools.topleveltools import sequence
from abjad.tools.topleveltools import set_
from abjad.tools.topleveltools import show
from abjad.tools.topleveltools import tweak

# frequently used patterntools functions
from abjad.tools.patterntools import select_all
from abjad.tools.patterntools import select_every
from abjad.tools.patterntools import select_first
from abjad.tools.patterntools import select_last

# frequently used rhythm-maker functions
from abjad.tools.rhythmmakertools import silence
from abjad.tools.rhythmmakertools import silence_all
from abjad.tools.rhythmmakertools import silence_every
from abjad.tools.rhythmmakertools import silence_except
from abjad.tools.rhythmmakertools import silence_first
from abjad.tools.rhythmmakertools import silence_last
from abjad.tools.rhythmmakertools import sustain
from abjad.tools.rhythmmakertools import sustain_all
from abjad.tools.rhythmmakertools import sustain_every
from abjad.tools.rhythmmakertools import sustain_first
from abjad.tools.rhythmmakertools import sustain_last

# import custom exceptions into the builtins module
import os
from abjad.tools.systemtools.ImportManager import ImportManager
ImportManager.import_public_names_from_path_into_namespace(
    os.path.join(__path__[0], 'tools', 'exceptiontools'),
    __builtins__,
    )
del ImportManager
del os
del tools

# import version information
from abjad._version import __version_info__, __version__
del _version

def f(argument):
    if hasattr(argument, '_publish_storage_format'):
        print(format(argument, 'storage'))
    else:
        print(format(argument, 'lilypond'))

from abjad import demos
from abjad import ext
from abjad import ly
