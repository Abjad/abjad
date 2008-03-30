from abjad import checks as _checks


def report(expr):
   for key, value in sorted(_checks.__dict__.iteritems( )):
      checker = value( )
      checker.report(expr)
