# -*- encoding: utf-8 -*-
from __future__ import print_function
import collections
import glob
import hashlib
import os
import posixpath
import subprocess
import re
import shutil
import sys
import traceback
from abjad.tools import abctools
from abjad.tools import systemtools
from docutils import nodes
from docutils.frontend import OptionParser
from docutils.parsers.rst import Parser
from docutils.parsers.rst import directives
from docutils.utils import new_document
from sphinx.util.console import bold, red


class SphinxDocumentHandler(abctools.AbjadObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Document Handlers'

    __slots__ = (
        '_errored',
        )

    _topleveltools_pattern = re.compile(r'''
        \b(
            graph |
            show |
            play |
            topleveltools\.graph |
            topleveltools\.show |
            topleveltools\.play
        )\b
        ''',
        re.VERBOSE,
        )

    _image_target_pattern = re.compile('.+-page(\d+)\..+')

    ### INITIALIZER ###

    def __init__(self):
        self._errored = False

    ### SPHINX HOOKS

    @staticmethod
    def interpret_image_source(
        self,
        node,
        absolute_source_file_path,
        absolute_target_file_path,
        ):
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
        return return_code

    @staticmethod
    def on_doctree_read(app, document):
        import abjad
        from abjad.tools import abjadbooktools
        if SphinxDocumentHandler.should_ignore_document(app, document):
            print()
            message = '    [abjad-book] ignoring'
            print(message)
            return
        try:
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
            if abjad_blocks or literal_blocks:
                print()
                handler.interpret_input_blocks(document, abjad_blocks, abjad_console)
                handler.interpret_input_blocks(document, literal_blocks, literal_console)
                handler.rebuild_document(document, abjad_blocks)
                handler.rebuild_document(document, literal_blocks)
            #else:
            #    print()
            #    message = '    [abjad-book] rendering not required'
            #    print(message)
            abjad_console.restore_topleveltools_dict()
            literal_console.restore_topleveltools_dict()
        except abjadbooktools.AbjadBookError as e:
            print()
            print(e.args[0])
        except Exception:
            print()
            traceback.print_exc()

    @staticmethod
    def on_builder_inited(app):
        app.builder.imagedir = '_images'
        stylesheets_directory = os.path.join(
            app.builder.srcdir,
            '_stylesheets',
            )
        image_directory = os.path.join(
            app.builder.outdir,
            app.builder.imagedir,
            'abjadbook',
            )
        if not os.path.exists(image_directory):
            os.makedirs(image_directory)
        if not os.path.exists(stylesheets_directory):
            return
        for file_name in os.listdir(stylesheets_directory):
            if os.path.splitext(file_name)[-1] not in ('.ly', '.ily'):
                continue
            source_file_path = os.path.join(
                stylesheets_directory,
                file_name,
                )
            #print('from', source_file_path, 'to', image_directory)
            shutil.copy(source_file_path, image_directory)

    @staticmethod
    def on_build_finished(app, exc):
        pass

    @staticmethod
    def get_image_directory_paths(self):
        absolute_image_directory_path = os.path.join(
            self.builder.outdir,
            self.builder.imagedir,
            'abjadbook',
            )
        relative_image_directory_path = posixpath.join(
            self.builder.imgpath,
            'abjadbook',
            )
        paths = (absolute_image_directory_path, relative_image_directory_path)
        return paths

    @staticmethod
    def find_target_file_names(
        absolute_directory_path,
        file_name_pattern,
        pages,
        ):
        #print(file_name_pattern, pages)
        with systemtools.TemporaryDirectoryChange(absolute_directory_path):
            file_name_matches = glob.glob(file_name_pattern)
        #print('\t', file_name_matches)
        target_file_name_dict = {}
        if len(file_name_matches) == 1 and '-page' not in file_name_matches[0]:
            target_file_name_dict[1] = file_name_matches[0]
        else:
            for file_name_match in file_name_matches:
                re_match = SphinxDocumentHandler._image_target_pattern.match(
                    file_name_match)
                page = int(re_match.groups()[0])
                target_file_name_dict[page] = file_name_match
        target_file_names = []
        found_all_pages = False
        if pages is None:
            target_file_names.extend(target_file_name_dict.values())
            found_all_pages = bool(target_file_names)
        else:
            for page in pages:
                if page in target_file_name_dict:
                    target_file_names.append(target_file_name_dict[page])
            if len(target_file_names) == len(pages):
                found_all_pages = True
        #print('\t', target_file_names, found_all_pages)
        return target_file_names, found_all_pages

    @staticmethod
    def render_png_image(self, node):
        from abjad.tools import abjadbooktools
        # Get all file and path parts.
        image_specifier = node.get('image_specifier', None)
        if image_specifier is None:
            image_specifier = abjadbooktools.ImageSpecifier()
        pages = image_specifier.pages
        #print(node.pformat())
        #print('PAGES', pages)
        target_extension = '.png'
        sha1sum = hashlib.sha1()
        sha1sum.update(node[0].encode('utf-8'))
        sha1sum.update(format(image_specifier, 'storage').encode('utf-8'))
        sha1sum = sha1sum.hexdigest()
        file_base_name = '{}-{}'.format(node['renderer'], sha1sum)
        file_name_pattern = '{}*{}'.format(file_base_name, target_extension)
        if node['renderer'] == 'graphviz':
            source_extension = '.dot'
        elif node['renderer'] == 'lilypond':
            source_extension = '.ly'
        absolute_directory_path, relative_directory_path = \
            SphinxDocumentHandler.get_image_directory_paths(self)
        #print(absolute_directory_path, relative_directory_path)
        relative_source_file_path = posixpath.join(
            relative_directory_path,
            file_base_name + source_extension,
            )
        # Check for pre-existing target(s).
        target_file_names, found_all_pages = \
            SphinxDocumentHandler.find_target_file_names(
                absolute_directory_path,
                file_name_pattern,
                pages,
                )
        if found_all_pages:
            return (
                relative_source_file_path,
                [posixpath.join(relative_directory_path, _) for _ in target_file_names],
                )
        # Write and render source to target(s).
        absolute_source_file_path = os.path.join(
            absolute_directory_path,
            file_base_name + source_extension,
            )
        absolute_target_file_path = os.path.join(
            absolute_directory_path,
            file_base_name + target_extension,
            )
        SphinxDocumentHandler.write_image_source(
            self, node, absolute_source_file_path)
        return_code = SphinxDocumentHandler.interpret_image_source(
            self, node, absolute_source_file_path, absolute_target_file_path)
        if return_code:
            return (
                relative_directory_path,
                [],
                )
        # Check for target(s).
        target_file_names, found_all_pages = \
            SphinxDocumentHandler.find_target_file_names(
                absolute_directory_path, file_name_pattern, pages,
                )
        if not found_all_pages:
            return (
                relative_source_file_path,
                [posixpath.join(relative_directory_path, _) for _ in target_file_names],
                )
        # Trim target(s).
        if image_specifier.no_trim:
            pass
        else:
            for target_name in target_file_names:
                target_path = os.path.join(absolute_directory_path, target_name)
                return_code = SphinxDocumentHandler.trim_image_target(
                    self, node, target_path)
        # Target(s) must exist, so simply return.
        return (
            relative_source_file_path,
            [posixpath.join(relative_directory_path, _) for _ in target_file_names],
            )

    @staticmethod
    def trim_image_target(
        self,
        node,
        absolute_target_file_path,
        ):
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
        return return_code

    @staticmethod
    def visit_abjad_import_block(self, node):
        try:
            print()
            message = bold(red('Found abjad_import_block.'))
            self.builder.warn(message, (self.builder.current_docname, node.line))
            print(systemtools.TestManager.clean_string(node.pformat()))
        except:
            traceback.print_exc()
        raise nodes.SkipNode

    @staticmethod
    def visit_abjad_input_block(self, node):
        try:
            print()
            message = bold(red('Found abjad_input_block.'))
            self.builder.warn(message, (self.builder.current_docname, node.line))
            print(systemtools.TestManager.clean_string(node.pformat()))
        except:
            traceback.print_exc()
        raise nodes.SkipNode

    @staticmethod
    def visit_abjad_output_block_html(self, node):
        from abjad.tools import abjadbooktools
        #print()
        #print(node.pformat())
        try:
            image_specifier = node.get('image_specifier', None)
            if image_specifier is None:
                image_specifier = abjadbooktools.ImageSpecifier()
            if node['renderer'] not in ('graphviz', 'lilypond'):
                raise nodes.SkipNode
            absolute_image_directory_path = os.path.join(
                self.builder.outdir,
                self.builder.imagedir,
                'abjadbook',
                )
            if not os.path.exists(absolute_image_directory_path):
                os.makedirs(absolute_image_directory_path)
            relative_source_file_path, relative_target_file_paths = \
                SphinxDocumentHandler.render_png_image(self, node)
            if image_specifier.with_columns:
                output = r'''
                <a class="table-cell thumbnail" href="{source}">
                    <img src="{target}" alt="View source." title="View source." />
                </a>
                '''
                row_open = r'''<div class="table-row">'''
                row_close = r'''</div>'''
                stop = len(relative_target_file_paths)
                step = image_specifier.with_columns
                for i in range(0, stop, step):
                    self.body.append(row_open)
                    paths = relative_target_file_paths[i:i + step]
                    for relative_target_file_path in paths:
                        result = output.format(
                            source=relative_source_file_path,
                            target=relative_target_file_path,
                            )
                        result = systemtools.TestManager.clean_string(result)
                        result = ('    ' + _ for _ in result.splitlines())
                        result = '\n'.join(result)
                        self.body.append(result)
                    self.body.append(row_close)
            else:
                output = r'''
                <div class="abjad-book-image">
                    <a href="{source}">
                        <img src="{target}" alt="View source." title="View source." />
                    </a>
                </div>
                '''
                for relative_target_file_path in relative_target_file_paths:
                    result = output.format(
                        source=relative_source_file_path,
                        target=relative_target_file_path,
                        )
                    result = systemtools.TestManager.clean_string(result)
                    self.body.append(result)
        except:
            traceback.print_exc()
        raise nodes.SkipNode

    @staticmethod
    def visit_abjad_output_block_latex(self, node):
        try:
            pass
        except:
            traceback.print_exc()
        raise nodes.SkipNode

    @staticmethod
    def write_image_source(self, node, absolute_source_file_path):
        with open(absolute_source_file_path, 'w') as file_pointer:
            code = node[0]
            if sys.version_info[0] == 2:
                code = code.encode('utf-8')
            file_pointer.write(code)

    ### PUBLIC METHODS ###

    def collect_abjad_input_blocks(self, document):
        def is_valid_node(node):
            prototype = (
                abjadbooktools.abjad_import_block,
                abjadbooktools.abjad_input_block,
                )
            return isinstance(node, prototype)
        from abjad.tools import abjadbooktools
        code_blocks = collections.OrderedDict()
        for block in document.traverse(is_valid_node):
            if isinstance(block, abjadbooktools.abjad_import_block):
                code_block = \
                    abjadbooktools.CodeBlock.from_docutils_abjad_import_block(block)
            else:
                code_block = \
                    abjadbooktools.CodeBlock.from_docutils_abjad_input_block(block)
            code_blocks[block] = code_block
        return code_blocks

    def collect_python_literal_blocks(self, document, renderable_only=True):
        def is_valid_node(node):
            prototype = (
                nodes.literal_block,
                nodes.doctest_block,
                )
            return isinstance(node, prototype)
        from abjad.tools import abjadbooktools
        should_process = False
        code_blocks = collections.OrderedDict()
        for block in document.traverse(is_valid_node):
            lines = block[0].splitlines()
            if not lines[0].startswith('>>>'):
                continue
            for line in lines:
                if self._topleveltools_pattern.search(line) is not None:
                    should_process = True
            code_block = \
                abjadbooktools.CodeBlock.from_docutils_literal_block(block)
            code_blocks[block] = code_block
        if renderable_only and not should_process:
            code_blocks.clear()
        return code_blocks

    def get_default_stylesheet(self):
        return 'default.ly'

    def interpret_input_blocks(
        self,
        document,
        input_blocks,
        console,
        ):
        code_blocks = tuple(input_blocks.values())
        if not code_blocks:
            return
        progress_indicator = systemtools.ProgressIndicator(
            message='    [abjad-book] interpreting',
            total=len(code_blocks),
            verbose=True,
            )
        with progress_indicator:
            for code_block in code_blocks:
                code_block.interpret(console)
                progress_indicator.advance()

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
                continue
            old_node.parent.replace(old_node, new_nodes)

    @staticmethod
    def setup_sphinx_extension(app):
        from abjad.tools import abjadbooktools
        app.add_config_value('abjadbook_ignored_documents', (), 'env')
        app.add_directive('abjad', abjadbooktools.AbjadDirective)
        app.add_directive('import', abjadbooktools.ImportDirective)
        app.add_directive('shell', abjadbooktools.ShellDirective)
        app.add_node(
            abjadbooktools.abjad_import_block,
            html=[SphinxDocumentHandler.visit_abjad_import_block, None],
            latex=[SphinxDocumentHandler.visit_abjad_import_block, None],
            )
        app.add_node(
            abjadbooktools.abjad_input_block,
            html=[SphinxDocumentHandler.visit_abjad_input_block, None],
            latex=[SphinxDocumentHandler.visit_abjad_input_block, None],
            )
        app.add_node(
            abjadbooktools.abjad_output_block,
            html=[SphinxDocumentHandler.visit_abjad_output_block_html, None],
            latex=[SphinxDocumentHandler.visit_abjad_output_block_latex, None],
            )
        app.connect('build-finished', SphinxDocumentHandler.on_build_finished)
        app.connect('builder-inited', SphinxDocumentHandler.on_builder_inited)
        app.connect('doctree-read', SphinxDocumentHandler.on_doctree_read)

    def register_error(self):
        self._errored = True

    def unregister_error(self):
        self._errored = False

    @staticmethod
    def should_ignore_document(app, document):
        if not app.config.abjadbook_ignored_documents:
            return False
        source = document['source']
        for pattern in app.config.abjadbook_ignored_documents:
            if isinstance(pattern, str):
                if pattern in source:
                    return True
            else:
                if pattern.match(source) is not None:
                    return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def errored(self):
        return self._errored