# -*- encoding: utf-8 -*-
import abc
import re
from abjad.tools.abctools import AbjadObject


class Check(AbjadObject):

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### PRIVATE PROPERTIES ###

    @property
    def _message(self):
        name = type(self).__name__
        parts = re.findall("[A-Z][a-z]*", name)
        parts = parts[:-1]
        return ' '.join([p.lower() for p in parts])

    ### PRIVATE METHODS ###

    @staticmethod
    def _list_checks():
        r'''List checks:

        ::

            >>> for check in wellformednesstools.Check._list_checks():
            ...     check
            BeamedQuarterNoteCheck()
            DiscontiguousSpannerCheck()
            DuplicateIdCheck()
            EmptyContainerCheck()
            IntermarkedHairpinCheck()
            MisduratedMeasureCheck()
            MisfilledMeasureCheck()
            MispitchedTieCheck()
            MisrepresentedFlagCheck()
            MissingParentCheck()
            NestedMeasureCheck()
            OverlappingBeamCheck()
            OverlappingGlissandoCheck()
            OverlappingOctavationCheck()
            ShortHairpinCheck()

        Returns list of checks.
        '''
        from abjad.tools import wellformednesstools
        result = []
        for name in dir(wellformednesstools):
            if not name in ('Check', 'WellformednessManager'):
                if name[0].isupper():
                    exec('check = wellformednesstools.{}()'.format(name))
                    result.append(check)
        return result

    @abc.abstractmethod
    def _run(self, expr):
        raise NotImplemented

    ### PUBLIC METHODS ###

    def check(self, expr):
        return not self.violators(expr)

    def report(self, expr):
        violators, total = self._run(expr)
        bad = len(violators)
        line = '%4d / %4d %s' % (bad, total, self._message)
        return line

    def violators(self, expr):
        violators, total = self._run(expr)
        return violators
