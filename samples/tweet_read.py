import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''


class TweetsListener(StreamListener):

  def __init__(self, csocket):
      self.client_socket = csocket
      self.counter = 0

  def on_data(self, data):
      try:
          msg = json.loads( data )
          print("\n#############################################################################")
          self.counter += 1
          #print(msg['text'].encode('utf-8') )
          msg_to_send = ( str(self.counter) + " :  " + msg['text'] + " $$$$$$ ").encode('utf-8')
          print(msg_to_send)
          #msg_to_send = msg_to_send.replace("\n", " ").encode('utf-8')
        #   print(msg_to_send)
          self.client_socket.send(msg_to_send)
          return True
      except BaseException as e:
          print("Error on_data: %s" % str(e))
      return True

  def on_error(self, status):
      print(status)
      return True

def sendData(c_socket):
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)

  twitter_stream = Stream(auth, TweetsListener(c_socket))
  twitter_stream.filter(languages=["en"],track=['ipl'])

if __name__ == "__main__":
  s = socket.socket()         # Create a socket object
  host = "192.168.0.100"      # Get local machine name
  port = 5556              # Reserve a port for your service.
  s.bind((host, port))        # Bind to the port

  print("Listening on port: %s" % str(port))

  s.listen(5)                 # Now wait for client connection.
  c, addr = s.accept()        # Establish connection with client.

  print( "Received request from: " + str( addr ) )

  sendData( c )