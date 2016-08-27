# -*- coding: utf-8 -*-
import abc
from abjad.tools import durationtools
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadObject


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

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        agent = systemtools.StorageFormatAgent(self)
        names = agent.signature_keyword_names
        for name in ('attachments',):
            if not getattr(self, name, None) and name in names:
                names.remove(name)
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_kwargs_names=names,
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
