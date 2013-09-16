# -*- encoding: utf-8 -*-


def format_lilypond_attribute(attribute):
    r'''Formats LilyPond attribute according to Scheme formatting conventions.

    Returns string.
    '''
    attribute = attribute.replace('__', " #'")
    result = attribute.replace('_', '-')
    result = "#'%s" % result
    return result
