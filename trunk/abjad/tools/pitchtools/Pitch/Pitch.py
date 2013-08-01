# -*- encoding: utf-8 -*-
import abc

from abjad.tools.abctools.SortableAttributeEqualityAbjadObject \
	import SortableAttributeEqualityAbjadObject


class Pitch(SortableAttributeEqualityAbjadObject):
    '''Pitch base class.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ('_format_string', )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __abs__(self):
        raise NotImplementedError(
            'TODO: all pitch-related classes must implement abs.')

    def __float__(self):
        raise NotImplementedError(
            'TODO: all pitch-related classes must implement float.')

    def __hash__(self):
        return hash(repr(self))

    def __int__(self):
        raise NotImplementedError(
            'TODO: all pitch-related classes must implement int.')

    def __repr__(self):
        return '%s(%s)' % (self._class_name, self._format_string)
