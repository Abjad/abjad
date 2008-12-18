from abjad import *
import py.test


def test_span_anonymous_01( ):
   '''Spanned empty sequential container;
      container formats no beam indications.'''
   t = Sequential([ ])
   p = Beam(t)
   assert len(p) == 1
   assert isinstance(p[0], Sequential)
   assert len(p.leaves) == 0
   assert t.format == '{\n}'
   r'''
   {
   }
   '''


def test_span_anonymous_02( ):
   '''Nonempty spanned sequential container;
      container formats beam indications on first and last leaves.'''
   t = Sequential(Note(0, (1, 8)) * 8)
   p = Beam(t)
   assert len(p) == 1
   assert isinstance(p[0], Sequential)
   assert len(p.leaves) == 8
   assert t.format == "{\n\tc'8 [\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8 ]\n}"
   r'''
   {
      c'8 [
      c'8
      c'8
      c'8
      c'8
      c'8
      c'8
      c'8 ]
   }
   '''


def test_span_anonymous_03( ):
   '''Contiguous nonempty spanned containers;
      first and last leaves in contiguity chain format
      beam indications.'''
   t = Staff(Sequential(Note(0, (1, 8)) * 4) * 2)
   p = Beam(t[ : ])
   assert len(p) == 2
   assert isinstance(p[0], Sequential)
   assert isinstance(p[1], Sequential)
   assert len(p.leaves) == 8
   "\\new Staff {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\t{\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n}"
   r'''
   \new Staff {
      {
         c'8 [
         c'8
         c'8
         c'8
      }
      {
         c'8
         c'8
         c'8
         c'8 ]
      }
   }
   '''

def test_span_anonymous_04( ):
   '''Contiguous nonempty containers and leaves;
      top-level attachment;
      first and last leaves in contiguity chain format
      beam indications.'''
   t = Staff([Sequential(Note(0, (1, 8)) * 4), Note(0, (1, 8)), Note(0, (1, 8))])
   p = Beam(t)
   assert len(p) == 1
   assert isinstance(p[0], Staff)
   assert len(p.leaves) == 6
   assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\tc'8\n\tc'8 ]\n}"
   r'''
   \new Staff {
      {
         c'8 [
         c'8
         c'8
         c'8
      }
      c'8
      c'8 ]
   }
   '''


def test_span_anonymous_05( ):
   '''Contiguous nonempty containers and leaves;
      intermediate attachment;
      first and last leaves in contiguity chain format beam indications.'''
   t = Staff([Sequential(Note(0, (1, 8)) * 4), Note(0, (1, 8)), Note(0, (1, 8))])
   p = Beam(t[ : ])
   assert len(p) == 3
   assert isinstance(p[0], Sequential)
   assert isinstance(p[1], Note)
   assert isinstance(t[2], Note)
   assert len(p.leaves) == 6
   assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\tc'8\n\tc'8 ]\n}"
   r'''
   \new Staff {
      {
         c'8 [
         c'8
         c'8
         c'8
      }
      c'8
      c'8 ]
   }
   '''


def test_span_anonymous_06( ):
   '''Contiguous nonempty containers and leaves;
      leaf-level attachment;
      first and last leaves in contiguity chain format beam indications.'''
   t = Staff([Sequential(Note(0, (1, 8)) * 4), Note(0, (1, 8)), Note(0, (1, 8))])
   p = Beam(t.leaves)
   assert len(p) == 6
   for x in p:
      assert isinstance(x, Note)
   assert len(p.leaves) == 6
   assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\tc'8\n\tc'8 ]\n}"
   r'''
   \new Staff {
      {
         c'8 [
         c'8
         c'8
         c'8
      }
      c'8
      c'8 ]
   }
   '''


def test_span_anonymous_07( ):
   '''Contiguous empty containers are OK;
      no beams appear at format-time.'''
   t = Staff(Sequential([ ]) * 3)
   p = Beam(t[ : ])
   assert len(p) == 3
   for x in p:
      assert isinstance(x, Sequential)
   assert len(p.leaves) == 0
   r'''
   \new Staff {
      {
      }
      {
      }
      {
      }
   }
   '''


def test_span_anonymous_08( ):
   '''Intervening empty containers are OK.'''
   t = Staff(Sequential(Note(0, (1, 8)) * 4) * 2)
   t.insert(1, Sequential([ ]))
   p = Beam(t[ : ])
   assert len(p) == 3
   for x in p:
      assert isinstance(x, Sequential)
   assert len(p.leaves) == 8
   assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\t{\n\t}\n\t{\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n}"
   r'''
   \new Staff {
      {
         c'8 [
         c'8
         c'8
         c'8
      }
      {
      }
      {
         c'8
         c'8
         c'8
         c'8 ]
      }
   }
   '''


def test_span_anonymous_09( ):
   '''Empty containers at edges are OK.'''
   t = Staff(Sequential([ ]) * 2)
   t.insert(1, Sequential(Note(0, (1, 8)) * 4))
   p = Beam(t[ : ])
   assert len(p) == 3
   for x in p:
      assert isinstance(x, Sequential)
   assert len(p.leaves) == 4
   assert t.format == "\\new Staff {\n\t{\n\t}\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n\t{\n\t}\n}"
   r'''
   \new Staff {
      {
      }
      {
         c'8 [
         c'8
         c'8
         c'8 ]
      }
      {
      }
   }
   '''

   
def test_span_anonymous_10( ):
   '''Spanners group anonymous containers at 
      completely different depths just fine;
      the only requirement is that the *leaves* of all
      arguments passed to Beam( ) be *temporarly contiguous*.
      Ie, there's a *leaf temporal contiguity* requirement.'''
   s1 = Sequential([Note(i, (1,8)) for i in range(4)])
   s1 = Sequential([s1])
   s2 = Sequential([Note(i, (1,8)) for i in range(4,8)])
   s2 = Sequential([s2])
   t = Voice([s1, s2])
   p = Beam(t)
   assert len(p) == 1
   assert len(p.leaves) == 8
   p.die( )
   p = Beam((t[0], t[1]))
   assert len(p) == 2
   assert len(p.leaves) == 8
   p.die( )
   p = Beam((t[0][0], t[1][0]))
   assert len(p) == 2
   assert len(p.leaves) == 8
   p.die( )
   p = Beam((t[0], t[1][0]))
   assert len(p) == 2
   assert len(p.leaves) == 8
   p.die( )
   p = Beam((t[0][0], t[1]))
   assert len(p) == 2
   assert len(p.leaves) == 8
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


def test_span_anonymous_11( ):
   '''Asymmetric structure;
      but otherwise same as immediately above.'''
   s1 = Sequential([Note(i, (1,8)) for i in range(4)])
   s1 = Sequential([s1])
   s1 = Sequential([s1])
   s2 = Sequential([Note(i, (1,8)) for i in range(4,8)])
   t = Voice([s1, s2])

   p = Beam(t)
   assert len(p) == 1
   assert len(p.leaves) == 8
   p.die( )

   p = Beam((t[0], t[1]))
   assert len(p) == 2
   assert len(p.leaves) == 8
   p.die( )

   p = Beam((t[0][0], t[1]))
   assert len(p) == 2
   assert len(p.leaves) == 8
   p.die( )

   p = Beam((t[0][0][0], t[1]))
   assert len(p) == 2
   assert len(p.leaves) == 8
   p.die( )

   r'''
   \new Voice {
      {
         {
            {
               c'8
               cs'8
               d'8
               ef'8
            }
         }
      }
      {
         e'8
         f'8
         fs'8
         g'8
      }
   }
   '''


def test_span_anonymous_12( ):
   '''Docs.'''
   s1 = Sequential([Note(i, (1, 8)) for i in range(2)])
   s2 = Sequential([Note(i, (1, 8)) for i in range(3, 5)])
   v = Voice([s1, Note(2, (1, 8)), s2])

   p = Beam(v)
   assert len(p) == 1
   assert len(p.leaves) == 5
   p.die( )

   p = Beam(v[ : ])
   assert len(p) == 3
   assert len(p.leaves) == 5
   p.die( )

   r'''
   \new Voice {
      {
         c'8
         cs'8
      }
      d'8
      {
         ef'8
         e'8
      }
   }
   '''


def test_span_anonymous_13( ):
   '''Alternating sequences of tuplets and notes span correctly.'''
   t1 = FixedDurationTuplet((1,4), [Note(i, (1,8)) for i in range(3)])
   t2 = FixedDurationTuplet((1,4), [Note(i, (1,8)) for i in range(4,7)])
   v = Voice([t1, Note(3, (1,8)), t2])

   p = Beam(v)
   assert len(p) == 1
   assert len(p.leaves) == 7
   p.die( )

   p = Beam(v[ : ])
   assert len(p) == 3
   assert len(p.leaves) == 7
   p.die( )

   r'''
   \new Voice {
      \times 2/3 {
         c'8
         cs'8
         d'8
      }
      ef'8
      \times 2/3 {
         e'8
         f'8
         fs'8
      }
   }
   '''


def test_span_anonymous_14( ):
   '''Asymmetrically nested tuplets span correctly.'''
   tinner = FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3)
   t = FixedDurationTuplet((2, 4), [Note(0, (1, 4)), tinner, Note(0, (1, 4))])

   p = Beam(t)
   assert len(p) == 1
   assert len(p.leaves) == 5
   p.die( )

   p = Beam(t[ : ])
   assert len(p) == 3
   assert len(p.leaves) == 5

   r'''
   \times 2/3 {
      c'4
      \times 2/3 {
         c'8
         c'8
         c'8
      }
      c'4
   }
   '''


### TODO - This is the current behavior but it's probably not
###        the optimal behavior;
###        optimal behavior will work on thread or voice signature.
###        We'll change this test when we change to optimal behavior.

def test_span_anonymous_15( ):
   '''
   Parent asymmetric structures allow spanning,
   even though LilyPond will not render the beam
   through two different anonymous voices.
   '''
   v1 = Voice([Note(i , (1, 8)) for i in range(3)])
   n = Note(3, (1,8))
   v2 = Voice([Note(i , (1, 8)) for i in range(4, 8)])
   t = Staff([v1, n, v2])

   p = Beam((t[0], t[1]))
   assert len(p) == 2
   assert len(p.leaves) == 4
   p.die( )

   p = Beam((t[1], t[2]))
   assert len(p) == 2
   assert len(p.leaves) == 5
   p.die( )

   r'''
   \new Staff {
      \new Voice {
         c'8
         cs'8
         d'8
      }
      ef'8
      \new Voice {
         e'8
         f'8
         fs'8
         g'8
      }
   }
   '''
