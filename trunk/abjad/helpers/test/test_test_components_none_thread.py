from abjad.component.component import _Component
from abjad.helpers.test_components import _test_components
from abjad import *
import py.test


def test_test_components_none_thread_01( ):
   '''Unincorporated leaves do not thread.
      Unicorporated leaves do not share a root component.
      False if not allow orphans; True if allow orphans.'''

   assert _test_components(scale(4), share = 'thread')
   assert not _test_components(scale(4), share = 'thread', 
      allow_orphans = False)


def test_test_components_none_thread_02( ):
   '''Sequential and leaves all thread.'''

   t = Sequential(scale(4))

   r'''{
      c'8
      d'8
      e'8
      f'8
   }'''

   assert _test_components(list(iterate(t, _Component)), share = 'thread')


def test_test_components_none_thread_03( ):
   '''Tuplet and leaves all thread.'''
   
   t = FixedDurationTuplet((2, 8), scale(3))
   
   r'''\times 2/3 {
      c'8
      d'8
      e'8
   }'''

   assert _test_components(list(iterate(t, _Component)), share = 'thread')


def test_test_components_none_thread_04( ):
   '''Parallel and leaves all currently thread.
      TODO: What the hell is the right behavior here?'''

   t = Parallel(scale(4))

   r'''<<
      c'8
      d'8
      e'8
      f'8
   >>'''

   assert _test_components(list(iterate(t, _Component)), share = 'thread')


def test_test_components_none_thread_05( ):
   '''Voice and leaves all thread.'''

   t = Voice(scale(4))

   r'''\new Voice {
      c'8
      d'8
      e'8
      f'8
   }'''

   assert _test_components(list(iterate(t, _Component)), share = 'thread')


def test_test_components_none_thread_06_trev( ):
   '''Anonymous staff and leaves all thread.'''

   py.test.skip('Unvoiced notes inside Staff do not thread with Staff. Does it make sense for a Leaf to thread with a non leaf? For a Voice to thread with a Staff, etc.? See the next test.')
   t = Staff(scale(4))

   r'''\new Staff {
      c'8
      d'8
      e'8
      f'8 
   }'''

   assert _test_components(list(iterate(t, _Component)), share = 'thread')


def test_test_components_none_thread_06( ):
   '''Leaves inside anonymous staff thread.'''

   t = Staff(scale(4))

   r'''\new Staff {
      c'8
      d'8
      e'8
      f'8 
   }'''

   assert _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_07( ):
   '''Voice, sequential and leaves all thread.'''

   t = Voice(Sequential(run(4)) * 2)
   diatonicize(t)

   r'''\new Voice {
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
   }'''

   assert _test_components(list(iterate(t, _Component)), share = 'thread')


def test_test_components_none_thread_08( ):
   '''Anonymous voice, tuplets and leaves all thread.'''

   t = Voice(FixedDurationTuplet((2, 8), run(3)) * 2)
   diatonicize(t)

   r'''\new Voice {
           \times 2/3 {
                   c'8
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
                   g'8
                   a'8
           }
   }'''

   assert _test_components(list(iterate(t, _Component)), share = 'thread')


def test_test_components_none_thread_09( ):
   '''Can not thread across anonymous voices.'''

   t = Staff(Voice(run(4)) * 2)
   diatonicize(t)

   r'''\new Staff {
           \new Voice {
                   c'8
                   d'8
                   e'8
                   f'8
           }
           \new Voice {
                   g'8
                   a'8
                   b'8
                   c''8
           }
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')
   assert not _test_components(t[:], share = 'thread')
   

def test_test_components_none_thread_10( ):
   '''Can thread across like-named voices.'''

   t = Staff(Voice(run(4)) * 2)
   diatonicize(t)
   t[0].invocation.name = 'foo'
   t[1].invocation.name = 'foo'

   r'''\new Staff {
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
   }'''

   assert _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_11( ):
   '''Can not thread across differently named voices.'''

   t = Staff(Voice(run(2)) * 2)
   diatonicize(t)
   t[0].invocation.name = 'foo'
   t[1].invocation.name = 'bar'

   r'''
   \new Staff {
      \context Voice = "foo" {
         c'8
         d'8
      }
      \context Voice = "bar" {
         e'8
         f'8
      }
   }
   '''

   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_12( ):
   '''Can not thread across anonymous voices.
      Can not thread across anonymous staves.'''

   t = Sequential(Staff([Voice(run(2))]) * 2)
   diatonicize(t)
   
   r'''
   {
      \new Staff {
         \new Voice {
            c'8
            d'8
         }
      }
      \new Staff {
         \new Voice {
            e'8
            f'8
         }
      }
   }
   '''   

   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_13( ):
   '''Can not thread across anonymous voices.
      Can not thread across anonymous staves.'''

   t = Sequential(Staff(Voice(run(2)) * 2) * 2)
   diatonicize(t)
   t[0].brackets = 'double-angle'
   t[1].brackets = 'double-angle'

   r'''{
      \new Staff <<
         \new Voice {
            c'8
            d'8
         }
         \new Voice {
            e'8
            f'8
         }
      >>
      \new Staff <<
         \new Voice {
            g'8
            a'8
         }
         \new Voice {
            b'8
            c''8
         }
      >>
   }'''

   assert not _test_components(t.leaves[:4], share = 'thread')


def test_test_components_none_thread_14( ):
   '''Anonymous voice, sequentials and leaves all thread.'''

   t = Voice(Sequential(run(2)) * 2)
   diatonicize(t)

   r'''\new Voice {
      {
         c'8
         d'8
      }
      {
         e'8
         f'8
      }
   }'''

   assert _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_15( ):
   '''Can thread across like-named staves.
      Can not thread across differently named IMPLICIT voices.'''

   t = Sequential(Staff(Note(0, (1, 8)) * 4) * 2)
   appictate(t)
   t[0].invocation.name = 'foo'
   t[1].invocation.name = 'foo'

   r'''{
      \context Staff = "foo" {
         c'8
         cs'8
         d'8
         ef'8
      }
      \context Staff = "foo" {
         e'8
         f'8
         fs'8
         g'8
      }
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_16( ):
   '''Can not thread across differently named IMPLICIT voices.'''

   t = Sequential([Sequential(run(4)), Voice(run(4))])
   diatonicize(t)
   
   r'''{
           {
                   c'8
                   d'8
                   e'8
                   f'8
           }
           \new Voice {
                   g'8
                   a'8
                   b'8
                   c''8
           }
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_17( ):
   '''Can not thread across differently named IMPLICIT voices.'''

   t = Sequential([Voice(run(4)), Sequential(run(4))])
   diatonicize(t)

   r'''{
           \new Voice {
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
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')

   
def test_test_components_none_thread_18( ):
   '''Can not thread across differently named IMPLICIT voices.'''

   t = Sequential([Sequential(run(4)), Voice(run(4))])
   t[1].invocation.name = 'foo'
   diatonicize(t)

   r'''{
           {
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
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_19( ):
   '''Can not thread over differently named IMPLICIT voices.'''

   t = Sequential([Voice(run(4)), Sequential(run(4))])
   t[0].invocation.name = 'foo'
   diatonicize(t)

   r'''{
           \context Voice = "foo" {
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
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')
   

def test_test_components_none_thread_20( ):
   '''Can not thread across differently named IMPLICIT voices.'''

   t = Sequential([Sequential(run(4)), Staff(run(4))])
   diatonicize(t)

   r'''{
           {
                   c'8
                   d'8
                   e'8
                   f'8
           }
           \new Staff {
                   g'8
                   a'8
                   b'8
                   c''8
           }
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_21( ):
   '''Can not thread across differently named IMPLICIT voices.'''

   t = Sequential([Staff(Note(0, (1, 8)) * 4), Sequential(Note(0, (1, 8)) * 4)])
   appictate(t)

   r'''{
      \new Staff {
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

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_22( ):
   '''Can not thread across differently named IMPLICIT voices.'''

   t = Sequential(Note(0, (1, 8)) * 4 + [Voice(Note(0, (1, 8)) * 4)])
   appictate(t)

   r'''{
      c'8
      cs'8
      d'8
      ef'8
      \new Voice {
         e'8
         f'8
         fs'8
         g'8
      }
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_23( ):
   '''Can not thread across differently named IMPLICIT voices.'''

   t = Sequential([Voice(Note(0, (1, 8)) * 4)] + Note(0, (1, 8)) * 4)
   appictate(t)


   r'''{
      \new Voice {
         c'8
         cs'8
         d'8
         ef'8
      }
      e'8
      f'8
      fs'8
      g'8
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')

   
def test_test_components_none_thread_24( ):
   '''Can not thread across differently named IMPLICIT voices.'''

   t = Sequential(Note(0, (1, 8)) * 4 + [Voice(Note(0, (1, 8)) * 4)])
   t[4].invocation.name = 'foo'
   appictate(t)

   r'''{
      c'8
      cs'8
      d'8
      ef'8
      \context Voice = "foo" {
         e'8
         f'8
         fs'8
         g'8
      }
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_25( ):
   '''Can not thread across differently named IMPLICIT voices.
      NOTE: THIS IS THE LILYPOND LACUNA.
      LilyPond *does* thread in this case.
      Abjad does not.'''

   t = Sequential([Voice(Note(0, (1, 8)) * 4)] + Note(0, (1, 8)) * 4)
   appictate(t)
   t[0].invocation.name = 'foo'

   r'''{
      \context Voice = "foo" {
         c'8
         cs'8
         d'8
         ef'8
      }
      e'8
      f'8
      fs'8
      g'8
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')
   

def test_test_components_none_thread_26( ):
   '''Can not thread across differently named IMPLICIT voices.'''

   t = Sequential(Note(0, (1, 8)) * 4 + [Voice(Note(0, (1, 8)) * 4)])
   appictate(t)

   r'''{
      c'8
      cs'8
      d'8
      ef'8
      \new Staff {
         e'8
         f'8
         fs'8
         g'8
      }
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_27( ):
   '''Can not thread across differently named IMPLICIT voices.'''

   t = Sequential(run(4))
   t.insert(0, Staff(run(4)))
   diatonicize(t)

   r'''{
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
           }
           g'8
           a'8
           b'8
           c''8
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_28( ):
   '''Can not thread across differently named IMPLICIT voices.'''

   v = Voice([Note(n, (1, 8)) for n in range(4)])
   q = Sequential([v])
   notes = [Note(n, (1, 8)) for n in range(4, 8)]
   t = Sequential([q] + notes)

   r'''{
      {
         \new Voice {
            c'8
            cs'8
            d'8
            ef'8
         }
      }
      e'8
      f'8
      fs'8
      g'8
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_29( ):
   '''Can not thread across differently named IMPLICIT voices.'''

   v = Voice([Note(n, (1, 8)) for n in range(4)])
   v.invocation.name = 'foo'
   q = Sequential([v])
   notes = [Note(n, (1, 8)) for n in range(4, 8)]
   t = Sequential([q] + notes)

   r'''{
      {
         \context Voice = "foo" {
            c'8
            cs'8
            d'8
            ef'8
         }
      }
      e'8
      f'8
      fs'8
      g'8
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_29( ):
   '''Can not thread across differently named IMPLICIT voices.'''

   v1 = Voice([Note(n, (1, 8)) for n in range(4)])
   v1.invocation.name = 'foo'
   v2 = Voice([v1])
   v2.invocation.name = 'bar'
   notes = [Note(n, (1, 8)) for n in range(4, 8)]
   t = Sequential([v2] + notes)

   r'''{
      \context Voice = "bar" {
         \context Voice = "foo" {
            c'8
            cs'8
            d'8
            ef'8
         }
      }
      e'8
      f'8
      fs'8
      g'8
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_30( ):
   '''Can not thread across differently named IMPLICIT voices.'''

   v1 = Voice([Note(n, (1, 8)) for n in range(4)])
   v2 = Voice([v1])
   notes = [Note(n, (1, 8)) for n in range(4, 8)]
   t = Sequential([v2] + notes)

   r'''{
      \new Voice {
         \new Voice {
            c'8
            cs'8
            d'8
            ef'8
         }
      }
      e'8
      f'8
      fs'8
      g'8
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_31( ):
   '''Can not thread across differently named IMPLICIT voices.'''
   
   notes = [Note(n, (1, 8)) for n in range(4)]
   vtop = Voice(Note(12, (1, 8)) * 4)
   vbottom = Voice(Note(0, (1, 8)) * 4)
   p = Parallel([vtop, vbottom])
   t = Sequential(notes + [p])

   r'''{
      c'8
      cs'8
      d'8
      ef'8
      <<
         \new Voice {
            af'8
            a'8
            bf'8
            b'8
         }
         \new Voice {
            e'8
            f'8
            fs'8
            g'8
         }
      >>
   }'''

   assert not _test_components(t.leaves[:8], share = 'thread')
   assert not _test_components(t.leaves[4:], share = 'thread')


def test_test_components_none_thread_32( ):
   '''Can not thread across differently named IMPLICIT voices.'''
   
   t = Sequential(
      [Parallel(Voice(Note(0, (1, 8)) * 4) * 2)] + Note(0, (1, 8)) * 4)
   appictate(t)

   r'''
   {
      <<
         \new Voice {
            c''8
            c''8
            c''8
            c''8
         }
         \new Voice {
            c'8
            c'8
            c'8
            c'8
         }
      >>
      c'8
      cs'8
      d'8
      ef'8
   }
   '''

   assert not _test_components(t.leaves[:8], share = 'thread')
   assert not _test_components(t.leaves[4:], share = 'thread')


def test_test_components_none_thread_33( ):
   '''Can thread across gaps.
      Can not thread across differently named voices.'''

   t = Sequential(Note(0, (1, 8)) * 4)
   a, b = Voice(Note(0, (1, 8)) * 4) * 2
   a.insert(2, b)
   t.insert(2, a)
   appictate(t)

   outer = (0, 1, 10, 11)
   middle = (2, 3, 8, 9)
   inner = (4, 5, 6, 7)

   r'''{
      c'8
      cs'8
      \new Voice {
         d'8
         ef'8
         \new Voice {
            e'8
            f'8
            fs'8
            g'8
         }
         af'8
         a'8
      }
      bf'8
      b'8
   }'''

   assert _test_components([t.leaves[i] for i in outer], share = 'thread')
   assert _test_components([t.leaves[i] for i in middle], share = 'thread')
   assert _test_components([t.leaves[i] for i in inner], share = 'thread')
   assert not _test_components(t.leaves[:4], share = 'thread')


def test_test_components_none_thread_34( ):
   '''Can thread across gaps.
      Can not thread across differently named IMPLICIT voices.'''

   t = Staff(Note(0, (1, 8)) * 4)
   a, b = t * 2
   a.insert(2, b)
   t.insert(2, a)
   appictate(t)

   outer = (0, 1, 10, 11)
   middle = (2, 3, 8, 9)
   inner = (4, 5, 6, 7)

   r'''\new Staff {
      c'8
      cs'8
      \new Staff {
         d'8
         ef'8
         \new Staff {
            e'8
            f'8
            fs'8
            g'8
         }
         af'8
         a'8
      }
      bf'8
      b'8
   }'''
   
   assert _test_components([t.leaves[i] for i in outer], share = 'thread')
   assert _test_components([t.leaves[i] for i in middle], share = 'thread')
   assert _test_components([t.leaves[i] for i in inner], share = 'thread')
   assert not _test_components(t.leaves[:4], share = 'thread')


def test_test_components_none_thread_35( ):
   '''Sequentials and leaves all thread.'''

   a, b, t = Sequential(Note(0, (1, 8)) * 4) * 3
   a.insert(2, b)
   t.insert(2, a)
   appictate(t)

   r'''{
      c'8
      cs'8
      {
         d'8
         ef'8
         {
            e'8
            f'8
            fs'8
            g'8
         }
         af'8
         a'8
      }
      bf'8
      b'8
   }'''

   assert _test_components(list(iterate(t, _Component)), share = 'thread')


def test_test_components_none_thread_36( ):
   '''Tuplets and leaves all thread.'''

   a, b, t = FixedDurationTuplet((3, 8), Note(0, (1, 8)) * 4) * 3
   b.insert(2, a)
   t.insert(2, b)
   b.duration.target = Rational(6, 8)
   t.duration.target = Rational(9, 8)
   appictate(t)

   r'''\fraction \times 9/10 {
      c'8
      cs'8
      \fraction \times 6/7 {
         d'8
         ef'8
         \fraction \times 3/4 {
            e'8
            f'8
            fs'8
            g'8
         }
         af'8
         a'8
      }
      bf'8
      b'8
   }'''

   assert _test_components(list(iterate(t, _Component)), share = 'thread')


def test_test_components_none_thread_37( ):
   '''Can not thread across differently named voices.'''

   t = Sequential(Note(0, (1, 8)) * 4)
   t.insert(2, Sequential([Sequential([Voice(Note(0, (1, 8)) * 4)])]))
   t[2][0][0].invocation.name = 'foo'
   appictate(t)

   r'''{
      c'8
      cs'8
      {
         {
            \context Voice = "foo" {
               d'8
               ef'8
               e'8
               f'8
            }
         }
      }
      fs'8
      g'8
   }'''

   outer = (0, 1, 6, 7)
   inner = (2, 3, 4, 5)

   assert _test_components([t.leaves[i] for i in outer]) 
   assert _test_components([t.leaves[i] for i in inner]) 
   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_38( ):
   '''Can not thread over differently named voices.'''

   t = Sequential(Note(0, (1, 8)) * 4)
   t.insert(0, Sequential([Sequential([Voice(Note(0, (1, 8)) * 4)])]))
   t[0][0][0].invocation.name = 'foo'
   appictate(t)

   r'''{
      {
         {
            \context Voice = "foo" {
               c'8
               cs'8
               d'8
               ef'8
            }
         }
      }
      e'8
      f'8
      fs'8
      g'8
   }'''
  
   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_39( ):
   '''Can not nest across differently named implicit voices.'''

   t = Sequential(Note(0, (1, 8)) * 4)
   t.insert(2, Voice(Note(0, (1, 8)) * 4))
   t = Sequential([t])
   t = Sequential([t])
   t = Voice([t])
   appictate(t)

   r'''\new Voice {
      {
         {
            {
               c'8
               cs'8
               \new Voice {
                  d'8
                  ef'8
                  e'8
                  f'8
               }
               fs'8
               g'8
            }
         }
      }
   }'''

   outer = (0, 1, 6, 7)
   inner = (2, 3, 4, 5)

   assert _test_components([t.leaves[i] for i in outer], share = 'thread')
   assert _test_components([t.leaves[i] for i in inner], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')

 
def test_test_components_none_thread_40( ):
   '''Can not thread across differently named voices.'''

   v = Voice(Note(0, (1, 8)) * 4)
   v.invocation.name = 'bar'
   q = Sequential(Note(0, (1, 8)) * 4)
   q.insert(2, v)
   qq = Sequential(Note(0, (1, 8)) * 4)
   qq.insert(2, q)
   t = Voice(Note(0, (1, 8)) * 4)
   t.insert(2, qq)
   t.invocation.name = 'foo'
   appictate(t)

   r'''\context Voice = "foo" {
      c'8
      cs'8
      {
         d'8
         ef'8
         {
            e'8
            f'8
            \context Voice = "bar" {
               fs'8
               g'8
               af'8
               a'8
            }
            bf'8
            b'8
         }
         c''8
         cs''8
      }
      d''8
      ef''8
   }'''

   outer = (0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15)
   inner = (6, 7, 8, 9)

   assert _test_components([t.leaves[i] for i in outer], share = 'thread')
   assert _test_components([t.leaves[i] for i in inner], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_41( ):
   '''Can not thread across differently named anonymous voices.'''

   t = Sequential(run(4))
   t[0:0] = Voice(run(4)) * 2
   appictate(t)

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
      af'8
      a'8
      bf'8
      b'8
   }'''

   assert _test_components(t.leaves[:4], share = 'thread')
   assert _test_components(t.leaves[4:8], share = 'thread')
   assert _test_components(t.leaves[8:], share = 'thread')
   assert not _test_components(t.leaves[:8], share = 'thread')
   assert not _test_components(t.leaves[4:], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')


def test_test_components_none_thread_42_trev( ):
   '''Staff and leaves all thread.'''

   py.test.skip("Unvoiced leaves inside Staff do not thread with Staff.")
   t = Staff(scale(4))
   t.brackets = 'double-angle'

   r'''\new Staff <<
      c'8
      d'8
      e'8
      f'8
   >>'''

   assert _test_components(list(iterate(t, _Component)), share = 'thread')
 
def test_test_components_none_thread_42( ):
   '''Leaves inside anonymous parallel Staff thread.'''

   t = Staff(scale(4))
   t.brackets = 'double-angle'

   r'''\new Staff <<
      c'8
      d'8
      e'8
      f'8
   >>'''

   assert _test_components(t.leaves, share = 'thread')
 

def test_test_components_none_thread_43( ):
   '''Parallel and sequential containers, and leaves, all thead.'''

   t = Sequential(Note(0, (1, 8)) * 4)
   p = Parallel(Note(0, (1, 8)) * 4)
   t.insert(2, p)
   appictate(t)

   r'''{
      c'8
      cs'8
      <<
         d'8
         ef'8
         e'8
         f'8
      >>
      fs'8
      g'8
   }'''

   assert _test_components(list(iterate(t, _Component)), share = 'thread')
 

def test_test_components_none_thread_44( ):
   '''Voice, containers and leaves all thread.'''

   t = Voice(Note(0, (1, 8)) * 4)
   p = Parallel(Note(0, (1, 8)) * 4)
   t.insert(2, p)
   appictate(t)

   r'''\new Voice {
      c'8
      cs'8
      <<
         d'8
         ef'8
         e'8
         f'8
      >>
      fs'8
      g'8
   }'''

   assert _test_components(list(iterate(t, _Component)), share = 'thread')


def test_test_components_none_thread_45( ):
   '''Containers and leaves all thread.
      TODO: We probably want to change this.
            LilyPond shoves all these things into a single voice.
            But Abjad threading turns out to be subtly different
            than LilyPond voice resolution.
      Abjad will probably be fine with a spanner restriction:
      spanners can span no more than one element from any paralllel.'''

   t = Parallel(Sequential(Note(0, (1, 8)) * 4) * 2)
   appictate(t)

   r'''<<
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
   >>'''


def test_test_components_none_thread_46( ):
   '''Everything threads.
      TODO: Implement one-element parallel spanner restriction.'''

   p = Parallel(Sequential(Note(0, (1, 8)) * 4) * 2)
   t = Sequential(Note(0, (1, 8)) * 4)
   t.insert(2, p)
   appictate(t)

   r'''{
      c'8
      cs'8
      <<
         {
            d'8
            ef'8
            e'8
            f'8
         }
         {
            fs'8
            g'8
            af'8
            a'8
         }
      >>
      bf'8
      b'8
   }'''

   assert _test_components(list(iterate(t, _Component)), share = 'thread')


def test_test_components_none_thread_47( ):
   '''Can not thread across differently named anonymous voices.'''

   p = Parallel(Voice(Note(0, (1, 8)) * 4) * 2)
   t = Sequential(Note(0, (1, 8)) * 4)
   t.insert(2, p)
   appictate(t)

   r'''{
      c'8
      cs'8
      <<
         \new Voice {
            d'8
            ef'8
            e'8
            f'8
         }
         \new Voice {
            fs'8
            g'8
            af'8
            a'8
         }
      >>
      bf'8
      b'8
   }'''

   outer = (0, 1, 10, 11)

   assert _test_components([t.leaves[i] for i in outer], share = 'thread')
   assert _test_components(t.leaves[2:6], share = 'thread')
   assert _test_components(t.leaves[6:10], share = 'thread')
   assert not _test_components(t.leaves[:6], share = 'thread')
   assert not _test_components(t.leaves, share = 'thread')
