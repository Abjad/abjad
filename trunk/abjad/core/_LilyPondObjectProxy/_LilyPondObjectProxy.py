class _LilyPondObjectProxy(object):
    '''.. versionadded:: 2.0

    Shared LilyPond grob proxy and LilyPond context proxy functionality.
    '''

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    ### OVERLOADS ###

    def __copy__(self):
        return eval(repr(self))

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return self._get_attribute_pairs() == arg._get_attribute_pairs()
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        #body_string = ' '
        body_string = ''
        skeleton_strings = self._get_skeleton_strings()
        if skeleton_strings:
            body_string = ', '.join(skeleton_strings)
        return '%s(%s)' % (self.__class__.__name__, body_string)

    ### PRIVATE METHODS ###

    def _get_attribute_pairs(self):
        return tuple(vars(self).iteritems())

    def _get_skeleton_strings(self):
        result = []
        for attribute_name, attribute_value in self._get_attribute_pairs():
            result.append('%s = %s' % (attribute_name, repr(attribute_value)))
        return result
