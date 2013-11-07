# -*- encoding: utf-8 -*-
import StringIO
import copy
import contextlib
import random
from abjad.tools import iotools
from abjad.tools.abctools import AbjadObject


class CodeBlock(AbjadObject):
    r'''Abjad model of a block of code to be interpreted in an abjad-book
    workflow:

    ::

        >>> lines = ['message = "hello, world!"', 'print message']
        >>> code_block = newabjadbooktools.CodeBlock(lines)

    ::

        >>> import code
        >>> console = code.InteractiveConsole()

    ::

        >>> output_proxies = code_block.execute(console)
        >>> print output_proxies
        [CodeOutputProxy((
            '>>> message = "hello, world!"',
            '>>> print message',
            'hello, world!',
            ))]

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

        >>> code_block_one.execute(console)
        [CodeOutputProxy((
            '>>> message = "hello, "',
            ))]
        >>> code_block_two.execute(console)
        [CodeOutputProxy((
            '>>> message += "world!"',
            ))]
        >>> code_block_three.execute(console)
        [CodeOutputProxy((
            '>>> print message',
            'hello, world!',
            ))]

    Code blocks intercept certain Abjad function calls and pull the 
    output_proxies out as output proxies, to be dealt with by other 
    processes.

    .. note:: We can push commands to the console directly, like the following
              import, in order to pull references into the console's local
              namespace.

    ::

        >>> status = console.push('from abjad import *')

    ::

        >>> lines = [
        ...     'staff = Staff(r"\clef bass c4 d4 e4 f4")',
        ...     'show(staff)',
        ...     'print len(staff)'
        ...     ]
        >>> code_block = newabjadbooktools.CodeBlock(lines)
        >>> output_proxies = code_block.execute(console)
        >>> for x in output_proxies:
        ...     x
        ...
        CodeOutputProxy((
            '>>> staff = Staff(r"\\clef bass c4 d4 e4 f4")',
            '>>> show(staff)',
            ))
        LilyPondOutputProxy()
        CodeOutputProxy((
            '>>> print len(staff)',
            '4',
            ))

    Code blocks also support a number of optional keyword arguments that
    affect what commands are executed in the code block's console, and what
    commands are returned as the published result.

    If ``hide`` is true, only any output proxies generated during
    interpretation will be returned:

    .. note:: Here we will reuse the previously defined console, which already
              has Abjad's default imports in its local namespace.

    ::

        >>> lines = [
        ...     'note = Note("dqf16..")',
        ...     'play(note)',
        ...     'print len(staff)'
        ...     ]
        >>> code_block = newabjadbooktools.CodeBlock(
        ...     lines,
        ...     hide=True,
        ...     )
        >>> output_proxies = code_block.execute(console)
        >>> for x in output_proxies:
        ...     x
        ...
        MIDIOutputProxy()

    Returns code block instance.
    '''

    ### CLASS VARIABLES ###

    #__slots__ = (
    #    '_allow_exceptions',
    #    '_displayed_lines',
    #    '_executed_lines',
    #    '_hide',
    #    '_output_proxies',
    #    '_strip_prompt',
    #    )

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
        self._output_proxies = []
        self._strip_prompt = bool(strip_prompt)

    ### SPECIAL METHDOS ###

    def __format__(self, format_specification=''):
        r'''Formats code block.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        if format_specification in ('', 'storage'):
            return self._tools_package_qualified_indented_repr
        return str(self)

    ### PUBLIC PROPERTIES ###

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
    def output_proxies(self):
        return self._output_proxies

    @property
    def output_triggers(self):
        from experimental.tools import newabjadbooktools
        return {
            'functiontools.graph': newabjadbooktools.GraphvizOutputProxy,
            'functiontools.play':  newabjadbooktools.MIDIOutputProxy,
            'iotools.plot': newabjadbooktools.GnuplotOutputProxy,
            'functiontools.show': newabjadbooktools.LilyPondOutputProxy,
            'play': newabjadbooktools.MIDIOutputProxy,
            'show': newabjadbooktools.LilyPondOutputProxy,
        }

    @property
    def strip_prompt(self):
        return self._strip_prompt

    ### PUBLIC METHODS ###

    def execute(self, console):
        from experimental.tools import newabjadbooktools

        self.output_proxies[:] = []
        is_incomplete_statement = False
        result = '>>> '
        lines = self.executed_lines or self.displayed_lines

        for i, line in enumerate(lines):

            result += line + '\n'
            first, sep, rest = line.partition('(')
            with contextlib.closing(StringIO.StringIO()) as stream:
                with iotools.RedirectedStreams(stream, stream):

                    output_method = first.strip()
                    # We treat the line as a normal line
                    # if we previously set ``is_incomplete_statement``
                    # to False - this indicates we're inside a quote.
                    if output_method in self.output_triggers and \
                        not is_incomplete_statement:
                        # TODO: Handle complex, nested input
                        if ',' in rest:
                            object_reference = rest.rpartition(',')[0].strip()
                        else:
                            object_reference = rest.rpartition(')')[0].strip()

                        # Is it a name, or something complex?
                        if object_reference in console.locals:
                            referent = console.locals[object_reference]
                        else:
                            # Prevent collisions, just in case abjad-book
                            # is being run inside abjad-book, is being
                            # run inside abjad-book, is being run inside...
                            identifier = '__abjad_book_{:08}__'.format(
                                random.randint(0, 99999999))
                            command = '{} = {}'.format(
                                identifier,
                                object_reference,
                                )
                            console.push(command)
                            referent = console.locals[identifier]
                            del(console.locals[identifier])
                                
                        asset_proxy_class = self.output_triggers[output_method]
                        asset_output_proxy = asset_proxy_class(referent)
                        self.output_proxies.append(result)
                        self.output_proxies.append(asset_output_proxy)
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
        if result == '>>> ':
            result = ''
        if result: 
            self.output_proxies.append(result)

        if self.executed_lines:
            self.output_proxies[:] = ['\n'.join(self.displayed_output_proxies)]

        if self.hide:
            for x in reversed(self.output_proxies):
                if isinstance(x, str):
                    self.output_proxies.remove(x)

        if self.strip_prompt:
            for i, x in enumerate(self.output_proxies):
                if instance(x, str):
                    lines = x.splitlines()
                    for j, line in enumerate(lines):
                        if line.startswith(('>>> ', '... ')):
                            lines[j] = line[4:]
                    self.output_proxies[i] = '\n'.join(lines) 

        # Replace strings with CodeOutputProxy instances.
        for i, result in enumerate(self.output_proxies):
            if isinstance(result, str):
                self.output_proxies[i] = newabjadbooktools.CodeOutputProxy(
                    result.splitlines())

        
        return self.output_proxies
