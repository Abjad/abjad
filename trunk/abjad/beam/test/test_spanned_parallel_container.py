from abjad import *
import py.test


py.test.skip('Tests for spanned containers development.')

def test_spanned_parallel_container_01( ):
   '''Empty parallel container refuses to be spanned.'''
   t = Parallel([ ])
   raises(ContiguityException, 'Beam(t)')


def test_spanned_parallel_container_02( ):
   '''Nonempty spanned parallel container;
      parallel container refuses to be spanned.'''
   t = Parallel(Voice(Note(0, (1, 8)) * 4) * 2)
   raises(ContiguityException, 'Beam(t)')


def test_spanned_parallel_container_03( ):
   '''Sequential container accepts spanner,
      even lodged within parallel parent container.'''
   t = Parallel(Voice(Note(0, (1, 8)) * 4) * 2)
   p = Beam(t[0])
   assert len(p) == 1
   assert isinstance(p, Voice)
   assert t.format == "<<\n\t\\new Voice {\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n\t\\new Voice {\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n>>"
   r''''
   <<
      \new Voice {
         c'8 [
         c'8
         c'8
         c'8 ]
      }
      \new Voice {
         c'8
         c'8
         c'8
         c'8
      }
   >>
   '''


def test_spanned_parallel_container_04( ):
   '''Contiguous leaves accept spanner,
      even lodged within parallel grandparent container.'''
   t = Parallel(Voice(Note(0, (1, 8)) * 4) * 2)
   p = Beam(t[0][ : ])
   assert len(p) == 4
   for x in p:
      assert isinstance(x, Note)
   assert t.format == "<<\n\t\\new Voice {\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n\t\\new Voice {\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n>>"
   r''''
   <<
      \new Voice {
         c'8 [
         c'8
         c'8
         c'8 ]
      }
      \new Voice {
         c'8
         c'8
         c'8
         c'8
      }
   >>
   '''


def test_spanned_parallel_container_05( ):
   '''Subterranean parallel container raises causes
      sequential parent container to refuse to be spanned.'''
   t = Staff(Note(0, (1, 8)) * 4)
   t.insert(2, Parallel(Sequential(Note(0, (1, 8)) * 4) * 2))
   raises(ContiguityError, 'Beam(t)')
   r'''
   \new Staff {
      c'8
      c'8
      <<
         {
            c'8
            c'8
            c'8
            c'8
         }
         {
            c'8
            c'8
            c'8
            c'8
         }
      >>
      c'8
      c'8
   }
   '''


def test_spanned_parallel_container_06( ):
   '''Subterranean parallel container causes
      parent to refuse spanner ... even when
      subterranean container is empty.'''
   t = Staff(Note(0, (1, 8)) * 4)
   t.insert(2, Parallel([ ]))
   raises(ContiguityError, 'Beam(t)')
   r'''
   \new Staff {
      c'8
      c'8
      <<
      >>
      c'8
      c'8
   }
   '''
