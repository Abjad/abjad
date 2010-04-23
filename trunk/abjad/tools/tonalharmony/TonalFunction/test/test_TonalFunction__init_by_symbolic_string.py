from abjad import *


def test_TonalFunction__init_by_symbolic_string_01( ):

   tonal_function = tonalharmony.TonalFunction('bII')
   correct = tonalharmony.TonalFunction(('flat', 2), 'major', 5, 0)
   assert tonal_function == correct

   tonal_function = tonalharmony.TonalFunction('bII6')
   correct = tonalharmony.TonalFunction(('flat', 2), 'major', 5, 1)
   assert tonal_function == correct

   tonal_function = tonalharmony.TonalFunction('bII6/4')
   correct = tonalharmony.TonalFunction(('flat', 2), 'major', 5, 2)
   assert tonal_function == correct


def test_TonalFunction__init_by_symbolic_string_02( ):

   tonal_function = tonalharmony.TonalFunction('V7')
   correct = tonalharmony.TonalFunction(5, 'dominant', 7, 0)
   assert tonal_function == correct

   tonal_function = tonalharmony.TonalFunction('V6/5')
   correct = tonalharmony.TonalFunction(5, 'dominant', 7, 1)
   assert tonal_function == correct

   tonal_function = tonalharmony.TonalFunction('V4/3')
   correct = tonalharmony.TonalFunction(5, 'dominant', 7, 2)
   assert tonal_function == correct

   tonal_function = tonalharmony.TonalFunction('V4/2')
   correct = tonalharmony.TonalFunction(5, 'dominant', 7, 3)
   assert tonal_function == correct


def test_TonalFunction__init_by_symbolic_string_03( ):

   tonal_function = tonalharmony.TonalFunction('V7/4-3')
   correct = tonalharmony.TonalFunction(5, 'dominant', 7, 0, (4, 3))
   assert tonal_function == correct

   tonal_function = tonalharmony.TonalFunction('V6/5/4-3')
   correct = tonalharmony.TonalFunction(5, 'dominant', 7, 1, (4, 3))
   assert tonal_function == correct


def test_TonalFunction__init_by_symbolic_string_04( ):

   tonal_function = tonalharmony.TonalFunction('vi6/5')
   correct = tonalharmony.TonalFunction(6, 'minor', 7, 1)
   assert tonal_function == correct
