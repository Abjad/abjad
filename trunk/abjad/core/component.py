from .. helpers.hasname import hasname
from .. barline.interface import BarLineInterface
from comments import Comments
from copier import Copier
from .. core.navigator import Navigator
from .. core.parentage import Parentage
from .. duration.rational import Rational
from .. staff.interface import StaffInterface
from tester import Tester

class _Component(object):

   def __init__(self):
      self._accidentals = None
      self._barline = BarLineInterface(self)
      self._copier = Copier(self)
      self.comments = Comments( )
      self._navigator = Navigator(self)
      self._parentage = Parentage(self)
      self.tester = Tester(self)

   ### CLASS NAME TESTING ###
   
   def kind(self, classname):
      return hasname(self, classname)

   ### COPY ###

   def __mul__(self, n):
      result = [ ]
      for i in range(n):
         result.append(self.copy( ))
      return result

   def __rmul__(self, n):
      return self * n

   def copy(self, i = None, j = None):
      return self._copier.copy(i, j)

   ### MANAGED ATTRIBUTES ###

   @apply
   def barline( ):
      def fget(self):
         return self._barline
      def fset(self, type):
         self._barline.type = type
      return property(**locals( ))

   @apply
   def accidentals( ):
      def fget(self):
         return self._accidentals
      def fset(self, style):
         assert isinstance(style, (str, type(None)))
         self._accidentals = style
      return property(**locals( ))

   ### PROPERTIES ###

   @property
   def format(self):
      return self.formatter.lily
