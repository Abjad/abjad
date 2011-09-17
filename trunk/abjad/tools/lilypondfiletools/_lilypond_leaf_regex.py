# TODO: make public #
numeric_body_strings = [str(2 ** n) for n in range(8)]
other_body_strings = [r'\\breve', r'\\longa', r'\\maxima']
body_strings = numeric_body_strings + other_body_strings
body_strings = '|'.join(body_strings)
_lilypond_leaf_regex = '^([Ra-z]+)(\,*|\'*)\s*(%s)(\\.*)$' % body_strings
