from abjad import *
import handlertools


def test_ReiteratedArticulationHandler___repr___01():

    handler = handlertools.articulations.ReiteratedArticulationHandler(
        articulation_list=['.', '^'],
        minimum_prolated_duration=Duration(1, 16),
        maximum_prolated_duration=Duration(1, 8),
        )

    assert repr(handler) == "ReiteratedArticulationHandler(articulation_list=['.', '^'], minimum_prolated_duration=Duration(1, 16), maximum_prolated_duration=Duration(1, 8))"

    assert handler._tools_package_qualified_indented_repr == "handlertools.articulations.ReiteratedArticulationHandler(\n\tarticulation_list=['.', '^'],\n\tminimum_prolated_duration=durationtools.Duration(\n\t\t1,\n\t\t16\n\t\t),\n\tmaximum_prolated_duration=durationtools.Duration(\n\t\t1,\n\t\t8\n\t\t)\n\t)"
