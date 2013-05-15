# -*- encoding: utf-8 -*-
from abjad import *
import collections


tags = collections.OrderedDict([
    ('instrumentation', scoretools.InstrumentationSpecifier(performers=scoretools.PerformerInventory([]))),
    ('title', 'Green Example Score'),
    ('year_of_completion', 2013)])