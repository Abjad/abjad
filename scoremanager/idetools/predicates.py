# -*- encoding: utf-8 -*-
import re
from abjad import *
from scoremanager.idetools.Configuration import Configuration
configuration = Configuration()


def is_argument_range_string(expr):
    pattern = re.compile('^(\w+( *- *\w+)?)(, *\w+( *- *\w+)?)*$')
    return pattern.match(expr) is not None

def is_articulation_token(expr):
    try:
        result = indicatortools.Articulation(expr)
        return isinstance(result, indicatortools.Articulation)
    except:
        return False

def is_boolean(expr):
    return isinstance(expr, bool)

def is_class_name_or_none(expr):
    return expr is None or stringtools.is_upper_camel_case(expr)

def is_clef_token(expr):
    try:
        result = indicatortools.Clef(expr)
        return isinstance(result, indicatortools.Clef)
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
        result = indicatortools.Dynamic(expr)
        return isinstance(result, indicatortools.Dynamic)
    except:
        return False

def is_hairpin_token(expr):
    return spannertools.Hairpin._is_hairpin_token(expr)

def is_identifier(expr, allow_spaces=False):
    if not isinstance(expr, str):
        return False
    if len(expr) < 1:
        return False
    if expr[0] in '0123456789':
        return False
    for _ in expr:
        if allow_spaces:
            if not (_.isalnum() or _ == '_' or _ == ' '):
                return False
        else:
            if not (_.isalnum() or _ == '_'):
                return False
    return True

def is_integer(expr):
    return isinstance(expr, int)

def is_integer_in_range(expr, start=None, stop=None, allow_none=False):
    if expr is None and allow_none:
        return True
    if is_integer(expr) and \
        (start is None or start <= expr) and \
        (stop is None or expr <= stop):
        return True
    return False

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

def is_named_pitch(expr):
    return isinstance(expr, NamedPitch)

def is_negative_integer(expr):
    return is_integer(expr) and expr < 0

def is_nonempty_string(expr):
    return isinstance(expr, str) and bool(expr)

def is_nonnegative_integer(expr):
    return is_integer(expr) and expr <= 0

def is_nonpositive_integer(expr):
    return is_integer(expr) and 0 <= expr

def is_page_layout_unit(expr):
    return expr in ('in', 'mm', 'cm', 'pt', 'pica')

def is_paper_dimension_string(expr):
    if not isinstance(expr, str):
        return False
    parts = expr.split()
    if not len(parts) == 4:
        return False
    width, x, height, units = parts
    try:
        float(width) 
    except ValueError:
        return False
    try:
        float(height) 
    except ValueError:
        return False
    if not x == 'x':
        return False
    if not is_page_layout_unit(units):
        return False
    return True

def is_pitch_range_or_none(expr):
    return isinstance(expr, (pitchtools.PitchRange, type(None)))

def is_positive_integer(expr):
    return is_integer(expr) and 0 < expr

def is_string(expr):
    return isinstance(expr, str)

def is_string_or_none(expr):
    return isinstance(expr, (str, type(None)))

def is_tempo_token(expr):
    import abjad
    from scoremanager import idetools
    try:
        namespace = abjad.__dict__.copy()
        command = 'tempo = indicatortools.Tempo({})'.format(expr)
        result = idetools.IOManager().execute_string(
            command,
            attribute_names=('tempo',),
            local_namespace=namespace,
            )
        tempo = result[0]
        return isinstance(tempo, indicatortools.Tempo)
    except:
        return False

def is_snake_case_package_name(expr):
    return stringtools.is_snake_case_package_name(expr)

def is_yes_no_string(expr):
    return 'yes'.startswith(expr.lower()) or 'no'.startswith(expr.lower())

def are_articulation_tokens(expr):
    if isinstance(expr, (tuple, list)):
        return all(is_articulation_token(x) for x in expr)

def are_duration_tokens(expr):
    if isinstance(expr, (tuple, list)):
        return all(is_duration_token(x) for x in expr)

def are_dynamic_tokens(expr):
    if isinstance(expr, (tuple, list)):
        return all(is_dynamic_token(x) for x in expr)

def are_hairpin_tokens(expr):
    if isinstance(expr, (tuple, list)):
        return all(is_hairpin_token(x) for x in expr)

def are_lists(expr):
    if isinstance(expr, (tuple, list)):
        return all(is_list(x) for x in expr)

def are_strings(expr):
    if isinstance(expr, (tuple, list)):
        return all(is_string(x) for x in expr)