from abjad import *
import py.test


def test_signature_01( ):
   '''Orphan leaves carry no voice signature.'''

   assert Note(0, (1, 4)).voice.signature is None
   assert Rest((1, 4)).voice.signature is None
   assert Chord([2, 3, 4], (1, 4)).voice.signature is None
   assert Skip((1, 4)).voice.signature is None


def test_signature_02( ):
   '''Sequential container carries the signature of the default voice;
      sequentialized leaves carry the signature of the default voice.'''

   t = Sequential([Note(n, (1, 8)) for n in range(4)])

   from abjad.component.component import _Component
   assert all([x.voice.default for x in iterate(t, _Component)])

   r'''
   {
      c'8
      cs'8
      d'8
      ef'8
   }
   '''


def test_signature_03( ):
   '''Tuplet carries the signature of the default voice.
      Tupletted leaves carry the signature of the default voice.'''
   
   t = FixedDurationTuplet((2, 8), [Note(n, (1, 8)) for n in range(3)])
   
   from abjad.component.component import _Component
   assert all([x.voice.default for x in iterate(t, _Component)])

   r'''
   \times 2/3 {
      c'8
      cs'8
      d'8
   }
   '''


def test_signature_04( ):
   '''Parallel container carries the signature of the default voice.
      Parallel leaves each carry a different voice signature.'''

   t = Parallel([Note(n, (1, 8)) for n in range(4)])

   assert t.voice.default
   assert len(set([x.voice.signature for x in t])) == len(t)

   r'''
   <<
      c'8
      cs'8
      d'8
      ef'8
   >>
   '''

   
def test_signature_05( ):
   '''Anonymous voice creates its own voice signature;
      voiced leaves each carry the signature of their containing voice.'''

   t = Voice([Note(i, (1, 8)) for i in range(4)])

   assert t.voice.signature == (id(t), )
   assert all([x.voice.signature == t.voice.signature for x in t])

   r'''
   \new Voice {
      c'8
      cs'8
      d'8
      ef'8
   }
   '''


def test_signature_06( ):
   '''
   Staff creates an implicit voice with a numeric signature.
   Staff leaves carry the same signature as staff.
   '''

   t = Staff([Note(i, (1, 8)) for i in range(4)])

   assert not t.voice.default
   assert all([x.voice.signature == t.voice.signature for x in t])

   r'''
   \new Staff {
      c'8
      cs'8
      d'8
      ef'8
   }
   '''


def test_signature_07( ):
   '''Voice creates a voice signature equal to its own id;
      all other components here inherit signature from voice.'''

   s1 = Sequential([Note(i, (1, 8)) for i in range(4)])
   s2 = Sequential([Note(i, (1, 8)) for i in range(4, 8)])
   t = Voice([s1, s2])

   from abjad.component.component import _Component
   assert t.voice.signature == (id(t), )
   components = iterate(t, _Component)
   assert all([x.voice.signature == t.voice.signature for x in components])

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


def test_signature_08( ):
   '''
   (Anonymous) voice creates its own (numeric) voice signature.
   All components here carry the same signature.
   '''

   t = Voice(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 2)
   appictate(t)

   from abjad.component.component import _Component
   assert not t.voice.default
   components = iterate(t, _Component)
   assert all([x.voice.signature == t.voice.signature for x in components])

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


def test_signature_09( ):
   '''
   (Anonymous) staff creates its own (numeric) voice signature.
   (Anonymous) voices each create their own (numeric) signatures.
   Voice leaves carry the same signature.
   '''

   t = Staff(Voice(Note(0, (1, 8)) * 4) * 2)
   appictate(t)

   assert not t.voice.default
   assert not t[0].voice.default
   assert all([x.voice.signature == t[0].voice.signature for x in t[0]])
   assert not t[1].voice.default
   assert all([x.voice.signature == t[1].voice.signature for x in t[1]])
   
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


def test_signature_10( ):
   '''
   (Anonymous) staff creates its own (numeric) voice signature.
   Both (named) voices carry the same (named) signature.
   Voice leaves all carry the same signature.
   '''

   t = Staff(Voice(Note(0, (1, 8)) * 4) * 2)
   appictate(t)
   t[0].invocation.name = 'foo'
   t[1].invocation.name = 'foo'

   assert not t.voice.default
   assert t[0].voice.signature == ('foo', )
   assert t[1].voice.signature == ('foo', )
   assert all([x.voice.signature == t[0].voice.signature for x in t.leaves])

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


def test_signature_11( ):
   '''
   (Anonymous) staff creates its own (numeric) signature.
   Differently named voices create different (named) signatures.   
   Voice leaves carry the signature of their containing voice.
   '''

   t = Staff(Voice(Note(0, (1, 8)) * 4) * 2)
   appictate(t)
   t[0].invocation.name = 'foo'
   t[1].invocation.name = 'bar'

   assert t.voice.anonymous and t.voice.numeric
   assert t[0].voice.named
   assert all([x.voice.signature == t[0].voice.signature for x in t[0]])
   assert t[1].voice.named
   assert all([x.voice.signature == t[1].voice.signature for x in t[1]])
   assert t.voice.signature != t[0].voice.signature != t[1].voice.signature

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
   '''
   Top-level sequential carries the default signature.
   (Anonymous) staves create two different (numeric) signatures.
   (Anonymous) voices create two different (numeric) signatures.
   Voice leaves carry the signature of their containing voice.
   '''

   t = Sequential(Staff([Voice(Note(0, (1, 8)) * 4)]) * 2)
   appictate(t)
   
   assert t.voice.default
   assert t[0].voice.numeric
   assert t[0][0].voice.numeric
   assert t[1].voice.numeric
   assert t[1][0].voice.numeric
   assert t[0][0].voice.signature != t[1][0].voice.signature
   assert t[0][0][0].voice.signature != t[1][0][0].voice.signature

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


def test_signature_13( ):
   '''
   Top-level sequential carries default signature.
   (Anonymous) parallel staves carry two different numeric signatures.
   (Anonymous) voices each carry different numeric signatures.
   Voice contents carry the signature of their containing voice.
   Abjad identifies the default voice and six different anonymous voices.
   '''

   t = Sequential(Staff(Voice(Note(0, (1, 8)) * 4) * 2) * 2)
   appictate(t)
   t[0].brackets = 'double-angle'
   t[1].brackets = 'double-angle'

   assert t.voice.default
   assert t[0].voice.numeric
   assert t[0][0].voice.numeric
   assert t[0][1].voice.numeric
   assert t[0][0].voice.signature != t[0][1].voice.signature
   assert t[1].voice.numeric
   assert t[1][0].voice.numeric
   assert t[1][1].voice.numeric
   assert t[1][0].voice.signature != t[1][1].voice.signature
   assert t[0].voice.signature != t[1].voice.signature

   r'''
   {
      \new Staff <<
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
      >>
      \new Staff <<
         \new Voice {
            af'8
            a'8
            bf'8
            b'8
         }
         \new Voice {
            c''8
            cs''8
            d''8
            ef''8
         }
      >>
   }
   '''


def test_signature_14( ):
   '''
   The (anonymous) voice creates its own (numeric) signature.
   All components carry the signature of this (anonymous) voice.
   Abjad identifies a single voice.
   '''

   t = Voice([Sequential(Note(0, (1, 8)) * 4)] * 2)
   appictate(t)

   from abjad.component.component import _Component
   assert t.voice.numeric
   components = iterate(t, _Component)
   assert all([x.voice.signature == t.voice.signature for x in components])

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


def test_signature_15( ):
   '''
   Top-level sequential carries the default signature.
   Like-named staves carry the same (named) signature.
   Staff contents carry the same signature as their containing staves.
   Abjad identifies the default voice and one named voice.
   '''

   t = Sequential(Staff(Note(0, (1, 8)) * 4) * 2)
   appictate(t)
   t[0].invocation.name = 'foo'
   t[1].invocation.name = 'foo'

   assert t.voice.default
   assert t[0].voice.named
   assert all([x.voice.signature == t[0].voice.signature for x in t.leaves])

   r'''
   {
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
   }
   '''


def test_signature_16( ):
   '''
   Sequential-enclosed notes followed by an (anonymous) voice.
   LilyPond assigns the first four notes to the default voice.
   The (anonymous) voice creates its own (numeric) signature.
   Voice notes carry the signature of their voice.
   LilyPond does NOT allow a continous beam over all eight notes.
   Abjad identifies the default voice and one anonymous voice.
   '''

   t = Sequential([Sequential(Note(0, (1, 8)) * 4), Voice(Note(0, (1, 8)) * 4)])
   appictate(t)

   assert t.voice.default
   assert t[0].voice.default
   assert all([x.voice.default for x in t[0]])
   assert t[1].voice.numeric
   assert all([x.voice.signature == t[1].voice.signature for x in t[1]])
   
   r'''
   {
      {
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


def test_signature_17( ):
   '''
   (Anonymous) voice followed by sequential notes.
   LilyPond identifies two voice.
   LilyPond DOES allow a continous beam over all eight notes.
   '''

   t = Sequential([Voice(Note(0, (1, 8)) * 4), Sequential(Note(0, (1, 8)) * 4)])
   appictate(t)

   assert t.voice.default
   assert t[0].voice.numeric
   assert all([x.voice.signature == t[0].voice.signature for x in t[0]])
   assert all([x.voice.default for x in t[1: ]])
   
   r'''
   {
      \new Voice {
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

   
def test_signature_18( ):
   '''
   Sequential notes follow by (named) voice.
   LilyPond identifies two voices.
   LilyPond does NOT allow a continous beam over all eight notes.
   Abjad assigns the signature of the default voice to the first four notes.
   Abjad assigns the signature of the (anonymous) voice to the last four.
   '''

   t = Sequential([Sequential(Note(0, (1, 8)) * 4), Voice(Note(0, (1, 8)) * 4)])
   t[1].invocation.name = 'foo'
   appictate(t)

   assert t.voice.default
   assert t[0].voice.default
   assert all([x.voice.default for x in t[0]])
   assert t[1].voice.named
   assert all([x.voice.named for x in t[1]])

   r'''
   {
      {
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


def test_signature_19( ):
   '''(Named) voice followed by sequential-contained notes, all seq-enclosed.

      LilyPond DOES allow a continous note over all eight notes.'''

   t = Sequential([Voice(Note(0, (1, 8)) * 4), Sequential(Note(0, (1, 8)) * 4)])
   t[0].invocation.name = 'foo'
   appictate(t)

   assert t.voice.default
   assert t[0].voice.named
   assert all([x.voice.named for x in t[0]])
   assert t[1].voice.default
   assert all([x.voice.default for x in t[1]])

   r'''
   {
      \context Voice = "foo" {
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

   
def test_signature_20( ):
   '''
   Sequential notes followed by (anonymous) staff.
   LilyPond identifies two separate voices each on a different staff.
   LilyPond does NOT allow a continous beam over all eight notes.
   '''

   t = Sequential([Sequential(Note(0, (1, 8)) * 4), Staff(Note(0, (1, 8)) * 4)])
   appictate(t)

   assert t.voice.default
   assert t[0].voice.default
   assert all([x.voice.default for x in t[0]])
   assert t[1].voice.numeric
   assert all([x.voice.numeric for x in t[1]])

   r'''
   {
      {
         c'8
         cs'8
         d'8
         ef'8
      }
      \new Staff {
         e'8
         f'8
         fs'8
         g'8
      }
   }
   '''


def test_signature_21( ):
   '''
   (Anonymous) staff followed by sequential notes.
   LilyPond identifies two separate voices each on a different staff.
   LilyPond DOES all a continous beam over all eight notes.
   '''

   t = Sequential([Staff(Note(0, (1, 8)) * 4), Sequential(Note(0, (1, 8)) * 4)])
   appictate(t)

   assert t.voice.default
   assert t[0].voice.numeric
   assert all([x.voice.numeric for x in t[0]])
   assert t[1].voice.default
   assert all([x.voice.default for x in t[1]])

   r'''
   {
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
   }
   '''


def test_signature_22( ):
   '''
   Naked notes followed by (anonymous) voice.
   LilyPond renders two different voices on a single staff.
   LilyPond: does NOT allow a continuous beam over all eight notes.
   '''

   t = Sequential(Note(0, (1, 8)) * 4 + [Voice(Note(0, (1, 8)) * 4)])
   appictate(t)

   assert t.voice.default
   assert all([x.voice.default for x in t[ : 4]])
   assert t[4].voice.numeric
   assert all([x.voice.numeric for x in t[4]])

   r'''
   {
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
   }
   '''



def test_signature_23( ):
   '''
   Voice followed by naked notes.
   LilyPond renders two different consecutive voices on a single staff.
   LilyPond DOES allow a continuous beam over all eight notes.
   '''

   t = Sequential([Voice(Note(0, (1, 8)) * 4)] + Note(0, (1, 8)) * 4)
   appictate(t)

   assert t.voice.default
   assert t[0].voice.numeric
   assert all([x.voice.numeric for x in t[0]])
   assert all([x.voice.default for x in t[1 : ]])

   r'''
   {
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
   }
   '''

   
def test_signature_24( ):
   '''
   Naked notes followed by (named) voice.
   LilyPond does NOT allow a continous beam over all eight notes.
   '''

   t = Sequential(Note(0, (1, 8)) * 4 + [Voice(Note(0, (1, 8)) * 4)])
   t[4].invocation.name = 'foo'
   appictate(t)

   assert t.voice.default
   assert all([x.voice.default for x in t[ : 4]])
   assert t[4].voice.named
   assert all([x.voice.named for x in t[4]])

   r'''
   {
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
   }
   '''


def test_signature_25a( ):
   '''
   (Named) voice followed by naked notes.
   ==> LilyPond renders a single voice on a single staff!
   LilyPond DOES allow a continous beam over all eight notes.
   I think what's going on here is that LilyPond finds its first
   'music' element in the c'8 and establishes the named 'foo' voice
   to render that first music element; this means that, because
   no music element precedes the c'8 that LiyPond has no need
   to create an implicit voice beforehand.

   Intuitively, there's something very 'special' about the first
   expression that LilyPond encounters during its interpretation
   process.
   '''

   t = Sequential([Voice(Note(0, (1, 8)) * 4)] + Note(0, (1, 8)) * 4)
   appictate(t)
   t[0].invocation.name = 'foo'

   ### TODO - make these asserts work

   #assert all([x.voice.named for x in components(t)])
   #assert all([x.voice.name == 'foo' for x in components(t)])

   r'''
   {
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
   }
   '''

   
def test_signature_26( ):
   '''
   Naked notes followed by (anonymous) staff.
   LilyPond does NOT allow a continous beam over all eight notes.
   '''

   t = Sequential(Note(0, (1, 8)) * 4 + [Voice(Note(0, (1, 8)) * 4)])
   appictate(t)

   assert t.voice.default
   assert all([x.voice.default for x in t[ : 4]])
   ### TODO - write the asserts for this test

   r'''
   {
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
   }
   '''


def test_signature_27( ):
   '''
   (Anonymous) staff followed by naked notes, al sequential-enclosed.
   LilyPond does NOT allow a continous beam over all eight notes.
   '''

   s1 = Staff([Note(n, (1, 8)) for n in range(4)])
   notes = [Note(n, (1, 8)) for n in range(4, 8)]
   t = Sequential([s1] + notes)

   ### TODO - write asserts for this test

   r'''
   {
      \new Staff {
         c'8
         cs'8
         d'8
         ef'8
      }
      e'8
      f'8
      fs'8
      g'8
   }
   '''

### TODO - test tautalogical voices
### TODO - test tautological staves

def test_signature_28( ):
   '''
   Voice enclosed in tautological sequential container.
   LilyPond DOES allow a continuous beam over all eight notes.
   '''

   v = Voice([Note(n, (1, 8)) for n in range(4)])
   q = Sequential([v])
   notes = [Note(n, (1, 8)) for n in range(4, 8)]
   t = Sequential([q] + notes)

   ### TODO - write asserts

   r'''
   {
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
   }
   '''


def test_signature_29( ):
   '''
   (Named) voice enclosed in tautological sequential container.
   LilyPond DOES allow a continuous beam over all eight notes.
   '''

   v = Voice([Note(n, (1, 8)) for n in range(4)])
   v.invocation.name = 'foo'
   q = Sequential([v])
   notes = [Note(n, (1, 8)) for n in range(4, 8)]
   t = Sequential([q] + notes)

   ### TODO - write asserts

   r'''
   {
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
   }
   '''


def test_signature_29( ):
   '''
   Nested (named) voices.
   LilyPond does NOT allow a continous beam over all eight notes.
   '''

   v1 = Voice([Note(n, (1, 8)) for n in range(4)])
   v1.invocation.name = 'foo'
   v2 = Voice([v1])
   v2.invocation.name = 'bar'
   notes = [Note(n, (1, 8)) for n in range(4, 8)]
   t = Sequential([v2] + notes)

   r'''
   {
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
   }
   '''


def test_signature_30( ):
   '''
   Nested (anonymous) voices.
   LilyPond does NOT allow a continous beam over all eight notes.
   '''

   v1 = Voice([Note(n, (1, 8)) for n in range(4)])
   v2 = Voice([v1])
   notes = [Note(n, (1, 8)) for n in range(4, 8)]
   t = Sequential([v2] + notes)

   r'''
   {
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
   }
   '''


def test_signature_31( ):
   '''
   Naked notes followed by parallel (anonymous) voices.

   LilyPond does NOT allow a continous beam over the first four notes
   together with either of the other two voices of four notes.
   '''
   
   notes = [Note(n, (1, 8)) for n in range(4)]
   vtop = Voice(Note(12, (1, 8)) * 4)
   vbottom = Voice(Note(0, (1, 8)) * 4)
   p = Parallel([vtop, vbottom])
   t = Sequential(notes + [p])

   ### TODO - write asserts

   r'''
   {
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
   }
   '''


def test_signature_32( ):
   '''
   Parallel (anonymous) voices followed by naked notes.
   LilyPond three separate voices on three different staves.
   LilyPond does NOT allow a continous beam over the first four notes
   together with either of the other two voices of four notes.
   '''
   
   t = Sequential(
      [Parallel(Voice(Note(0, (1, 8)) * 4) * 2)] + Note(0, (1, 8)) * 4)
   appictate(t)

   assert t.voice.default
   assert t[0].voice.default
   assert all([x.voice.default for x in t[1 : ]])
   assert t[0][0].voice.numeric
   assert t[0][1].voice.numeric

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


def test_signature_33( ):
   '''
   LilyPond identifies three separate and strictly nested voices.
   LilyPond assigns notes (0, 1, 10, 11) to first voice.
   LilyPond assigns notes (2, 3, 8, 9) to the second voice.
   LilyPond assigns notes (4, 5, 6, 7) to the third voice.
   Abjad identifies the same three separate and strictly nested voices.
   Abjad assigns the default voice to the top-level sequential.
   Abjad assigns a different numeric signature to each of the two others.
   '''

   t = Sequential(Note(0, (1, 8)) * 4)
   a, b = Voice(Note(0, (1, 8)) * 4) * 2
   a.insert(2, b)
   t.insert(2, a)
   appictate(t)

   outer = (0, 1, 10, 11)
   middle = (2, 3, 8, 9)
   inner = (4, 5, 6, 7)
   
   assert t.voice.default
   assert all([t.leaves[n].voice.default for n in outer])
   assert t[2].voice.numeric
   assert all([t.leaves[n].voice.signature == t[2].voice.signature
      for n in middle])
   assert t[2][2].voice.numeric
   assert all([t.leaves[n].voice.signature == t[2][2].voice.signature
      for n in inner])

   r'''
   {
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
   }
   '''


def test_siganture_34( ):
   '''
   LilyPond identifies three independent and strictly nesting voices.
   LilyPond renders each of these voices on a separate staff.
   Abjad identifies these same three voices.
   '''

   t = Staff(Note(0, (1, 8)) * 4)
   a, b = t * 2
   a.insert(2, b)
   t.insert(2, a)
   appictate(t)

   assert t.voice.numeric
   assert all([t.leaves[n].voice.signature == t.voice.signature 
      for n in (0, 1, 10, 11)])
   assert t[2].voice.numeric
   assert all([t.leaves[n].voice.signature == t[2].voice.signature
      for n in (2, 3, 8, 9)])
   assert t[2][2].voice.numeric
   assert all([t.leaves[n].voice.signature == t[2][2].voice.signature
      for n in (4, 5, 6, 7)])

   r'''
   \new Staff {
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
   }
   '''
   

def test_signature_35( ):
   '''
   LilyPond voice-identificaation in strictly Nested sequentials.
   LilyPond identifies only one voice; the sequential nesting
   has nothing to do with the creation or destruction of voice.
   '''

   a, b, t = Sequential(Note(0, (1, 8)) * 4) * 3
   a.insert(2, b)
   t.insert(2, a)
   appictate(t)

   from abjad.component.component import _Component
   assert t.voice.default
   assert all([x.voice.default for x in iterate(t, _Component)])

   r'''
   {
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
   }
   '''


def test_signature_36( ):
   '''
   LilyPond identifies only one voice here.
   Abjad components all carry the signature of the default voice.
   '''

   a, b, t = FixedDurationTuplet((3, 8), Note(0, (1, 8)) * 4) * 3
   b.insert(2, a)
   t.insert(2, b)
   b.duration.target = Rational(6, 8)
   t.duration.target = Rational(9, 8)
   appictate(t)

   from abjad.component.component import _Component
   assert all([x.voice.default for x in iterate(t, _Component)])

   r'''
   \fraction \times 9/10 {
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
   }
   '''


def test_signature_37( ):
   '''
   Tautologically 'buried' voice in middle of stream of notes.
   LilyPond renders one voice nested inside another both on a single staff.
   '''

   t = Sequential(Note(0, (1, 8)) * 4)
   t.insert(2, Sequential([Sequential([Voice(Note(0, (1, 8)) * 4)])]))
   t[2][0][0].invocation.name = 'foo'
   appictate(t)

   assert all([t.leaves[x].voice.default for x in (0, 1, 6, 7)])
   assert all([t.leaves[x].voice.named for x in (2, 3, 4, 5)])

   r'''
   {
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
   }
   '''


def test_signature_38( ):
   '''
   Tautologically 'buried' voice at the beginning of a stream of notes.
   LilyPond renders a single voice on a single staff.
   '''

   t = Sequential(Note(0, (1, 8)) * 4)
   t.insert(0, Sequential([Sequential([Voice(Note(0, (1, 8)) * 4)])]))
   t[0][0][0].invocation.name = 'foo'
   appictate(t)

   ### TODO -- make this assert work

   #assert all([x.voice.named for x in components(t)])

   r'''
   {
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
   }
   '''


def test_signature_39( ):
   '''
   Governing voice with intervening tautological sequentials.
   LilyPond renders one voice nested inside another, on a single staff.
   The tautological sequentials do not affect voice resolution.
   '''

   t = Sequential(Note(0, (1, 8)) * 4)
   t.insert(2, Voice(Note(0, (1, 8)) * 4))
   t = Sequential([t])
   t = Sequential([t])
   t = Voice([t])
   appictate(t)

   ### TODO -- make these asserts work

   #assert t.voice.default
   #assert t[0].voice.default
   #assert t[0][0].voice.default
   #assert t[0][0][0].voice.default
   #assert all([x.voice.numeric for x in components(t[0][0][0][2])])
  
   r'''
   \new Voice {
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
   }
   '''
 
def test_signature_40( ):
   '''
   Tautological sequentials filled with notes.
   LilyPond renders one voice nested inside another both on a single staff.
   The tautological sequentials do not affect voice resolution.
   '''

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

   from abjad.component.component import _Component
   assert all([x.voice.name == 'bar' for x in iterate(v, _Component)])
   components_t = set(list(iterate(t, _Component)))
   components_v = set(list(iterate(v, _Component)))
   assert all([x.voice.name == 'foo' 
      for x in components_t - components_v])

   r'''
   \context Voice = "foo" {
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
   }
   '''


def test_signature_41( ):
   '''
   Expression-initial voice followed by second explicit voice fb notes.
   '''

   t = Sequential(Note(0, (1, 8)) * 4)
   t[0 : 0] = Voice(Note(0, (1, 8)) * 4) * 2
   appictate(t)

   r'''
   {
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
   }
   '''
