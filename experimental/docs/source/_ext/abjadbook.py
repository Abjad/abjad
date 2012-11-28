import docutils
import os
import shutil
import subprocess
import tempfile
from abjad.tools import documentationtools


# app.env.images is a dict:
# {u'appendices/history/images/index-5.png': (set(['appendices/history/index']), u'index-5.png')}
# etc.

def add_image_block(literal_block, uri):
    image = docutils.nodes.image(uri=uri)
    literal_block.replace_self([literal_block, image])


def collect_literal_block_pairs(doctree):
    pairs = []
    has_show_command = False
    for literal_block in doctree.traverse(docutils.nodes.literal_block):
        stripped_lines = []
        for line in literal_block[0].splitlines():
            if line.startswith(('>>> ', '... ')):
                line = line[4:]
                if line.startswith('show('):
                    has_show_command = True
                stripped_lines.append(line)
        pairs.append((literal_block, tuple(stripped_lines)))
    if has_show_command:
        return tuple(pairs)
    return None


def process_doctree(app, doctree):

    docname = doctree['source'].partition(app.srcdir)[-1][1:-4]
    if not (app.config.abjadbook_should_process and \
        docname.startswith(app.config.abjadbook_transform_path)):
        return

    pairs = collect_literal_block_pairs(doctree)
    if pairs is None:
        return

    #print ''

    # setup
    docname_parts = docname.split('/')
    doctree_directory = os.path.join(*([app.srcdir] + docname_parts[:-1]))
    png_directory = os.path.join(doctree_directory, 'images')
    if not os.path.exists(png_directory):
        os.mkdir(png_directory)
    literal_block_images = {}
    image_prefix = docname_parts[-1]
    image_count = 0
    tmp_directory = os.path.abspath(tempfile.mkdtemp(dir=doctree_directory))

    # create tmp python file, create .ly files
    f = open(os.path.join(tmp_directory, 'tmp.py'), 'w')
    f.write('from abjad import *\n')
    for literal_block, stripped_lines in pairs:
        for line in stripped_lines:
            if line.startswith('show('):
                image_count += 1
                file_name = '{}-{}'.format(image_prefix, image_count)
                object_name = line.partition(')')[0][5:]
                command = "iotools.write_expr_to_ly({}, {!r}, docs=True)".format(
                    object_name, os.path.join(tmp_directory, file_name))
                f.write(command + '\n')

                # 
                if literal_block not in literal_block_images:
                    literal_block_images[literal_block] = []
                literal_block_images[literal_block].append(file_name)

                # 
                #sphinx_image_name = file_name + '.png'
                #sphinx_image_path = os.path.join(*(docname_parts[:-1] + [sphinx_image_name]))
                #app.env.images[sphinx_image_path] = (
                #    set((docname,)),
                #    sphinx_image_name
                #    )

            else:
                f.write(line + '\n')
    f.close()
    command = 'python {}'.format(os.path.join(tmp_directory, 'tmp.py'))
    subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # run LilyPond on generated .ly files, move 
    for literal_block, file_names in literal_block_images.items():
        for file_name in sorted(file_names):
            lilypond_file_name = os.path.join(tmp_directory, file_name + '.ly')
            tmp_png_file_name = os.path.join(tmp_directory, file_name + '.png')
            final_png_file_name = os.path.join(png_directory, file_name + '.png')
            command = 'lilypond --png -dresolution=300 -o {} {}'.format(
                os.path.join(tmp_directory, file_name), lilypond_file_name)
            subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            command = 'convert {} -trim -resample 40%% {}'.format(
                tmp_png_file_name, final_png_file_name)
            subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            uri = '/'.join(docname_parts[:-1] + ['images', file_name + '.png'])
            #print 'URI:', uri
            #print 'FILENAME:', file_name
            add_image_block(literal_block, 'images/{}.png'.format(file_name))
        
    #print 'DOCNAME:', docname
    app.env.process_images(docname, doctree)

    # cleanup
    #shutil.rmtree(tmp_directory)


def setup(app):
    app.add_config_value('abjadbook_should_process', False, 'env')
    app.add_config_value('abjadbook_transform_path', 'api/tools/', 'env')
    app.connect('doctree-read', process_doctree)

