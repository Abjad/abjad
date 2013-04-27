from experimental.tools.scoremanagertools.menuing.UserInputGetter import UserInputGetter


def get_articulation(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_articulation(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_articulations(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_articulations(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_direction_string(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_direction_string(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_duration(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_duration(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_dynamic(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_dynamic(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_dynamics(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_dynamics(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_hairpin_token(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_hairpin_token(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_hairpin_tokens(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_hairpin_tokens(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_integer(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_integer(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_integers(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_integers(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_lists(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_lists(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_markup(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_markup(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_named_chromatic_pitch(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_named_chromatic_pitch(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_nonnegative_integers(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_nonnegative_integers(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_nonzero_integers(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_nonzero_integers(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_positive_integer_power_of_two(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_positive_integer_power_of_two(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_positive_integers(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_positive_integers(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_string(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_string(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_strings(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_strings(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter

def get_symbolic_pitch_range_string(space_delimited_attribute_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_symbolic_pitch_range_string(space_delimited_attribute_name)
    getter.allow_none = allow_none
    return getter
