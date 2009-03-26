from abjad import *
import py.test


def test_navigator_is_threadable_01( ):
   '''Voice and leaves all thread.'''

   t = Voice(scale(4))

   assert t[0]._navigator._isThreadable(t[1])
   assert t[1]._navigator._isThreadable(t[2])
   assert t[2]._navigator._isThreadable(t[3])

   r'''
   \new Voice {
      c'8
      d'8
      e'8
      f'8
   }
   '''


def test_navigator_is_threadable_02( ):
   '''Staff and leaves all thread.'''

   t = Staff(scale(4))

   assert t[0]._navigator._isThreadable(t[1])
   assert t[1]._navigator._isThreadable(t[2])
   assert t[2]._navigator._isThreadable(t[3])

   r'''
   \new Staff {
      c'8
      d'8
      e'8
      f'8
   }
   '''


def test_navigator_is_threadable_03( ):
   '''Paths exist between all notes in a sequential.'''

   t = Sequential(scale(4))

   assert t[0]._navigator._isThreadable(t[1])
   assert t[1]._navigator._isThreadable(t[2])
   assert t[2]._navigator._isThreadable(t[3])

   r'''
   {
      c'8
      d'8
      e'8
      f'8
   }
   '''


def test_navigator_is_threadable_04( ):
   '''TODO: Determine the correct behavior here.
            Should paths exist between NONE of the leaves in a parallel?
            Should paths exist between ALL of the leaves in a parallel?'''
   ## [VA] None... i think. 
   ## [Baca] I tend to agree. It certainly doesn't make sense to *span* more than one component within a parallel container. But it occurs to me that _threadale_ means something subtly different than _spannable_. Without thinking through all the cases yes, I'm pretty sure that 'threadability' is a necessary (but not sufficient) condition for 'spanability'. That is, 'spanability' is a special, rarer cases of 'threadability'; or, said the other way around, 'threadability' is a more general phenomenon and 'spanability' is a more specific phenomenon. We should discuss more soon.
  
   py.test.skip("Need to figure out what it means for the contents of parallel containers to be 'threadable', 'contiguous' or 'spannable'. Come back to the test case when we're discussing parallel containers.")

   t = Parallel(scale(4))

   assert not t[0]._navigator._isThreadable(t[1])
   assert not t[1]._navigator._isThreadable(t[2])
   assert not t[2]._navigator._isThreadable(t[3])

   r'''
   <<
      c'8
      d'8
      e'8
      f'8
   >>
   '''


def test_navigator_is_threadable_05( ):
   '''Tuplets and leaves all thread.'''

   t = FixedDurationTuplet((2, 8), scale(3))

   assert t[0]._navigator._isThreadable(t[1])
   assert t[1]._navigator._isThreadable(t[0])

   assert t[1]._navigator._isThreadable(t[2])
   assert t[2]._navigator._isThreadable(t[1])

   r'''
   \times 2/3 {
      c'8
      d'8
      e'8
   }
   '''


def test_navigator_is_threadable_06( ):
   '''Voice and its noncontext contents all thread.'''

   t = Voice(Sequential(run(4)) * 2)
   diatonicize(t)

   r'''
   \new Voice {
      {
         c'8
         d'8
         e'8
         f'8
      }
      {
         g'8
         a'8
         b'8
         c''8
      }
   }
   '''

   assert t[0]._navigator._isThreadable(t[1])
   assert t[1]._navigator._isThreadable(t[0])

   assert t[0]._navigator._isThreadable(t[1][0])
   assert t[0]._navigator._isThreadable(t[1][1])
   assert t[0]._navigator._isThreadable(t[1][2])
   assert t[0]._navigator._isThreadable(t[1][3])
   assert t[1]._navigator._isThreadable(t[0][0])
   assert t[1]._navigator._isThreadable(t[0][1])
   assert t[1]._navigator._isThreadable(t[0][2])
   assert t[1]._navigator._isThreadable(t[0][3])


def test_navigator_is_threadable_07( ):
   '''Voice and its noncontext contents all thread.'''

   t1 = FixedDurationTuplet((2, 8), [Note(i, (1, 8)) for i in range(3)])
   t2 = FixedDurationTuplet((2, 8), [Note(i, (1, 8)) for i in range(3, 6)])
   t = Voice([t1, t2])

   assert t[0]._navigator._isThreadable(t[1])
   assert t[1]._navigator._isThreadable(t[0])

   assert t[0]._navigator._isThreadable(t[1][0])
   assert t[0]._navigator._isThreadable(t[1][1])
   assert t[0]._navigator._isThreadable(t[1][2])
   assert t[1]._navigator._isThreadable(t[0][0])
   assert t[1]._navigator._isThreadable(t[0][1])
   assert t[1]._navigator._isThreadable(t[0][2])

   r'''
   \new Voice {
      \times 2/3 {
         c'8
         cs'8
         d'8
      }
      \times 2/3 {
         ef'8
         e'8
         f'8
      }
   }
   '''


def test_navigator_is_threadable_08( ):
   '''Can not thread across differently identified anonymous voices.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   t = Staff([v1, v2])

   assert not t[0]._navigator._isThreadable(t[1])
   assert not t[1]._navigator._isThreadable(t[0])
   assert not t[0][0]._navigator._isThreadable(t[1][0])
   assert not t[1][0]._navigator._isThreadable(t[0][-1])

   assert v1[0]._navigator._isThreadable(v1[1])
   assert v1[1]._navigator._isThreadable(v1[2])
   assert v1[2]._navigator._isThreadable(v1[3])

   assert v2[0]._navigator._isThreadable(v2[1])
   assert v2[1]._navigator._isThreadable(v2[2])
   assert v2[2]._navigator._isThreadable(v2[3])

   r'''
   \new Staff {
      \new Voice {
         c'8
         cs'8
         d'8
         ef'8
      }
      \new Voice {
         e'8
         f'8
         fs'8
         g'8
      }
   }
   '''


def test_navigator_is_threadable_09( ):
   '''Can thread across like-named voices.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v1.invocation.name = 'foo'
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   v2.invocation.name = 'foo'
   t = Staff([v1, v2])

   assert t[0]._navigator._isThreadable(t[1])
   assert t[1]._navigator._isThreadable(t[0])

   assert t[0]._navigator._isThreadable(t[1][0])
   assert t[0]._navigator._isThreadable(t[1][1])
   assert t[0]._navigator._isThreadable(t[1][2])
   assert t[0]._navigator._isThreadable(t[1][3])
   assert t[1]._navigator._isThreadable(t[0][0])
   assert t[1]._navigator._isThreadable(t[0][1])
   assert t[1]._navigator._isThreadable(t[0][2])
   assert t[1]._navigator._isThreadable(t[0][3])

   r'''
   \new Staff {
      \context Voice = "foo" {
         c'8
         cs'8
         d'8
         ef'8
      }
      \context Voice = "foo" {
         e'8
         f'8
         fs'8
         g'8
      }
   }
   '''


def test_navigator_is_threadable_10( ):
   '''Can not thread across differently named voices.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v1.invocation.name = 'foo'
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   v2.invocation.name = 'bar'
   t = Staff([v1, v2])

   assert not t[0]._navigator._isThreadable(t[1])
   assert not t[1]._navigator._isThreadable(t[0])

   r'''
   \new Staff {
      \context Voice = "foo" {
         c'8
         cs'8
         d'8
         ef'8
      }
      \context Voice = "bar" {
         e'8
         f'8
         fs'8
         g'8
      }
   }
   '''


def test_navigator_is_threadable_11( ):
   '''Can not thread across differently identified anonymous voices.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   s1 = Staff([v1])
   s2 = Staff([v2])
   seq = Sequential([s1, s2])
   
   assert not seq[0]._navigator._isThreadable(seq[1])
   assert not seq[1]._navigator._isThreadable(seq[0])

   assert not seq[0][0]._navigator._isThreadable(seq[1][0])
   assert not seq[1][0]._navigator._isThreadable(seq[0][0])

   assert not seq[0]._navigator._isThreadable(seq[0][0])
   assert not seq[0]._navigator._isThreadable(seq[1][0])
   assert not seq[1]._navigator._isThreadable(seq[0][0])
   assert not seq[1]._navigator._isThreadable(seq[1][0])

   r'''
   {
      \new Staff {
         \new Voice {
            c'8
            cs'8
            d'8
            ef'8
         }
      }
      \new Staff {
         \new Voice {
            e'8
            f'8
            fs'8
            g'8
         }
      }
   }
   '''   


def test_navigator_is_threadable_12( ):
   '''Can not thread across differently identified anonymous voices.'''

   vl1 = Voice([Note(i, (1, 8)) for i in range(4)])
   vl2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   vh1 = Voice([Note(i, (1, 8)) for i in range(12, 16)])
   vh2 = Voice([Note(i, (1, 8)) for i in range(16, 20)])
   s1 = Staff([vh1, vl1])
   #s1.brackets = 'double-angle'
   s1.parallel = True
   s2 = Staff([vl2, vh2])
   #s2.brackets = 'double-angle'
   s2.parallel = True
   seq = Sequential([s1, s2])

   assert not seq[0]._navigator._isThreadable(seq[1])
   assert not seq[0]._navigator._isThreadable(seq[1][0])
   assert not seq[0]._navigator._isThreadable(seq[1][0][0])
   assert not seq[0]._navigator._isThreadable(seq[1][1])
   assert not seq[0]._navigator._isThreadable(seq[1][1][0])

   assert not seq[0][0]._navigator._isThreadable(seq[1])
   assert not seq[0][0]._navigator._isThreadable(seq[1][0])
   assert not seq[0][0]._navigator._isThreadable(seq[1][0][0])
   assert not seq[0][0]._navigator._isThreadable(seq[1][1])
   assert not seq[0][0]._navigator._isThreadable(seq[1][1][0])

   assert not seq[0][0][-1]._navigator._isThreadable(seq[1])
   assert not seq[0][0][-1]._navigator._isThreadable(seq[1][0])
   assert not seq[0][0][-1]._navigator._isThreadable(seq[1][0][0])
   assert not seq[0][0][-1]._navigator._isThreadable(seq[1][1])
   assert not seq[0][0][-1]._navigator._isThreadable(seq[1][1][0])

   assert not seq[0][1]._navigator._isThreadable(seq[1])
   assert not seq[0][1]._navigator._isThreadable(seq[1][0])
   assert not seq[0][1]._navigator._isThreadable(seq[1][0][0])
   assert not seq[0][1]._navigator._isThreadable(seq[1][1])
   assert not seq[0][1]._navigator._isThreadable(seq[1][1][0])

   assert not seq[0][1][-1]._navigator._isThreadable(seq[1])
   assert not seq[0][1][-1]._navigator._isThreadable(seq[1][0])
   assert not seq[0][1][-1]._navigator._isThreadable(seq[1][0][0])
   assert not seq[0][1][-1]._navigator._isThreadable(seq[1][1])
   assert not seq[0][1][-1]._navigator._isThreadable(seq[1][1][0])

   r'''
   {
      \new Staff <<
         \new Voice {
            c''8
            cs''8
            d''8
            ef''8
         }
         \new Voice {
            c'8
            cs'8
            d'8
            ef'8
         }
      >>
      \new Staff <<
         \new Voice {
            e'8
            f'8
            fs'8
            g'8
         }
         \new Voice {
            e''8
            f''8
            fs''8
            g''8
         }
      >>
   }
   '''


def test_navigator_is_threadable_13( ):
   '''Voice threads its noncontext contents.'''

   s1 = Sequential([Note(i, (1, 8)) for i in range(4)])
   s1 = Sequential([s1])
   s2 = Sequential([Note(i, (1, 8)) for i in range(4, 8)])
   s2 = Sequential([s2])
   t = Voice([s1, s2])

   r'''
   \new Voice {
      {
         {
            c'8
            cs'8
            d'8
            ef'8
         }
      }
      {
         {
            e'8
            f'8
            fs'8
            g'8
         }
      }
   }
   '''

   assert t[0]._navigator._isThreadable(t[1])
   assert t[0]._navigator._isThreadable(t[1][0])
   assert t[0]._navigator._isThreadable(t[1][0][0])
   
   assert t[0][0]._navigator._isThreadable(t[1])
   assert t[0][0]._navigator._isThreadable(t[1][0])
   assert t[0][0]._navigator._isThreadable(t[1][0][0])
   
   assert t[0][0][-1]._navigator._isThreadable(t[1])
   assert t[0][0][-1]._navigator._isThreadable(t[1][0])
   assert t[0][0][-1]._navigator._isThreadable(t[1][0][0])


def test_navigator_is_threadable_14( ):
   '''Like-named staves thread.'''

   t = Sequential(Staff([ ]) * 2)
   t[0].invocation.name = 'foo'
   t[1].invocation.name = 'foo'

   r'''
   {
      \context Staff = "foo" {
      }
      \context Staff = "foo" {
      }
   }
   '''

   assert t[0]._navigator._isThreadable(t[1])
   assert t[1]._navigator._isThreadable(t[0])


def test_navigator_is_threadable_15( ):
   '''Like-named staves thread.
      Leaves in differently IMPLICIT voices do not thread.'''

   t = Sequential(Staff(run(4)) * 2)
   t[0].invocation.name = 'foo'
   t[1].invocation.name = 'foo'
   diatonicize(t)

   r'''
   {
      \context Staff = "foo" {
         c'8
         d'8
         e'8
         f'8
      }
      \context Staff = "foo" {
         g'8
         a'8
         b'8
         c''8
      }
   }
   '''

   assert t[0]._navigator._isThreadable(t[1])
   assert t[1]._navigator._isThreadable(t[0])

   assert not t[0][0]._navigator._isThreadable(t[1][0])
   assert not t[1][0]._navigator._isThreadable(t[0][1])


def test_navigator_is_threadable_16( ):
   '''Can thread across like-named voices in like-named staves.'''

   t = Sequential(Staff([Voice(run(4))]) * 2)
   t[0].invocation.name = 'staff'
   t[0][0].invocation.name = 'voice'
   t[1].invocation.name = 'staff'
   t[1][0].invocation.name = 'voice'
   diatonicize(t)

   r'''{
           \context Staff = "staff" {
                   \context Voice = "voice" {
                           c'8
                           d'8
                           e'8
                           f'8
                   }
           }
           \context Staff = "staff" {
                   \context Voice = "voice" {
                           g'8
                           a'8
                           b'8
                           c''8
                   }
           }
   }'''

   leaves = t.leaves

   assert leaves[0]._navigator._isThreadable(leaves[1])
   assert leaves[0]._navigator._isThreadable(leaves[4])

   assert leaves[4]._navigator._isThreadable(leaves[0])
   assert leaves[4]._navigator._isThreadable(leaves[7])


def test_navigator_is_threadable_17( ):
   '''Can thread across like-named voices.
      But can NOT thread across differently identified anonymous staves.'''

   t = Sequential(Staff([Voice(run(4))]) * 2)
   t[0][0].invocation.name = 'voice'
   t[1][0].invocation.name = 'voice'
   diatonicize(t)

   r'''{
           \new Staff {
                   \context Voice = "voice" {
                           c'8
                           d'8
                           e'8
                           f'8
                   }
           }
           \new Staff {
                   \context Voice = "voice" {
                           g'8
                           a'8
                           b'8
                           c''8
                   }
           }
   }'''

   leaves = t.leaves

   assert leaves[0]._navigator._isThreadable(leaves[1])
   assert not leaves[0]._navigator._isThreadable(leaves[4])

   assert not leaves[4]._navigator._isThreadable(leaves[0])
   assert leaves[4]._navigator._isThreadable(leaves[7])


def test_navigator_is_threadable_18( ):
   '''Like-named voices thread.'''

   t = Sequential(Voice(run(4)) * 2)
   t[0].invocation.name = 'foo'
   t[1].invocation.name = 'foo'
   diatonicize(t)

   r'''
   {
      \context Voice = "foo" {
         c'8
         d'8
         e'8
         f'8
      }
      \context Voice = "foo" {
         g'8
         a'8
         b'8
         c''8
      }
   }
   '''

   assert t[0]._navigator._isThreadable(t[1])
   assert t[1]._navigator._isThreadable(t[0])

   assert t[0][0]._navigator._isThreadable(t[1][0])
   assert t[1][0]._navigator._isThreadable(t[0][1])


def test_navigator_is_threadable_19( ):
   '''Can not thread from differently identified 
      anonymous and implicit voices.'''

   t = Staff(run(4))
   t.insert(2, Voice(run(2)))
   diatonicize(t)

   r'''\new Staff {
      c'8
      d'8
      \new Voice {
         e'8
         f'8
      }
      g'8
      a'8
   }'''

   assert t[0]._navigator._isThreadable(t[1])
   assert not t[0]._navigator._isThreadable(t[2][0])
   assert t[0]._navigator._isThreadable(t[3])

   assert not t[2][0]._navigator._isThreadable(t[0])
   assert t[2][0]._navigator._isThreadable(t[2][1])
   assert not t[2][0]._navigator._isThreadable(t[3])


def test_navigator_is_threadable_20( ):
   '''Like-named voices thread.'''

   v1 = Voice(run(4))
   v2 = Voice(run(4))
   v1.invocation.name = v2.invocation.name = 'voiceOne'
   t = Parallel([Sequential([v1, v2])])
   diatonicize(t)

   r'''
   <<
           {
                   \context Voice = "voiceOne" {
                           c'8
                           d'8
                           e'8
                           f'8
                   }
                   \context Voice = "voiceOne" {
                           g'8
                           a'8
                           b'8
                           c''8
                   }
           }
   >>
   '''
   assert v1._navigator._isThreadable(v2)
   for n1, n2 in zip(t.leaves[0:-1], t.leaves[1:]):
      assert n1._navigator._isThreadable(n2)


def test_navigator_is_threadable_21( ):
   '''Like-named voices thread.'''

   v1 = Voice(run(4))
   v2 = Voice(run(4))
   v1.invocation.name = v2.invocation.name = 'voiceOne'
   t = Sequential([Parallel([v1]), Parallel([v2])])
   diatonicize(t)

   r'''
   {
           <<
                   \context Voice = "voiceOne" {
                           c'8
                           d'8
                           e'8
                           f'8
                   }
           >>
           <<
                   \context Voice = "voiceOne" {
                           g'8
                           a'8
                           b'8
                           c''8
                   }
           >>
   }
   '''

   assert v1._navigator._isThreadable(v2)
   for n1, n2 in zip(t.leaves[0:-1], t.leaves[1:]):
      assert n1._navigator._isThreadable(n2)


def test_navigator_is_threadable_22( ):
   '''Like-named voices in like-named staves thread.'''

   v1 = Voice(run(4))
   v2 = Voice(run(4))
   v1.invocation.name = v2.invocation.name = 'voiceOne'
   s1 = Staff([v1])
   s2 = Staff([v2])
   s1.invocation.name = s2.invocation.name = 'staffOne'
   #s1.brackets = 'double-angle'
   #s2.brackets = 'double-angle'
   s1.parallel = True
   s2.parallel = True
   t = Sequential([s1, s2])
   diatonicize(t)

   r'''
   {
           \context Staff = "staffOne" <<
                   \context Voice = "voiceOne" {
                           c'8
                           d'8
                           e'8
                           f'8
                   }
           >>
           \context Staff = "staffOne" <<
                   \context Voice = "voiceOne" {
                           g'8
                           a'8
                           b'8
                           c''8
                   }
           >>
   }
   '''

   assert v1._navigator._isThreadable(v2)
   assert s1._navigator._isThreadable(s2)
   for n1, n2 in zip(t.leaves[0:-1], t.leaves[1:]):
      assert n1._navigator._isThreadable(n2)


def test_navigator_is_threadable_23( ):
   '''Like-name staff groups thread.'''

   t = Sequential([StaffGroup([ ]), StaffGroup([ ])])
   t[0].invocation.name = t[1].invocation.name = 'staffGroup'

   r'''{
           \context StaffGroup = "staffGroup" <<
           >>
           \context StaffGroup = "staffGroup" <<
           >>
   }
   '''

   assert t[0]._navigator._isThreadable(t[1])


def test_navigator_is_threadable_24( ):
   r'''Sequentials and leaves here all inhabit the same implicit voice.
      All components thread.'''

   t = Sequential(Sequential(run(4)) * 2)
   appictate(t)

   assert t[0][-1]._navigator._isThreadable(t[1][0])
   assert t[1][0]._navigator._isThreadable(t[0][-1])

   r'''{
      {
         c'8
         cs'8
         d'8
         ef'8
      }
      {
         e'8
         f'8
         fs'8
         g'8
      }
   }'''

   
def test_navigator_is_threadable_25( ):
   '''Differently identified anonymous voices do not thread.'''

   t = Sequential(Voice(run(4)) * 2)
   appictate(t)

   assert not t[0][-1]._navigator._isThreadable(t[1][0])
   assert not t[1][0]._navigator._isThreadable(t[0][-1])

   r'''{
      \new Voice {
         c'8
         cs'8
         d'8
         ef'8
      }
      \new Voice {
         e'8
         f'8
         fs'8
         g'8
      }
   }'''


def test_navigator_is_threadable_26( ):
   '''Differently identified anonymous voices do not thread.
      Differently identified anonymous staves do not thread.'''

   t = Sequential(Staff([Voice(run(4))]) * 2)
   appictate(t)
   
   assert not t[0][0][-1]._navigator._isThreadable(t[1][0][0])
   assert not t[1][0][0]._navigator._isThreadable(t[0][0][-1])

   assert not t[0][0]._navigator._isThreadable(t[1][0])
   assert not t[1][0]._navigator._isThreadable(t[0][0])

   assert not t[0]._navigator._isThreadable(t[1])
   assert t[0]._navigator._isThreadable(t[0])

   r'''{
      \new Staff {
         \new Voice {
            c'8
            cs'8
            d'8
            ef'8
         }
      }
      \new Staff {
         \new Voice {
            e'8
            f'8
            fs'8
            g'8
         }
      }
   }'''
