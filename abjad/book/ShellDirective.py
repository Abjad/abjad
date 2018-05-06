import os
import subprocess
from typing import Dict  # noqa
from docutils import nodes  # type: ignore
from docutils.parsers.rst import Directive  # type: ignore
from sphinx.util.nodes import set_source_info  # type: ignore


class ShellDirective(Directive):
    r'''An abjad-book shell directive.

    Represents a shell session.

    Generates a docutils ``literal_block`` node.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Sphinx Internals'

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}  # type: Dict[str, object]

    ### PRIVATE METHODS ###

    def _read_from_pipe(self, pipe):
        lines = []
        string = pipe.read()
        for line in string.splitlines():
            line = line.decode('utf-8')
            lines.append(line)
        return '\n'.join(lines)

    ### PUBLIC METHODS ###

    def run(self):
        r'''Executes the directive.
        '''
        from abjad import abjad_configuration
        self.assert_has_content()
        os.chdir(abjad_configuration.abjad_directory)
        result = []
        for line in self.content:
            curdir = os.path.basename(os.path.abspath(os.path.curdir))
            prompt = '{}$ '.format(curdir)
            prompt += line
            result.append(prompt)
            process = subprocess.Popen(
                line,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                )
            stdout = self._read_from_pipe(process.stdout)
            stderr = self._read_from_pipe(process.stderr)
            result.append(stdout)
            result.append(stderr)
        code = '\n'.join(result)
        literal = nodes.literal_block(code, code)
        literal['language'] = 'console'
        set_source_info(self, literal)
        return [literal]
