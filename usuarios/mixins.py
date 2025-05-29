class NestedUpdateMixin:
    def update_nested_serializer(self, serializer_class, instance_field, parent_instance, validated_data, data_field_name):
        nested_data = validated_data.pop(data_field_name, None)
        if nested_data:
            nested_instance = getattr(parent_instance, instance_field)
            serializer = serializer_class(instance=nested_instance, data=nested_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
