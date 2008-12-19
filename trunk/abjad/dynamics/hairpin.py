from abjad.spanner.spanner import Spanner


class _Hairpin(Spanner):

   def __init__(self, music, start = None, stop = None, trim = False):
      Spanner.__init__(self, music)
      self.start = start
      self.stop = stop
      self.trim = trim

   def _right(self, leaf):
      result = [ ]
      if not self.trim:
         if self._isMyFirstLeaf(leaf):
            result.append('\\%s' % self._shape)
            if self.start:
               result.append('\\%sX' % self.start)
         if self._isMyLastLeaf(leaf):
            if self.stop:
               result.append('\\%sX' % self.stop)
            elif not leaf.dynamics:
               result.append('\\!')
      else:
         if self._isMyFirst(leaf, ('Note', 'Chord')):
            result.append('\\%s' % self._shape)
            if self.start:
               result.append('\\%sX' % self.start)
         if self._isMyLast(leaf, ('Note', 'Chord')):
            if self.stop:
               result.append('\\%sX' % self.stop)
            elif not leaf.dynamics:
               result.append('\\!')
      return result


def _parse_descriptor(descriptor):
   '''Example descriptors:
      '<'
      'p <'
      'p < f'
   '''
   assert isinstance(descriptor, str)
   parts = descriptor.split( )
   num_parts = len(parts)
   start, shape, stop = None, None, None
   if parts[0] in ('<', '>'):
      assert 1 <= num_parts <= 2
      if num_parts == 1:
         shape = parts[0]
      else:
         shape = parts[0]
         stop = parts[1]
   else:
      assert 2 <= num_parts <= 3
      if num_parts == 2:
         start = parts[0]
         shape = parts[1]
      else:
         start = parts[0]
         shape = parts[1]
         stop = parts[2]
   assert shape in ('<', '>')
   return start, shape, stop


def Hairpin(music, descriptor, trim = False):
   start, shape, stop = _parse_descriptor(descriptor)
   if shape == '<':
      from crescendo import Crescendo
      result = Crescendo(music, start = start, stop = stop, trim = trim)
   elif shape == '>':
      from decrescendo import Decrescendo
      result = Decrescendo(music, start = start, stop = stop, trim = trim)
   return result
