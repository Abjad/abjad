from abjad import *
from abjad.demos.presentation.statement import Statement
from abjad.tools import *

class Presentation(object):

   def __init__(self, title, abstract, statements, subtitle=' '):
      assert isinstance(statements, list)
      self.abstract = abstract
      self.statements = statements
      self.subtitle = subtitle 
      self.title = title


   ### PUBLIC METHODS ###

   def run(self):
      print "\n\t* * * *    %s    * * * *" % self.title
      print "\n%s" % self.subtitle
      print "\n%s" % self.abstract
      for i, statement in enumerate(self.statements):
         raw_input('\n\n\n%d. %s\n' % (i+1, statement.text))
         for expr in statement.code:
            #if isinstance(expr, basestring):
            print '   abjad> ' + expr
            if '=' in expr and not '==' in expr:
               exec(expr)
            else:
               result = eval(expr) 
               if not result is None:
                  print '   %s' % result
      print "\n\t* * * End of presentation. * * *\n"


