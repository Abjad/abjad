from ply.yacc import (
    YaccProduction,
    YaccSymbol,
    error_count,
    format_result,
    format_stack_entry
)

def _parse(self, input=None, lexer=None, debug=None, tracking=0, tokenfunc=None):
    self.lookahead = None                 # Current lookahead symbol
    actions = self.action            # Local reference to action table (to avoid lookup on self.)
    goto    = self.goto              # Local reference to goto table (to avoid lookup on self.)
    prod    = self.productions       # Local reference to production list (to avoid lookup on self.)
    pslice  = YaccProduction(None)   # Production object passed to grammar rules
    errorcount = 0                   # Used during error recovery 

    # --! DEBUG
    debug.info("PLY: PARSE DEBUG START")
    # --! DEBUG

    # Set up the lexer and parser objects on pslice
    pslice.lexer = lexer
    pslice.parser = self

    # If input was supplied, pass to lexer
    if input is not None:
        lexer.input(input)

    if tokenfunc is None:
       # Tokenize function
       get_token = lexer.token
    else:
       get_token = tokenfunc

    # Set up the state and symbol stacks

    lookaheadstack = [ ]                    # Stack of lookahead tokens
    self.lookaheadstack = lookaheadstack
    statestack = [ ]                        # Stack of parsing states
    self.statestack = statestack
    symstack   = [ ]                        # Stack of grammar symbols
    self.symstack = symstack

    pslice.stack = symstack                 # Put in the production
    errtoken   = None                       # Err token

    # The start state is assumed to be (0,$end)

    statestack.append(0)
    sym = YaccSymbol()
    sym.type = "$end"
    symstack.append(sym)
    state = 0
    while 1:
        # Get the next symbol on the input.  If a lookahead symbol
        # is already set, we just use that. Otherwise, we'll pull
        # the next token off of the lookaheadstack or from the lexer

        # --! DEBUG
        debug.debug('')
        debug.debug('State  : %s', state)
        # --! DEBUG

        if not self.lookahead:
            if not self.lookaheadstack:
                self.lookahead = get_token()     # Get the next token
            else:
                self.lookahead = self.lookaheadstack.pop()
            if not self.lookahead:
                self.lookahead = YaccSymbol()
                self.lookahead.type = "$end"

        # --! DEBUG
        debug.debug('Stack  : %s',
                    ("%s . %s" % (" ".join([xx.type for xx in symstack][1:]), str(self.lookahead))).lstrip())
        # --! DEBUG

        # Check the action table
        ltype = self.lookahead.type
        t = actions[state].get(ltype)

        if t is not None:
            if t > 0:
                # shift a symbol on the stack
                statestack.append(t)
                state = t
                
                # --! DEBUG
                debug.debug("Action : Shift and goto state %s", t)
                # --! DEBUG

                symstack.append(self.lookahead)
                self.lookahead = None

                # Decrease error count on successful shift
                if errorcount: errorcount -=1
                continue

            if t < 0:
                # reduce a symbol on the stack, emit a production
                p = prod[-t]
                pname = p.name
                plen  = p.len

                # Get production function
                sym = YaccSymbol()
                sym.type = pname       # Production name
                sym.value = None

                # --! DEBUG
                if plen:
                    debug.info("Action : Reduce rule [%s] with %s and goto state %d", p.str, "["+",".join([format_stack_entry(_v.value) for _v in symstack[-plen:]])+"]",-t)
                else:
                    debug.info("Action : Reduce rule [%s] with %s and goto state %d", p.str, [],-t)
                    
                # --! DEBUG

                if plen:
                    targ = symstack[-plen-1:]
                    targ[0] = sym

                    # --! TRACKING
                    if tracking:
                       t1 = targ[1]
                       sym.lineno = t1.lineno
                       sym.lexpos = t1.lexpos
                       t1 = targ[-1]
                       sym.endlineno = getattr(t1,"endlineno",t1.lineno)
                       sym.endlexpos = getattr(t1,"endlexpos",t1.lexpos)

                    # --! TRACKING

                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # The code enclosed in this section is duplicated 
                    # below as a performance optimization.  Make sure
                    # changes get made in both locations.

                    pslice.slice = targ
                    
                    try:
                        # Call the grammar rule with our special slice object
                        del symstack[-plen:]
                        del statestack[-plen:]
                        p.callable(pslice)
                        # --! DEBUG
                        debug.info("Result : %s", format_result(pslice[0]))
                        # --! DEBUG
                        symstack.append(sym)
                        state = goto[statestack[-1]][pname]
                        statestack.append(state)
                    except SyntaxError:
                        # If an error was set. Enter error recovery state
                        self.lookaheadstack.append(self.lookahead)
                        symstack.pop()
                        statestack.pop()
                        state = statestack[-1]
                        sym.type = 'error'
                        self.lookahead = sym
                        errorcount = error_count
                        self.errorok = 0
                    continue
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                else:

                    # --! TRACKING
                    if tracking:
                       sym.lineno = lexer.lineno
                       sym.lexpos = lexer.lexpos
                    # --! TRACKING

                    targ = [ sym ]

                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # The code enclosed in this section is duplicated 
                    # above as a performance optimization.  Make sure
                    # changes get made in both locations.

                    pslice.slice = targ

                    try:
                        # Call the grammar rule with our special slice object
                        p.callable(pslice)
                        # --! DEBUG
                        debug.info("Result : %s", format_result(pslice[0]))
                        # --! DEBUG
                        symstack.append(sym)
                        state = goto[statestack[-1]][pname]
                        statestack.append(state)
                    except SyntaxError:
                        # If an error was set. Enter error recovery state
                        self.lookaheadstack.append(self.lookahead)
                        symstack.pop()
                        statestack.pop()
                        state = statestack[-1]
                        sym.type = 'error'
                        self.lookahead = sym
                        errorcount = error_count
                        self.errorok = 0
                    continue
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            if t == 0:
                n = symstack[-1]
                result = getattr(n,"value",None)
                # --! DEBUG
                debug.info("Done   : Returning %s", format_result(result))
                debug.info("PLY: PARSE DEBUG END")
                # --! DEBUG
                return result

        if t == None:

            # --! DEBUG
            debug.error('Error  : %s',
                        ("%s . %s" % (" ".join([xx.type for xx in symstack][1:]), str(self.lookahead))).lstrip())
            # --! DEBUG

            # We have some kind of parsing error here.  To handle
            # this, we are going to push the current token onto
            # the tokenstack and replace it with an 'error' token.
            # If there are any synchronization rules, they may
            # catch it.
            #
            # In addition to pushing the error token, we call call
            # the user defined p_error() function if this is the
            # first syntax error.  This function is only called if
            # errorcount == 0.
            if errorcount == 0 or self.errorok:
                errorcount = error_count
                self.errorok = 0
                errtoken = self.lookahead
                if errtoken.type == "$end":
                    errtoken = None               # End of file!
                if self.errorfunc:
                    global errok,token,restart
                    errok = self.errok        # Set some special functions available in error recovery
                    token = get_token
                    restart = self.restart
                    if errtoken and not hasattr(errtoken,'lexer'):
                        errtoken.lexer = lexer
                    tok = self.errorfunc(errtoken)
                    del errok, token, restart   # Delete special functions

                    if self.errorok:
                        # User must have done some kind of panic
                        # mode recovery on their own.  The
                        # returned token is the next self.lookahead
                        self.lookahead = tok
                        errtoken = None
                        continue
                else:
                    if errtoken:
                        if hasattr(errtoken,"lineno"): lineno = self.lookahead.lineno
                        else: lineno = 0
                        if lineno:
                            sys.stderr.write("yacc: Syntax error at line %d, token=%s\n" % (lineno, errtoken.type))
                        else:
                            sys.stderr.write("yacc: Syntax error, token=%s" % errtoken.type)
                    else:
                        sys.stderr.write("yacc: Parse error in input. EOF\n")
                        return

            else:
                errorcount = error_count

            # case 1:  the statestack only has 1 entry on it.  If we're in this state, the
            # entire parse has been rolled back and we're completely hosed.   The token is
            # discarded and we just keep going.

            if len(statestack) <= 1 and self.lookahead.type != "$end":
                self.lookahead = None
                errtoken = None
                state = 0
                # Nuke the pushback stack
                del self.lookaheadstack[:]
                continue

            # case 2: the statestack has a couple of entries on it, but we're
            # at the end of the file. nuke the top entry and generate an error token

            # Start nuking entries on the stack
            if self.lookahead.type == "$end":
                # Whoa. We're really hosed here. Bail out
                return

            if self.lookahead.type != 'error':
                sym = symstack[-1]
                if sym.type == 'error':
                    # Hmmm. Error is on top of stack, we'll just nuke input
                    # symbol and continue
                    self.lookahead = None
                    continue
                t = YaccSymbol()
                t.type = 'error'
                if hasattr(self.lookahead,"lineno"):
                    t.lineno = self.lookahead.lineno
                t.value = self.lookahead
                self.lookaheadstack.append(self.lookahead)
                self.lookahead = t
            else:
                symstack.pop()
                statestack.pop()
                state = statestack[-1]       # Potential bug fix

            continue

        # Call an error function here
        raise RuntimeError("yacc: internal parser error!!!\n")

