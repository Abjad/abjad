from abjad import *
import py.test


def test_like_named_01( ):
   '''Abjad lets you span whatever you want.
      With like-named containers this poses no problem for LilyPond.'''

   t = Staff(Voice(run(4)) * 2)
   t[0].invocation.name = 'foo'
   t[1].invocation.name = 'foo'
   appictate(t)

   p = Beam(t)
   assert len(p.components) == 1
   assert isinstance(p.components[0], Staff)
   assert len(p.leaves) == 8
   assert t.format == '\\new Staff {\n\t\\context Voice = "foo" {\n\t\tc\'8 [\n\t\tcs\'8\n\t\td\'8\n\t\tef\'8\n\t}\n\t\\context Voice = "foo" {\n\t\te\'8\n\t\tf\'8\n\t\tfs\'8\n\t\tg\'8 ]\n\t}\n}'
   p.clear( )

   p = Beam(t[ : ])
   assert len(p.components) == 2
   for x in p.components:
      assert isinstance(x, Voice)
   assert len(p.leaves) == 8
   assert t.format == '\\new Staff {\n\t\\context Voice = "foo" {\n\t\tc\'8 [\n\t\tcs\'8\n\t\td\'8\n\t\tef\'8\n\t}\n\t\\context Voice = "foo" {\n\t\te\'8\n\t\tf\'8\n\t\tfs\'8\n\t\tg\'8 ]\n\t}\n}'

   r'''
   \new Staff {
      \context Voice = "foo" {
         c'8 [
         cs'8
         d'8
         ef'8
      }
      \context Voice = "foo" {
         e'8
         f'8
         fs'8
         g'8 ]
      }
   }
   '''

 
def test_span_like_named_02( ):
   '''
   Abjad lets you span whatever you want.
   No LilyPond problem for like-named containers.
   '''

   t = Sequential(Staff([Voice(run(4))]) * 2)
   t[0].invocation.name, t[1].invocation.name = 'foo', 'foo'
   t[0][0].invocation.name, t[1][0].invocation.name = 'bar', 'bar'
   appictate(t)
   
   p = Beam(t)
   assert len(p.components) == 1
   assert isinstance(p.components[0], Sequential)
   assert len(p.leaves) == 8
   p.clear( )

   p = Beam(t[ : ])
   assert len(p.components) == 2
   for x in p.components:
      assert isinstance(x, Staff)
   assert len(p.leaves) == 8

   p = Beam([t[0][0], t[1][0]])
   assert len(p.components) == 2
   for x in p.components:
      assert isinstance(x, Voice)
   assert len(p.leaves) == 8

   r'''
   {
      \context Staff = "foo" {
         \context Voice = "bar" {
            c'8 [
            cs'8
            d'8
            ef'8
         }
      }
      \context Staff = "foo" {
         \context Voice = "bar" {
            e'8
            f'8
            fs'8
            g'8 ]
         }
      }
   }
   '''


def test_span_like_named_03( ):
   '''
   Like-named containers need not be lexically contiguous.
   '''

   t = Sequential(Staff(Voice(run(4)) * 2) * 2)
   t[0].invocation.name, t[1].invocation.name = 'foo', 'foo'
   #t[0].brackets = 'double-angle'
   #t[1].brackets = 'double-angle'
   t[0].parallel = True
   t[1].parallel = True
   t[0][0].invocation.name, t[1][1].invocation.name = 'first', 'first'
   t[0][1].invocation.name, t[1][0].invocation.name = 'second', 'second'
   appictate(t)
   
   p = Beam([t[0][0], t[1][1]])
   assert len(p.components) == 2
   assert isinstance(p.components[0], Voice)
   assert isinstance(p.components[1], Voice)
   assert len(p.leaves) == 8
   p.clear( ) 

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
         \context Voice = "second" {
            af'8
            a'8
            bf'8
            b'8
         }
         \context Voice = "first" {
            c''8
            cs''8
            d''8
            ef''8 ]
         }
      >>
   }
   '''


def test_span_like_named_04( ):
   '''
   Abjad lets you span whatever you like.
   Asymmetric structures are no problem.
   '''

   t = Sequential(Staff(Voice(run(4)) * 2) * 2)
   t[0].invocation.name, t[1].invocation.name = 'foo', 'foo'
   #t[0].brackets = 'double-angle'
   #t[1].brackets = 'double-angle'
   t[0].parallel = True
   t[1].parallel = True
   t[0][0].invocation.name, t[1][0].invocation.name = 'first', 'first'
   t[0][1].invocation.name, t[1][1].invocation.name = 'second', 'second'
   del(t[1][1])
   appictate(t)
   p = Beam([t[0][0], t[1][0]])
   
   assert len(p.components) == 2
   assert len(p.leaves) == 8

   #assert t.format == '{\n\t\\context Staff = "foo" <<\n\t\t\\context Voice = "first" {\n\t\t\tc\'8 [\n\t\t\tcs\'8\n\t\t\td\'8\n\t\t\tef\'8\n\t\t}\n\t\t\\context Voice = "second" {\n\t\t\te\'8\n\t\t\tf\'8\n\t\t\tfs\'8\n\t\t\tg\'8\n\t\t}\n\t>>\n\t\\context Staff = "foo" <<\n\t\t\\context Voice = "first" {\n\t\t\taf\'8\n\t\t\ta\'8\n\t\t\tbf\'8\n\t\t\tb\'8 ]\n\t\t}\n\t>>\n}'
   assert t.format == '{\n\t\\context Staff = "foo" <<\n\t\t\\context Voice = "first" {\n\t\t\tc\'8 [\n\t\t\tcs\'8\n\t\t\td\'8\n\t\t\tef\'8\n\t\t}\n\t\t\\context Voice = "second" {\n\t\t\te\'8\n\t\t\tf\'8\n\t\t\tfs\'8\n\t\t\tg\'8\n\t\t}\n\t>>\n\t\\context Staff = "foo" <<\n\t\t\\context Voice = "first" {\n\t\t\t\\change Staff = foo\n\t\t\taf\'8\n\t\t\ta\'8\n\t\t\tbf\'8\n\t\t\tb\'8 ]\n\t\t}\n\t>>\n}'

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
      >>
   }
   '''
