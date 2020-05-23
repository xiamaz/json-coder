import json
from dataclasses import is_dataclass, asdict

def normalize_key(key):
    if not key.startswith("__"):
        key = f"__{key}__"
    key = key.lower()
    return key

def normalize(fun):
    def wrapper(self, key, *args, **kwargs):
        key = normalize_key(key)
        return fun(self, key, *args, **kwargs)
    return wrapper


class ObjectRegister:
    _key_serializer_pairs = {}
    _key_deserializer_pairs = {}
    _type_key_pairs = {}

    def get_object_key(self, obj):
        obj_type = type(obj)
        for reg_type, reg_key in self._type_key_pairs.items():
            if obj_type is reg_type:
                return reg_key
        return None

    def register_type(self, key, reg_type, init_fun, dump_fun):
        if key in self._key_deserializer_pairs:
            raise KeyError(f"{key} already exists.")
        if reg_type in self._type_key_pairs:
            raise KeyError(f"{type} already exists. Registered as {self._type_key_pairs[reg_type]}")
        self._key_deserializer_pairs[key] = init_fun
        self._key_serializer_pairs[key] = dump_fun
        self._type_key_pairs[reg_type] = key

    @normalize
    def get_deserializer(self, key):
        return self._key_deserializer_pairs[key]

    @normalize
    def get_serializer(self, key):
        return self._key_serializer_pairs[key]

    @normalize
    def __setitem__(self, key, val):
        init_fun = find_init(val)
        dump_fun = find_dump(val)
        self.register_type(key, val, init_fun, dump_fun)

    def __iter__(self):
        return iter(self._key_serializer_pairs.keys())


_OBJ_REGISTER = ObjectRegister()


class ObjectEncoder(json.JSONEncoder):

    def default(self, o):  # pylint: disable=E0202
        obj_key = _OBJ_REGISTER.get_object_key(o)
        if obj_key is not None:
            return {obj_key: _OBJ_REGISTER.get_serializer(obj_key)(o)}
        return json.JSONEncoder.default(self, o)


def _object_hook(dct):
    for key in _OBJ_REGISTER:
        if key in dct:
            obj_data = dct[key]
            if type(obj_data) is dict:
                return _OBJ_REGISTER.get_deserializer(key)(**obj_data)
            else:
                return _OBJ_REGISTER.get_deserializer(key)(obj_data)
    return dct


def jsonify_loads(s):
    return _json_loads(s, object_hook=_object_hook)


def jsonify_load(s):
    return _json_load(s, object_hook=_object_hook)


def jsonify_dumps(o):
    return _json_dumps(o, cls=ObjectEncoder)


def jsonify_dump(o, fp):
    return _json_dump(o, fp, cls=ObjectEncoder)


def find_init(cls):
    """Find proper init function for the given class."""
    cls_attrs = dir(cls)
    if "from_json" in cls_attrs:
        return getattr(cls, "from_json")
    return cls  # use default constructor if nothing else found


def find_dump(cls):
    """Find the proper dump function for given class."""
    cls_attrs = dir(cls)
    if "to_json" in cls_attrs:
        return cls.to_json
    if "json" in cls_attrs:
        return lambda o: o.json
    if is_dataclass(cls):
        return asdict
    raise ValueError(f"Cannot find a dumper method for {cls}")


def jsonify(key: str):
    def clswrapper(cls):
        _OBJ_REGISTER[key] = cls
        return cls
    return clswrapper



def register(key: str, rtype: "type", init_fun: "Callable", dump_fun: "Callable"):
    key = normalize_key(key)
    _OBJ_REGISTER.register_type(key, rtype, init_fun, dump_fun)


_json_loads = json.loads
_json_dumps = json.dumps
_json_dump = json.dump
_json_load = json.load
json.loads = jsonify_loads
json.dumps = jsonify_dumps
json.load = jsonify_load
json.dump = jsonify_dump
