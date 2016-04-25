# -*- coding: utf-8 -*-
import random
from abjad import *


def test_selectortools_Selector_run_selectors_01():

    staff = Staff("c'4 d'8 e'8 f'4 g'8 a'4 b'8 c'8")

    selector = selectortools.Selector()
    logical_tie_selector = selector.by_logical_tie()
    pitched_selector = logical_tie_selector.by_pitch('C4')
    duration_selector = logical_tie_selector.by_duration('==', (1, 8))
    contiguity_selector = duration_selector.by_contiguity()

    selectors = [
        selector,
        logical_tie_selector,
        pitched_selector,
        duration_selector,
        contiguity_selector,
        ]

    all_results = []

    for _ in range(10):
        result = selectortools.Selector.run_selectors(staff, selectors)
        all_results.append(result)
        random.shuffle(selectors)

    for result in all_results:
        assert len(result) == 5
        assert selector in result
        assert logical_tie_selector in result
        assert pitched_selector in result
        assert duration_selector in result
        assert contiguity_selector in result

    iterator = sequencetools.iterate_sequence_nwise(all_results)
    for results_one, results_two in iterator:
        for selector in selectors:
            assert results_one[selector] == results_two[selector]
