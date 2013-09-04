# -*- encoding: utf-8 -*-
import re
from abjad.tools.pitchtools.is_diatonic_pitch_class_name \
	import diatonic_pitch_class_name_regex_body
from abjad.tools.pitchtools.OctaveIndication \
	import OctaveIndication


diatonic_pitch_name_regex_body = '''
    {}  # exactly one diatonic pitch-class name
    {}  # followed by exactly one octave tick string
    '''.format(
        diatonic_pitch_class_name_regex_body,
        OctaveIndication._octave_tick_regex_body,
        )

diatonic_pitch_name_regex = re.compile(
    '^{}$'.format(diatonic_pitch_name_regex_body),
    re.VERBOSE,
    )

def is_diatonic_pitch_name(expr):
    '''True when `expr` is a diatonic pitch name. Otherwise false:

    ::

        >>> pitchtools.is_diatonic_pitch_name("c''")
        True

    The regex ``(^[a-g,A-G])(,+|'+|)$`` underlies this predicate.

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(diatonic_pitch_name_regex.match(expr))
