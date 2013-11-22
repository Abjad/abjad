# -*- encoding: utf-8 -*-
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
        return self.is_left_closed and self.is_right_closed

    @property
    def is_half_closed(self):
        return not self.is_left_closed == self.is_right_closed

    @property
    def is_half_open(self):
        return not self.is_left_open == self.is_right_open

    @property
    def is_left_closed(self):
        return self._is_left_closed

    @is_left_closed.setter
    def is_left_closed(self, is_left_closed):
        assert isinstance(is_left_closed, bool), is_left_closed
        self._is_left_closed = is_left_closed

    @property
    def is_left_open(self):
        return not self.is_left_closed

    @is_left_open.setter
    def is_left_open(self, is_left_open):
        assert isinstance(is_left_open, bool), is_left_open
        self._is_left_closed = not is_left_open

    @property
    def is_open(self):
        return not self.is_left_closed and not self.is_right_closed

    @property
    def is_right_closed(self):
        return self._is_right_closed

    @is_right_closed.setter
    def is_right_closed(self, is_right_closed):
        assert isinstance(is_right_closed, bool), is_right_closed
        self._is_right_closed = is_right_closed

    @property
    def is_right_open(self):
        return not self.is_right_closed

    @is_right_open.setter
    def is_right_open(self, is_right_open):
        assert isinstance(is_right_open, bool), is_right_open
        self._is_right_closed = not is_right_open
