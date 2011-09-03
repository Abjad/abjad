from abjad.demos.presentation.statement import Statement


class Presentation(object):

    def __init__(self, title, abstract, statements, subtitle=' '):
        assert isinstance(statements, list)
        self.abstract = abstract
        self.statements = statements
        self.subtitle = subtitle
        self.title = title
        self.setup = [ ]

    ### PRIVATE METHODS ###

    def _print_header(self):
        print "\n\t* * * *    %s    * * * *" % self.title
        print "\n%s" % self.subtitle
        print "\n%s" % self.abstract


    def _is_executable(self, arg):
        kwds = ['for', 'while', 'if', 'else']
        if '=' in arg and not '==' in arg:
            return True
        for w in kwds:
            if w in arg:
                return True
        return False

    ### PUBLIC METHODS ###

    def make_repeated_notes(self, live=False):
        '''
        This method runs the presentation.
        Set live to True in live presentation. When live is True the commands
        are not executed, only displayed.
        '''
        # run setup code
        # TODO: there must be a better way to insert imports and variables
        # into the scope of this function.
        for expr in self.setup:
            exec(expr)
        #
        self._print_header( )
        for i, statement in enumerate(self.statements):
            raw_input('\n\n%d. %s\n' % (i+1, statement.text))
            for expr in statement.code:
                print '   abjad> ' + expr
                if not live:
                    if self._is_executable(expr):
                        exec(expr)
                    else:
                        result = eval(expr)
                        if result:
                            print '   %s' % result
        print "\n\t* * * End of presentation. * * *\n"
