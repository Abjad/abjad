from abjad import *
import py.test


def test_Measure_empty_01( ):
   assert py.test.raises(TypeError, 't = Measure(None, macros.scale(4))')


def test_Measure_empty_02( ):
   t = Measure((4, 4), [ ])
   assert repr(t) == 'Measure(4/4)'
   assert str(t) == '|4/4|'
   assert py.test.raises(UnderfullMeasureError, 't.format')
   assert len(t) == 0
   assert t.duration.preprolated == 0
   assert t.duration.prolated == 0
   assert not componenttools.is_well_formed_component(t)


def test_Measure_empty_03( ):
   t = Measure((4, 5), [ ])
   assert repr(t) == 'Measure(4/5)'
   assert str(t) == '|4/5|'
   assert py.test.raises(UnderfullMeasureError, 't.format')
   assert len(t) == 0
   assert t.duration.preprolated == 0
   assert t.duration.prolated == 0
   assert not componenttools.is_well_formed_component(t)
