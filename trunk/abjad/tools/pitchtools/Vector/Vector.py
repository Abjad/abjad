# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class Vector(dict, AbjadObject):
    '''Music theoretic vector base class.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass
