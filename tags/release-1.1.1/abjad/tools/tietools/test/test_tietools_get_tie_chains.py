from abjad import *

def test_tietools_get_tie_chains_01( ):
   '''returns an empty list on a list of untied leaves.'''

   t = construct.run(4)
   chains = tietools.get_tie_chains(t)

   assert chains == [ ]


def test_tietools_get_tie_chains_02( ):
   '''returns an empty list on a list of untied containers.'''

   t = Voice(construct.run(4))
   chains = tietools.get_tie_chains([t])

   assert chains == [ ]


def test_tietools_get_tie_chains_03( ):
   '''returns an list of leaves on a list of tied leaves.'''

   t = construct.run(4)
   Tie(t[0:2])
   chains = tietools.get_tie_chains(t)

   assert chains == [tuple(t[0:2])]


def test_tietools_get_tie_chains_04( ):
   '''returns an list of leaves on a list of tied containers.'''

   t = Voice(construct.run(4))
   Tie(t)
   chains = tietools.get_tie_chains([t])

   assert chains == [tuple(t.leaves)]


def test_tietools_get_tie_chains_05( ):
   '''returns an list of two elements if two Tie spanners are found.'''

   t = Voice(construct.scale(4))
   Tie(t[0:2])
   Tie(t[2:])
   chains = tietools.get_tie_chains(t.leaves)

   assert chains == [tuple(t[0:2]), tuple(t[2:])]


def test_tietools_get_tie_chains_06( ):
   '''returns an empty list if the given list of components is not 
   tie-spanned, while its decendents are.'''

   t = Voice(construct.scale(4))
   Tie(t[0:2])
   Tie(t[2:])
   chains = tietools.get_tie_chains([t])

   assert chains == []


def test_tietools_get_tie_chains_07( ):
   '''returns an list those leaves that intersect a Tie spanner and the 
   components given.'''

   t = Voice(construct.scale(4))
   Tie(t.leaves)
   chains = tietools.get_tie_chains(t.leaves[1:3])

   assert chains == [tuple(t.leaves[1:3])]


def test_tietools_get_tie_chains_08( ):
   '''get_tie_chains( ) works across containers.'''

   t = Voice(Container(construct.scale(4)) * 3)
   Tie(t[0:2])
   chains = tietools.get_tie_chains(t[:])

   assert chains == [tuple(t.leaves[0:8])]


