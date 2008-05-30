from abjad import *
from py.test import raises


def test_articulations_interface_01( ):
   t = Note(0, (1, 4))
   assert repr(t.articulations) == 'Articulations( )'
   assert len(t.articulations) == 0
   assert t.format == "c'4"


def test_articulations_interface_02a( ):
   t = Note(0, (1, 4))
   t.articulations = ['staccato']
   assert len(t.articulations) == 1
   assert t.format == "c'4 -\\staccato"


def test_articulations_interface_02b( ):
   '''Articulations can be set as list of (string, direction) pairs.'''
   t = Note(0, (1, 4))
   t.articulations = [('staccato', 'up')]
   assert len(t.articulations) == 1
   assert t.format == "c'4 ^\\staccato"

def test_articulations_interface_03a( ):
   t = Note(0, (1, 4))
   t.articulations = ['staccato', 'marcato']
   assert len(t.articulations) == 2
   assert t.format == "c'4 -\\staccato -\\marcato"

def test_articulations_interface_03b( ):
   '''Articulations can be set as list of (string, direction) pairs.'''
   t = Note(0, (1, 4))
   t.articulations = [('staccato', 'up'), ('marcato', 'down')]
   assert len(t.articulations) == 2
   assert t.format == "c'4 ^\\staccato _\\marcato"

def test_articulations_interface_03c( ):
   '''Articulations can be set as list of (string, direction) pairs.'''
   t = Note(0, (1, 4))
   t.articulations = [('staccato', 'up'), 'marcato']
   assert len(t.articulations) == 2
   assert t.format == "c'4 ^\\staccato -\\marcato"

def test_articulations_interface_04( ):
   '''Append.'''
   t = Note(0, (1, 4))
   t.articulations.append('staccato')
   assert len(t.articulations) == 1
   assert t.format == "c'4 -\\staccato"


def test_articulations_interface_05( ):
   '''Extend.'''
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert len(t.articulations) == 2
   assert t.format == "c'4 -\\staccato -\\marcato"


def test_articulations_interface_06( ):
   '''Sort works on articulations.'''
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   t.articulations.sort( )
   assert len(t.articulations) == 2
   assert t.format == "c'4 -\\marcato -\\staccato"
   
   
def test_articulations_interface_07( ):
   '''Includes works on articulations.'''
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert 'staccato' in t.articulations
   assert 'marcato' in t.articulations


def test_articulations_interface_08( ):
   '''Pop.'''
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert len(t.articulations) == 2
   t.articulations.pop( )
   assert len(t.articulations) == 1
   t.articulations.pop( )
   assert len(t.articulations) == 0


def test_articulations_interface_09( ):
   '''Remove.'''
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert len(t.articulations) == 2
   t.articulations.remove('staccato')
   assert len(t.articulations) == 1
   t.articulations.remove('marcato')
   assert len(t.articulations) == 0
   
   
def test_articulations_interface_10( ):
   '''Articulations can be set with empty list.'''
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert len(t.articulations) == 2
   t.articulations = [ ]
   assert len(t.articulations) == 0


def test_articulations_interface_11( ):
   '''Articulations can be set with None.'''
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert len(t.articulations) == 2
   t.articulations = None
   assert len(t.articulations) == 0
   assert repr(t.articulations) == 'Articulations( )'

def test_articulations_interface_12( ):
   '''Articulations can only be directly set with list or tuple.'''
   t = Note(0, (1, 4))
   assert raises(ValueError, "t.articulations = 'staccato'")
   
