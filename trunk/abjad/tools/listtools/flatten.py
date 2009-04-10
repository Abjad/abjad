def flatten(l, ltypes=(list, tuple)):
   '''Flatten nested lists. Returns a 0-depth list or tuple.
      Based on Mike C. Fletcher's flatten.'''

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
