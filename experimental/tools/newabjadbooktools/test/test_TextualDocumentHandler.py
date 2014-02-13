# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_TextualDocumentHandler_01():

    document = r'''Let's print something:

    <abjad>
    print "hello, world!"
    </abjad>

    This is just a simple Python string:

    <abjad>
    just_a_string = \'\'\'
    show(Nothing!)
    \'\'\'
    </abjad>

    And let's show some music too:

    <abjad>
    show(Note("c'4"))
    </abjad>

    That's it!
    '''

    test_directory_path = os.path.abspath(os.path.dirname(__file__))
    test_document_file_name = 'document.rst'
    test_document_file_path = os.path.join(
        test_directory_path,
        test_document_file_name,
        )

    document_handler = newabjadbooktools.ReSTDocumentHandler(
        document,
        document_file_name=test_document_file_name,
        output_directory_path=test_directory_path,
        )
    document_handler.extract_code_blocks()
    document_handler.execute_code_blocks()
    rebuilt_document = '\n'.join(document_handler.rebuild_document())

    try:
        document_handler.write_rebuilt_document()
        assert os.path.exists(test_document_file_path)
        with open(test_document_file_path, 'r') as f:
            written_document = f.read()
        assert rebuilt_document == written_document
        os.remove(test_document_file_path)
    finally:
        if os.path.exists(test_document_file_path):
            os.remove(test_document_file_path)
        assert not os.path.exists(test_document_file_path)
