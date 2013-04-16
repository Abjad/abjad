from abjad import *
from experimental import *


def test_UserInputWrapper_public_attributes_01():

    wrapper = scoremanagementtools.editors.UserInputWrapper()
    wrapper['flavor'] = 'cherry'
    wrapper['duration'] = Duration(1, 4)

    assert wrapper.editable_lines == ["flavor: 'cherry'", 'duration: Duration(1, 4)']
    assert wrapper.formatted_lines == ['user_input_wrapper = UserInputWrapper([', "\t('flavor', 'cherry'),", "\t('duration', durationtools.Duration(1, 4))])"]
    assert wrapper.is_complete
    assert not wrapper.is_empty
    assert not wrapper.is_partially_complete
    assert wrapper.user_input_module_import_statements == ['from experimental.tools.scoremanagementtools.editors import UserInputWrapper']

    assert wrapper.list_items() == [('flavor', 'cherry'), ('duration', Duration(1, 4))]
    assert wrapper.list_keys() == ['flavor', 'duration']
    assert wrapper.list_values() == ['cherry', Duration(1, 4)]


def test_UserInputWrapper_public_attributes_02():

    wrapper = scoremanagementtools.editors.UserInputWrapper()

    assert wrapper.editable_lines == []
    assert wrapper.formatted_lines == ['user_input_wrapper = UserInputWrapper([])']
    assert wrapper.is_complete
    assert wrapper.is_empty
    assert not wrapper.is_partially_complete
    assert wrapper.user_input_module_import_statements == ['from experimental.tools.scoremanagementtools.editors import UserInputWrapper']

    assert wrapper.list_items() == []
    assert wrapper.list_keys() == []
    assert wrapper.list_values() == []
