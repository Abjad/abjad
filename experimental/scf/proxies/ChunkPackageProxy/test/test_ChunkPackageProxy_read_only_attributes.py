import scf


def test_ChunkPackageProxy_read_only_attributes_01():

    cpp = scf.proxies.ChunkPackageProxy('manos.mus.chunks.test_chunk')
    assert cpp.breadcrumb == 'test chunk'
    assert cpp.score_template is None
