from abjad import *
import py.test


def test_signature_01( ):
   '''Unincorporated leaves carry no voice signature.'''

   assert Note(0, (1, 4)).voice.signature is None
   assert Rest((1, 4)).voice.signature is None
   assert Chord([2, 3, 4], (1, 4)).voice.signature is None
   assert Skip((1, 4)).voice.signature is None


def test_signature_02( ):
   '''Unincorporated sequential container carries 
      the default -1 voice signature;
      sequentialized leaves carry the voice signature 
      of their containing sequential container.'''

   t = Sequential([Note(n, (1, 8)) for n in range(4)])

   assert t.voice.signature == (-1, )
   assert t[0].voice.signature == (-1, )
   assert t[1].voice.signature == (-1, )
   assert t[2].voice.signature == (-1, )
   assert t[3].voice.signature == (-1, )

   r'''
   {
      c'8
      cs'8
      d'8
      ef'8
   }
   '''


def test_signature_03( ):
   '''Unincorporated tuplet carries the default -1 voice signature;
      tupletted notes carry the voice signature of their containing tuplet.'''
   
   t = FixedDurationTuplet((2, 8), [Note(n, (1, 8)) for n in range(3)])

   assert t.voice.signature == (-1, )
   assert t[0].voice.signature == (-1, )
   assert t[1].voice.signature == (-1, )
   assert t[2].voice.signature == (-1, )

   r'''
   \times 2/3 {
      c'8
      cs'8
      d'8
   }
   '''


def test_signature_04( ):
   '''Parallel container carries no voice signature.
      Parallelized leaves each carry a different voice signature.'''

   t = Parallel([Note(n, (1, 8)) for n in range(4)])

   assert t.voice.signature is None
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
   '''Unincorporated staff carries no voice signature;
      in-staff leaves each carry the same signature.'''

   t = Staff([Note(i, (1, 8)) for i in range(4)])

   assert t.voice.signature is None
   assert len(set([x.voice.signature for x in t])) == 1

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

   assert t.voice.signature == (id(t), )
   components = instances(t, '_Component')
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
   '''Voice creates its own voice signature;
      all other components here inherit signature from voice.'''

   t1 = FixedDurationTuplet((2, 8), [Note(i, (1, 8)) for i in range(3)])
   t2 = FixedDurationTuplet((2, 8), [Note(i, (1, 8)) for i in range(3, 6)])
   t = Voice([t1, t2])

   assert t.voice.signature == (id(t), )
   components = instances(t, '_Component')
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
   '''Staff can not be contained in voice and carries no voice signature;
      each voice creates its own voice signature;
      in-voice contents inherit signature from voice.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   t = Staff([v1, v2])

   assert t.voice.signature is None
   assert t[0].voice.signature == (id(t[0]), )
   assert all([x.voice.signature == t[0].voice.signature for x in t[0]])
   assert t[1].voice.signature == (id(t[1]), )
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
   '''Staff can not be voice-contained and so carries no voice signature;
      both named voices carry the same signature;
      in-voice contents inherit signature from voice.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v1.invocation.name = 'foo'
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   v2.invocation.name = 'foo'
   t = Staff([v1, v2])

   assert t.voice.signature is None
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
   '''Staff can not be voice-contained and so carries no voice signature;
      the differently named voices here carry different signatures;
      in-voice contents inherit signature from containing voice.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v1.invocation.name = 'foo'
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 88)])
   v2.invocation.name = 'bar'
   t = Staff([v1, v2])

   assert t.voice.signature is None
   assert t[0].voice.signature == ('foo', )
   assert all([x.voice.signature == t[0].voice.signature for x in t[0]])
   assert t[1].voice.signature == ('bar', )
   assert all([x.voice.signature == t[1].voice.signature for x in t[1]])

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
   '''Outermost sequential container contains voice-breakers and
      so carries no voice signature;
      staves can not be voice-contained and so carry no voice signatures;
      different anonymous voices carry different numeric voice signatures;
      in-voice components inherit signature from voice.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   s1 = Staff([v1])
   s2 = Staff([v2])
   t = Sequential([s1, s2])
   
   assert t.voice.signature is None
   assert t[0].voice.signature is None
   assert t[0][0].voice.signature == (id(t[0][0]), )
   assert t[1].voice.signature is None
   assert t[1][0].voice.signature == (id(t[1][0]), )
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
   '''Results.'''

   vl1 = Voice([Note(i, (1, 8)) for i in range(4)])
   vl2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   vh1 = Voice([Note(i, (1, 8)) for i in range(12, 16)])
   vh2 = Voice([Note(i, (1, 8)) for i in range(16, 20)])
   s1 = Staff([vh1, vl1])
   s1.brackets = 'double-angle'
   s2 = Staff([vl2, vh2])
   s2.brackets = 'double-angle'
   t = Sequential([s1, s2])

   assert t.voice.signature is None
   assert t[0].voice.signature is None
   assert t[0][0].voice.signature == (id(t[0][0]), )
   assert t[0][1].voice.signature == (id(t[0][1]), )
   assert t[0][0].voice.signature != t[0][1].voice.signature
   assert t[1].voice.signature is None
   assert t[1][0].voice.signature == (id(t[1][0]), )
   assert t[1][1].voice.signature == (id(t[1][1]), )
   assert t[1][0].voice.signature != t[1][1].voice.signature

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


def test_signature_14( ):
   '''The voice creates its own voice signature;
      all other components here inherit their signature from voice.'''

   s1 = Sequential([Note(i, (1, 8)) for i in range(4)])
   s1 = Sequential([s1])
   s2 = Sequential([Note(i, (1, 8)) for i in range(4, 8)])
   s2 = Sequential([s2])
   t = Voice([s1, s2])

   assert t.voice.signature == (id(t), )
   components = instances(t, '_Component')
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
   '''The topmost sequential here carries no voice signature;
      the two named staves here carry no voice signature;
      the contents of each staff derive signature from an implicit voice.'''

   s1 = Staff([Note(n, (1, 8)) for n in range(4)])
   s1.invocation.name = 'foo'
   s2 = Staff([Note(n, (1, 8)) for n in range(4, 8)])
   s2.invocation.name = 'foo'
   t = Sequential([s1, s2])

   assert t.voice.signature is None
   assert t[0].voice.signature is None
   assert len(set([x.voice.signature for x in t[0]])) == 1
   assert t[1].voice.signature is None
   assert len(set([x.voice.signature for x in t[1]])) == 1
   assert t[0][0].voice.signature != t[1][0].voice.signature

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
   '''Sequential-enclosed notes followed by (anonymous) voice, all enclosed.

      LilyPond does NOT allow a continous beam over all eight notes.'''

   s1 = Sequential([Note(n, (1, 8)) for n in range(4)])
   v1 = Voice([Note(n, (1, 8)) for n in range(4, 8)])
   t = Sequential([s1, v1])

   ### TODO - write the asserts for this test

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
   '''(Anonymous) voice followed by sequential-enclosed notes, all enclosed.

      LilyPond DOES allow a continous beam over all eight notes.'''

   v1 = Voice([Note(n, (1, 8)) for n in range(4)])
   s1 = Sequential([Note(n, (1, 8)) for n in range(4, 8)])
   t = Sequential([v1, s1])

   ### TODO - write asserts for this test

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
   '''Sequential-enclosed notes follow by (named) voice, all seq-enclosed.

      LilyPond does NOT allow a continous beam over all eight notes.'''

   s1 = Sequential([Note(n, (1, 8)) for n in range(4)])
   v1 = Voice([Note(n, (1, 8)) for n in range(4, 8)])
   v1.invocation.name = 'foo'
   t = Sequential([s1, v1])

   ### TODO - write the asserts for this test

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

   v1 = Voice([Note(n, (1, 8)) for n in range(4)])
   v1.invocation.name
   s1 = Sequential([Note(n, (1, 8)) for n in range(4, 8)])
   t = Sequential([v1, s1])

   ### TODO - write asserts for this test

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
   '''Sequential-enclosed notes followed by (anonymous) staff, seq-enclosed.

      LilyPond does NOT allow a continous beam over all eight notes.'''

   sq1 = Sequential([Note(n, (1, 8)) for n in range(4)])
   st1 = Staff([Note(n, (1, 8)) for n in range(4, 8)])
   t = Sequential([sq1, st1])

   ### TODO - write the asserts for this test

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
   '''(Anonymous) staff followed by sequential-enclosed notes.

      LilyPond DOES all a continous beam over all eight notes.'''

   st1 = Staff([Note(n, (1, 8)) for n in range(4)])
   sq1 = Sequential([Note(n, (1, 8)) for n in range(4, 8)])
   t = Sequential([st1, sq1])

   ### TODO - write asserts for this test

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
   '''Naked notes followed by (anonymous) voice, all enclosed.
   
      LilyPond: does NOT allow a continuous beam over all eight notes.'''

   notes = [Note(n, (1, 8)) for n in range(4)]
   v1 = Voice([Note(n, (1, 8)) for n in range(4, 8)])
   t = Sequential(notes + [v1])

   ### TODO - write the asserts for this test

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
   '''Voice followed by nake notes, all enclosed.

      LilyPond DOES allow a continuous beam over all eight notes.'''

   v1 = Voice([Note(n, (1, 8)) for n in range(4)])
   notes = [Note(n, (1, 8)) for n in range(4, 8)]
   t = Sequential([v1] + notes)

   ### TODO - write asserts for this test

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
   '''Naked notes followed by (named) voice, all enclosed.

      LilyPond does NOT allow a continous beam over all eight notes.'''

   notes = [Note(n, (1, 8)) for n in range(4)]
   v1 = Voice([Note(n, (1, 8)) for n in range(4, 8)])
   v1.invocation.name = 'foo'
   t = Sequential(notes + [v1])

   ### TODO - write the asserts for this test

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


def test_signature_25( ):
   '''(Named) voice followed by naked notes, all sequential-enclosed.

      LilyPond DOES allow a continous beam over all eight notes.'''

   v1 = Voice([Note(n, (1, 8)) for n in range(4)])
   v1.invocation.name = 'foo'
   notes = [Note(n, (1, 8)) for n in range(4, 8)]
   t = Sequential([v1] + notes)

   ### TODO - write asserts for this test

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

   
def test_signature_26( ):
   '''Naked notes followed by (anonymous) staff, all sequential-enclosed.

      LilyPond does NOT allow a continous beam over all eight notes.'''

   notes = [Note(n, (1, 8)) for n in range(4)]
   s1 = Staff([Note(n, (1, 8)) for n in range(4, 8)])
   t = Sequential(notes + [s1])

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
   '''(Anonymous) staff followed by naked notes, al sequential-enclosed.

      LilyPond does NOT allow a continous beam over all eight notes.'''

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
