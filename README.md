# ICS 460 Chat Room Assignment

This assignmet is an online chat room application, composed of a client python script and a server python script. The client connections to the server, which then forwards messages of either publicy to all logged on users or to a user specified by the client. 


## Directory Structure And Files

The directory, named assignment_2, is composed of four files: the client program, named chatclient.py, the server program, named chatserver.py, a file to hold user login credentials, named users.csv, and a README file, named README.md. 


## Instructions To Run The Applications 

### Running The Server Script
To run the server application, enter the following in the linux terminal inside the assignment_2 directory:
>> python3 chatserver.py <port number>


### Running The Client Script
To run the client application, enter the following in the linux terminal inside the assignment_2 directory:
>> python3 chatclient.py <server name> <server port> <username>


## Instructions To Use The Application
To use the client application, the program will send the username you provided in the terminal to the server. You will receive a prompt to enter your password if your username is on file. If you are not registered, you will be prompted to create a password and your username and password will be saved for future logins. Once your login is created or verified, you will be provide a listing of options. To message everyone in the chat room, enter 'PM' for public message. For messaging a specific user, enter 'DM' for direct message. And to leave the chat room, enter 'EX' to exit the chat room and end the program. 
