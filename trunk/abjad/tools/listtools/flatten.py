def flatten(l, ltypes=(list, tuple), depth = float('infinity')):
   '''Flatten nested lists. Returns a 0-depth list or tuple.
      Set optional 'depth' keyword set to positive integer.
      Keyword controls depth to which flatten operates.
      Based on Mike C. Fletcher's flatten.

   abjad> t = [1, [2, 3, [4]], 5, [6, 7, [8]]]

   abjad> listtools.flatten(t)
   [1, 2, 3, 4, 5, 6, 7, 8]

   abjad> listtools.flatten(t, depth = 0)
   [1, [2, 3, [4]], 5, [6, 7, [8]]]

   abjad> listtools.flatten(t, depth = 1)
   [1, 2, 3, [4], 5, 6, 7, [8]]

   abjad> listtools.flatten(t, depth = 2)
   [1, 2, 3, 4, 5, 6, 7, 8]'''

   if depth < float('infinity'):
      return _flatten_to_depth(l, depth)

   assert isinstance(l, ltypes)
   ltype = type(l)
   l = list(l)
   i = 0
   while i < len(l):
      while isinstance(l[i], ltypes):
         if not l[i]:
            l.pop(i)
            i -= 1
            break
         else:
            l[i:i + 1] = l[i]
      i += 1
   return ltype(l)


def _flatten_to_depth(l, depth):
   assert isinstance(l, list)
   assert isinstance(depth, int)
   assert 0 <= depth

   prev_sweep = l[:]
   for sweep in range(depth):
      cur_sweep = [ ]
      at_bottom = True
      for x in prev_sweep:
         if isinstance(x, list):
            cur_sweep.extend(x)
            at_bottom = False
         else:
            cur_sweep.append(x)
      prev_sweep = cur_sweep
      if at_bottom:
         break

   return prev_sweep
