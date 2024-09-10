def add_set_cls_attr(cls):
    @classmethod
    def set_cls_attr(cls, attr: str, value):
        if hasattr(cls, attr):
            setattr(cls, attr, value)
        else:
            raise ValueError(f"Attribute {attr} does not exist in class {cls.__name__}.")
    
    cls.set_cls_attr = set_cls_attr
    x = 1
    return cls


# 使用示例
@add_set_cls_attr
class MyClass:
    class_attr = 10

print(MyClass.class_attr)
# 测试
MyClass.set_cls_attr('class_attr', 20)
print(MyClass.class_attr)  # 输出 20

x = 21
y = [1, 2]
y.append(x)

