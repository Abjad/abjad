# -*- encoding: utf-8 -*-
import os
from abjad import *
from experimental.tools import segmentmakertools


time_signatures = 5 * [(3, 4)]
rh_divisions = []
rh_divisions.extend(4 * [(2, 8)])
rh_divisions.extend(4 * [(2, 16)])
rh_divisions.extend(4 * [(3, 8)])
rh_divisions.extend(4 * [(3, 16)])
lh_divisions = []
lh_divisions.extend(4 * [(3, 8)])
lh_divisions.extend(4 * [(3, 16)])
lh_divisions.extend(4 * [(2, 8)])
lh_divisions.extend(4 * [(2, 16)])
divisions = {
    'RH Voice': rh_divisions,
    'LH Voice': lh_divisions,
    }

segment_maker = segmentmakertools.PianoStaffSegmentMaker(
    time_signatures=time_signatures,
    divisions=divisions,
    )