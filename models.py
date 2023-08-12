
import managers


class MetaModel(type):
    manager_class = managers.BaseManager

    def _get_manager_instance(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager_instance()


class BaseModel(metaclass=MetaModel):
    table_name = ""
    manager_class = managers.BaseManager

    def __init__(self, **row_data):
        for field_name, value in row_data.items():
            setattr(self, field_name, value)

    def __repr__(self):
        attrs_format = ", ".join([f'{field}={value}' for field, value in self.__dict__.items()])
        return f"<{self.__class__.__name__}: ({attrs_format})>"
