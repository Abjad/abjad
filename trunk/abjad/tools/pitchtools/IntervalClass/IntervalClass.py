# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools import AbjadObject


class IntervalClass(AbjadObject):
    '''Interval-class base class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __abs__(self):
        return type(self)(abs(self._number))

    def __float__(self):
        return float(self._number)

    def __hash__(self):
        return hash(repr(self))

    def __int__(self):
        return self._number

    def __repr__(self):
        return '%s(%s)' % (self._class_name, self._format_string)

    def __str__(self):
        return self._format_string

    ### PRIVATE METHODS ###

    # do not indent in storage
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        from abjad.tools import abctools
        return [''.join(
            abctools.AbjadObject._get_tools_package_qualified_repr_pieces(
                self, is_indented=False))]

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return str(self.number)

    ### PUBLIC PROPERTIES ###

    @property
    def number(self):
        return self._number
