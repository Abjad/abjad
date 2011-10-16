class _LilyPondComponentPlugIn(object):
    '''.. versionadded:: 2.0

    Shared LilyPond grob proxy and LilyPond context proxy functionality.
    '''

    def __init__(self, **kwargs):
        # note_head__color = 'red' or staff__tuplet_full_length = True
        for key, value in kwargs.iteritems():
            proxy_name, attr_name = key.split('__')
            proxy = getattr(self, proxy_name)
            setattr(proxy, attr_name, value)

    ### OVERLOADS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return self._get_attribute_tuples() == arg._get_attribute_tuples()
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        body_string = ' '
        skeleton_strings = self._get_skeleton_strings()
        if skeleton_strings:
            body_string = ', '.join(skeleton_strings)
        return '%s(%s)' % (self.__class__.__name__, body_string)
