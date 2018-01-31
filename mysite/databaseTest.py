from RSVP.models import *
from django.utils import timezone
p = People (username = "yououhan", name = "Ouhan You");
p.save()
e = Event(event_name = "wedding", creator = p, create_time = timezone.now(), last_updated_time = timezone.now())
e.save()
