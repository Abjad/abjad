from abjad import *
import py.test


def test_Meter_compare_01( ):
   '''Meters referentially equal compare equally.
   '''

   m1 = m2 = Meter(3, 8)
   assert     m1 == m2
   assert not m1 != m2 
   assert not m1 >  m2
   assert     m1 >= m2
   assert not m1 <  m2
   assert     m1 <= m2


def test_Meter_compare_02( ):
   '''Meters equal by numerator and denominator compare equally.
   '''

   m1, m2 = Meter(3, 8), Meter(3, 8)
   assert     m1 == m2
   assert not m1 != m2 
   assert not m1 >  m2
   assert     m1 >= m2
   assert not m1 <  m2
   assert     m1 <= m2


def test_Meter_compare_03( ):
   '''Meters unequal by numerator and denominator compare unequally.
   '''
   
   m1, m2 = Meter(3, 8), Meter(6, 16)
   assert not m1 == m2
   assert     m1 != m2 
   assert not m1 >  m2
   assert     m1 >= m2
   assert not m1 <  m2
   assert     m1 <= m2


def test_Meter_compare_04( ):
   '''Meters unequal by numerator and denominator compare unequally.
   '''

   m1, m2 = Meter(3, 8), Meter(4, 8)
   assert not m1 == m2
   assert     m1 != m2 
   assert not m1 >  m2
   assert not m1 >= m2
   assert     m1 <  m2
   assert     m1 <= m2


def test_Meter_compare_05( ):
   '''Meters compare unequally with other types of object.
   '''

   m1, x = Meter(3, 8), 'foo'
   assert not m1 == x
   assert     m1 != x 
   assert py.test.raises(TypeError, 'm1 >  x')
   assert py.test.raises(TypeError, 'm1 >= x')
   assert py.test.raises(TypeError, 'm1 <  x')
   assert py.test.raises(TypeError, 'm1 >= x')
