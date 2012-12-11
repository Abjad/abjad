from abjad.tools import stringtools
from abjad.tools.lilypondproxytools.LilyPondGrobProxy import LilyPondGrobProxy


class LilyPondGrobProxyContextWrapper(object):
    '''.. versionadded:: 2.0

    Context wrapper for LilyPond grob overrides.
    '''

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        from abjad import ly
        try:
            return vars(self)[name]
        except KeyError:
            if stringtools.underscore_delimited_lowercase_to_uppercamelcase(name) in ly.grob_interfaces:
                vars(self)[name] = LilyPondGrobProxy()
                return vars(self)[name]
            else:
                raise AttributeError('object can have only LilyPond grob attributes: "%s".' %
                    self.__class__.__name__)

    def __repr__(self):
        return '%s()' % self.__class__.__name__

