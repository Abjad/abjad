# -*- encoding: utf-8 -*-
import locale
from experimental import *


locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
def test_optimization_targets_01():
    r'''Score with 1 voice, 50 measures, 100 divisions, 300 notes.

    2.12 (r9746) 1,307,616 function calls.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(50 * [(3, 8)])
    score_specification.set_divisions([(3, 16)])
    score_specification.set_rhythm(library.sixteenths)

    string = 'score_specification.interpret()'
    count = systemtools.IOManager.count_function_calls(string, globals(), locals(), fixed_point=False)
    score = score_specification.score_specification.interpreter.score
    assert count < locale.atoi('1,500,000')


def test_optimization_targets_02():
    r'''Score with 1 voice, 50 measures, 100 divisions, 300 notes.
    Set color of all leaves.

    2.12 (r9746) 1,341,529 function calls.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(50 * [(3, 8)])
    score_specification.set_divisions([(3, 16)])
    score_specification.set_rhythm(library.sixteenths)
    score_specification.select_leaves('Voice 1').set_leaf_color('red')

    string = 'score_specification.interpret()'
    count = systemtools.IOManager.count_function_calls(string, globals(), locals(), fixed_point=False)
    score = score_specification.score_specification.interpreter.score
    assert count < locale.atoi('1,500,000')


def test_optimization_targets_03():
    r'''Score with 1 voice, 50 measures, 100 divisions, 300 notes.
    Set color of all leaves via division select expression.

    2.12 (r9746) 1,425,846 function calls.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(50 * [(3, 8)])
    score_specification.set_divisions([(3, 16)])
    score_specification.set_rhythm(library.sixteenths)
    divisions = score_specification.select_divisions('Voice 1')
    divisions.select_leaves('Voice 1').set_leaf_color('red')

    string = 'score_specification.interpret()'
    count = systemtools.IOManager.count_function_calls(string, globals(), locals(), fixed_point=False)
    score = score_specification.score_specification.interpreter.score
    assert count < locale.atoi('1,500,000')


def test_optimization_targets_04():
    r'''Score with 1 voice, 50 measures, 100 divisions, 300 notes.
    Partition *leaves* in 16 parts and then set leaf color of each part.

    TODO: partition_by_ratio() is called 16 times (r9746) and should only be called *once*.

    2.12 (r9746) 2,479,921 function calls.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(50 * [(3, 8)])
    score_specification.set_divisions([(3, 16)])
    score_specification.set_rhythm(library.sixteenths)

    parts = score_specification.select_leaves('Voice 1').partition_by_ratio(16 * [1])
    for i, part in enumerate(parts):
        if i % 2 == 0:
            part.set_leaf_color('red')
        else:
            part.set_leaf_color('blue')

    string = 'score_specification.interpret()'
    count = systemtools.IOManager.count_function_calls(string, globals(), locals(), fixed_point=False)
    score = score_specification.score_specification.interpreter.score
    assert count < locale.atoi('3,300,000')


def test_optimization_targets_05():
    r'''Score with 1 voice, 50 measures, 100 divisions, 300 notes.
    Partition *divisions* in 16 parts and then set leaf color of each part.

    2.12 (r9746) 2,444,770 function calls.
    2.12 (r9752) 1,955,779 function calls.
    2.12 (r9753) 1,848,278 function calls.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(50 * [(3, 8)])
    score_specification.set_divisions([(3, 16)])
    score_specification.set_rhythm(library.sixteenths)

    parts = score_specification.select_divisions('Voice 1').partition_by_ratio(16 * [1])
    for i, part in enumerate(parts):
        if i % 2 == 0:
            part.select_leaves('Voice 1').set_leaf_color('red')
        else:
            part.select_leaves('Voice 1').set_leaf_color('blue')

    string = 'score_specification.interpret()'
    count = systemtools.IOManager.count_function_calls(string, globals(), locals(), fixed_point=False)
    score = score_specification.score_specification.interpreter.score
    assert count < locale.atoi('2,900,000')