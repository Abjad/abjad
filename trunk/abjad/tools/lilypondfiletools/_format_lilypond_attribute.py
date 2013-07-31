# TODO: make public and move somewhere, perhaps to stringtools
def _format_lilypond_attribute(attribute):
    r'''Return Scheme-formatted attribute.
    '''
    attribute = attribute.replace('__', " #'")
    result = attribute.replace('_', '-')
    result = "#'%s" % result
    return result
