from .models import (
    Event,
    Tag,
    db,
)

def bind_db(**kwargs):
    db.bind(**kwargs)
    db.generate_mapping(create_tables=True)