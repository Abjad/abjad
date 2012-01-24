from ply import lex


class _LexerProxy(object):
    '''_LexerProxy exports PLY's lexer interface, with the 
    addition of a token stack, allowing the parser to push
    artificial tokens onto the token stream.  This allows us
    to mimic LilyPond's scheme function parsing, which relies
    on artificial tokens to stand as placeholders for arguments.
    '''

    def __init__(self, client, **kwargs):
        self.client = client
        self._lexer = lex.lex(
            **kwargs)
        self._token_stack = [ ]

    def input(self, input):
        self._lexer.input(input)

    def pop_state(self):
        self._lexer.pop_state( )

    def push_state(self, state):
        self._lexer.push_state(state)

    def push_extra_token(self, token):
        self._token_stack.append(token)

    def token(self):
        print '\n'
        print 'SYMSTACK:\n%s' % '\n'.join(['\t%s' % x for x in self.client._parser.symstack])
        print 'LOOKAHEAD: %s' % self.client._parser.lookahead
        print 'LA STACK:  %s' % self.client._parser.lookaheadstack

        if self._token_stack:
            token = self._token_stack.pop( )
        else:
            token = self._lexer.token( )

        print 'NEWTOKEN:  %s' % token

        return token

