from experimental import quantizationtools


def test_MeteredQSchema___init___01():

    item_a = quantizationtools.MeteredQSchemaItem(tempo=((1, 4), 76))
    item_b = quantizationtools.MeteredQSchemaItem(time_signature=(3, 4))
    item_c = quantizationtools.MeteredQSchemaItem(use_full_measure=True)
    #item_d = quantizationtools.MeteredQSchemaItem(search_tree=None)

    schema = quantizationtools.MeteredQSchema({
        2: item_a,
        4: item_b,
        6: item_c
        })


