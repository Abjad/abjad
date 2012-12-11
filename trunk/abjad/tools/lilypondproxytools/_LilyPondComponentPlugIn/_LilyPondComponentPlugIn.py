import abc
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class _LilyPondComponentPlugIn(AbjadObject):
    '''.. versionadded:: 2.0

    Shared LilyPond grob proxy and LilyPond context proxy functionality.
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        # note_head__color = 'red' or staff__tuplet_full_length = True
        for key, value in kwargs.iteritems():
            proxy_name, attr_name = key.split('__')
            proxy = getattr(self, proxy_name)
            setattr(proxy, attr_name, value)

    ### SPECIAL METHODS ###

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

    ### PRIVATE METHODS ###

    def _get_known_lilypond_context_names(self):
        from abjad import ly
        return set([stringtools.uppercamelcase_to_underscore_delimited_lowercase(x)
            for x in ly.contexts])

    def _get_known_lilypond_grob_names(self):
        from abjad import ly
        return set([stringtools.uppercamelcase_to_underscore_delimited_lowercase(x)
            for x in ly.grob_interfaces])

    def _get_lilypond_grob_properties(self, grob_name):
        from abjad import ly
        grob_name = stringtools.underscore_delimited_lowercase_to_uppercamelcase(grob_name)
        properties = []
        for interface in ly.grob_interfaces[grob_name]:
            properties.extend(ly.interface_properties[interface])
        return set([x.replace('-', '_') for x in properties])
