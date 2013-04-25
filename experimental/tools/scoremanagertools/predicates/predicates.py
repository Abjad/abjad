from abjad import *
import re


def is_argument_range_string(expr):
    pattern = re.compile('^(\w+( *- *\w+)?)(, *\w+( *- *\w+)?)*$')
    return pattern.match(expr) is not None

def is_articulation_token(expr):
    try:
        result = marktools.Articulation(expr)
        return isinstance(result, marktools.Articulation)
    except:
        return False

def is_available_underscore_delimited_lowercase_package_name(expr):
    from experimental.tools.scoremanagertools.core.ScoreManagementObject import ScoreManagementObject
    if stringtools.is_underscore_delimited_lowercase_package_name(expr):
        if 3 <= len(expr):
            score_management_object = ScoreManagementObject()
            return not score_management_object.package_exists(expr)
    return False

def is_boolean(expr):
    return isinstance(expr, bool)

def is_class_name_or_none(expr):
    return expr is None or stringtools.is_uppercamelcase_string(expr)

def is_clef_token(expr):
    try:
        result = contexttools.ClefMark(expr)
        return isinstance(result, contexttools.ClefMark)
    except:
        return False

def is_direction_string(expr):
    return expr in ('up', 'down')

def is_duration_token(expr):
    try:
        durationtools.Duration(expr)
        return True
    except:
        return False

def is_dynamic_token(expr):
    try:
        result = contexttools.DynamicMark(expr)
        return isinstance(result, contexttools.DynamicMark)
    except:
        return False

def is_existing_package_name(expr):
    from experimental.tools.scoremanagertools.core.ScoreManagementObject import ScoreManagementObject
    score_management_object = ScoreManagementObject()
    return score_management_object.package_exists(expr)

def is_hairpin_token(expr):
    return spannertools.HairpinSpanner.is_hairpin_token(expr)

def is_integer(expr):
    return isinstance(expr, int)

def is_integer_or_none(expr):
    return expr is None or is_integer(expr)

def is_list(expr):
    return isinstance(expr, list)

def is_markup(expr):
    return isinstance(expr, markuptools.Markup)

def is_markup_token(expr):
    try:
        result = markuptools.Markup(expr)
        return isinstance(result, markuptools.Markup)
    except:
        return False

def is_named_chromatic_pitch(expr):
    return isinstance(expr, pitchtools.NamedChromaticPitch)

def is_negative_integer(expr):
    return is_integer(expr) and expr < 0

def is_nonnegative_integer(expr):
    return is_integer(expr) and expr <= 0

def is_nonpositive_integer(expr):
    return is_integer(expr) and 0 <= expr

def is_pitch_range_or_none(expr):
    return isinstance(expr, (pitchtools.PitchRange, type(None)))

def is_positive_integer(expr):
    return is_integer(expr) and 0 < expr

def is_string(expr):
    return isinstance(expr, str)

def is_string_or_none(expr):
    return isinstance(expr, (str, type(None)))

def is_readable_argument_range_string_for_argument_list(argument_range_string, argument_list):
    from experimental.tools.scoremanagertools.menuing.MenuSection import MenuSection
    if isinstance(argument_range_string, str):
        dummy_section = MenuSection()
        dummy_section.tokens = argument_list[:]
        if dummy_section.argument_range_string_to_numbers(argument_range_string) is not None:
            return True
    return False

def is_tempo_token(expr):
    try:
        exec('from abjad import *')
        command = 'tempo_mark = contexttools.TempoMark({})'.format(expr)
        exec(command)
        return isinstance(tempo_mark, contexttools.TempoMark)
    except:
        return False

def is_underscore_delimited_lowercase_package_name(expr):
    return stringtools.is_underscore_delimited_lowercase_package_name(expr) and 3 <= len(expr)

def is_yes_no_string(expr):
    return 'yes'.startswith(expr.lower()) or 'no'.startswith(expr.lower())

def are_articulation_tokens(expr):
    if isinstance(expr, (tuple, list)):
        return all([is_articulation_token(x) for x in expr])

def are_dynamic_tokens(expr):
    if isinstance(expr, (tuple, list)):
        return all([is_dynamic_token(x) for x in expr])

def are_hairpin_tokens(expr):
    if isinstance(expr, (tuple, list)):
        return all([is_hairpin_token(x) for x in expr])

def are_lists(expr):
    if isinstance(expr, (tuple, list)):
        return all([is_list(x) for x in expr])

def are_strings(expr):
    if isinstance(expr, (tuple, list)):
        return all([is_string(x) for x in expr])
