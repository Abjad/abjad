from docutils.parsers.rst import directives
from sphinx.util.compat import Directive
from sphinx.util.nodes import set_source_info
from docutils.nodes import literal_block


class AbjadDirective(Directive):
    r'''An `..  abjad::` docutils directive.

    Represents a portion of an interactive session.

    Generates a SphinxDocumentHandler.abjad_input_block node.
    '''

    ### CLASS VARIABLES ###

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'allow-exceptions': directives.flag,
        'hide': directives.flag,
        'strip-prompt': directives.flag,
        'text-width': int,
        }

    ### PUBLIC METHODS ###

    def run(self):
        r'''Executes the directive.
        '''
        from abjad.tools import abjadbooktools
        self.assert_has_content()
        code = u'\n'.join(self.content)
        literal = literal_block(code, code)
        block = abjadbooktools.SphinxDocumentHandler.abjad_input_block(
            code, literal)
        block['allow-exceptions'] = 'allow-exceptions' in self.options
        block['hide'] = 'hide' in self.options
        block['strip-prompt'] = 'strip-prompt' in self.options
        block['text-width'] = self.options.get('text-width', None)
        set_source_info(self, block)
        return [block]