# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.lilypondproxytools.LilyPondGrobProxy import LilyPondGrobProxy


class LilyPondGrobProxyContextWrapper(object):
    '''Context wrapper for LilyPond grob overrides.
    '''

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        from abjad import ly
        try:
            return vars(self)[name]
        except KeyError:
            if stringtools.snake_case_to_upper_camel_case(name) in \
                ly.grob_interfaces:
                vars(self)[name] = LilyPondGrobProxy()
                return vars(self)[name]
            else:
                message = 'object can have only'
                message += ' LilyPond grob attributes: "%s".'
                raise AttributeError(message % self._class_name)

    def __repr__(self):
        return '%s()' % self.__class__.__name__
