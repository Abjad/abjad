# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedInversionEquivalentIntervalClassSegment___init___01():

    dicg = pitchtools.NamedInversionEquivalentIntervalClassSegment([
        ('major', 2), ('major', 2), ('minor', 2),
        ('major', 2), ('major', 2), ('major', 2), ('minor', 2)])

    assert str(dicg) == '<M2, M2, m2, M2, M2, M2, m2>'
