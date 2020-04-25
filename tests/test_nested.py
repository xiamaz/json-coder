import datetime
import json
import json_coder


@json_coder.jsonify("testclass")
class TestClass:
    def __init__(self, date):
        self.date = date

    def to_json(self):
        return {"date": self.date}

json_coder.register("datetime", datetime.datetime, datetime.datetime.fromisoformat, datetime.datetime.isoformat)


a = TestClass(datetime.datetime.now())
print(a)

print(type(json.loads(json.dumps(a)).date))
