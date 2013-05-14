# -*- encoding: utf-8 -*-
from abjad import *
from collections import OrderedDict
import collections


tags = collections.OrderedDict([
    ('instrumentation', scoretools.InstrumentationSpecifier(performers=scoretools.PerformerInventory([]))),
    ('title', 'Red Example ScoreI'),
    ('year_of_completion', 2013)])