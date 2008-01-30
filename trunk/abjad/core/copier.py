from copy import deepcopy

class _Copier(object):

   def __init__(self, client):
      self._client = client

   def copy(self, i = None, j = None):
      '''
      First fractures and then cuts parent;
      (cut followed by fracture destroys 'next');
      deepcopies reference-pruned version of expr;
      reestablishes parent and spanners references to expr;
      returns the deepcopy;
      leaves expr unchanged.
      '''

      ### TODO - decide whether to keep this interface or
      ### mimic slicing interface instead;
      ### right now self.copy(0, 2) return items 0, 1, 2;
      ### imitating slice would return only 0, 1;
      ### probably easier to give in and follow python's pattern.

      ### TODO - decide whether t.copy(i, j) should return a
      ### built-in list (as in the current implementation) or
      ### rather a Container (which would be involve commenting 1 line).

      ### NOTE - even though the special handling of clef-capture 
      ### and -reinsertion looks exceptional here, I think this
      ### is just the beginning of a patternt that will repeat for
      ### other derived attributes not modelled by a spanner,
      ### such as key signature.

      from .. containers.container import Container

      # allow single-index self.copy(2) equivalent to self[ : 2]
      if i is not None and j is None:
         j = i

      if i is None and j is None:
         #if self._client.leaves:
         #   clef = self._client.leaves[0].clef
         hairpins = self._client.spanners.get(classname = '_Hairpin')
         hairpinKillList = [ ]
         clientLeaves = set(self._client.leaves)
         hairpinKillList = [
            not set(hp.leaves).issubset(clientLeaves) for hp in hairpins]
         receipt = self._client.spanners.fracture( )
         parent = self._client._parentage._cutOutgoingReferenceToParent( )
         result = deepcopy(self._client)
         for source, left, right in reversed(receipt):
            source._unblock( )
            left._sever( )
            right._sever( )
         self._client._parent = parent
         #if result.leaves:
         #   result.leaves[0].clef = clef
         for i, hp in enumerate(result.spanners.get(classname = '_Hairpin')):
            if hairpinKillList[i]:
               hp.die( )
         return result
      else:
         if i == -1:
            source = self._client[-1 : ]
         else:
            source = self._client[i : j + 1]
         #if source:
         #   clef = source[0].leaves[0].clef
         result = Container(source)
         result = result.copy( )
         result = result._music[ : ]
         for x in result:
            x._parent = None
         for x in source:
            x._parent = self._client
         #if result:
         #   result[0].leaves[0].clef = clef
         return result
