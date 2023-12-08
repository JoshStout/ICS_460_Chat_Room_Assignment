#!/usr/bin/env python3

""""
Client side python script for an online chat room application. The application makes a 
connection to the server specified in the command line argument. 

To run, type in the terminal the following:
>> python3 chatlient.py <server name> <server port number> <username> 

"""

import sys, socket, threading, time

HOST = sys.argv[1] # localhost in this assignment
PORT = int(sys.argv[2]) # port number of the server 
USERNAME = sys.argv[3] # username for sign-in

# handle input from server 
# thread to accept messages from server
def handle_input(sock):
	while True:
		try:
			message = sock.recv(1024).decode()
			print(message)
		except:
			print('Error. Disconnecting...')
			threading.Threadd.join(thread)
			
# handle output to server 
# function to send messages to the server 
def handle_output(sock):
	while True:
		msg = input()
		try:				
			sock.send(msg.encode())		
		except:
			pass
		if msg == 'EX':
			print('Disconnecting...')
			ex_mode(sock)

# helper function to close sockets 
def ex_mode(sock):
	sock.close()
	sys.exit(0)

# main thread
# creates connection to server
def main():
	
	# start connection with server 
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((HOST, PORT))
	except socket.error as e:
		print(e)
		sys.exit(1)
	
	# start thread to handle input from server 
	thread = threading.Thread(target=handle_input,args=[sock],daemon=True)
	thread.start()
	
	# send username to server 
	sock.send(USERNAME.encode())
	
	# read user input and send to server 
	handle_output(sock)
	
if __name__ == '__main__':
	main() 

