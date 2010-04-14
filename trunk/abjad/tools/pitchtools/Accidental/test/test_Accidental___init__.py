from abjad import *
import py.test


def test_accidental_init_01( ):
   '''Accidentals can initialize from a string.'''
   t = pitchtools.Accidental('s')
   assert t == pitchtools.Accidental('s')


def test_accidental_init_02( ):
   '''Accidentals can initialize from other accidentals.'''
   t = pitchtools.Accidental(pitchtools.Accidental('s'))
   assert t == pitchtools.Accidental('s')


def test_accidental_init_03( ):
   '''Accidentals can initialize with none.'''
   t = pitchtools.Accidental(None)
   assert t == pitchtools.Accidental('')


def test_accidental_init_04( ):
   '''Accidentals can initialize with full accidental name.'''
   assert pitchtools.Accidental('sharp') == pitchtools.Accidental('s')
   assert pitchtools.Accidental('flat') == pitchtools.Accidental('f')
   assert pitchtools.Accidental('natural') == pitchtools.Accidental('')


def test_accidental_init_05( ):
   assert py.test.raises(ValueError, "pitchtools.Accidental('foo')")


def test_accidental_init_06( ):
   '''Init with number.'''
   assert pitchtools.Accidental(0) == pitchtools.Accidental( )
   assert pitchtools.Accidental(1) == pitchtools.Accidental('sharp')
   assert pitchtools.Accidental(-1) == pitchtools.Accidental('flat')
   assert py.test.raises(ValueError, "pitchtools.Accidental(99)")
