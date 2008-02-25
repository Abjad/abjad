from abjad import *


def test_beam_spanner_copy_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 4])
   u = t[0].copy( )
   len(u.spanners) == 1
   assert u.beam.spanned and u.beam.only


def test_beam_spanner_copy_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 4])
   u = tcopy(t[0 : 1])
   assert u[0].beam.spanned and u[0].beam.only


def test_beam_spanner_copy_03( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 4])
   u = tcopy(t[0 : 2])
   assert u[0].beam.spanned and u[0].beam.first
   assert u[1].beam.spanned and u[1].beam.last
   

def test_beam_spanner_copy_04( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 4])
   u = tcopy(t[0 : 4])
   assert u[0].beam.spanned and u[0].beam.first
   assert u[1].beam.spanned
   assert u[2].beam.spanned
   assert u[3].beam.spanned and u[3].beam.last
