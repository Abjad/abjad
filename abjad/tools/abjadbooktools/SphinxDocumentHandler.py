# -*- encoding: utf-8 -*-
from __future__ import print_function
import collections
import hashlib
import os
import posixpath
import subprocess
import sys
import traceback
from abjad.tools import abctools
from abjad.tools import systemtools
from docutils import nodes
from docutils.frontend import OptionParser
from docutils.parsers.rst import Parser
from docutils.parsers.rst import directives
from docutils.utils import new_document


class SphinxDocumentHandler(abctools.AbjadObject):

    ### CLASS VARIABLES ###

    class abjad_import_block(nodes.General, nodes.Element):
        pass

    class abjad_input_block(nodes.General, nodes.Element):
        pass

    class abjad_output_block(nodes.General, nodes.FixedTextElement):
        pass

    __slots__ = (
        '_errored',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._errored = False

    ### SPHINX HOOKS

    @staticmethod
    def on_doctree_read(app, document):
        try:
            import abjad
            from abjad.tools import abjadbooktools
            #if 'api' not in document['source']:
            #    return
            handler = SphinxDocumentHandler()
            abjad_blocks = handler.collect_abjad_input_blocks(document)
            abjad_console = abjadbooktools.AbjadBookConsole(
                document_handler=handler,
                locals=abjad.__dict__.copy(),
                )
            literal_blocks = handler.collect_python_literal_blocks(document)
            literal_console = abjadbooktools.AbjadBookConsole(
                document_handler=handler,
                locals=abjad.__dict__.copy(),
                )
            handler.interpret_input_blocks(document, abjad_blocks, abjad_console)
            handler.interpret_input_blocks(document, literal_blocks, literal_console)
            handler.rebuild_document(document, abjad_blocks)
            handler.rebuild_document(document, literal_blocks)
            abjad_console.restore_topleveltools_dict()
            literal_console.restore_topleveltools_dict()
        except Exception:
            app.builder.warn(
                'Encountered parsing error.',
                (app.builder.current_docname, 0),
                )
            traceback.print_exc()

    @staticmethod
    def on_builder_inited(app):
        app.builder.imagedir = '_images'

    @staticmethod
    def on_build_finished(app, exc):
        pass

    def visit_abjad_output_block_html(self, node):
        if node['renderer'] not in ('graphviz', 'lilypond'):
            raise nodes.SkipNode
        absolute_image_directory_path = os.path.join(
            self.builder.outdir,
            self.builder.imagedir,
            'abjadbook',
            )
        if not os.path.exists(absolute_image_directory_path):
            os.makedirs(absolute_image_directory_path)
        relative_source_file_path, relative_target_file_path, succeeded = \
            SphinxDocumentHandler.render_png_image(self, node)
        output = r'''
        <div class="abjad-book-image">
            <a href="{source}">
                <img src="{target}" alt="View source." title="View source." />
            </a>
        </div>
        '''
        output = output.format(
            source=relative_source_file_path,
            target=relative_target_file_path,
            )
        output = systemtools.TestManager.clean_string(output)
        self.body.append(output)
        raise nodes.SkipNode

    def visit_abjad_output_block_latex(self, node):
        raise nodes.SkipNode

    def get_paths(self, node, target_extension='.png'):
        sha1sum = hashlib.sha1(node[0].encode('utf-8')).hexdigest()
        file_base_name = '{}-{}'.format(node['renderer'], sha1sum)
        if node['renderer'] == 'graphviz':
            source_extension = '.dot'
        elif node['renderer'] == 'lilypond':
            source_extension = '.ly'
        relative_image_directory_path = posixpath.join(
            self.builder.imgpath,
            'abjadbook',
            )
        absolute_image_directory_path = os.path.join(
            self.builder.outdir,
            self.builder.imagedir,
            'abjadbook',
            )
        absolute_source_file_path = os.path.join(
            absolute_image_directory_path,
            file_base_name + source_extension,
            )
        absolute_target_file_path = os.path.join(
            absolute_image_directory_path,
            file_base_name + target_extension,
            )
        relative_source_file_path = posixpath.join(
            relative_image_directory_path,
            file_base_name + source_extension,
            )
        relative_target_file_path = posixpath.join(
            relative_image_directory_path,
            file_base_name + target_extension,
            )
        return (
            absolute_image_directory_path,
            absolute_source_file_path,
            absolute_target_file_path,
            relative_source_file_path,
            relative_target_file_path,
            )

    def render_png_image(self, node):
        (
            absolute_image_directory_path,
            absolute_source_file_path,
            absolute_target_file_path,
            relative_source_file_path,
            relative_target_file_path,
            ) = SphinxDocumentHandler.get_paths(self, node)
        if os.path.isfile(absolute_target_file_path):
            #self.builder.info('Preserved {}.'.format(absolute_target_file_path))
            return relative_source_file_path, relative_target_file_path, True
        if node['renderer'] == 'graphviz':
            render_command = 'dot -Tpng {} -o {}'.format(
                absolute_source_file_path,
                absolute_target_file_path,
                )
        elif node['renderer'] == 'lilypond':
            render_command = 'lilypond --png -dresolution=300 -dno-point-and-click -o {} {}'.format(
                os.path.splitext(absolute_target_file_path)[0],
                absolute_source_file_path,
                )
        with open(absolute_source_file_path, 'w') as file_pointer:
            file_pointer.write(node[0])

        process = subprocess.Popen(
            render_command,
            shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            )
        stdout, stderr = process.communicate()
        return_code = process.returncode

        if return_code:
            self.builder.warn(
                'Failed to render {}.'.format(absolute_target_file_path),
                (self.builder.current_docname, node.line),
                )
            self.builder.warn(render_command)
            if stdout:
                if sys.version_info[0] == 3:
                    stdout = stdout.decode('utf-8')
                self.builder.warn(stdout)
            return relative_source_file_path, relative_target_file_path, False

        trim_command = 'convert -trim -resize 50%% {} {}'.format(
            absolute_target_file_path,
            absolute_target_file_path,
            )
        process = subprocess.Popen(
            trim_command,
            shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            )
        stdout, stderr = process.communicate()
        return_code = process.returncode

        if return_code:
            self.builder.warn(
                'Failed to render {}.'.format(absolute_target_file_path),
                (self.builder.current_docname, node.line),
                )
            self.builder.warn(trim_command)
            if stdout:
                if sys.version_info[0] == 3:
                    stdout = stdout.decode('utf-8')
                self.builder.warn(stdout)
            return relative_source_file_path, relative_target_file_path, False

        #self.builder.info('Rendered {}.'.format(absolute_target_file_path))

        return relative_source_file_path, relative_target_file_path, True

    ### PUBLIC METHODS ###

    def collect_abjad_input_blocks(self, document):
        def is_valid_node(node):
            prototype = (
                SphinxDocumentHandler.abjad_import_block,
                SphinxDocumentHandler.abjad_input_block,
                )
            return isinstance(node, prototype)
        from abjad.tools import abjadbooktools
        code_blocks = collections.OrderedDict()
        for block in document.traverse(is_valid_node):
            if isinstance(block, SphinxDocumentHandler.abjad_import_block):
                code_block = \
                    abjadbooktools.CodeBlock.from_docutils_abjad_import_block(block)
            else:
                code_block = \
                    abjadbooktools.CodeBlock.from_docutils_abjad_input_block(block)
            code_blocks[block] = code_block
        return code_blocks

    def collect_python_literal_blocks(self, document):
        def is_valid_node(node):
            prototype = (
                nodes.literal_block,
                nodes.doctest_block,
                )
            return isinstance(node, prototype)
        from abjad.tools import abjadbooktools
        code_blocks = collections.OrderedDict()
        for block in document.traverse(is_valid_node):
            lines = block[0].splitlines()
            if not lines[0].startswith('>>>'):
                continue
            code_block = \
                abjadbooktools.CodeBlock.from_docutils_literal_block(block)
            code_blocks[block] = code_block
        #for block, code_block in code_blocks.items():
        #    print(block.pformat())
        #    print(format(code_block))
        #    print()
        return code_blocks

    def interpret_input_blocks(
        self,
        document,
        input_blocks,
        console,
        ):
        from abjad.tools import abjadbooktools
        #print('preparing to interpret')
        try:
            code_blocks = tuple(input_blocks.values())
            if not code_blocks:
                return
            progress_indicator = systemtools.ProgressIndicator(
                message='    Interpreting code blocks',
                total=len(code_blocks),
                verbose=False,
                )
            with progress_indicator:
                for code_block in code_blocks:
                    code_block.interpret(console)
                    progress_indicator.advance()
        except abjadbooktools.AbjadBookError:
            #print()
            traceback.print_exc()
            #print()
        #print('interpreted...')
        #print()
        #for block, code_block in input_blocks.items():
        #    print(block.pformat())
        #    print(format(code_block))
        #    for output_proxy in code_block.output_proxies:
        #        print(format(output_proxy))
        #    print()

    @staticmethod
    def parse_rst(rst_string):
        from abjad.tools import abjadbooktools
        parser = Parser()
        directives.register_directive(
            'abjad', abjadbooktools.AbjadDirective,
            )
        directives.register_directive(
            'import', abjadbooktools.ImportDirective,
            )
        directives.register_directive('shell', abjadbooktools.ShellDirective)
        settings = OptionParser(components=(Parser,)).get_default_values()
        document = new_document('test', settings)
        parser.parse(rst_string, document)
        document = parser.document
        return document

    def rebuild_document(self, document, blocks):
        for old_node, code_block in reversed(tuple(blocks.items())):
            new_nodes = code_block.as_docutils()
            if (
                len(new_nodes) == 1 and
                systemtools.TestManager.clean_string(old_node.pformat()) ==
                systemtools.TestManager.clean_string(new_nodes[0].pformat())
                ):
                #print('Preserving...')
                continue
            #print('Replacing...')
            #print(old_node.pformat())
            #print('...with...')
            #for new_node in new_nodes:
            #    print(new_node.pformat())
            old_node.parent.replace(old_node, new_nodes)

    @staticmethod
    def setup_sphinx_extension(app):
        from abjad.tools import abjadbooktools
        app.add_directive('abjad', abjadbooktools.AbjadDirective)
        app.add_directive('import', abjadbooktools.ImportDirective)
        app.add_directive('shell', abjadbooktools.ShellDirective)
        app.add_node(
            SphinxDocumentHandler.abjad_output_block,
            html=[
                SphinxDocumentHandler.visit_abjad_output_block_html,
                None,
                ],
            latex=[
                SphinxDocumentHandler.visit_abjad_output_block_latex,
                None,
                ],
            )
        app.connect('build-finished', SphinxDocumentHandler.on_build_finished)
        app.connect('builder-inited', SphinxDocumentHandler.on_builder_inited)
        app.connect('doctree-read', SphinxDocumentHandler.on_doctree_read)

    def register_error(self):
        self._errored = True

    def unregister_error(self):
        self._errored = False

    ### PUBLIC PROPERTIES ###

    @property
    def errored(self):
        return self._errored