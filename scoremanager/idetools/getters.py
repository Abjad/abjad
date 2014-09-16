# -*- encoding: utf-8 -*-
from scoremanager.idetools.Getter import Getter


def get_articulation(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_articulation(space_delimited_attribute_name)
    return getter

def get_articulations(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_articulations(space_delimited_attribute_name)
    return getter

def get_boolean(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_boolean(space_delimited_attribute_name)
    return getter

def get_direction_string(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_direction_string(space_delimited_attribute_name)
    return getter

def get_duration(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_duration(space_delimited_attribute_name)
    return getter

def get_durations(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_durations(space_delimited_attribute_name)
    return getter

def get_dynamic(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_dynamic(space_delimited_attribute_name)
    return getter

def get_dynamics(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_dynamics(space_delimited_attribute_name)
    return getter

def get_hairpin_token(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_hairpin_token(space_delimited_attribute_name)
    return getter

def get_hairpin_tokens(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_hairpin_tokens(space_delimited_attribute_name)
    return getter

def get_integer(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_integer(space_delimited_attribute_name)
    return getter

def get_integers(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_integers(space_delimited_attribute_name)
    return getter

def get_list(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_list(space_delimited_attribute_name)
    return getter

def get_lists(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_lists(space_delimited_attribute_name)
    return getter

def get_markup(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_markup(space_delimited_attribute_name)
    return getter

def get_named_pitch(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_named_pitch(space_delimited_attribute_name)
    return getter

def get_nonnegative_integer(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_nonnegative_integer(space_delimited_attribute_name)
    return getter

def get_nonnegative_integers(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_nonnegative_integers(space_delimited_attribute_name)
    return getter

def get_nonzero_integers(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_nonzero_integers(space_delimited_attribute_name)
    return getter

def get_number(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_number(space_delimited_attribute_name)
    return getter

def get_positive_integer_power_of_two(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_positive_integer_power_of_two(space_delimited_attribute_name)
    return getter

def get_positive_integer_powers_of_two(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_positive_integer_powers_of_two(
        space_delimited_attribute_name)
    return getter

def get_positive_integers(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_positive_integers(space_delimited_attribute_name)
    return getter

def get_string(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_string(space_delimited_attribute_name)
    return getter

def get_strings(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_strings(space_delimited_attribute_name)
    return getter

def get_pitch_range_string(
    space_delimited_attribute_name,
    session=None,
    prepopulated_value=None,
    allow_none=True,
    ):
    getter = Getter(session=session, allow_none=allow_none)
    getter.append_pitch_range_string(space_delimited_attribute_name)
    return getter