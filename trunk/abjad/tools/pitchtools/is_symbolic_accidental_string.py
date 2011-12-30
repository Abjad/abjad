import re


symbolic_accidental_string_regex_body = """
    ([#]{1,2}       # # or ## for sharp or double sharp
    |[b]{1,2}       # or b or bb for flat or double flat
    |[#]?[+]        # or + or #+ for qs and tqs
    |[b]?[~]        # or ~ and b~ for qf and tqf
    |               # or empty string for no symbolic string
    )
    """

symbolic_accidental_string_regex = re.compile('^%s$' % symbolic_accidental_string_regex_body, re.VERBOSE)

def is_symbolic_accidental_string(expr):
    '''.. versionadded:: 2.5

    True when `expr` is a symbolic accidental string. Otherwise false::

        abjad> pitchtools.is_symbolic_accidental_string('#+')
        True

    True on empty string.

    The regex ``^([#]{1,2}|[b]{1,2}|[#]?[+]|[b]?[~]|)$`` underlies this predicate.

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(symbolic_accidental_string_regex.match(expr))
