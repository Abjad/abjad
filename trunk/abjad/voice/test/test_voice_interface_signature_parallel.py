from abjad import *


def test_voice_interface_signature_parallel_01( ):
   '''Top-level parallel containing only notes.
      LilyPond renders four separate voices each on a seaprate staff.
      Abjad identified five separate voices.
      Abjad assigns the orphan parallel to the default voice.
      Abjad assigns each of the four parallel notes to a 
      different (anonymous) voice.'''

   t = Parallel(Note(0, (1, 8)) * 4)
   appictate(t)

   assert t.voice.default
   assert not any([x.voice.signature == t.voice.signature for x in t])

   r'''
   <<
      c'8
      cs'8
      d'8
      ef'8
   >>
   '''
 

def test_voice_interface_signature_parallel_01b( ):
   '''Top-level (anonymous) parallel staff containing only notes.
      LilyPond renders a single staff containing four separate voices.
      Abjad identifies five separate voices.
      Abjad assigns the (anonymous) staff a numeric signature.
      Abjad assigns each of the four notes a different numeric signature.'''

   t = Staff(Note(0, (1, 8)) * 4)
   t.brackets = 'double-angle'
   appictate(t)

   assert t.voice.numeric
   assert all([x.voice.numeric for x in t])
   assert t.voice.signature != t[0].voice.signature != t[1].voice.signature

   r'''
   \new Staff <<
      c'8
      cs'8
      d'8
      ef'8
   >>
   '''
 

def test_voice_interface_signature_parallel_02( ):
   '''Parallel notes nested inside top-level sequential.
      LilyPond renders a single voice on a single staff.
      ==> LilyPond renders the four parallel notes as a single chord!
      Abjad identifies a single (default) voice.
      All components carry the signature of the (default) voice.'''

   t = Sequential(Note(0, (1, 8)) * 4)
   p = Parallel(Note(0, (1, 8)) * 4)
   t.insert(2, p)
   appictate(t)

   from abjad.component.component import _Component
   assert all([x.voice.default for x in iterate(t, _Component)])

   r'''
   {
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
   }
   '''
 

def test_voice_interface_signature_parallel_03( ):
   '''Parallel notes nested inside top-level (anonymous) voice.
      LilyPond renders as in test 02, above.
      Abjad identifies a single (anonymous) voice.
      All components carry the signature of the (anonymous) voice.'''

   t = Voice(Note(0, (1, 8)) * 4)
   p = Parallel(Note(0, (1, 8)) * 4)
   t.insert(2, p)
   appictate(t)

   from abjad.component.component import _Component
   components = iterate(t, _Component)
   assert all([x.voice.signature == t.voice.signature for x in components])

   r'''
   \new Voice {
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
   }
   '''


def test_voice_interface_signature_parallel_04( ):
   '''Sequential containers of notes enclosed in *orphan* parallel.
      LilyPond renders two separate voices each in a separate staff.
      Abjad identifies three separate voices.
      Abjad assigns the orphan parallel to the default voice.
      Abjad assigns each of the sequential to a different (anonymous) voice.'''

   t = Parallel(Sequential(Note(0, (1, 8)) * 4) * 2)
   appictate(t)

   assert t.voice.default
   assert all([x.voice.signature == t[0].voice.signature for x in t[0]])
   assert all([x.voice.signature == t[1].voice.signature for x in t[1]])
   assert t.voice.signature != t[0].voice.signature != t[1].voice.signature

   r'''
   <<
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
   >>
   '''


def test_voice_interface_signature_parallel_05( ):
   '''Sequential containers of notes enclosed in *parented* parallel.
      LilyPond renders a single voice on a single staff.
      LilyPond renders the parallel sequential containers as two-note chords.
      Abjad identifies only a single (default) voice.'''

   p = Parallel(Sequential(Note(0, (1, 8)) * 4) * 2)
   t = Sequential(Note(0, (1, 8)) * 4)
   t.insert(2, p)
   appictate(t)

   from abjad.component.component import _Component
   assert all([x.voice.default for x in iterate(t, _Component)])

   r'''
   {
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
   }
   '''


def test_voice_interface_signature_parallel_06( ):
   '''(Anonymous) voices enclosed in *parented* parallel.
      LilyPond render three separate voices on a single staff.
      LilyPond groups leaves 0, 1, 10, 11 into an outer discontiguous voice.
      LilyPond groups leaves 2, 3, 4, 5 into a second voice.
      LilyPond groups leaves 6, 7, 8, 9 into a third voice.
      Abjad identifies three separate voices.
      Abjad assigns the sequential and its immediate contents to the deafault v.
      Abjad assigns each explicit (anonymous) voice to a different signature.'''

   p = Parallel(Voice(Note(0, (1, 8)) * 4) * 2)
   t = Sequential(Note(0, (1, 8)) * 4)
   t.insert(2, p)
   appictate(t)

   assert t.voice.default
   assert all([t.leaves[i].voice.default for i in (0, 1, 10, 11)])
   assert t[2].voice.default
   assert all([x.voice.signature == t[2][0].voice.signature for x in t[2][0]])
   assert all([x.voice.signature == t[2][1].voice.signature for x in t[2][1]])
   assert t.voice.signature != t[2][0].voice.signature != \
      t[2][1].voice.signature

   r'''
   {
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
   }
   '''
