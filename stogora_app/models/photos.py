from stogora_app.models import client, conn, db
from boto.s3.key import Key

class Photos():
  def __init__(self, main=None, alternates=None):
    self.main = main
    self.alternates = alternates

  @staticmethod
  def make_user_folder(user_email):
    bucket = conn.get_bucket('stogoraphotos')
    key = bucket.new_key('/' + user_email + '/')
    key.set_contents_from_string('')

  @staticmethod
  def upload_listing_photo(file_name,buffer,user_email):
    """
      Upload image to s3 via a string buffer
    """
    bucket = conn.get_bucket('stogoraphotos')
    k = Key(bucket)
    k.key = '/' + str(user_email)
    k.name = '/'+ str(user_email)+ '/'+ file_name
    k.set_contents_from_string(buffer.getvalue(), headers={"Content-Type": "image/jpeg"})
    k.make_public()
    url = k.generate_url(expires_in=0, query_auth=False)
    return url

