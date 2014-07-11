# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.idetools.Session(is_test=True)


def test_Selector_make_material_package_selector_01():

    selector = scoremanager.idetools.Selector(session=session)
    selector = selector.make_package_selector(
        output_material_class_name='ReiteratedArticulationHandler',
        )
    selector._session._is_test = True
    input_ = 'blue_example_score.materials.articulation_handler'
    selector._session._pending_input = input_
    result = selector._run()

    package = 'blue_example_score.materials.articulation_handler'
    assert result == package