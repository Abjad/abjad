from abjad import *


### NEXT LEAVES ###

def test_nextLeaves_navigation_01( ):
   '''nextLeaves works on simple Voice.'''
   t = Voice([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._nextLeaves == [t[1]]
   assert t[1]._navigator._nextLeaves == [t[2]]
   assert t[2]._navigator._nextLeaves == [t[3]]
   assert t[3]._navigator._nextLeaves is None
   r'''
   \new Voice {
      c'8
      cs'8
      d'8
      ef'8
   }
   '''


def test_nextLeaves_navigation_02( ):
   '''NextLeaf works on simple Sequential.'''
   t = Sequential([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._nextLeaves == [t[1]]
   assert t[1]._navigator._nextLeaves == [t[2]]
   assert t[2]._navigator._nextLeaves == [t[3]]
   assert t[3]._navigator._nextLeaves is None
   r'''
   {
      c'8
      cs'8
      d'8
      ef'8
   }
   '''


def test_nextLeaves_navigation_03( ):
   '''NextLeaf works on simple Parallel.'''
   t = Parallel([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._nextLeaves is None
   assert t[1]._navigator._nextLeaves is None
   assert t[2]._navigator._nextLeaves is None
   assert t[3]._navigator._nextLeaves is None
   r'''
   <<
      c'8
      cs'8
      d'8
      ef'8
   >>
   '''


### LEVEL 1 NESTING ###

def test_nextLeaves_navigation_10( ):
   '''nextLeaves works on contiguous Sequentials inside a Voice.'''
   s1 = Sequential([Note(i, (1,8)) for i in range(4)])
   s2 = Sequential([Note(i, (1,8)) for i in range(4,8)])
   t = Voice([s1, s2])
   assert s1[0]._navigator._nextLeaves == [s1[1]]
   assert s1[1]._navigator._nextLeaves == [s1[2]]
   assert s1[2]._navigator._nextLeaves == [s1[3]]
   assert s1[3]._navigator._nextLeaves == [s2[0]]
   r'''
   \new Voice {
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
   }
   '''


def test_nextLeaves_navigation_11( ):
   '''nextLeaves works on contiguous Voices inside a Staff.'''
   v1 = Voice([Note(i, (1,8)) for i in range(4)])
   v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   t = Staff([v1, v2])
   assert v1[0]._navigator._nextLeaves == [v1[1]]
   assert v1[1]._navigator._nextLeaves == [v1[2]]
   assert v1[2]._navigator._nextLeaves == [v1[3]]
   assert v1[3]._navigator._nextLeaves == [v2[0]]
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


### LEVEL 2 NESTING ###

def test_nextLeaves_navigation_20( ):
   v1 = Voice([Note(i, (1,8)) for i in range(4)])
   v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   s1 = Staff([v1])
   s2 = Staff([v2])
   seq = Sequential([s1, s2])
   assert v1[3]._navigator._nextLeaves == [v2[0]]
   assert v1._navigator._nextLeaves == [v2[0]]
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


def test_nextLeaves_navigation_21( ):
   vl1 = Voice([Note(i, (1,8)) for i in range(4)])
   vl2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   vh1 = Voice([Note(i, (1,8)) for i in range(12,16)])
   vh2 = Voice([Note(i, (1,8)) for i in range(16,20)])

   s1 = Staff([vh1, vl1])
   #s1.brackets = 'double-angle'
   s1.parallel = True
   s2 = Staff([vl2, vh2])
   #s2.brackets = 'double-angle'
   s2.parallel = True

   seq = Sequential([s1, s2])

   assert vl1[3]._navigator._nextLeaves == [vl2[0], vh2[0]]
   assert vh1[3]._navigator._nextLeaves == [vl2[0], vh2[0]]
   assert vh1._navigator._nextLeaves  == [vl2[0], vh2[0]]
   assert vl1._navigator._nextLeaves  == [vl2[0], vh2[0]]

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


### PREVIOUS LEAVES ###

def test_prevLeaves_navigation_01( ):
   '''prevLeaves works on simple Voice.'''
   t = Voice([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._prevLeaves is None
   assert t[1]._navigator._prevLeaves == [t[0]]
   assert t[2]._navigator._prevLeaves == [t[1]]
   assert t[3]._navigator._prevLeaves == [t[2]] 
   r'''
   \new Voice {
      c'8
      cs'8
      d'8
      ef'8
   }
   '''


def test_prevLeaves_navigation_02( ):
   '''prevLeaves works on simple Sequential.'''
   t = Sequential([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._prevLeaves is None
   assert t[1]._navigator._prevLeaves == [t[0]]
   assert t[2]._navigator._prevLeaves == [t[1]]
   assert t[3]._navigator._prevLeaves == [t[2]]
   r'''
   {
      c'8
      cs'8
      d'8
      ef'8
   }
   '''


def test_prevLeaves_navigation_03( ):
   '''prevLeaves works on simple Parallel.'''
   t = Parallel([Note(i, (1,8)) for i in range(4)])
   assert t[0]._navigator._prevLeaves is None
   assert t[1]._navigator._prevLeaves is None
   assert t[2]._navigator._prevLeaves is None
   assert t[3]._navigator._prevLeaves is None
   r'''
   <<
      c'8
      cs'8
      d'8
      ef'8
   >>
   '''


### LEVEL 1 NESTING ###

def test_prevLeaves_navigation_10( ):
   '''prevLeaves works on contiguous Sequentials inside a Voice.'''
   s1 = Sequential([Note(i, (1,8)) for i in range(4)])
   s2 = Sequential([Note(i, (1,8)) for i in range(4,8)])
   t = Voice([s1, s2])
   assert s2[0]._navigator._prevLeaves == [s1[3]]
   assert s2._navigator._prevLeaves == [s1[3]]
   assert s1[0]._navigator._prevLeaves is None
   r'''
   \new Voice {
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
   }
   '''


def test_prevLeaves_navigation_11( ):
   '''prevLeaves works on contiguous Voices inside a Staff.'''
   v1 = Voice([Note(i, (1,8)) for i in range(4)])
   v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   t = Staff([v1, v2])
   assert v2[0]._navigator._prevLeaves == [v1[3]]
   assert v2._navigator._prevLeaves == [v1[3]]
   assert v1[0]._navigator._prevLeaves is None
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


### LEVEL 2 NESTING ###

def test_prevLeaves_navigation_20( ):
   v1 = Voice([Note(i, (1,8)) for i in range(4)])
   v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   s1 = Staff([v1])
   s2 = Staff([v2])
   seq = Sequential([s1, s2])
   assert v2[0]._navigator._prevLeaves == [v1[3]]
   assert v2._navigator._prevLeaves == [v1[3]]
   assert s2._navigator._prevLeaves == [v1[3]]

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
   

def test_prevLeaves_navigation_21( ):
   vl1 = Voice([Note(i, (1,8)) for i in range(4)])
   vl2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   vh1 = Voice([Note(i, (1,8)) for i in range(12,16)])
   vh2 = Voice([Note(i, (1,8)) for i in range(16,20)])

   s1 = Staff([vh1, vl1])
   #s1.brackets = 'double-angle'
   s1.parallel = True
   s2 = Staff([vl2, vh2])
   #s2.brackets = 'double-angle'
   s2.parallel = True

   seq = Sequential([s1, s2])

   assert vl2[0]._navigator._prevLeaves == [vh1[3], vl1[3]]
   assert vh2[0]._navigator._prevLeaves == [vh1[3], vl1[3]]
   assert vl2._navigator._prevLeaves  == [vh1[3], vl1[3]]
   assert vh2._navigator._prevLeaves  == [vh1[3], vl1[3]]

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
