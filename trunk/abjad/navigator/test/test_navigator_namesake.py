from abjad import *
from abjad.component.component import _Component

## nextNamesake ##

def test_navigator_namesake_01( ):
   '''Leaves within different anonymous parents have different  
   parentage signatures and thus have no _nextNamesake.'''
   t = Container(Voice(construct.run(2)) * 2)

   assert t.leaves[0]._navigator._nextNamesake is t.leaves[1]
   assert t.leaves[1]._navigator._nextNamesake is None
   assert t.leaves[2]._navigator._nextNamesake is t.leaves[3]


def test_navigator_namesake_02( ):
   '''Anonymous containers with the same parentage structure have  
   different parentage signatures and thus have no _nextNamesake.'''
   t = Container(Voice(construct.run(2)) * 2)

   assert t[0]._navigator._nextNamesake is None


def test_navigator_namesake_03( ):
   '''Differently named containers have a different parentage signature
   and thus do not _nextNamesake.'''
   t = Container(Voice(construct.run(2)) * 2)
   t[0].name = 'voice'

   assert t[0]._navigator._nextNamesake is None
   assert t.leaves[0]._navigator._nextNamesake is t.leaves[1]
   assert t.leaves[1]._navigator._nextNamesake is None
   assert t.leaves[2]._navigator._nextNamesake is t.leaves[3]


def test_navigator_namesake_04( ):
   '''Calling _nextNamesake on a named component when another component
   with the same type and name exists after the caller returns the first
   next namesake Component found.'''
   t = Container(Voice(construct.run(2)) * 2)
   t[0].name = 'voice'
   t[1].name = 'voice'

   assert t[0]._navigator._nextNamesake is t[1]
   assert t[1]._navigator._nextNamesake is None
   assert t.leaves[1]._navigator._nextNamesake is t.leaves[2]


def test_navigator_namesake_05( ):
   '''Components need not be strictly contiguous.'''
   t = Container(Voice(construct.run(2)) * 2)
   t[0].name = 'voice'
   t[1].name = 'voice'
   t.insert(1, Rest((1, 2)))

   assert t[0]._navigator._nextNamesake is t[2]
   assert t.leaves[1]._navigator._nextNamesake is t.leaves[3]



def test_navigator_namesake_06( ):
   '''Components need not thread (Staves don't thread).'''
   t = Container(Staff(construct.run(2)) * 2)
   t[0].name = 'staff'
   t[1].name = 'staff'
   assert t[0]._navigator._nextNamesake is t[1]
   assert t.leaves[1]._navigator._nextNamesake is t.leaves[2]


def test_navigator_namesake_07( ):
   '''_nextNamesake works on parallel structures.'''
   a = Container(Voice(construct.run(2)) * 2)
   a[0].name = 'voiceOne'
   a[1].name = 'voiceTwo'
   a.parallel = True
   b = Container(Voice(construct.run(2)) * 2)
   b[0].name = 'voiceOne'
   b[1].name = 'voiceTwo'
   b.parallel = True
   t = Staff([a, b])

   r'''\new Staff {
           <<
                   \context Voice = "voiceOne" {
                           c'8
                           c'8
                   }
                   \context Voice = "voiceTwo" {
                           c'8
                           c'8
                   }
           >>
           <<
                   \context Voice = "voiceOne" {
                           c'8
                           c'8
                   }
                   \context Voice = "voiceTwo" {
                           c'8
                           c'8
                   }
           >>
   }'''

   assert a[0]._navigator._nextNamesake is b[0]
   assert a[1]._navigator._nextNamesake is b[1]
   assert a[0][1]._navigator._nextNamesake is b[0][0]
   assert a[1][1]._navigator._nextNamesake is b[1][0]


