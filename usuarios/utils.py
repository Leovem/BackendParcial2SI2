
def update_nested_serializer(serializer_class, instance_field, instance, data_field_name):
    data = instance.initial_data.get(data_field_name)
    if data:
        nested_instance = getattr(instance.instance, instance_field)
        serializer = serializer_class(instance=nested_instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
