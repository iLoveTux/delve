from pony.orm import db_session, select

from delve.models import Event, Tag

def save(argv, results):
    with db_session:
        for result in results:
            event = select(e for e in Event if e.id == result["id"]).first()
            event.text = result["text"]
            event.extracted_fields = result["extracted_fields"]
            yield result

