from abjad import *
import py.test


def test_path_exists_between_01( ):
   '''Paths exist between all leaves in a voice.'''

   t = Voice(scale(4))

   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[2])
   assert t[2]._navigator._pathExistsBetween(t[3])

   r'''
   \new Voice {
      c'8
      d'8
      e'8
      f'8
   }
   '''


def test_path_exists_between_02( ):
   '''Paths exist between all notes in a staff.'''

   t = Staff(scale(4))

   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[2])
   assert t[2]._navigator._pathExistsBetween(t[3])

   r'''
   \new Staff {
      c'8
      d'8
      e'8
      f'8
   }
   '''


def test_path_exists_between_03( ):
   '''Paths exist between all notes in a sequential.'''

   t = Sequential(scale(4))

   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[2])
   assert t[2]._navigator._pathExistsBetween(t[3])

   r'''
   {
      c'8
      d'8
      e'8
      f'8
   }
   '''


def test_path_exists_between_04( ):
   '''Paths exist between none of the leaves in a parallel container.'''

   t = Parallel(scale(4))

   assert not t[0]._navigator._pathExistsBetween(t[1])
   assert not t[1]._navigator._pathExistsBetween(t[2])
   assert not t[2]._navigator._pathExistsBetween(t[3])

   r'''
   <<
      c'8
      d'8
      e'8
      f'8
   >>
   '''


def test_path_exists_between_05( ):
   '''Paths exist between tuplet leaves.'''

   t = FixedDurationTuplet((2, 8), scale(3))

   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[0])

   assert t[1]._navigator._pathExistsBetween(t[2])
   assert t[2]._navigator._pathExistsBetween(t[1])

   r'''
   \times 2/3 {
      c'8
      d'8
      e'8
   }
   '''


def test_path_exists_between_06( ):
   '''Paths exist between all components here.'''

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

   ### paths exist between sequential containers
   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[0])

   ### paths exist between sequential containers and leaves
   assert t[0]._navigator._pathExistsBetween(t[1][0])
   assert t[0]._navigator._pathExistsBetween(t[1][1])
   assert t[0]._navigator._pathExistsBetween(t[1][2])
   assert t[0]._navigator._pathExistsBetween(t[1][3])
   assert t[1]._navigator._pathExistsBetween(t[0][0])
   assert t[1]._navigator._pathExistsBetween(t[0][1])
   assert t[1]._navigator._pathExistsBetween(t[0][2])
   assert t[1]._navigator._pathExistsBetween(t[0][3])


def test_path_exists_between_07( ):
   '''Paths exist between all components here.'''

   t1 = FixedDurationTuplet((2, 8), [Note(i, (1, 8)) for i in range(3)])
   t2 = FixedDurationTuplet((2, 8), [Note(i, (1, 8)) for i in range(3, 6)])
   t = Voice([t1, t2])

   ### paths exist between tuplets
   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[0])

   ### paths exist between tuplets and leaves
   assert t[0]._navigator._pathExistsBetween(t[1][0])
   assert t[0]._navigator._pathExistsBetween(t[1][1])
   assert t[0]._navigator._pathExistsBetween(t[1][2])
   assert t[1]._navigator._pathExistsBetween(t[0][0])
   assert t[1]._navigator._pathExistsBetween(t[0][1])
   assert t[1]._navigator._pathExistsBetween(t[0][2])

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


def test_path_exists_between_08( ):
   '''Paths exist here only within voices and not across voices.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   t = Staff([v1, v2])

   assert not t[0]._navigator._pathExistsBetween(t[1])
   assert not t[1]._navigator._pathExistsBetween(t[0])

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


def test_path_exists_between_09( ):
   r'''Paths exist between all components here.
      Paths can cross the \context-boundary because
      contexts share the same name.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v1.invocation.name = 'foo'
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   v2.invocation.name = 'foo'
   t = Staff([v1, v2])

   ### path exists between like-named voices
   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[0])

   ### path exists between like-named voices and voice contents
   assert t[0]._navigator._pathExistsBetween(t[1][0])
   assert t[0]._navigator._pathExistsBetween(t[1][1])
   assert t[0]._navigator._pathExistsBetween(t[1][2])
   assert t[0]._navigator._pathExistsBetween(t[1][3])
   assert t[1]._navigator._pathExistsBetween(t[0][0])
   assert t[1]._navigator._pathExistsBetween(t[0][1])
   assert t[1]._navigator._pathExistsBetween(t[0][2])
   assert t[1]._navigator._pathExistsBetween(t[0][3])

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


def test_path_exists_between_10( ):
   '''Paths exist here only within voices and not across voices.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v1.invocation.name = 'foo'
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 88)])
   v2.invocation.name = 'bar'
   t = Staff([v1, v2])

   assert not t[0]._navigator._pathExistsBetween(t[1])
   assert not t[1]._navigator._pathExistsBetween(t[0])

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


def test_path_exists_between_11( ):
   '''Paths exist here only within voices and nowhere else.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   s1 = Staff([v1])
   s2 = Staff([v2])
   seq = Sequential([s1, s2])
   
   ### paths do not exist between anonymous staves 
   assert not seq[0]._navigator._pathExistsBetween(seq[1])
   assert not seq[1]._navigator._pathExistsBetween(seq[0])

   ### paths do not exist between anonymous voices
   assert not seq[0][0]._navigator._pathExistsBetween(seq[1][0])
   assert not seq[1][0]._navigator._pathExistsBetween(seq[0][0])

   ### paths do not exist between anonymous staves and voices
   assert not seq[0]._navigator._pathExistsBetween(seq[0][0])
   assert not seq[0]._navigator._pathExistsBetween(seq[1][0])
   assert not seq[1]._navigator._pathExistsBetween(seq[0][0])
   assert not seq[1]._navigator._pathExistsBetween(seq[1][0])

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


def test_path_exists_between_12( ):
   '''Paths exist here only within voices.'''

   vl1 = Voice([Note(i, (1, 8)) for i in range(4)])
   vl2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   vh1 = Voice([Note(i, (1, 8)) for i in range(12, 16)])
   vh2 = Voice([Note(i, (1, 8)) for i in range(16, 20)])
   s1 = Staff([vh1, vl1])
   s1.brackets = 'double-angle'
   s2 = Staff([vl2, vh2])
   s2.brackets = 'double-angle'
   seq = Sequential([s1, s2])

   assert not seq[0]._navigator._pathExistsBetween(seq[1])
   assert not seq[0]._navigator._pathExistsBetween(seq[1][0])
   assert not seq[0]._navigator._pathExistsBetween(seq[1][0][0])
   assert not seq[0]._navigator._pathExistsBetween(seq[1][1])
   assert not seq[0]._navigator._pathExistsBetween(seq[1][1][0])

   assert not seq[0][0]._navigator._pathExistsBetween(seq[1])
   assert not seq[0][0]._navigator._pathExistsBetween(seq[1][0])
   assert not seq[0][0]._navigator._pathExistsBetween(seq[1][0][0])
   assert not seq[0][0]._navigator._pathExistsBetween(seq[1][1])
   assert not seq[0][0]._navigator._pathExistsBetween(seq[1][1][0])

   assert not seq[0][0][-1]._navigator._pathExistsBetween(seq[1])
   assert not seq[0][0][-1]._navigator._pathExistsBetween(seq[1][0])
   assert not seq[0][0][-1]._navigator._pathExistsBetween(seq[1][0][0])
   assert not seq[0][0][-1]._navigator._pathExistsBetween(seq[1][1])
   assert not seq[0][0][-1]._navigator._pathExistsBetween(seq[1][1][0])

   assert not seq[0][1]._navigator._pathExistsBetween(seq[1])
   assert not seq[0][1]._navigator._pathExistsBetween(seq[1][0])
   assert not seq[0][1]._navigator._pathExistsBetween(seq[1][0][0])
   assert not seq[0][1]._navigator._pathExistsBetween(seq[1][1])
   assert not seq[0][1]._navigator._pathExistsBetween(seq[1][1][0])

   assert not seq[0][1][-1]._navigator._pathExistsBetween(seq[1])
   assert not seq[0][1][-1]._navigator._pathExistsBetween(seq[1][0])
   assert not seq[0][1][-1]._navigator._pathExistsBetween(seq[1][0][0])
   assert not seq[0][1][-1]._navigator._pathExistsBetween(seq[1][1])
   assert not seq[0][1][-1]._navigator._pathExistsBetween(seq[1][1][0])

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


def test_path_exists_betwee_13( ):
   '''Paths exist between all components here.'''

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

   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[0]._navigator._pathExistsBetween(t[1][0])
   assert t[0]._navigator._pathExistsBetween(t[1][0][0])
   
   assert t[0][0]._navigator._pathExistsBetween(t[1])
   assert t[0][0]._navigator._pathExistsBetween(t[1][0])
   assert t[0][0]._navigator._pathExistsBetween(t[1][0][0])
   
   assert t[0][0][-1]._navigator._pathExistsBetween(t[1])
   assert t[0][0][-1]._navigator._pathExistsBetween(t[1][0])
   assert t[0][0][-1]._navigator._pathExistsBetween(t[1][0][0])
   


## TODO - this test doesn't work yet;
##        it's quite surprising that LilyPond
##        DOES ALLOW a path between consecutive like-named *voices*
##        BUT DOES NOT ALLOW between consecutive like-named *staves*.
def test_path_exists_between_14( ):
   '''Path DOES NOT exist between consecutive like-named staves.'''

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

   ## TODO - make all four of these asserts work correctly
   #assert not t[0]._navigator._pathExistsBetween(t[1])
   #assert not t[1]._navigator._pathExistsBetween(t[0])

   #assert not t[0][0]._navigator._pathExistsBetween(t[1][0])
   #assert not t[1][0]._navigator._pathExistsBetween(t[0][1])


def test_path_exists_between_15( ):
   '''Path DOES exist between consecutive like-named voices.'''

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

   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[0])

   assert t[0][0]._navigator._pathExistsBetween(t[1][0])
   assert t[1][0]._navigator._pathExistsBetween(t[0][1])



## TODO - two more tests to cover:
##        a (named / anonymous) voice followed by naked notes;
##        a (named / anonymous) staff followed by naked notes;
