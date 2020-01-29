from typing import List

from google.cloud import ndb


class EmailMessage(ndb.Model):
    sender = ndb.StringProperty()
    message_id = ndb.StringProperty(indexed=True)
    files = ndb.StringProperty(repeated=True)

    @classmethod
    def make_record(cls, sender: str, message_id: str, files: List[str]):
        obj = cls(sender=sender, message_id=message_id, files=files)
        obj.put()
