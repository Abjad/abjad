import itertools

def group_by_equality(lst):
   '''Group elements in *lst* by equality. All adjacent elements that
   are equal are grouped together in a tuple. 

   Returns a generator.

   Examples::

      abjad> l = [0, 0, -1, -1, 2, 3, -5, 1, 1, 5, -5]

   ::
   
      abjad> list(listtools.group_by_equality(l))
      [(0, 0), (-1, -1), (2,), (3,), (-5,), (1, 1), (5,), (-5,)] '''


   g = itertools.groupby(lst, lambda x: x)
   for n, group in g:
      yield tuple(group)
