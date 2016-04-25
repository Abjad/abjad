# -*- coding: utf-8 -*-
import abc
import inspect
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject
from abjad.tools.topleveltools import new


class QEvent(AbjadObject):
    r'''Abstract base class from which concrete ``QEvent`` subclasses
    inherit.

    Represents an attack point to be quantized.

    All ``QEvents`` possess a rational offset in milliseconds,
    and an optional index for disambiguating events which fall
    on the same offset in a ``QGrid``.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_index',
        '_offset',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, offset=0, index=None):
        offset = durationtools.Offset(offset)
        self._offset = offset
        self._index = index

    ### SPECIAL METHODS ###

    def __lt__(self, expr):
        r'''Is true when `epxr` is a q-event with offset greater than that of this
        q-event. Otherwise false.

        Returns true or false.
        '''
        if type(self) == type(self):
            if self.offset < expr.offset:
                return True
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def _repr_specification(self):
        return new(
            self._storage_format_specification,
            is_indented=False,
            )

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            keywords_ignored_when_false=(
                'attachments',
                ),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def index(self):
        r'''The optional index, for sorting QEvents with identical offsets.
        '''
        return self._index

    @property
    def offset(self):
        r'''The offset in milliseconds of the event.
        '''
        return self._offset
