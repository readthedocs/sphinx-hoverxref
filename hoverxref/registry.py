class HoverXRefObjectTypeRegistry:
    """
    Registry of user-defined object types.

    Using this registry automatically consider the object to be rendered with a
    tooltip with the content of the linked section.
    """

    object_types = []

    def add_object_type(self, name):
        self.object_types.append(name)


registry = HoverXRefObjectTypeRegistry()
