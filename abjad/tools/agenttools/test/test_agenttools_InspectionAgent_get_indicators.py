# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_InspectionAgent_get_indicators_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = Slur()
    attach(slur, staff[:])
    command_1 = indicatortools.LilyPondCommand('slurDotted')
    attach(command_1, staff[0])
    command_2 = indicatortools.LilyPondCommand('slurUp')
    attach(command_2, staff[0])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \slurDotted
            \slurUp
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        ), format(staff)

    indicators = inspect_(staff[0]).get_indicators(
        indicatortools.LilyPondCommand)
    assert command_1 in indicators
    assert command_2 in indicators
    assert len(indicators) == 2


def test_agenttools_InspectionAgent_get_indicators_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = Slur()
    attach(slur, staff[:])
    comment = indicatortools.LilyPondComment('beginning of note content')
    attach(comment, staff[0])
    command = indicatortools.LilyPondCommand('slurDotted')
    attach(command, staff[0])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            % beginning of note content
            \slurDotted
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        ), format(staff)

    items = inspect_(staff[0]).get_indicators()
    assert comment in items
    assert command in items
    assert len(items) == 2


def test_agenttools_InspectionAgent_get_indicators_03():

    staff = Staff("c'8 d'8 e'8 f'8")
    clef = Clef('treble')
    attach(clef, staff)
    dynamic = Dynamic('p')
    attach(dynamic, staff[0])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \clef "treble"
            c'8 \p
            d'8
            e'8
            f'8
        }
        '''
        ), format(staff)

    indicators = inspect_(staff[0]).get_indicators()
    assert dynamic == indicators[0]
    assert len(indicators) == 1


def test_agenttools_InspectionAgent_get_indicators_04():

    staff = Staff("c'8 d'8 e'8 f'8")
    clef = Clef('treble')
    attach(clef, staff)
    dynamic = Dynamic('p')
    attach(dynamic, staff[0])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \clef "treble"
            c'8 \p
            d'8
            e'8
            f'8
        }
        '''
        ), format(staff)

    dynamics = inspect_(staff[0]).get_indicators(Dynamic)
    assert dynamic == dynamics[0]
    assert len(dynamics) == 1


def test_agenttools_InspectionAgent_get_indicators_05():

    staff = Staff("c'8 d'8 e'8 f'8")
    annotation_1 = indicatortools.Annotation('annotation 1')
    attach(annotation_1, staff[0])
    annotation_2 = indicatortools.Annotation('annotation 2')
    attach(annotation_2, staff[0])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        ), format(staff)

    annotations = inspect_(staff[0]).get_indicators(indicatortools.Annotation)
    assert annotations == (annotation_1, annotation_2)


def test_agenttools_InspectionAgent_get_indicators_06():

    staff = Staff("c'8 d'8 e'8 f'8")
    comment_1 = indicatortools.LilyPondComment('comment 1')
    attach(comment_1, staff[0])
    comment_2 = indicatortools.LilyPondComment('comment 2')
    attach(comment_2, staff[0])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            % comment 1
            % comment 2
            c'8
            d'8
            e'8
            f'8
        }
        '''
        ), format(staff)

    indicators = inspect_(staff[0]).get_indicators(
        indicatortools.LilyPondComment)
    assert comment_1 in indicators
    assert comment_2 in indicators
    assert len(indicators) == 2


def test_agenttools_InspectionAgent_get_indicators_07():

    note = Note("c'4")
    stem_tremolo = indicatortools.StemTremolo(16)
    attach(stem_tremolo, note)
    stem_tremolos = inspect_(note).get_indicators(indicatortools.StemTremolo)

    assert stem_tremolos[0] is stem_tremolo