import datetime

from dataclasses import dataclass

import json
import jsonify

# Usage idea 1
@jsonify.jsonify("testclass")
class TestClass:
    def __init__(self, a: int):
        self.a = a

    def to_json(self):
        return {"a": self.a}

a = json.loads('{"__testclass__": {"a": 10}}')
print(a)  # should now be an object of testclass
print(json.dumps(a))

@jsonify.jsonify("testclassb")
class TestClassB:
    def __init__(self, a: int):
        self.a = a

    @property
    def json(self):
        return {"a": self.a}

b = TestClassB(20)
print(json.dumps(b))


# Usage idea 2
@jsonify.jsonify("testdataclass")
@dataclass
class TestDataClass:
    a: int


a = json.loads('{"__testdataclass__": {"a": 10}}')
print(a)  # should now be an object of testdataclass
print(json.dumps(a))

# Usage idea 3
jsonify.register("datetime", datetime.datetime, datetime.datetime.fromisoformat, datetime.datetime.isoformat)
d = json.loads('{"__datetime__": "2018-10-10"}')
print(d)
print(json.dumps(d))
