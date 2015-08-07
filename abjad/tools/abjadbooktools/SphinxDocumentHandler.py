# -*- encoding: utf-8 -*-
from __future__ import print_function
import collections
import glob
import hashlib
import importlib
import inspect
import os
import posixpath
import platform
import re
import shutil
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
from sphinx import addnodes
from sphinx.util import FilenameUniqDict
from sphinx.util.console import bold, red, brown
from sphinx.util.osutil import copyfile, ensuredir


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
            render_command = 'lilypond --png -dpixmap-format=pngalpha -dresolution=300 -dno-point-and-click -o {} {}'.format(
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
        SphinxDocumentHandler.style_document(app, document)
        SphinxDocumentHandler.interpret_code_blocks(app, document)

    @staticmethod
    def style_document(app, document):
        def get_unique_parts(parts):
            unique_parts = [parts[0]]
            for part in parts[1:]:
                if part != unique_parts[-1]:
                    unique_parts.append(part)
                else:
                    break
            return unique_parts
        classes_to_attributes = {}
        for desc_node in document.traverse(addnodes.desc):
            if desc_node.get('domain') != 'py':
                continue
            signature_node = desc_node.traverse(addnodes.desc_signature)[0]
            module_name = signature_node.get('module')
            object_name = signature_node.get('fullname')
            object_type = desc_node.get('objtype')
            module = importlib.import_module(module_name)
            if object_type in ('function', 'class'):
                addname_node = signature_node.traverse(addnodes.desc_addname)[0]
                text = addname_node[0].astext()
                parts = [x for x in text.split('.') if x]
                parts = get_unique_parts(parts)
                if parts[0] in ('abjad', 'experimental', 'ide'):
                    parts = parts[-1:]
                if parts:
                    text = '{}.'.format('.'.join(parts))
                else:
                    text = ''
                addname_node[0] = nodes.Text(text)
            if object_type == 'class':
                cls = getattr(module, object_name, None)
                if cls is None:
                    continue
                if cls not in classes_to_attributes:
                    classes_to_attributes[cls] = {}
                    attributes = inspect.classify_class_attrs(cls)
                    for attribute in attributes:
                        classes_to_attributes[cls][attribute.name] = attribute
                if inspect.isabstract(cls):
                    labelnode = addnodes.only(expr='html')
                    labelnode.append(nodes.emphasis(
                        'abstract ',
                        'abstract ',
                        classes=['property'],
                        ))
                    signature_node.insert(0, labelnode)
            elif object_type in ('method', 'attribute', 'staticmethod', 'classmethod'):
                cls_name, attr_name = object_name.split('.')
                cls = getattr(module, cls_name, None)
                if cls is None:
                    continue
                attr = getattr(cls, attr_name)
                inspected_attr = classes_to_attributes[cls][attr_name]
                label_node = addnodes.only(expr='html')
                defining_class = inspected_attr.defining_class
                if defining_class != cls:
                    addname_node = signature_node.traverse(
                        addnodes.desc_addname)[0]
                    if defining_class.__module__.startswith('abjad'):
                        reftarget = defining_class.__module__
                    else:
                        reftarget = '{}.{}'.format(
                            defining_class.__module__,
                            defining_class.__name__,
                            )
                    xref_node = addnodes.pending_xref(
                        '',
                        refdomain='py',
                        refexplicit=True,
                        reftype='class',
                        reftarget=reftarget,
                        )
                    xref_node.append(nodes.literal(
                        '',
                        '{}'.format(defining_class.__name__),
                        classes=['descclassname'],
                        ))
                    html_only_class_name_node = addnodes.only(expr='html')
                    html_only_class_name_node.append(nodes.Text('('))
                    html_only_class_name_node.append(xref_node)
                    html_only_class_name_node.append(nodes.Text(').'))
                    latex_only_class_name_node = addnodes.only(expr='latex')
                    latex_only_class_name_node.append(nodes.Text(
                        '({}).'.format(defining_class.__name__),
                        ))
                    addname_node.clear()
                    addname_node.append(html_only_class_name_node)
                    addname_node.append(latex_only_class_name_node)
                if getattr(attr, '__isabstractmethod__', False):
                    label_node.append(nodes.emphasis(
                        'abstract ',
                        'abstract ',
                        classes=['property'],
                        ))
                if hasattr(attr, 'im_self') and attr.im_self is not None:
                    signature_node.pop(0)
                    label_node.append(nodes.emphasis(
                        'classmethod ',
                        'classmethod ',
                        classes=['property'],
                        ))
                signature_node.insert(0, label_node)

    @staticmethod
    def interpret_code_blocks(app, document):
        import abjad
        from abjad.tools import abjadbooktools
        if SphinxDocumentHandler.should_ignore_document(app, document):
            print()
            message = '    [abjad-book] ignoring'
            print(message)
            return
        try:
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
        app.builder.thumbnails = FilenameUniqDict()
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
            shutil.copy(source_file_path, image_directory)

    @staticmethod
    def on_build_finished(app, exc):
        try:
            SphinxDocumentHandler.render_thumbnails(app)
        except:
            traceback.print_exc()

    @staticmethod
    def on_env_updated(app, env):
        try:
            SphinxDocumentHandler.install_lightbox_static_files(app)
        except:
            traceback.print_exc()

    @staticmethod
    def install_lightbox_static_files(app):
        source_static_path = os.path.join(app.builder.srcdir, '_static')
        target_static_path = os.path.join(app.builder.outdir, '_static')
        source_lightbox_path = os.path.join(source_static_path, 'lightbox2')
        target_lightbox_path = os.path.join(target_static_path, 'lightbox2')
        relative_file_paths = []
        for root, _, file_names in os.walk(source_lightbox_path):
            for file_name in file_names:
                absolute_file_path = os.path.join(root, file_name)
                relative_file_path = os.path.relpath(
                    absolute_file_path,
                    source_static_path,
                    )
                relative_file_paths.append(relative_file_path)
        if os.path.exists(target_lightbox_path):
            shutil.rmtree(target_lightbox_path)
        for relative_file_path in app.builder.status_iterator(
            relative_file_paths,
            'installing lightbox files... ',
            brown,
            len(relative_file_paths),
            ):
            source_path = os.path.join(source_static_path, relative_file_path)
            target_path = os.path.join(target_static_path, relative_file_path)
            target_directory = os.path.dirname(target_path)
            if not os.path.exists(target_directory):
                ensuredir(target_directory)
            copyfile(source_path, target_path)
            if relative_file_path.endswith('.js'):
                app.add_javascript(relative_file_path)
            elif relative_file_path.endswith('.css'):
                app.add_stylesheet(relative_file_path)

    @staticmethod
    def render_thumbnails(app):
        image_directory = os.path.join(
            app.builder.outdir,
            app.builder.imagedir,
            )
        thumbnail_paths = app.builder.thumbnails
        for path in app.builder.status_iterator(
            thumbnail_paths,
            'rendering gallery thumbnails...',
            brown,
            len(thumbnail_paths),
            ):
            image_name = os.path.basename(path)
            prefix, suffix = os.path.splitext(image_name)
            thumbnail_name = '{}-thumbnail{}'.format(prefix, suffix)
            image_path = os.path.join(image_directory, image_name)
            thumbnail_path = os.path.join(image_directory, thumbnail_name)
            if os.path.exists(thumbnail_path):
                continue
            resize_command = 'convert {} -resize 696x {}'.format(
                image_path,
                thumbnail_path,
                )
            process = subprocess.Popen(
                resize_command,
                shell=True,
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE,
                )
            stdout, stderr = process.communicate()
            return_code = process.returncode
            if return_code:
                message = 'Failed to render {}.'
                message = message.format(thumbnail_name)
                app.builder.warn(message)
                app.builder.warn(resize_command)
                if stdout:
                    if sys.version_info[0] == 3:
                        stdout = stdout.decode('utf-8')
                    app.builder.warn(stdout)

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
        return target_file_names, found_all_pages

    @staticmethod
    def render_png_image(self, node):
        from abjad.tools import abjadbooktools
        # Get all file and path parts.
        image_layout_specifier = node.get('image_layout_specifier', None)
        if image_layout_specifier is None:
            image_layout_specifier = abjadbooktools.ImageLayoutSpecifier()
        image_render_specifier = node.get('image_render_specifier', None)
        if image_render_specifier is None:
            image_render_specifier = abjadbooktools.ImageRenderSpecifier()
        pages = image_layout_specifier.pages
        target_extension = '.png'
        sha1sum = hashlib.sha1()
        sha1sum.update(node[0].encode('utf-8'))
        sha1sum.update(format(image_render_specifier, 'storage').encode('utf-8'))
        sha1sum = sha1sum.hexdigest()
        file_base_name = '{}-{}'.format(node['renderer'], sha1sum)
        file_name_pattern = '{}*{}'.format(file_base_name, target_extension)
        if node['renderer'] == 'graphviz':
            source_extension = '.dot'
        elif node['renderer'] == 'lilypond':
            source_extension = '.ly'
        absolute_directory_path, relative_directory_path = \
            SphinxDocumentHandler.get_image_directory_paths(self)
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
        if image_render_specifier.no_trim:
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
        if platform.system() == 'Windows':
            trim_command = 'convert {} -resize 33%% -trim {}'
        else:
            trim_command = 'convert {} -resize 33% -trim {}'
        trim_command = trim_command.format(
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
            #print()
            message = bold(red('Found abjad_import_block.'))
            self.builder.warn(message, (self.builder.current_docname, node.line))
            #print(systemtools.TestManager.clean_string(node.pformat()))
        except:
            traceback.print_exc()
        raise nodes.SkipNode

    @staticmethod
    def visit_abjad_input_block(self, node):
        try:
            #print()
            message = bold(red('Found abjad_input_block.'))
            self.builder.warn(message, (self.builder.current_docname, node.line))
            #print(systemtools.TestManager.clean_string(node.pformat()))
        except:
            traceback.print_exc()
        raise nodes.SkipNode

    @staticmethod
    def visit_abjad_output_block_html(self, node):
        from abjad.tools import abjadbooktools
        image_layout_specifier = node.get('image_layout_specifier', None)
        if image_layout_specifier is None:
            image_layout_specifier = abjadbooktools.ImageLayoutSpecifier()
        image_render_specifier = node.get('image_render_specifier', None)
        if image_render_specifier is None:
            image_render_specifier = abjadbooktools.ImageRenderSpecifier()
        if node['renderer'] not in ('graphviz', 'lilypond'):
            raise nodes.SkipNode
        absolute_image_directory_path = os.path.join(
            self.builder.outdir,
            self.builder.imagedir,
            'abjadbook',
            )
        if not os.path.exists(absolute_image_directory_path):
            os.makedirs(absolute_image_directory_path)
        try:
            relative_source_file_path, relative_target_file_paths = \
                SphinxDocumentHandler.render_png_image(self, node)
        except:
            traceback.print_exc()
            raise nodes.SkipNode
        if image_layout_specifier.with_columns:
            output = r'''
            <a class="table-cell thumbnail" href="{source}">
                <img src="{target}" alt="View source." title="View source." />
            </a>
            '''
            row_open = r'''<div class="table-row">'''
            row_close = r'''</div>'''
            stop = len(relative_target_file_paths)
            step = image_layout_specifier.with_columns
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
        raise nodes.SkipNode

    @staticmethod
    def visit_abjad_output_block_latex(self, node):
        raise nodes.SkipNode

    @staticmethod
    def visit_abjad_thumbnail_block_html(self, node):
        try:
            self.builder.thumbnails.add_file('', node['uri'])
            alt = node['title']
            title = node['title']
            classes = ' '.join(node['classes'])
            group = 'group-{}'.format(
                node['group'] if node['group'] else node['uri']
                )
            if node['uri'] in self.builder.images:
                node['uri'] = os.path.join(
                    self.builder.imgpath,
                    self.builder.images[node['uri']],
                    )
            image_path = node['uri']
            prefix, suffix = os.path.splitext(image_path)
            thumbnail_path = '{}-thumbnail{}'.format(prefix, suffix)
            line = u'<a data-lightbox="{group}" href="{href}" class="{cls}" '
            line += u'title="{title}" data-title="{title}">'
            line = line.format(
                group=group,
                href=image_path,
                cls=classes,
                title=title,
                )
            self.body.append(line)
            line = u'<img src="{src}" alt="{alt}"/>'
            line = line.format(src=thumbnail_path, alt=alt)
            self.body.append(line)
            line = u'</a>'
            self.body.append(line)
        except:
            traceback.print_exc()
        raise nodes.SkipNode

    @staticmethod
    def visit_abjad_thumbnail_block_latex(self, node):
        try:
            print()
            message = bold(red('Found abjad_thumbnail_block.'))
            self.builder.warn(message, (self.builder.current_docname, node.line))
            print(systemtools.TestManager.clean_string(node.pformat()))
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
        app.add_directive('doctest', abjadbooktools.DoctestDirective)
        app.add_directive('import', abjadbooktools.ImportDirective)
        app.add_directive('shell', abjadbooktools.ShellDirective)
        app.add_directive('thumbnail', abjadbooktools.ThumbnailDirective)
        app.add_javascript('abjad.js')
        app.add_javascript('copybutton.js')
        app.add_javascript('ga.js')
        app.add_stylesheet('abjad.css')
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
        app.add_node(
            abjadbooktools.abjad_thumbnail_block,
            html=[SphinxDocumentHandler.visit_abjad_thumbnail_block_html, None],
            latex=[SphinxDocumentHandler.visit_abjad_thumbnail_block_latex, None],
            )
        app.connect('build-finished', SphinxDocumentHandler.on_build_finished)
        app.connect('builder-inited', SphinxDocumentHandler.on_builder_inited)
        app.connect('doctree-read', SphinxDocumentHandler.on_doctree_read)
        app.connect('env-updated', SphinxDocumentHandler.on_env_updated)

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