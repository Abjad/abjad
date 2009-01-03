from abjad import *
import py.test


def test_spanned_parallel_container_01( ):
   '''
   Abjad lets you span whatever you want.
   Abjad spanners will not inspect the contents of parallel containers.
   '''

   t = Parallel([ ])
   p = Beam(t)

   assert len(p.components) == 1
   assert p.components[0] is t
   assert len(p.leaves) == 0
   assert t.format == '<<\n>>'


def test_spanned_parallel_container_02( ):
   '''
   Nonempty spanned parallel container;
   '''

   t = Parallel(Sequential(run(4)) * 2)
   appictate(t)
   p = Beam(t)

   assert len(p.components) == 1
   assert p.components[0] is t
   assert len(p.leaves) == 0
   assert t.format == "<<\n\t{\n\t\tc'8\n\t\tcs'8\n\t\td'8\n\t\tef'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t\tfs'8\n\t\tg'8\n\t}\n>>"

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


def test_spanned_parallel_container_03( ):
   '''
   Abjad lets you span whatever you want.
   Sequential container accepts spanner,
   even lodged within parallel parent container.
   '''

   t = Parallel(Sequential(run(4)) * 2)
   appictate(t)
   p = Beam(t[0])

   assert len(p.components) == 1
   assert isinstance(p.components[0], Sequential)
   assert t.format == "<<\n\t{\n\t\tc'8 [\n\t\tcs'8\n\t\td'8\n\t\tef'8 ]\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t\tfs'8\n\t\tg'8\n\t}\n>>"

   r'''
   <<
      {
         c'8 [
         cs'8
         d'8
         ef'8 ]
      }
      {
         e'8
         f'8
         fs'8
         g'8
      }
   >>
   '''


def test_spanned_parallel_container_04( ):
   '''
   Abjad ignores intervening parallel container.
   LilyPond is happy here.
   '''

   t = Staff(run(4))
   t.insert(2, Parallel(Sequential(run(4)) * 2))
   appictate(t)
   p = Beam(t)

   assert len(p.components) == 1
   assert len(p.leaves) == 4
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\t<<\n\t\t{\n\t\t\td'8\n\t\t\tef'8\n\t\t\te'8\n\t\t\tf'8\n\t\t}\n\t\t{\n\t\t\tfs'8\n\t\t\tg'8\n\t\t\taf'8\n\t\t\ta'8\n\t\t}\n\t>>\n\tbf'8\n\tb'8 ]\n}"

   r'''
   \new Staff {
      c'8 [
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
      b'8 ]
   }
   '''


def test_spanned_parallel_container_05( ):
   '''
   Abjad ignores intervening empty parallel containers.
   LilyPond is happy here.
   '''

   t = Staff(run(4))
   t.insert(2, Parallel([ ]))
   appictate(t)
   p = Beam(t)

   assert len(p.components) == 1
   assert len(p.leaves) == 4
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\t<<\n\t>>\n\td'8\n\tef'8 ]\n}"
   
   r'''
   \new Staff {
      c'8 [
      cs'8
      <<
      >>
      d'8
      ef'8 ]
   }
   '''


def test_spanned_parallel_container_06( ):
   '''
   Abjad lets you span whatever you want.
   You can select through parallel and sequential structures.
   LilyPond is happy here again.
   '''

   t = Staff(Voice(run(4)) * 2)
   t[0].invocation.name, t[1].invocation.name = 'foo', 'foo'
   t.insert(1, Parallel(Voice(run(4)) * 2))
   t[1][0].invocation.name = 'foo'
   t[1][1].invocation.name = 'bar'
   appictate(t)
   p = Beam((t[0], t[1][0], t[2]))

   assert len(p.components) == 3
   assert p.components[0] is t[0]
   assert p.components[1] is t[1][0]
   assert p.components[2] is t[2]
   assert len(p.leaves) == 12
   assert t.format == '\\new Staff {\n\t\\context Voice = "foo" {\n\t\tc\'8 [\n\t\tcs\'8\n\t\td\'8\n\t\tef\'8\n\t}\n\t<<\n\t\t\\context Voice = "foo" {\n\t\t\te\'8\n\t\t\tf\'8\n\t\t\tfs\'8\n\t\t\tg\'8\n\t\t}\n\t\t\\context Voice = "bar" {\n\t\t\taf\'8\n\t\t\ta\'8\n\t\t\tbf\'8\n\t\t\tb\'8\n\t\t}\n\t>>\n\t\\context Voice = "foo" {\n\t\tc\'\'8\n\t\tcs\'\'8\n\t\td\'\'8\n\t\tef\'\'8 ]\n\t}\n}'

   r'''
   \new Staff {
      \context Voice = "foo" {
         c'8 [
         cs'8
         d'8
         ef'8
      }
      <<
         \context Voice = "foo" {
            e'8
            f'8
            fs'8
            g'8
         }
         \context Voice = "bar" {
            af'8
            a'8
            bf'8
            b'8
         }
      >>
      \context Voice = "foo" {
         c''8
         cs''8
         d''8
         ef''8 ]
      }
   }
   '''
