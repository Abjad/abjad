from abjad import *


def test_articulations_interface_01( ):
   t = Note(0, (1, 4))
   assert repr(t.articulations) == 'Articulations( )'
   assert len(t.articulations) == 0
   assert t.format == "c'4"


def test_articulations_interface_02( ):
   t = Note(0, (1, 4))
   t.articulations = ['staccato']
   assert len(t.articulations) == 1
   assert t.format == "c'4 \\staccato"


def test_articulations_interface_03( ):
   t = Note(0, (1, 4))
   t.articulations = ['staccato', 'marcato']
   assert len(t.articulations) == 2
   assert t.format == "c'4 \\staccato \\marcato"


def test_articulations_interface_04( ):
   t = Note(0, (1, 4))
   t.articulations.append('staccato')
   assert len(t.articulations) == 1
   assert t.format == "c'4 \\staccato"


def test_articulations_interface_05( ):
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert len(t.articulations) == 2
   assert t.format == "c'4 \\staccato \\marcato"


def test_articulations_interface_06( ):
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   t.articulations.sort( )
   assert len(t.articulations) == 2
   assert t.format == "c'4 \\marcato \\staccato"
   
   
def test_articulations_interface_07( ):
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert 'staccato' in t.articulations
   assert 'marcato' in t.articulations


def test_articulations_interface_08( ):
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert len(t.articulations) == 2
   t.articulations.pop( )
   assert len(t.articulations) == 1
   t.articulations.pop( )
   assert len(t.articulations) == 0


def test_articulations_interface_08( ):
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert len(t.articulations) == 2
   t.articulations.remove('staccato')
   assert len(t.articulations) == 1
   t.articulations.remove('marcato')
   assert len(t.articulations) == 0
   
   
def test_articulations_interface_09( ):
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert len(t.articulations) == 2
   t.articulations = [ ]
   assert len(t.articulations) == 0


def test_articulations_interface_10( ):
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert len(t.articulations) == 2
   t.articulations = None
   assert len(t.articulations) == 0
