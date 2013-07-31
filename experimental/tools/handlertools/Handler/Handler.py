# -*- encoding: utf-8 -*-
import abc
from abjad.tools import abctools


class Handler(abctools.AbjadObject):

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self._positional_argument_values == \
                other._positional_argument_values:
                if self._keyword_argument_values == \
                    other._keyword_argument_values:
                    return True
        return False

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _tools_package_name(self):
        pass

    ### PUBLIC METHODS ###

    def new(self, *args, **kwargs):
        new = type(self)(*args, **kwargs)
        return new
