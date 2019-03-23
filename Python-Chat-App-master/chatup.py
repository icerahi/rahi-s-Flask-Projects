from flask import Flask, render_template
from flask_socketio import SocketIO, emit

 

app = Flask(__name__)

app.config[ 'SECRET_KEY' ] = 'jsbcfsbfjefebw237u3gdbdc'
socketio = SocketIO( app )
user="rahi"
@app.route( '/')
def hello():
  return render_template( './ChatApp.html' ,user=user)

def messageRecived():
  print( 'message was received!!!' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) )
  socketio.emit( 'my response', json, callback=messageRecived )

if __name__ == '__main__':
  socketio.run( app, debug = True )
