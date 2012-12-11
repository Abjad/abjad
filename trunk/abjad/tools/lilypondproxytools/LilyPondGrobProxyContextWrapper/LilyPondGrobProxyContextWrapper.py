from abjad.tools import stringtools
from abjad.tools.lilypondproxytools.LilyPondGrobProxy import LilyPondGrobProxy


class LilyPondGrobProxyContextWrapper(object):
    '''.. versionadded:: 2.0

    Context wrapper for LilyPond grob overrides.
    '''

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        try:
            return vars(self)[name]
        except KeyError:
            if name in self._get_known_lilypond_grob_names():
                vars(self)[name] = LilyPondGrobProxy()
                return vars(self)[name]
            else:
                raise AttributeError('object can have only LilyPond grob attributes: "%s".' %
                    self.__class__.__name__)

    def __repr__(self):
        return '%s()' % self.__class__.__name__

    ### PRIVATE METHODS ###

    def _get_known_lilypond_grob_names(self):
        from abjad import ly
        return set([stringtools.uppercamelcase_to_underscore_delimited_lowercase(x)
            for x in ly.grob_interfaces])

