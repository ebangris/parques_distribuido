import sys
import zmq
import random
import os
"""
 una lista de diccionarios
players=[{
	"id": name
	"ip": ip:port 
	"c": colour (r,g,b,y)
	"pos":[0,0,0,0] # casilla de las fichas
}
]

posicion del tablero
 b g
 r y
"""
class Server:
	def __init__(self):
		port = "8001"
		self.players= [{},{},{},{}]
		context = zmq.Context()
		self.socket = context.socket(zmq.REP)
		self.socket.bind("tcp://*:"+port)
		print("Server of UltraParchis3000 is runing in port "+port)
		self.start_game()

	def start_game(self):
		init = [0,0,0,0] # 4 numeros de casilla de 4 fichas
		colours = ["r","g","b","y"]
		waiting = True # que esten los 4 jugadores o uno decida empezar la partida
		while waiting:
			k = 4 - len(colours)
			query = self.socket.recv_multipart()
			if query[0].decode() == "add player":
				turn = random.randrange(len(colours))
				player = eval(query[1].decode())

				print("\nnew player request : "+player.get("id"))
				colour = colours.pop(turn) # le asigna un color aleatorio y lo quita para que otro no lo tome
				player.update({"c":colour,"pos":init})
				self.players[k].update(player)
				self.socket.send(str({"c":colour,"pos":init}).encode())
				print("sending confirmation for play as "+colour)
				if len(colours) == 0:
					waiting = False
					print("List players empty ")
			if query[0].decode() == "start" :
				if k >= 2:
					waiting = False	
				else:

		print("Starting game now")
		#se determina quien juega primero, luego ira hacia la derecha
		max_score=0
		order_game=[]
		while True:
			query = self.socket.recv_multipart()
			if query[0].decode() == "add player": # ya no recibe mas jugadores
				self.socket.send(b"full")
			if query[0].decode() == "dice score": # el puntaje mas alto empieza el juego
				if query[2] > max_score:
					max_score = query[2]
					order_game[0]=query[1]


if __name__ == '__main__':
	board = Server()
