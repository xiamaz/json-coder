# json-coder: Quickly serialize and deserialize python to json objects

The default library python `json` module supports custom decoders and encoders
allowing for saving and restoring custom objects into json. In comparison to
pickling objects, this is more portable and easier to manually edit.

This library supports the following use-cases:

- Class with json loading and dumping functions
  (define `.json` property or `.to_json()` method for dumping, define
  `.from_json()` constructor or proper init for reading)

- python `dataclass` classes

- custom loading and dumping functions for classes defined elsewhere

Fundamentally classes are assigned an identifier and json objects of the
following structure are created:

```
{
    '__<identifier>__': <object data>
}
```

## Usage examples

Custom class using predefined schema:

```
import json
import json_coder

@json.jsonify("testclass")
class TestClass:
    def __init__(self, a: int):
        self.a = a

    def to_json(self):
        return {"a": self.a}


# Usage
a = json.loads('{"__testclass__": {"a": 10}}')

print(a)
# <__main__.TestClass object at 0x10eb26810>

print(json.dumps(a))
# {"__testclass__": {"a": 10}}
```

Dataclasses do not require any additional methods to work properly.

```
from dataclasses import dataclass
import json
import json_coder

@json_coder.jsonify("testdataclass")
@dataclass
class TestDataClass:
    a: int


a = json.loads('{"__testdataclass__": {"a": 10}}')
print(type(a))  # should now be an object of testdataclass
print(json.dumps(a))
```

Custom dumper and reading functions can also be added to existing classes by
registering manually:

```
import datetime
import json
import json_coder

json_coder.register("datetime", datetime.datetime, datetime.datetime.fromisoformat, datetime.datetime.isoformat)
d = json.loads('{"__datetime__": "2018-10-10"}')
print(d)
print(json.dumps(d))
```
