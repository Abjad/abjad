# -*- encoding: utf-8 -*-
from abjad import *
from experimental.tools import makertools


time_signatures = 2 * [(6, 8)]
rh_divisions = []
rh_divisions.extend(6 * [(2, 16)])
rh_divisions.extend(3 * [(3, 8)])
rh_divisions.extend(6 * [(2, 16)])
rh_divisions.extend(3 * [(3, 8)])
lh_divisions = []
lh_divisions.extend(3 * [(3, 8)])
lh_divisions.extend(6 * [(2, 16)])
lh_divisions.extend(3 * [(3, 8)])
lh_divisions.extend(6 * [(2, 16)])
divisions = {
    'RH Voice': rh_divisions,
    'LH Voice': lh_divisions,
    }
segment_maker = makertools.PianoStaffSegmentMaker(
    time_signatures=time_signatures,
    divisions=divisions,
    )