import datetime
import random
import json

def _fake_cpu_readings():
    now = datetime.datetime.now() 
    for t in [now - datetime.timedelta(seconds=10 * x) for x in range(0, 100)]:
        yield json.dumps(
            {
                "cpu_usage": random.randint(0, 100),
                "host": random.choice(("uws01", "uws02")),
                "t": t.isoformat(),
            }
        )
fake_cpu_readings = _fake_cpu_readings()