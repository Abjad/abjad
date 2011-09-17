def _format_lilypond_attribute(attribute):
    '''Return Scheme-formatted attribute.
    '''
    attribute = attribute.replace('__', " #'")
    result = attribute.replace('_', '-')
    result = "#'%s" % result
    return result
