import socket
import threading

HOST = '0.0.0.0' 
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

waiting_players = []
active_games = {}

def handle_client(client_socket, player_id):
    global waiting_players
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data: break
            if player_id in active_games:
                opponent = active_games[player_id]
                opponent.send(data.encode('utf-8'))
    except: pass
    finally:
        if client_socket in waiting_players: waiting_players.remove(client_socket)
        if player_id in active_games:
            opp = active_games[player_id]
            try: opp.send("RAKIP_CIKTI".encode('utf-8'))
            except: pass
            del active_games[player_id]
        client_socket.close()

def matchmaker():
    global waiting_players
    print("Sunucu aktif...")
    while True:
        client, addr = server.accept()
        waiting_players.append(client)
        client.send("BAGLANDI".encode('utf-8'))
        if len(waiting_players) >= 2:
            p1 = waiting_players.pop(0)
            p2 = waiting_players.pop(0)
            active_games[p1] = p2
            active_games[p2] = p1
            p1.send("BASLA:X".encode('utf-8'))
            p2.send("BASLA:O".encode('utf-8'))
            threading.Thread(target=handle_client, args=(p1, p1)).start()
            threading.Thread(target=handle_client, args=(p2, p2)).start()

if __name__ == "__main__":
    matchmaker()
