from abjad import *


def test_beam_interface_01( ):
   t = Note(0, (3, 64))
   assert t.beam.flags == 3
   assert t.beam.beamable
   assert not t.beam.spanned
   assert not t.beam.first
   assert not t.beam.last
   assert not t.beam.only


def test_beam_interface_02( ):
   t = Voice([Note(n, (1, 8)) for n in range(8)])
   Beam(t.leaves[ : 4])
   assert t[0].beam.flags == 1
   assert t[0].beam.beamable
   assert t[0].beam.spanned
   assert t[0].beam.first
   assert not t[0].beam.last
   assert not t[0].beam.only
   assert t.format == "\\new Voice {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"


def test_beam_interface_03( ):
   t = Voice([Note(n, (1, 8)) for n in range(8)])
   Beam(t.leaves[ : 4])
   assert t[3].beam.flags == 1
   assert t[3].beam.beamable
   assert t[3].beam.spanned
   assert not t[3].beam.first
   assert t[3].beam.last
   assert not t[3].beam.only
   assert t.format == "\\new Voice {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"


def test_beam_interface_04( ):
   t = Voice([Note(n, (1, 8)) for n in range(8)])
   Beam(t[3])
   assert t[3].beam.flags == 1
   assert t[3].beam.beamable
   assert t[3].beam.spanned
   assert t[3].beam.first
   assert t[3].beam.last
   assert t[3].beam.only
   assert t.format == "\\new Voice {\n\tc'8\n\tcs'8\n\td'8\n\tef'8 [ ]\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"


def test_beam_interface_05( ):
   note = Note(0, (1, 8))
   note.beam.counts = (1, 0)
   assert note.format == "\\set stemLeftBeamCount #1\n\\set stemRightBeamCount #0\nc'8"

