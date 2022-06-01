
def recursive_attribute_compare(entity_1, entity_2, template: dict[str, None | dict | type]):
    for field_name, field_type in template.items():
        val_1 = getattr(entity_1, field_name)
        val_2 = getattr(entity_2, field_name)
        if val_1 is None or val_2 is None:
            assert val_1 == val_2
        elif isinstance(field_type, dict):
            recursive_attribute_compare(val_1, val_2, field_type)
        else:
            assert val_1 == val_2


def recursive_container_compare(val_1, val_2):
    assert isinstance(val_1, type(val_2))
    if isinstance(val_1, (list, tuple)):
        assert len(val_1) == len(val_2)
        for elem_1, elem_2 in zip(val_1, val_2):
            recursive_container_compare(elem_1, elem_2)
    elif isinstance(val_1, dict):
        assert set(val_1) == set(val_2)
        for key in val_1:
            recursive_container_compare(val_1[key], val_2[key])
    elif isinstance(val_1, str):
        assert val_1 == val_2
