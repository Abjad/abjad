# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class LilyPondEvent(AbjadObject):
    r'''Model of an arbitrary event in LilyPond.

    Not composer-safe.

    Used internally by LilyPondParser.
    '''

    ### INITIALIZER ###

    def __init__(self, name=None, **kwargs):
        self.name = name
        for k, v in kwargs.items():
            if k != 'name':
                setattr(self, k, v)

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of LilyPond event.

        Returns string.
        '''
        return '{}({})'.format(type(self).__name__, self._format_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        result = repr(self.name)
        for key in self.__dict__:
            if key == 'name':
                continue
            result += ', {} = {!r}'.format(key, getattr(self, key))
        return result