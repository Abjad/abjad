# -*- coding: utf-8 -*-
import copy
from abjad import Beam
from abjad import Clef
from abjad import Crescendo
from abjad import Decrescendo
from abjad import Dynamic
from abjad import Markup
from abjad import Measure
from abjad import Score
from abjad import Slur
from abjad import Staff
from abjad import StaffGroup
from abjad import Tie
from abjad import Voice
from abjad import attach
from abjad import indicatortools
from abjad import override
from abjad import spannertools
from abjad.tools.topleveltools import select


def make_bartok_score():
    score = Score([])
    piano_staff = StaffGroup([], context_name='PianoStaff')
    upper_staff = Staff([])
    lower_staff = Staff([])
    piano_staff.append(upper_staff)
    piano_staff.append(lower_staff)
    score.append(piano_staff)
    upper_measures = []
    upper_measures.append(Measure((2, 4), []))
    upper_measures.append(Measure((3, 4), []))
    upper_measures.append(Measure((2, 4), []))
    upper_measures.append(Measure((2, 4), []))
    upper_measures.append(Measure((2, 4), []))
    lower_measures = copy.deepcopy(upper_measures)
    upper_staff.extend(upper_measures)
    lower_staff.extend(lower_measures)
    upper_measures[0].extend("a'8 g'8 f'8 e'8")
    upper_measures[1].extend("d'4 g'8 f'8 e'8 d'8")
    upper_measures[2].extend("c'8 d'16 e'16 f'8 e'8")
    upper_measures[3].append("d'2")
    upper_measures[4].append("d'2")
    lower_measures[0].extend("b4 d'8 c'8")
    lower_measures[1].extend("b8 a8 af4 c'8 bf8")
    lower_measures[2].extend("a8 g8 fs8 g16 a16")
    upper_voice = Voice("b2", name='upper voice')
    command = indicatortools.LilyPondCommand('voiceOne')
    attach(command, upper_voice)
    lower_voice = Voice("b4 a4", name='lower voice')
    command = indicatortools.LilyPondCommand('voiceTwo')
    attach(command, lower_voice)
    lower_measures[3].extend([upper_voice, lower_voice])
    lower_measures[3].is_simultaneous = True
    upper_voice = Voice("b2", name='upper voice')
    command = indicatortools.LilyPondCommand('voiceOne')
    attach(command, upper_voice)
    lower_voice = Voice("g2", name='lower voice')
    command = indicatortools.LilyPondCommand('voiceTwo')
    attach(command, lower_voice)
    lower_measures[4].extend([upper_voice, lower_voice])
    lower_measures[4].is_simultaneous = True
    clef = Clef('bass')
    attach(clef, lower_staff)
    dynamic = Dynamic('pp')
    attach(dynamic, upper_measures[0][0])
    dynamic = Dynamic('mp')
    attach(dynamic, upper_measures[1][1])
    dynamic = Dynamic('pp')
    attach(dynamic, lower_measures[0][1])
    dynamic = Dynamic('mp')
    attach(dynamic, lower_measures[1][3])
    score.add_final_bar_line()
    selector = select().by_leaf(flatten=True)
    upper_leaves = selector(upper_staff)
    lower_leaves = selector(lower_staff)
    beam = Beam()
    attach(beam, upper_leaves[:4])
    beam = Beam()
    attach(beam, lower_leaves[1:5])
    beam = Beam()
    attach(beam, lower_leaves[6:10])
    slur = Slur()
    attach(slur, upper_leaves[:5])
    slur = Slur()
    attach(slur, upper_leaves[5:])
    slur = Slur()
    attach(slur, lower_leaves[1:6])
    crescendo = Crescendo()
    attach(crescendo, upper_leaves[-7:-2])
    decrescendo = Decrescendo()
    attach(decrescendo, upper_leaves[-2:])
    markup = Markup('ritard.')
    text_spanner = spannertools.TextSpanner()
    override(text_spanner).text_spanner.bound_details__left__text = markup
    attach(text_spanner, upper_leaves[-7:])
    tie = Tie()
    attach(tie, upper_leaves[-2:])
    note_1 = lower_staff[-2]['upper voice'][0]
    note_2 = lower_staff[-1]['upper voice'][0]
    notes = [note_1, note_2]
    tie = Tie()
    attach(tie, notes)
    return score