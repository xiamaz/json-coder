import datetime

from dataclasses import dataclass

import json
import json_coder

# Usage idea 1
@json_coder.jsonify("testclass")
class TestClass:
    def __init__(self, a: int):
        self.a = a

    def to_json(self):
        return {"a": self.a}

a = json.loads('{"__testclass__": {"a": 10}}')
print(a)  # should now be an object of testclass
print(json.dumps(a))

@json_coder.jsonify("testclassb")
class TestClassB:
    def __init__(self, a: int):
        self.a = a

    @property
    def json(self):
        return {"a": self.a}

b = TestClassB(20)
print(json.dumps(b))


# Usage idea 2
@json_coder.jsonify("testdataclass")
@dataclass
class TestDataClass:
    a: int


a = json.loads('{"__testdataclass__": {"a": 10}}')
print(a)  # should now be an object of testdataclass
print(json.dumps(a))

# Usage idea 3
json_coder.register("datetime", datetime.datetime, datetime.datetime.fromisoformat, datetime.datetime.isoformat)
d = json.loads('{"__datetime__": "2018-10-10"}')
print(d)
print(json.dumps(d))
