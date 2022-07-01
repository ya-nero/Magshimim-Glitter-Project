import glitter
import socket

CHOICES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
SERVER_ADDRESS = ("44.224.228.136", 1336)

def welcome():
    print('Welcome to Yaniv\'s Glitter Project: Swissknife!')

def menu():
    print('''[1] Login without a password!
[2] Get the ascii checksum of a username!
[3] Get a password of a username!
[4] Get the id of a user!
[5] Change a font color of a glit!
[6] Send a friend request to yourself!
[7] Send a like request twice!
[8] Show all the commands  the server can do!
[9] Search for users with a search entry.
[10] Publish a wow to a glit.
[11] Quit.
Please choose one of the above: ''')

def main():
    welcome()

    while True:
        menu()

        # Get a choice from the user.
        while True:
            try:
                choice = int(input())

                # Check if the choice is invalid.
                if choice not in CHOICES:
                    raise ValueError("Invalid choice, please try again.")
                break
            # If an error was thrown, print it.
            except ValueError as error:
                print(error)
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(SERVER_ADDRESS)

            if choice == 1:
                username = str(input("Enter a username: "))
                print(glitter.glitterClientLogin(username, sock))
            elif choice == 2:
                username = str(input("Enter a username: "))
                print(glitter.usernameAsciiSum(username))
            elif choice == 3:
                username = str(input("Enter a username: "))
                code = str(input("Enter a code (DDMMcksmHHmm): "))
                print(glitter.passwordChallenge(username, code))
            elif choice == 4:
                username = str(input("Enter a username: "))
                print(glitter.getUserId(username, sock))
            elif choice == 5:
                username = str(input("Enter a username: "))
                glitter.changeFontColor(username, sock)
            elif choice == 6:
                username = str(input("Enter a username: "))
                glitter.sendFriendRequest(username, sock)
            elif choice == 7:
                username = str(input("Enter a username: "))
                glitID = str(input("Enter a GLITID: "))
                glitter.sendLikeTwice(username, sock, glitID)
            elif choice == 8:
                print(glitter.showAllCommands(sock))
            elif choice == 9:
                username = str(input("Enter a username: "))
                searchEntry = str(input("Enter a search entry: "))
                print(glitter.search(sock, searchEntry, username))
            elif choice == 10:
                username = str(input("Enter a username: "))
                glitID = str(input("Enter a GLITID: "))
                print(glitter.publish_wow(sock, username, glitID))
            elif choice == 11:
                print("Goodbye!")
                break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nThe user has interrupted the program.")
    except Exception as e:
        print("\nSomething went wrong:", e)