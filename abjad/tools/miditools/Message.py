# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Message(AbjadValueObject):
    '''
    MIDI track message.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass
