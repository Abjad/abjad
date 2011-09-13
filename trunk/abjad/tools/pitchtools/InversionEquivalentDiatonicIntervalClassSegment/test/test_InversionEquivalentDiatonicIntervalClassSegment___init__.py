from abjad import *


def test_InversionEquivalentDiatonicIntervalClassSegment___init___01():

    dicg = pitchtools.InversionEquivalentDiatonicIntervalClassSegment([
        ('major', 2), ('major', 2), ('minor', 2),
        ('major', 2), ('major', 2), ('major', 2), ('minor', 2)])

    assert str(dicg) == '<M2, M2, m2, M2, M2, M2, m2>'
