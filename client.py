import sys
import zmq
import random
import json
import os

class Client:
	def __init__(self):
		# python3 client.py nombre ip:puerto  
		self.player={"id":sys.argv[1],"ip":sys.argv[2]}

		context = zmq.Context()
		self.socket = context.socket(zmq.REQ)
		self.socket.connect("tcp://"+self.player.get("ip"))
		conected = False
		print("connecting to server...\n")
		self.socket.send_multipart([b"add player",str(self.player).encode()])
		response = self.socket.recv()
		if response.decode() == "full":
			print("game full, can't play :(")
			exit()
		print("Let's start ")
		self.stats = eval(response.decode())
		self.player.update(self.stats)
		x = input("Dice score :") # escrito por teclado para pruebas
		#x = random.randrange(12) # aleatorio para dados 
		self.dice_score(str(x))


	def dice_score(self, score):
		self.socket.send_multipart([b"dice_score",str(self.player.get("c")).encode(),score.encode()])
		print("score sended")
if __name__ == '__main__':
	client = Client()
	