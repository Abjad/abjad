from abjad import *
import py.test


def test_lily_voice_resolution_01( ):
   '''Sequential with a sequence of leaves,
      in the middle of which there is a parallel.
      How does LilyPond resolve voices?'''

   t = Sequential(run(4))
   t.insert(2, Parallel(Sequential(run(2)) * 2))
   diatonicize(t)
   t.notehead.color = 'red'

   r'''{
           \override NoteHead #'color = #red
           c'8
           d'8
           <<
                   {
                           e'8
                           f'8
                   }
                   {
                           g'8
                           a'8
                   }
           >>
           b'8
           c''8
           \revert NoteHead #'color
   }'''

   '''LilyPond groups all eight notes here together into a single voice.
      LilyPond colors all eight noteheads red.
      LilyPond fills the third and fourth moments with thirds.
      How should Abjad resolve voices?'''


def test_lily_voice_resolution_02( ):
   '''Named with  with a sequence of leaves,
      in the middle of which there is a parallel.
      How does LilyPond resolve voices?'''

   t = Voice(run(4))
   t.invocation.name = 'foo'
   t.insert(2, Parallel(Sequential(run(2)) * 2))
   diatonicize(t)
   t.notehead.color = 'red'

   r'''\context Voice = "foo" \with {
           \override NoteHead #'color = #red
   } {
           c'8
           d'8
           <<
                   {
                           e'8
                           f'8
                   }
                   {
                           g'8
                           a'8
                   }
           >>
           b'8
           c''8
   }'''

   '''LilyPond groups all eight notes here together into a single voice.
      LilyPond colors all eight noteheads red.
      LilyPond fills the third and fourth moments with thirds.
      Exactly the same LilyPond voice resolution as in the previous test.
      How should Abjad resolve voices?'''


def test_lily_voice_resolution_03( ):
   '''Anonymous voice with  with a sequence of leaves,
      in the middle of which there is a parallel.
      How does LilyPond resolve voices?'''

   t = Voice(run(4))
   t.insert(2, Parallel(Sequential(run(2)) * 2))
   diatonicize(t)
   t.notehead.color = 'red'

   r'''\new Voice \with {
           \override NoteHead #'color = #red
   } {
           c'8
           d'8
           <<
                   {
                           e'8
                           f'8
                   }
                   {
                           g'8
                           a'8
                   }
           >>
           b'8
           c''8
   }'''


   '''LilyPond groups all eight notes here together into a single voice.
      LilyPond colors all eight noteheads red.
      LilyPond fills the third and fourth moments with thirds.
      Exactly the same LilyPond voice resolution as in the previous tests.
      How should Abjad resolve voices?'''


def test_lily_voice_resolution_04( ):
   '''Anonymous voice with  with a sequence of leaves,
      in the middle of which there is a parallel,
      which in turn contains two anonymous voices.
      How does LilyPond resolve voices?'''

   t = Voice(run(4))
   t.insert(2, Parallel(Voice(run(2)) * 2))
   diatonicize(t)
   t.notehead.color = 'red'

   r'''\new Voice \with {
           \override NoteHead #'color = #red
   } {
           c'8
           d'8
           <<
                   \new Voice {
                           e'8
                           f'8
                   }
                   \new Voice {
                           g'8
                           a'8
                   }
           >>
           b'8
           c''8
   }'''

   '''LilyPond identifies three separate voices.
      LilyPond colors the outer four notes (c'8 d'8 b'8 c''8) red.
      LilyPond colors the inner four notes black.
      LilyPond issues clashing note column warnings for the inner notes. 
      How should Abjad resolve voices?'''


def test_lily_voice_resolution_05( ):
   '''Named voice with  with a sequence of leaves,
      in the middle of which there is a parallel,
      which in turn contains one like-named and one differently named voice.
      How does LilyPond resolve voices?'''

   t = Voice(run(4))
   t.invocation.name = 'foo'
   t.insert(2, Parallel(Voice(run(2)) * 2))
   t[2][0].invocation.name = 'foo'
   diatonicize(t)
   t.notehead.color = 'red'

   r'''\context Voice = "foo" \with {
           \override NoteHead #'color = #red
   } {
           c'8
           d'8
           <<
                   \context Voice = "foo" {
                           e'8
                           f'8
                   }
                   \new Voice {
                           g'8
                           a'8
                   }
           >>
           b'8
           c''8
   }
   '''

   '''LilyPond colors six notes red and two notes black.
      LilyPond identifies two voices.''' 


def test_lily_voice_resolution_06( ):
   '''Two like-named voices in two differently named staves.'''

   t = Sequential(Staff([Voice(scale(2))]) * 2)
   t[0].invocation.name = 'staff1'
   t[1].invocation.name = 'staff2'
   t[0][0].invocation.name = 'voicefoo'
   t[1][0].invocation.name = 'voicefoo'
   diatonicize(t)
   py.test.raises(ContiguityError, 'Beam(t.leaves)')

   '''LilyPond gives unterminated beam warnings.
      LilyPond gives grob direction programming errors.
      We conclude that LilyPond identifies two separate voices.
      Good example for Abjad voice resolution.'''


def test_lily_voice_resolution_07( ):
   '''Sequential containing a run of leaves.
      Two like-structured parallels in the middle of the run.'''

   t = Sequential(run(2))
   t[1:1] = Parallel(Voice(run(2)) * 2) * 2
   t[1][0].invocation.name = 'alto'
   t[1][1].invocation.name = 'soprano'
   t[2][0].invocation.name = 'alto'
   t[2][1].invocation.name = 'soprano'
   diatonicize(t)

   t[1][1][0].formatter.before.append(r"\override NoteHead #'color = #red")
   t[2][1][-1].formatter.after.append(r"\revert NoteHead #'color")

   r'''{
           c'8
           <<
                   \context Voice = "alto" {
                           d'8
                           e'8
                   }
                   \context Voice = "soprano" {
                           \override NoteHead #'color = #red
                           f'8
                           g'8
                   }
           >>
           <<
                   \context Voice = "alto" {
                           a'8
                           b'8
                   }
                   \context Voice = "soprano" {
                           c''8
                           d''8
                           \revert NoteHead #'color
                   }
           >>
           e''8
   }'''

   '''LilyPond handles this example perfectly.
      LilyPond colors the four noteheads of the soprano voice red.
      LilyPond colors all other noteheads black.'''
