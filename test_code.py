#!/usr/bin/env python

from models import storage
from models.state import State

storage.reload()
new_state = State(name="California")
new_state.save()

all_states = storage.all(State)
print(all_states)