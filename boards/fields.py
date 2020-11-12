from django.db import models


class ListField(models.Field):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value

        return value.split(",")

    def to_python(self, value):
        if isinstance(value, list):
            return value

        if value is None:
            return value

        return value.split(",")

    def get_prep_value(self, value):
        if value is None:
            return None
        return ",".join(item for item in value)

    def value_to_string(self, obj):
        value = self.to_python(obj)
        return self.get_prep_value(value)

    def db_type(self, connection):
        return 'varchar(200)'
