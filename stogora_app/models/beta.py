from stogora_app.models import client
import time

beta_collection = client.emails


class Beta():
  def __init__(self, email=None, time_posted=None):
    self.email = email
    self.time_posted = time_posted

  def save(self):
    email_to_check = {'email': self.email}
    if beta_collection.find(email_to_check).count() > 0:
      return self
    else:
      json_row = {
        'email': self.email,
        'time_posted': time.strftime("%c")
      }
      beta_collection.insert_one(json_row)
    return self
