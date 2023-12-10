#!/usr/bin/env python3

""""
Server python script for online chat room application. The program listens for connections 
on the port specified in the command line argument when running the program. 

To run, type in the terminal the following: 
>> python3 chatserver.py <port number> 

"""

from socket import *
import sys, threading, os, csv

users = [] # list to hold user objects
PORT = int(sys.argv[1]) # port number for the server to listen to for connections

# each user is an object
class User:
	def __init__(self, username, password, socket):
		self._username = username
		self._password = password
		self._socket = socket
		
	def get_username(self):
		return self._username
	
	def get_password(self):
		return self._password
	
	def get_socket(self):
		return self._socket
	
	def set_socket(self, socket):
		self._socket = socket

# store users to a file
def add_user_to_file(new_user):
	with open('users.csv', 'a') as csv_file:
		csv_writer = csv.writer(csv_file)
		user_list = [new_user.get_username(), new_user.get_password()]
		csv_writer.writerow(user_list)
		csv_file.close()
		
# retreive users from file
def get_users_from_file():
	with open('users.csv', 'r') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			users.append(User(row[0], row[1], None))
		csv_file.close() 

# validate usernames and passwords
# returns true if username and password are correct 	
def login(username, password):
	for user in users:
		if (user.get_username() == username) and (user.get_password() == password):
			return True
	return False 

# funtion to prompt for and validate password
# returns true if username and password are correct 
def loginClient(connection_socket, username):
	message = 'Enter password' 
	connection_socket.send(message.encode())
	password = connection_socket.recv(1024).decode()
	if login(username, password):
		user_obj = get_obj_from_username(username)
		user_obj.set_socket(connection_socket)
		return True
	return False

# helper function to return user object
def get_obj_from_username(username):
	for user in users:
		if user.get_username() == username:
			return user

# function to add a new user
# returns true if successful 
def register_user(connection_socket, username):
	message = 'Create a password'
	connection_socket.send(message.encode())
	password = (connection_socket.recv(1024).decode())
	new_user = User(username, password, connection_socket)
	users.append(new_user)
	add_user_to_file(new_user)
	return True

# function to send messages to each user
def send_pm(this_user, message):
	message = '\nPM from ' + this_user + ': ' + message 
	for user in users:
		if user.get_socket():
			user.get_socket().send(message.encode())

# function to send message to specified user 
def send_dm(this_user, message, username):
	message = '\nDM from ' + this_user + ': ' + message 
	user_obj = get_obj_from_username(username)
	user_obj.get_socket().send(message.encode())

# function to check if user is logged in
# returns true if user is logged in on the chat program
def user_online(username):
	for user in users:
		if (user.get_socket() is not None) and (user.get_username() == username):
			return True
	return False

# function to return a string of all logged in users
def logged_in_users_tostring():
	logged_in = ''
	for user in users:
		if user.get_socket() is not None:
			logged_in += user.get_username()
			logged_in += '\n'
	return logged_in 

# function to close user socket
def close_socket(connection_socket):
	get_user_obj_from_socket(connection_socket).set_socket(None)
	connection_socket.close()

# function to return user object from socket connection 
def get_user_obj_from_socket(connection_socket):
	for user in users:
		if user.get_socket() == connection_socket:
			return user
	return None

# function to check if username is on file
# returns true if username is on file
def check_if_user_on_file(username):
	for user in users:
		if user.get_username() == username:
			return True
	return False

# function to send public message
def pm_mode(connection_socket, this_username):
	message = '\n--Public Message Mode--\nEnter message:'
	connection_socket.send(message.encode())
	message = connection_socket.recv(1024).decode()
	send_pm(this_username, message)		

# function to send direct message to another user
def dm_mode(connection_socket, this_username):
	message = '\n--Direct Message Mode--\n'
	message += 'List of currently logged in users:\n'
	connection_socket.send(message.encode())
	message = logged_in_users_tostring()
	connection_socket.send(message.encode())
	message = '\nEnter username of user you want to message:'
	connection_socket.send(message.encode())
	selected_user = connection_socket.recv(1024).decode()
	if user_online(selected_user):
		message = '\nEnter message for ' + selected_user + ':'
		connection_socket.send(message.encode())
		message = connection_socket.recv(1024).decode()
		send_dm(this_username, message, selected_user)
		message = '\nMessage sent.'
		connection_socket.send(message.encode())
	else:
		message = 'User not online.'
		connection_socket.send(message.encode())

# function for user to disconnect connection 
def ex_mode(connection_socket, this_username):
	message = 'EX'
	connection_socket.send(message.encode())
	print('Closing connection for ' + this_username + ' from ' + str(connection_socket.getpeername()))
	close_socket(connection_socket)	

# function to select which command mode 
def command_mode(connection_socket):
	while True:
		try:
			message = '\n\n'
			message += 'Enter PM for Public Message\n'
			message += 'Enter DM for Direct Message\n'
			message += 'Enter EX to exit chat room'
			connection_socket.send(message.encode())
			
			this_username = get_user_obj_from_socket(connection_socket).get_username()
			mode = connection_socket.recv(1024).decode()
			
			match mode:
				case 'PM':
					pm_mode(connection_socket, this_username)
				case 'DM':
					dm_mode(connection_socket, this_username)
				case 'EX':
					ex_mode(connection_socket, this_username)
		except: 
			pass

# thread to handle the client socket 
def handle_request(connection_socket):
	try:
		username = connection_socket.recv(1024).decode() # 1024 is the max amt of data to be received
		print('User ' + username + ' connecting from ' + str(connection_socket.getpeername()))
		
		if check_if_user_on_file(username):
			status = loginClient(connection_socket, username)
		else:
			message = 'Username not on file. Register as new user: \n'
			connection_socket.send(message.encode())
			status = register_user(connection_socket, username)
				
		if status:
			message = '\nWelcome ' + username
			connection_socket.send(message.encode())
		else:
			message = 'Login failed. Closing connection'
			connection_socket.send(message.encode())
			connection_socket.close()
			
		command_mode(connection_socket)
		    
	except:
		messsage = 'An Error Occured. Closing Connection.'
		connection_socket.send(message.encode())
		connection_socket.close()
		print('closed connection for:')
		print(connection_socket)

# main thread to accept socket connections 
def main():
	get_users_from_file()
	
	server_socket = socket(AF_INET, SOCK_STREAM)
	
	# Allow address reuse for crashes 
	server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
    	# Bind to an address and port
	server_socket.bind(('', PORT))

    	# Listen for incoming connections
	server_socket.listen()
	print('Waiting for users to connect...')
	
	# create threads from socket connections 
	while True:
		connection_socket, addr = server_socket.accept()
		thread = threading.Thread(target=handle_request, args=(connection_socket,),daemon=True)
		thread.start()

	server_socket.close()
	sys.exit()  # Terminate the program

if __name__ == "__main__":
	main()
