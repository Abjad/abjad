from abjad.duration.rational import Rational

class _Parentage(object):

   def __init__(self, client):
      self._client = client

   @property
   def _parentage(self):
      result = [ ]
      parent = self._client._parent
      while parent is not None:
         result.append(parent)
         parent = parent._parent
      return result

   @property
   def _threadParentage(self):
      '''Return thread-pertinent parentage structure.
         Same as _parentage but with _Tuplets, redundant Sequentials, 
         Parallels and tautologies (unlikely) removed.'''
      parentage = self._parentage
      #if len(parentage) > 1: why was this 1???
      if len(parentage) > 0:
      ### remove sequentials
         for p in parentage[:]:
            if p.kind('Sequential') or p.kind('_Tuplet'):
               parentage.remove(p)
            else:
               break
      # remove tautological nesting
         for i, p in enumerate(parentage[:-1]):
            if type(p) == type(parentage[i+1]):
               if p.kind('Parallel') : # or p.kind('Sequential'):
                  parentage.remove(p)
               #elif p.kind('Context'):
               elif p.kind('_Context'):
                  if p.invocation == parentage[i+1].invocation:
                     parentage.remove(p)
      return parentage
               
            

   @property
   def _governor(self):
      p = self._client._parent
      if p is None or p.parallel:
         return None
      while p._parent is not None and not p._parent.parallel:
         p = p._parent
      return p

   def _first(self, classname):
      p = self._client._parent
      while p is not None:
         if p.__class__.__name__ == classname:
            return p
         else:
            p = p._parent
      return None

   @property
   def _number(self):
      p = self._client._parent
      while p is not None:
         if p.formatter.number:
            return True
         else:
            p = p._parent
      return None
      
   ### REFERENCE MANAGEMENT ###

   def _removeFromParent(self):
      '''
      Parent no longer references self;
      but self continues to reference parent.
      '''
      if hasattr(self._client, '_parent'):
         try:
            self._client._parent._music.remove(self._client)
         except:
            pass

   def _cutOutgoingReferenceToParent(self):
      '''
      Self no longer references parent;
      but parent continues to reference self.
      '''
      if hasattr(self._client, '_parent'):
         result = self._client._parent
         self._client._parent = None
         return result

   def _detach(self):
      '''
      Sever incoming reference from and
      outgoing reference to parent.
      '''
      self._removeFromParent( )
      self._cutOutgoingReferenceToParent( )
