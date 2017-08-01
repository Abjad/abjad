# -*- coding: utf-8 -*-
import copy
#from abjad.tools.abctools.AbjadObject import AbjadObject


#class LilyPondNameManager(AbjadObject):
class LilyPondNameManager(object):
    r'''LilyPond name manager.
    
    Base class from which grob, context setting and tweak managers inherit.
    '''

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is a LilyPond name manager with attribute
        pairs equal to those of this LilyPond name manager. Otherwise false.

        Returns true or false.
        '''
        if isinstance(argument, type(self)):
            attribute_pairs_1 = self._get_attribute_pairs()
            attribute_pairs_2 = argument._get_attribute_pairs()
            return attribute_pairs_1 == attribute_pairs_2
        return False

    def __getstate__(self):
        r'''Gets object state.
        '''
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
        pairs = self._get_attribute_pairs()
        pairs = [str(_) for _ in pairs]
        body_string = ''.join(pairs)
        return '{}({})'.format(type(self).__name__, body_string)

    def __setstate__(self, state):
        r'''Sets object state.
        '''
        for key, value in state.items():
            self.__dict__[key] = value

    ### PRIVATE METHODS ###

    def _get_attribute_pairs(self):
        return tuple(sorted(vars(self).items()))
