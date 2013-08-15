# -*- encoding: utf-8 -*-
# load constants into __builtins__ namespace
from abjad.tools import datastructuretools
from abjad.tools import mathtools
__builtins__['Left'] = datastructuretools.OrdinalConstant('x', -1, 'Left')
__builtins__['Right'] = datastructuretools.OrdinalConstant('x', 1, 'Right')
__builtins__['Center'] = datastructuretools.OrdinalConstant('y', 0, 'Center')
__builtins__['Up'] = datastructuretools.OrdinalConstant('y', 1, 'Up')
__builtins__['Down'] = datastructuretools.OrdinalConstant('y', -1, 'Down')
__builtins__['Infinity'] = mathtools.Infinity()
__builtins__['NegativeInfinity'] = mathtools.NegativeInfinity()

from abjad.tools import abctools
from abjad.tools import abjadbooktools
from abjad.tools import chordtools
from abjad.tools import componenttools
from abjad.tools import configurationtools
from abjad.tools import containertools
from abjad.tools import contexttools
from abjad.tools import decoratortools
from abjad.tools import developerscripttools
from abjad.tools import documentationtools
from abjad.tools import durationtools
from abjad.tools import exceptiontools
from abjad.tools import formattools
from abjad.tools import importtools
from abjad.tools import instrumenttools
from abjad.tools import introspectiontools
from abjad.tools import iotools
from abjad.tools import iterationtools
from abjad.tools import labeltools
from abjad.tools import layouttools
from abjad.tools import leaftools
from abjad.tools import lilypondfiletools
from abjad.tools import lilypondparsertools
from abjad.tools import lilypondproxytools
from abjad.tools import marktools
from abjad.tools import markuptools
from abjad.tools import measuretools
from abjad.tools import notetools
from abjad.tools import updatetools
from abjad.tools import pitcharraytools
from abjad.tools import pitchtools
from abjad.tools import quantizationtools
from abjad.tools import resttools
from abjad.tools import rhythmmakertools
from abjad.tools import rhythmtreetools
from abjad.tools import schemetools
from abjad.tools import scoretemplatetools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import sievetools
from abjad.tools import skiptools
from abjad.tools import spannertools
from abjad.tools import stafftools
from abjad.tools import stringtools
from abjad.tools import tempotools
from abjad.tools import testtools
from abjad.tools import timeintervaltools
from abjad.tools import timesignaturetools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from abjad.tools import tonalanalysistools
from abjad.tools import tuplettools
from abjad.tools import voicetools
from abjad.tools import wellformednesstools
