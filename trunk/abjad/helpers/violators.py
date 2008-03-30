from abjad import checks as _checks


def violators(expr):
   violators = [ ]
   for key, value in sorted(_checks.__dict__.iteritems()):
      checker = value( )
      violators.extend(checker.violators(expr))
   return violators
