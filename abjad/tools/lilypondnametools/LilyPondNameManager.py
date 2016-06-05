# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class LilyPondNameManager(AbjadObject):
    r'''Base class from which LilyPond grob and setting managers inherit.
    '''

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        r'''Is true when `arg` is a LilyPond name manager with attribute pairs
        equal to those of this LilyPond name manager. Otherwise false.

        Returns true or false.
        '''
        if isinstance(arg, type(self)):
            return self._get_attribute_pairs() == arg._get_attribute_pairs()
        return False

    def __getstate__(self):
        r'''Gets object state.
        '''
        import copy
        return copy.deepcopy(vars(self))

    def __hash__(self):
        r'''Hashes LilyPond name manager.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(LilyPondNameManager, self).__hash__()

    def __repr__(self):
        r'''Gets interpreter representation of LilyPond name manager.

        Returns string.
        '''
        body_string = ''
        strings = self._get_skeleton_strings()
        if strings:
            prefix = getattr(self, 'skeleton_string_prefix', '')
            strings = [x.replace(prefix, '') for x in strings]
            body_string = ', '.join(strings)
        return '{}({})'.format(type(self).__name__, body_string)

    def __setstate__(self, state):
        r'''Sets object state.
        '''
        for key, value in state.items():
            self.__dict__[key] = value

    ### PRIVATE METHODS ###

    def _get_attribute_pairs(self):
        return tuple(sorted(vars(self).items()))

    def _get_skeleton_strings(self):
        result = []
        for attribute_name, attribute_value in self._get_attribute_pairs():
            string = '{} = {}'.format(attribute_name, repr(attribute_value))
            result.append(string)
        return result
