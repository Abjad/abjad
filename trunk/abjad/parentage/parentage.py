from abjad.core.abjadcore import _Abjad
from abjad.rational.rational import Rational


class _Parentage(_Abjad):

   def __init__(self, client):
      self._client = client

   ### PRIVATE METHODS ###

   def _cutOutgoingReferenceToParent(self):
      '''
      Self no longer references parent;
      but parent continues to reference self.
      '''
      if hasattr(self._client, '_parent'):
         result = self._client._parent
         self._client._parent = None
         return result

#   def _disjunctParentageBetween(self, arg):
#      '''
#      Returns just those elements in the parentage that do not
#      appear in the parentage of self, together with just those
#      elements in the parentage of self that do not appear in the 
#      parentage of arg.
#      '''
#
#      return set(self._parentage) ^ set(arg._parentage._parentage)

   def _disjunctInclusiveParentageBetween(self, arg):
      '''
      Same as _disjunctParentageBetween( ) but including
      references to self._client and arg.
      '''

      #return self._disjunctParentageBetween(arg) | set((self._client, arg))
      #return set(self._iparentage) ^ set (arg._parentage._iparentage)
      #return set(self._parentage) ^ set (arg._parentage._parentage)
      #return set(self._parentage) ^ set (arg.parentage._parentage)
      return set(self.parentage) ^ set (arg.parentage.parentage)

   def _first(self, classname):
      p = self._client._parent
      while p is not None:
         #if p.__class__.__name__ == classname:
         if p.kind(classname):
            return p
         else:
            p = p._parent
      return None

   def _getFirstSharedParent(self, arg):
      '''
      Returns first shared parent between self._client and arg,
      otherwise None.
      '''

      #shared = set(self._parentage) & set(arg._parentage._parentage)
      #shared = set(self._iparentage) & set(arg._parentage._iparentage)
      #shared = set(self._parentage) & set(arg._parentage._parentage)
      #shared = set(self._parentage) & set(arg.parentage._parentage)
      shared = set(self.parentage) & set(arg.parentage.parentage)
      if shared:
         #for parent in self._parentage:
         #for parent in self._iparentage:
         #for parent in self._parentage:
         for parent in self.parentage:
            if parent in shared:
               return parent
      return None

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

   def _switchParentTo(self, new_parent):
      client = self._client
      old_parent = client._parent
      if old_parent is not None:
         old_parent._music.remove(client)
      client._parent = new_parent

   ### PRIVATE ATTRIBUTES ###
   
   @property
   def _enclosingContextName(self):
      #inclusive_parentage = [self._client] + self._parentage
      #inclusive_parentage = self._iparentage
      #for p in self._parentage:
      for p in self.parentage:
         invocation = getattr(p, 'invocation', None)
         if invocation:
            return invocation.name
      else:
         return None

   @property
   def _governor(self):
      p = self._client._parent
      if p is None or p.parallel:
         return None
      while p._parent is not None and not p._parent.parallel:
         p = p._parent
      return p

   @property
   def _number(self):
      p = self._client._parent
      while p is not None:
         if p.formatter.number:
            return True
         else:
            p = p._parent
      return None
   
   @property
   def _threadParentage(self):
      '''Return thread-pertinent parentage structure.
         Same as _parentage but with _Tuplets, redundant Sequentials, 
         Parallels and tautologies (unlikely) removed.'''
      #parentage = self._parentage
      #parentage = self._iparentage[1:]
      #parentage = self._parentage[1:]
      parentage = self.parentage[1:]
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
               if p.kind('Parallel'): # or p.kind('Sequential'):
                  parentage.remove(p)
               elif p.kind('_Context'):
                  if p.invocation == parentage[i+1].invocation:
                     parentage.remove(p)
      return parentage

   ### PUBLIC ATTRIBUTES ###

   @property
   #def _orphan(self):
   def orphan(self):
      #return len(self._parentage) == 1
      return len(self.parentage) == 1
      
   @property
   #def _parentage(self):
   def parentage(self):
      '''
      Return a list of all of elements in the
      parentage of client, including client.
      '''
      result = [ ]
      cur = self._client
      while cur is not None:
         result.append(cur)
         cur = cur._parent
      return result

   @property
   #def _root(self):
   def root(self):
      #return self._parentage[-1]
      return self.parentage[-1]

   ### PUBLIC METHODS ###

   def detach(self):
      '''
      Sever both incoming reference from and
      outgoing reference to parent.
      '''
      client = self._client
      client._update._markForUpdateToRoot( )
      self._removeFromParent( )
      self._cutOutgoingReferenceToParent( )
      return client
