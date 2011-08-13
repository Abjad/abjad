from abjad.core import _StrictComparator
import re


class _Check(_StrictComparator):

    def __init__(self):
        pass

    ### PRIVATE ATTRIBUTES ###

    @property
    def _message(self):
        name = self.__class__.__name__
        parts = re.findall("[A-Z][a-z]*", name)
        parts = parts[:-1]
        return ' '.join([p.lower( ) for p in parts])

    ### PUBLIC ATTRIBUTES ###

    def check(self, expr):
        return not self.violators(expr)

    def report(self, expr):
        violators, total = self._run(expr)
        bad = len(violators)
        print '%4d / %4d %s' % (bad, total, self._message)

    def violators(self, expr):
        violators, total = self._run(expr)
        return violators
