from abjad import *
import handlers


def test_ReiteratedArticulationHandler___eq___01():
    
    handler_1 = handlers.articulations.ReiteratedArticulationHandler(
        articulation_list = ['.', '^'],
        minimum_prolated_duration = Duration(1, 16),
        maximum_prolated_duration = Duration(1, 8))

    handler_2 = handlers.articulations.ReiteratedArticulationHandler(
        articulation_list = ['.', '^'],
        minimum_prolated_duration = Duration(1, 16),
        maximum_prolated_duration = Duration(1, 8))

    handler_3 = handlers.articulations.ReiteratedArticulationHandler(articulation_list = ['.'])

    assert handler_1 == handler_1
    assert handler_1 == handler_2
    assert not handler_1 == handler_3
    assert handler_2 == handler_1
    assert handler_2 == handler_2
    assert not handler_2 == handler_3
    assert not handler_3 == handler_1
    assert not handler_3 == handler_2
    assert handler_3 == handler_3
