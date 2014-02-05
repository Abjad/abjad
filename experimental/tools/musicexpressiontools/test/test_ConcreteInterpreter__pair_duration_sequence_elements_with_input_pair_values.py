# -*- encoding: utf-8 -*-
from experimental import *


def test_sequencetools_pair_duration_sequence_elements_with_input_pair_values_01():


    duration_sequence = [10, 10, 10, 10]
    interpreter = musicexpressiontools.ConcreteInterpreter

    result = interpreter._pair_duration_sequence_elements_with_input_pair_values(
        duration_sequence, [('red', 100)])
    assert result == [(10, 'red'), (10, 'red'), (10, 'red'), (10, 'red')]

    result = interpreter._pair_duration_sequence_elements_with_input_pair_values(
        duration_sequence, [('red', 1), ('blue', 99)])

    result = interpreter._pair_duration_sequence_elements_with_input_pair_values(
        duration_sequence, [('red', 1), ('blue', 1), ('green', 98)])
    assert result == [(10, 'red'), (10, 'green'), (10, 'green'), (10, 'green')]

    result = interpreter._pair_duration_sequence_elements_with_input_pair_values(
        duration_sequence, [('red', 100), ('blue', 100), ('green', 100)])
    assert result == [(10, 'red'), (10, 'red'), (10, 'red'), (10, 'red')]
