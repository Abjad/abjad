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
