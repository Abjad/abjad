import docutils
import os
from abjad.tools.abctools import AbjadObject


class AbjadBookDoctreeProcessor(AbjadObject):
    '''Process a single doctree prior to Sphinx environment pickling.

    Extract Python code blocks, and test if they contain 'show(...)' anywhere.

    If so, preprocess to replace 'show(...)' statements, then exec(), using
    a synthetic global namespace.

    Pass the retrieved MD5-based .ly filenames into the task queue.

    On any error in LilyPond or ImageMagick rendering, halt Sphinx.
    '''

    def __init__(self, app, doctree):
        self._app = app
        self._doctree = doctree

    ### SPECIAL METHODS ###

    def __call__(self):

        pairs = self._collect_stripped_code()
        if pairs is None:
            return

        environment = {'__builtins__': __builtins__}
        exec('from abjad import *\n', environment) 
            
        all_md5hashes = set([])
        for literal_block, stripped_code in pairs:
            md5hashes = self._exec_code_block(stripped_code, environment)

            for md5hash in md5hashes:
                relative_uri = self._get_relative_image_uri(md5hash)
                self._add_image_block(literal_block, relative_uri)
                all_md5hashes.add(md5hash)

        for md5hash in all_md5hashes:
            ly_file_name = os.path.join(self.tmp_directory, md5hash + '.ly')
            self.task_queue.put(ly_file_name)
            
        result = []
        for _ in xrange(len(all_md5hashes)):
            result.append(self.done_queue.get())

    ### PRIVATE METHODS ###

    def _add_image_block(self, literal_block, uri):
        image = docutils.nodes.image(
            candidates={'*': uri},
            uri=uri,
            )
        literal_block.replace_self([literal_block, image])

    def _collect_stripped_code(self):
        '''Iterate through all literal blocks in `doctree`.

        If 'show(...)' appears anywhere, return (literal_block, stripped code) pairs.

        Otherwise return None to indicate no need to process further.
        '''
        pairs = []
        has_show_command = False
        for literal_block in self.doctree.traverse(docutils.nodes.literal_block):
            stripped_lines = []
            for line in literal_block[0].splitlines():
                if line.startswith(('>>> ', '... ')):
                    line = line[4:]
                    if line.startswith('show('):
                        has_show_command = True
                    line = self._rewrite_line(line)
                    stripped_lines.append(line)
            stripped_lines = '\n'.join(stripped_lines) + '\n'
            pairs.append((literal_block, stripped_lines))
        if has_show_command:
            return tuple(pairs)
        return None

    def _exec_code_block(self, code_block, environment):
        environment['__md5hashes__'] = []
        exec(code_block, environment)
        return environment['__md5hashes__']

    def _get_relative_image_uri(self, md5hash):
        import sphinx.util.osutil
        return sphinx.util.osutil.relative_uri(
            self.builder.get_target_uri(self.docname),
            os.path.join('_images', 'api', md5hash + '.png'))

    def _rewrite_line(self, line):
        if line.startswith('show('):
            object_name = line[5:]
            object_name = object_name.rpartition(')')[0]
            if ')' in object_name:
                object_name = object_name.rpartition(')')[0] + ')'
            elif ',' in object_name:
                object_name = object_name.rpartition(',')[0]
            object_name = object_name.strip()
            command = 'documentationtools.write_expr_to_md5_hashed_ly(' \
                '{}, {!r}, overwrite=False)'.format(object_name, self.tmp_directory)
            command = '__md5hashes__.append({})'.format(command)
            line = command
        elif line.startswith(('f(', 'print ', 'z(')):
            line = ''
        return line + '\n'

    ### PUBLIC ATTRIBUTES ###

    @property
    def app(self):
        return self._app

    @property
    def builder(self):
        return self.app.builder

    @property
    def docname(self):
        return self.doctree['source'][:-4].partition(self.app.srcdir)[-1][1:]

    @property
    def doctree(self):
        return self._doctree

    @property
    def done_queue(self):
        return self.builder._abjadbook_done_queue

    @property
    def img_directory(self):
        return os.path.join(self.builder.outdir, '_images', 'api')

    @property
    def task_queue(self):
        return self.builder._abjadbook_task_queue

    @property
    def tmp_directory(self):
        return self.builder._abjadbook_tempdir
