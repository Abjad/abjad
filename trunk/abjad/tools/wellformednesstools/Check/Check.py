from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.abctools import AbjadObject
import re


class Check(AbjadObject):
    
    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### READ-ONLY PRIVATE ATTRIBUTES ###

    @property
    def _message(self):
        name = self.__class__.__name__
        parts = re.findall("[A-Z][a-z]*", name)
        parts = parts[:-1]
        return ' '.join([p.lower( ) for p in parts])

    ### PRIVATE METHODS ###

    @abstractmethod
    def _run(self, expr):
        raise NotImplemented

    ### PUBLIC METHODS ###

    def check(self, expr):
        return not self.violators(expr)

    def report(self, expr):
        violators, total = self._run(expr)
        bad = len(violators)
        print '%4d / %4d %s' % (bad, total, self._message)

    def violators(self, expr):
        violators, total = self._run(expr)
        return violators
