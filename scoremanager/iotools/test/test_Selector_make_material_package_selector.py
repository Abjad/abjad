# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.core.Session(is_test=True)


def test_Selector_make_material_package_selector_01():

    selector = scoremanager.iotools.Selector(session=session)
    selector = selector.make_package_selector(
        output_material_class_name='ArticulationHandler',
        )
    selector._session._is_test = True
    input_ = 'scoremanager.materials.example_articulation_handler'
    result = selector._run(pending_user_input=input_)

    package = 'scoremanager.materials.example_articulation_handler'
    assert result == package