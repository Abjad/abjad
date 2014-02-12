# -*- encoding: utf-8 -*-
import os
from experimental import *


time_signatures = [(15, 8), (18, 8)]
rh_divisions = []
rh_divisions.extend(4 * [(3, 8)])
rh_divisions.extend(4 * [(3, 16)])
rh_divisions.extend(6 * [(5, 16)])
lh_divisions = []
lh_divisions.extend(6 * [(5, 16)])
lh_divisions.extend(4 * [(3, 8)])
lh_divisions.extend(4 * [(3, 16)])
divisions = {
    'RH Voice': rh_divisions,
    'LH Voice': lh_divisions,
    }
segment_maker = segmentmakertools.PianoStaffSegmentMaker(
    time_signatures=time_signatures,
    divisions=divisions,
    )

if __name__ == '__main__':
    lilypond_file = segment_maker()
    current_directory_path = os.path.dirname(__file__)
    ly_file_path = os.path.join(current_directory_path, 'output.ly')
    persist(lilypond_file).as_ly(ly_file_path)
    pdf_file_path = os.path.join(current_directory_path, 'output.pdf')
    persist(lilypond_file).as_pdf(pdf_file_path)
    command = 'open {}'.format(pdf_file_path)
    os.system(command)
