from abjad import *


def test_rigid_measure_block_01( ):
   '''Measures format LilyPond comments when block is True.'''

   t = Staff(measures_make([(2, 16), (3, 16), (3, 16)]))
   measures_populate(t, Rational(1, 16))
   RigidMeasure.block = True

   r'''
   \new Staff {
           %% start measure
                   \time 2/16
                   c'16
                   c'16
           %% stop measure
           %% start measure
                   \time 3/16
                   c'16
                   c'16
                   c'16
           %% stop measure
           %% start measure
                   \time 3/16
                   c'16
                   c'16
                   c'16
           %% stop measure
   }
   '''
  
   assert check(t)
   assert t.format == "\\new Staff {\n\t%% start measure\n\t\t\\time 2/16\n\t\tc'16\n\t\tc'16\n\t%% stop measure\n\t%% start measure\n\t\t\\time 3/16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t%% stop measure\n\t%% start measure\n\t\t\\time 3/16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t%% stop measure\n}"


def test_rigid_measure_block_02( ):
   '''Measures format LilyPond comments with numbers when block is 'number'.'''

   t = Staff(measures_make([(2, 16), (3, 16), (3, 16)]))
   measures_populate(t, Rational(1, 16))
   RigidMeasure.block = 'number'

   r'''
   \new Staff {
           % start measure 0
                   \time 2/16
                   c'16
                   c'16
           % stop measure 0
           % start measure 1
                   \time 3/16
                   c'16
                   c'16
                   c'16
           % stop measure 1
           % start measure 2
                   \time 3/16
                   c'16
                   c'16
                   c'16
           % stop measure 2
   }
   '''

   assert check(t)
   assert t.format == "\\new Staff {\n\t% start measure 0\n\t\t\\time 2/16\n\t\tc'16\n\t\tc'16\n\t% stop measure 0\n\t% start measure 1\n\t\t\\time 3/16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t% stop measure 1\n\t% start measure 2\n\t\t\\time 3/16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t% stop measure 2\n}"


def test_rigid_measure_block_03( ):
   '''Measures format no LilyPond comments when block is False.'''

   t = Staff(measures_make([(2, 16), (3, 16), (3, 16)]))
   measures_populate(t, Rational(1, 16))
   RigidMeasure.block = False

   r'''
   \new Staff {
                   \time 2/16
                   c'16
                   c'16
                   \time 3/16
                   c'16
                   c'16
                   c'16
                   \time 3/16
                   c'16
                   c'16
                   c'16
   }
   '''

   assert check(t)
   assert t.format == "\\new Staff {\n\t\t\\time 2/16\n\t\tc'16\n\t\tc'16\n\t\t\\time 3/16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\t\\time 3/16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n}"
