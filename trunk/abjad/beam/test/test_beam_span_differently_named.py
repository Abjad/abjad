from abjad import *
import py.test


def test_span_differently_named_01( ):
   '''
   You can span containers however you.
   LilyPond will render beams correctly through some combinations of container.
   LilyPond will not render beams correctly through others.
   Abjad gives you enough rope to hang yourself, so span intelligently.
   '''

   v1 = Voice(run(4))
   v1.invocation.name = 'foo'
   v2 = Voice(run(4))
   v2.invocation.name = 'bar'
   t = Staff([v1, v2])
   appictate(t)

   p = Beam(t)
   assert t.format == '\\new Staff {\n\t\\context Voice = "foo" {\n\t\tc\'8 [\n\t\tcs\'8\n\t\td\'8\n\t\tef\'8\n\t}\n\t\\context Voice = "bar" {\n\t\te\'8\n\t\tf\'8\n\t\tfs\'8\n\t\tg\'8 ]\n\t}\n}'
   r'''
   \new Staff {
      \context Voice = "foo" {
         c'8 [
         cs'8
         d'8
         ef'8
      }
      \context Voice = "bar" {
         e'8
         f'8
         fs'8
         g'8 ]
      }
   }
   '''
   p.clear( )

   p = Beam(t[0])
   assert t.format == '\\new Staff {\n\t\\context Voice = "foo" {\n\t\tc\'8 [\n\t\tcs\'8\n\t\td\'8\n\t\tef\'8 ]\n\t}\n\t\\context Voice = "bar" {\n\t\te\'8\n\t\tf\'8\n\t\tfs\'8\n\t\tg\'8\n\t}\n}'
   r'''
   \new Staff {
      \context Voice = "foo" {
         c'8 [
         cs'8
         d'8
         ef'8 ]
      }
      \context Voice = "bar" {
         e'8
         f'8
         fs'8
         g'8
      }
   }
   '''
   p.clear( )




def test_span_differently_named_02( ):
   '''
   Abjad lets you span whatever you want.
   '''

   t = Sequential(Staff(Voice(run(4)) * 2) * 2)
   t[0].brackets = 'double-angle'
   t[1].brackets = 'double-angle'
   t[0].invocation.name, t[1].invocation.name = 'foo', 'foo'
   t[0][0].invocation.name, t[1][0].invocation.name = 'first', 'first'
   t[0][1].invocation.name, t[1][1].invocation.name = 'second', 'second'
   appictate(t)

   p = Beam([t[0][0], t[1][0]])
   assert t.format == '{\n\t\\context Staff = "foo" <<\n\t\t\\context Voice = "first" {\n\t\t\tc\'8 [\n\t\t\tcs\'8\n\t\t\td\'8\n\t\t\tef\'8\n\t\t}\n\t\t\\context Voice = "second" {\n\t\t\te\'8\n\t\t\tf\'8\n\t\t\tfs\'8\n\t\t\tg\'8\n\t\t}\n\t>>\n\t\\context Staff = "foo" <<\n\t\t\\context Voice = "first" {\n\t\t\taf\'8\n\t\t\ta\'8\n\t\t\tbf\'8\n\t\t\tb\'8 ]\n\t\t}\n\t\t\\context Voice = "second" {\n\t\t\tc\'\'8\n\t\t\tcs\'\'8\n\t\t\td\'\'8\n\t\t\tef\'\'8\n\t\t}\n\t>>\n}'
   r'''
   {
      \context Staff = "foo" <<
         \context Voice = "first" {
            c'8 [
            cs'8
            d'8
            ef'8
         }
         \context Voice = "second" {
            e'8
            f'8
            fs'8
            g'8
         }
      >>
      \context Staff = "foo" <<
         \context Voice = "first" {
            af'8
            a'8
            bf'8
            b'8 ]
         }
         \context Voice = "second" {
            c''8
            cs''8
            d''8
            ef''8
         }
      >>
   }
   '''
   p.clear( )


   p = Beam([t[0][1], t[1][1]])
   assert t.format == '{\n\t\\context Staff = "foo" <<\n\t\t\\context Voice = "first" {\n\t\t\tc\'8\n\t\t\tcs\'8\n\t\t\td\'8\n\t\t\tef\'8\n\t\t}\n\t\t\\context Voice = "second" {\n\t\t\te\'8 [\n\t\t\tf\'8\n\t\t\tfs\'8\n\t\t\tg\'8\n\t\t}\n\t>>\n\t\\context Staff = "foo" <<\n\t\t\\context Voice = "first" {\n\t\t\taf\'8\n\t\t\ta\'8\n\t\t\tbf\'8\n\t\t\tb\'8\n\t\t}\n\t\t\\context Voice = "second" {\n\t\t\tc\'\'8\n\t\t\tcs\'\'8\n\t\t\td\'\'8\n\t\t\tef\'\'8 ]\n\t\t}\n\t>>\n}'
   r'''
   {
      \context Staff = "foo" <<
         \context Voice = "first" {
            c'8
            cs'8
            d'8
            ef'8
         }
         \context Voice = "second" {
            e'8 [
            f'8
            fs'8
            g'8
         }
      >>
      \context Staff = "foo" <<
         \context Voice = "first" {
            af'8
            a'8
            bf'8
            b'8
         }
         \context Voice = "second" {
            c''8
            cs''8
            d''8
            ef''8 ]
         }
      >>
   }
   '''
   p.clear( )
