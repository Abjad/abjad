from abjad.helpers.zip_cycle import zip_cycle

def test_zip_cycle_01( ):
   '''zip_cycle can take two non-iterables.'''
   t = zip_cycle(1, 2)
   assert t == [(1, 2)]


def test_zip_cycle_02( ):
   '''zip_cycle can take a list of length 1 and a non-iterables.'''
   t = zip_cycle([1], 2)
   assert t == [(1, 2)]
   t = zip_cycle(1, [2])
   assert t == [(1, 2)]


def test_zip_cycle_03( ):
   '''zip_cycle can take two lists of the same size.'''
   t = zip_cycle([1, 2], ['a', 'b'])
   assert t == [(1, 'a'), (2, 'b')]


def test_zip_cycle_04( ):
   '''
   zip_cycle can take two lists of the different sizes.
   The list with the shortest size is cycled through.
   '''
   t = zip_cycle([1, 2, 3], ['a', 'b'])
   assert t == [(1, 'a'), (2, 'b'), (3, 'a')]
   t = zip_cycle([1, 2], ['a', 'b', 'c'])
   assert t == [(1, 'a'), (2, 'b'), (1, 'c')]



