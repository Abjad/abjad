import code
import copy
import contextlib
import StringIO
from abjad.tools import iotools
from abjad.tools.abctools import AbjadObject


class CodeBlock(AbjadObject):
    r'''Abjad model of a block of code to be interpreted in an abjad-book
    workflow:

    ::

        >>> lines = ['message = "hello, world!"', 'print message']
        >>> code_block = newabjadbooktools.CodeBlock(lines)
        >>> results = code_block.execute()
        >>> print results
        ['>>> message = "hello, world!"\n>>> print message\nhello, world!']

    Multiple code block interpretations can be chained together by using a
    common InteractiveConsole instance:

    ::

        >>> lines_one = ['message = "hello, "']
        >>> lines_two = ['message += "world!"']
        >>> lines_three = ['print message']
        >>> code_block_one = newabjadbooktools.CodeBlock(lines_one)
        >>> code_block_two = newabjadbooktools.CodeBlock(lines_two)
        >>> code_block_three = newabjadbooktools.CodeBlock(lines_three)

    ::

        >>> import code
        >>> console = code.InteractiveConsole()

    ::

        >>> code_block_one.execute(console)
        ['>>> message = "hello, "']
        >>> code_block_two.execute(console)
        ['>>> message += "world!"']
        >>> code_block_three.execute(console)
        ['>>> print message\nhello, world!']

    Code blocks intercept certain Abjad function calls and pull the results
    out as output proxies, to be dealt with by other processes:

    ::

        >>> console = code.InteractiveConsole()
        >>> status = console.push('from abjad import *')
        >>> lines = [
        ...     'staff = Staff(r"\clef bass c4 d4 e4 f4")',
        ...     'show(staff)',
        ...     'print len(staff)'
        ...     ]
        >>> code_block = newabjadbooktools.CodeBlock(lines)
        >>> results = code_block.execute(console)
        >>> for x in results:
        ...     x
        ...
        '>>> staff = Staff(r"\\clef bass c4 d4 e4 f4")\n>>> show(staff)\n'
        LilyPondOutputProxy(Staff{4})
        '>>> print len(staff)\n4'

    Code blocks also supported a number of optional keyword arguments that
    affect what commands are executed in the code block's console, and what
    commands are returned as the published result.

    If ``hide`` is true, 

    Return code block instance.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_exceptions',
        '_displayed_lines',
        '_executed_lines',
        '_hide',
        '_processed_results',
        '_strip_prompt',
        )

    ### INITIALIZER ###

    def __init__(self,
        displayed_lines,
        allow_exceptions=False,
        executed_lines=None,
        hide=False,
        strip_prompt=False,
        ):
        self._allow_exceptions = bool(allow_exceptions)
        self._displayed_lines = tuple(displayed_lines)
        self._executed_lines = None
        if executed_lines is not None:
            self._executed_lines = tuple(executed_lines)
        self._hide = bool(hide)
        self._processed_results = []
        self._strip_prompt = bool(strip_prompt)

    ### SPECIAL METHODS ###

    def __call__(self, console):
        self.processed_results.extend(self.execute(console))

    ### PUBLIC METHODS ###

    def execute(self, console=None):
        from experimental.tools import newabjadbooktools

        if console is None:
            console = code.InteractiveConsole()

        results = []
        is_incomplete_statement = False
        result = '>>> '
        lines = self.executed_lines or self.displayed_lines

        for line in lines:

            result += line + '\n'
            first, sep, rest = line.partition('(')
            with contextlib.closing(StringIO.StringIO()) as stream:
                with iotools.RedirectedStreams(stream, stream):
                    output_method = first.strip()
                    if output_method in self.output_triggers:

                        if ',' in rest:
                            object_reference = rest.rpartition(',')[0].strip()
                        else:
                            object_reference = rest.rpartition(')')[0].strip()
                        if object_reference not in console.locals:
                            # Simulate a bad reference, 
                            # and cause a captured Exception.
                            console.push(line)
                        else:
                            # Otherwise, it's OK: just grab it out of the
                            # console's locals. 
                            proxy_class = self.output_triggers[output_method]
                            output_proxy = proxy_class(
                                copy.deepcopy(console.locals[object_reference]),
                                )
                            results.append(result)
                            results.append(output_proxy)
                            # Then empty the current result buffer:
                            # the output proxy represents a break in the 
                            # printed code blocks.
                            result = ''
                        is_incomplete_statement = False
                    else:
                        is_incomplete_statement = console.push(line)
                    output = stream.getvalue()
                    if output:
                        result += output
                if not is_incomplete_statement:
                    result += '>>> '
                else:
                    result += '... '

        # Simulate a final carriage return to break any incomplete indents
        with contextlib.closing(StringIO.StringIO()) as stream:
            with iotools.RedirectedStreams(stream, stream):
                console.push('')
                output = stream.getvalue()
                if output:
                    result += output
        while result.endswith('\n>>> '):
            result = result[:-5]
         
        results.append(result)

        if self.executed_lines:
            results = ['\n'.join(self.displayed_results)]

        if self.hide:
            for x in reversed(results):
                if isinstance(x, str):
                    results.remove(x)

        if self.strip_prompt:
            for i, x in enumerate(results):
                if instance(x, str):
                    lines = x.splitlines()
                    for j, line in enumerate(lines):
                        if line.startswith(('>>> ', '... ')):
                            lines[j] = line[4:]
                    results[i] = '\n'.join(lines) 

        return results

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def allow_exceptions(self):
        return self._allow_exceptions

    @property
    def displayed_lines(self):
        return self._displayed_lines

    @property
    def executed_lines(self):
        return self._executed_lines

    @property
    def hide(self):
        return self._hide

    @property
    def output_triggers(self):
        from experimental.tools import newabjadbooktools
        return {
            'iotools.graph': newabjadbooktools.GraphvizOutputProxy,
            'iotools.play':  newabjadbooktools.MIDIOutputProxy,
            'iotools.plot': newabjadbooktools.GnuplotOutputProxy,
            'iotools.show': newabjadbooktools.LilyPondOutputProxy,
            'play': newabjadbooktools.MIDIOutputProxy,
            'show': newabjadbooktools.LilyPondOutputProxy,
        }

    @property
    def processed_results(self):
        return self._processed_results

    @property
    def strip_prompt(self):
        return self._strip_prompt


