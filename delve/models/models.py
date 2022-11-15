from datetime import datetime
import uuid

from pony.orm import (
    Database,
    Required,
    Optional,
    PrimaryKey,
    Set,
    Json,
)

db = Database()

class Event(db.Entity):
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    raw = Required(str)
    created = Required(datetime, default=datetime.now)
    modified = Required(datetime, volatile=True, sql_default='CURRENT_TIMESTAMP')

    index = Required(str)
    host = Required(str)
    source = Required(str)
    sourcetype = Required(str)

    text = Optional(str)
    extracted_fields = Optional(Json)

    tags = Set("Tag")

class Tag(db.Entity):
    name = PrimaryKey(str)
    
    events = Set(Event)