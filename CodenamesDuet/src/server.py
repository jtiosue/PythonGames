import socket
from threading import Thread
from game import Game

if __name__ == "__main__":
    
    clients = []
    game = Game()
    new_game = [False, False]
    
    def recv(clientsocket, player):
        while True:
            # wait for message from any of the clients.
            msg = clientsocket.recv(1024)
            msg = msg.decode().strip()
            
            m, d = msg[0], msg[1:]
            if m in "29":
                for c in clients: c.send(msg.encode())
            elif m == "5": # new game code
                new_game[player-1] = True
                if all(new_game): 
                    game.new_game()
                    msg1 = "0" + str(game.get_game_info(1))
                    msg2 = "0" + str(game.get_game_info(2))
                    clients[0].send(msg1.encode())
                    clients[1].send(msg2.encode())
                    new_game[0], new_game[1] = False, False
                else:
                    for c in clients: c.send(m.encode())
            else:
                if m == "3": game.turn_complete()
                elif m == "4" and player == game.get_turn(): game.guess(d)
                
                msg = ("1" + str(game.get_update_info())).encode()
                for c in clients: c.send(msg)
                    
    
    
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    #port = 3001                 # Reserve a port for your service.
    port = int(input("Enter port: "))
    
    print ('Server started at [%s]' % socket.gethostbyname(host))
    print ('Waiting for clients...')
    
#    s.bind((host, port))        # Bind to the port
    s.bind((socket.gethostbyname(host), port))        # Bind to the port
#    s.bind(('0.0.0.0', port))
    s.listen(5)                 # Now wait for client connection.
    
    try:
        while True:
            #Waits until someone new to accept
            
            ### update this
            c, addr = s.accept()
            print(addr, "connected.")
            if len(clients) < 2:
                player = len(clients) + 1
                clients.append(c)
                thread_recv = Thread(target=recv, args=((c, player)))
                thread_recv.start()
                msg = "0" + str(game.get_game_info(player))
                c.send(msg.encode())
                player += 1
            else:
                print("Server already has two players")
    finally:
        s.close()