# -*- encoding: utf-8 -*-
from abjad.tools.miditools.MetaMessage import MetaMessage


class TimeSignatureMessage(MetaMessage):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_numerator',
        '_denominator',
        '_clocks_per_tick',
        '_user_scaling',
        )

    _meta_type_char = 0x58

    ### INITIALIZER ###

    def __init__(
        self,
        numerator,
        denominator,
        clocks_per_tick,
        user_scaling=8,
        ):
        self._numerator = int(numerator)
        self._denominator = int(denominator)
        self._clocks_per_tick = int(clocks_per_tick)
        self._user_scaling = int(user_scaling)

    ### PRIVATE METHODS ###

    @classmethod
    def _from_bytes(cls, data, index=0):
        assert data[index] == cls._meta_type_char
        index += 1
        assert data[index] == 0x04
        index += 1
        (
            numerator,
            denominator,
            clocks_per_tick,
            user_scaling,
            ) = data[index:index + 4]
        index += 4
        denominator = 2 ** denominator
        message = cls(
            numerator,
            denominator,
            clocks_per_tick,
            user_scaling,
            )
        return message, index

    ### PRIVATE METHODS ###

    @property
    def numerator(self):
        return self._numerator

    @property
    def denominator(self):
        return self._denominator

    @property
    def clocks_per_tick(self):
        return self._clocks_per_tick

    @property
    def user_scaling(self):
        return self._user_scaling
