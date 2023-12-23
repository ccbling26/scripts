"""通过 metaclass 修改类定义，实现 ORM (Object Relational Mapping) 框架 (示例)"""

# 定义 Filed 类, 负责保存数据库表的字段名和字段类型
from typing import Any


class Field(object):
    def __init__(self, name, column_type) -> None:
        self.name = name
        self.column_type = column_type
    
    def __str__(self):
        return "<%s:%s>" % (self.__class__.__name__, self.name)

# 在 Filed 的基础上实现各种类型的 Filed, 如 StringField, IntegerField
class StringField(Field):
    def __init__(self, name) -> None:
        super(StringField, self).__init__(name, "varchar(100)")

class IntegerField(Field):
    def __init__(self, name) -> None:
        super(IntegerField, self).__init__(name, "bigint")

# 编写 Model 元类
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name != "Model":
            print("Found Model: %s" % name)
            mappings = dict()
            for k, v in attrs.items():
                if isinstance(v, Field):
                    print("Found mapping %s ==> %s" % (k, v))
                    mappings[k] = v
            for k in mappings.keys():
                attrs.pop(k)
            attrs["__mappings__"] = mappings
            attrs["__table__"] = name
        return type.__new__(cls, name, bases, attrs)

# 编写 Model 基类
class Model(object, metaclass=ModelMetaclass):
    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value
    
    def save(self):
        fields, params, args = [], [], []
        for k, v in self.__mappings__.items():
            fields.append(v.name)
            params.append("?")
            args.append(getattr(self, k, None))
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (self.__table__, ",".join(fields), ",".join(params))
        print("SQL: %s" % sql)
        print("ARGS: %s" % str(args))

