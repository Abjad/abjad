# -*- coding: utf-8 -*-
import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class BoundedObject(AbjadObject):
    r'''Bounded object mix-in.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC PROPERTIES ###

    @property
    def is_closed(self):
        r'''Is true when left closed and right closed. Otherwise false.

        Returns true or false.
        '''
        return self.is_left_closed and self.is_right_closed

    @property
    def is_half_closed(self):
        r'''Is true when left closed xor right closed.

        Returns true or false.
        '''
        return not self.is_left_closed == self.is_right_closed

    @property
    def is_half_open(self):
        r'''Is true when left and right open are not the same. Otherwise false.

        Return boolean.
        '''
        return not self.is_left_open == self.is_right_open

    @property
    def is_left_closed(self):
        r'''Is true when left closed. Otherwise false.

        Returns true or false.
        '''
        return self._is_left_closed

    @is_left_closed.setter
    def is_left_closed(self, is_left_closed):
        assert isinstance(is_left_closed, bool), is_left_closed
        self._is_left_closed = is_left_closed

    @property
    def is_left_open(self):
        r'''Is true when left open. Otherwise false.

        Returns true or false.
        '''
        return not self.is_left_closed

    @is_left_open.setter
    def is_left_open(self, is_left_open):
        assert isinstance(is_left_open, bool), is_left_open
        self._is_left_closed = not is_left_open

    @property
    def is_open(self):
        r'''Is true when left or right open. Otherwise false.

        Returns true or false.
        '''
        return not self.is_left_closed and not self.is_right_closed

    @property
    def is_right_closed(self):
        r'''Is true when right closed. Otherwise false.

        Returns true or false.
        '''
        return self._is_right_closed

    @is_right_closed.setter
    def is_right_closed(self, is_right_closed):
        assert isinstance(is_right_closed, bool), is_right_closed
        self._is_right_closed = is_right_closed

    @property
    def is_right_open(self):
        r'''Is true when right open. Otherwise false.

        Returns true or false.
        '''
        return not self.is_right_closed

    @is_right_open.setter
    def is_right_open(self, is_right_open):
        assert isinstance(is_right_open, bool), is_right_open
        self._is_right_closed = not is_right_open
