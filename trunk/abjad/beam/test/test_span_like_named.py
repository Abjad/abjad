from abjad import *
import py.test


### TODO - sure would be nice to have a single word,
###        probably a concocted neologism, to mean
###        'like-named containers'.

py.test.skip('Tests for spanned containers development.')

def test_like_named_01( ):
   v1 = Voice([Note(i, (1,8)) for i in range(4)])
   v1.invocation.name = 'myvoice'
   v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   v2.invocation.name = 'myvoice'
   t = Staff([v1, v2])
   p = Beam(t)
   assert len(p) == 1
   assert isinstance(p[0], Staff)
   assert len(p.leaves) == 8
   p.die( )
   p = Beam(t[ : ])
   assert len(p) == 2
   for x in p:
      assert isinstance(x, Voice)
   assert len(p.leaves) == 8
   r'''
   \new Staff {
      \context Voice = "myvoice" {
         c'8
         cs'8
         d'8
         ef'8
      }
      \context Voice = "myvoice" {
         e'8
         f'8
         fs'8
         g'8
      }
   }
   '''

 
def test_span_like_named_02( ):
   v1 = Voice([Note(i, (1,8)) for i in range(4)])
   v1.invocation.name = 'low'
   v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   v2.invocation.name = 'low'
   s1 = Staff([v1])
   s1.invocation.name = 'mystaff'
   s2 = Staff([v2])
   s2.invocation.name = 'mystaff'
   seq = Sequential([s1, s2])
   p = Beam(seq)
   assert len(p) == 1
   assert isinstance(p[0], Sequential)
   assert len(p.leaves) == 8
   p.die( )
   p = Beam(seq[ : ])
   assert len(p) == 2
   for x in p:
      assert isinstance(x, Staff)
   assert len(p.leaves) == 8
   r'''
   {
      \context Staff = "mystaff" {
         \context Voice = "low" {
            c'8
            cs'8
            d'8
            ef'8
         }
      }
      \context Staff = "mystaff" {
         \context Voice = "low" {
            e'8
            f'8
            fs'8
            g'8
         }
      }
   }
   '''


def test_span_like_named_03( ):
   '''Like-named containers need not be *lexically* contiguous;
      like-named containers need only be *temporally* contiguous.'''
   vl1 = Voice([Note(i, (1,8)) for i in range(4)])
   vl1.invocation.name = 'low'
   vl1.invocation.command = 'context'
   vl2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   vl2.invocation.name = 'low'
   vl2.invocation.command = 'context'
   vh1 = Voice([Note(i, (1,8)) for i in range(12,16)])
   vh1.invocation.name = 'high'
   vh1.invocation.command = 'context'
   vh2 = Voice([Note(i, (1,8)) for i in range(16,20)])
   vh2.invocation.name = 'high'
   vh2.invocation.command = 'context'
   s1 = Staff([vh1, vl1])
   s1.invocation.name = 'mystaff'
   s1.invocation.command = 'context'
   s1.brackets = 'double-angle'
   s2 = Staff([vl2, vh2])
   s2.invocation.name = 'mystaff'
   s2.invocation.command = 'context'
   s2.brackets = 'double-angle'
   seq = Sequential([s1, s2])
   p = Beam((seq[0][0], seq[1][1]))
   assert len(p) == 2
   assert isinstance(p[0], Voice)
   assert isinstance(p[1], Voice)
   assert len(p.leaves) == 8
   p.die( ) 
   p = Beam((seq[0][1], seq[1][0]))
   assert len(p) == 2
   assert isinstance(p[0], Voice)
   assert isinstance(p[1], Voice)
   assert len(p.leaves) == 8
   r'''
   {
      \context Staff = "mystaff" <<
         \context Voice = "high" {
            c''8
            cs''8
            d''8
            ef''8
         }
         \context Voice = "low" {
            c'8
            cs'8
            d'8
            ef'8
         }
      >>
      \context Staff = "mystaff" <<
         \context Voice = "low" {
            e'8
            f'8
            fs'8
            g'8
         }
         \context Voice = "high" {
            e''8
            f''8
            fs''8
            g''8
         }
      >>
   }
   '''

def test_span_like_named_04( ):
   '''Like-named containers need not be *lexically* contiguous;
      like-named containers need only be *temporally* contiguous.'''
   vl1 = Voice([Note(i, (1,8)) for i in range(4)])
   vl1.invocation.name = 'low'
   vl2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   vl2.invocation.name = 'low'
   vh = Voice([Note(i, (1,8)) for i in range(12,16)])
   vh.invocation.name = 'high'
   s1 = Staff([vh, vl1])
   s1.invocation.name = 'mystaff'
   s1.brackets = 'double-angle'
   s2 = Staff([vl2])
   s2.invocation.name = 'mystaff'
   seq = Sequential([s1, s2])
   p = Beam((vl1, vl2))
   assert len(p) == 2
   assert len(p.leaves) == 8
   p.die( )
   assert raises(ContiguityError, 'Beam((s1, s2))')
   assert raises(ContiguityError, 'Beam(seq)')
   r'''
   {
      \context Staff = "mystaff" <<
         \context Voice = "high" {
            c''8
            cs''8
            d''8
            ef''8
         }
         \context Voice = "low" {
            c'8
            cs'8
            d'8
            ef'8
         }
      >>
      \context Staff = "mystaff" {
         \context Voice = "low" {
            e'8
            f'8
            fs'8
            g'8
         }
      }
   }
   '''
