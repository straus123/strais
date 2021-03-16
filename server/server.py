import socket
import re
import selectors


class StraisServer:
    def __init__(self, host='', port=9999, db=None):
        self.sel = selectors.DefaultSelector()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))
        self.s.listen()
        self.db = db
        self.s.setblocking(False)
        print(f"Listen {host}:{port}")

    def register(self):
        self.sel.register(self.s, selectors.EVENT_READ, self.accept)

    def read(self, conn, mask) -> None:
        data = conn.recv(1024)  # Should be ready
        if data:
            action, key, value = self.split_input_data(data)
            if action == "get":
                conn.sendall(self.db.get(key))
            elif action == "set":
                if self.db.set(key, value):
                    conn.sendall(b"OK")
                else:
                    conn.sendall(b"Error while setting data")
            elif action == "error":
                conn.sendall(value.encode())
            else:
                conn.sendall(b"Unhandled error")
        else:
            print('closing', conn)
            self.sel.unregister(conn)
            conn.close()

    def accept(self, sock, mask) -> None:
        conn, addr = sock.accept()  # Should be ready
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read)

    def split_input_data(self, data: bytes) -> tuple:
        """
        Split raw socket input into tuple.
        ex:
            b'get key' -> ('get', key', '')
            b'set key some value' -> ('set', 'key', 'some value')
            b'blalbalba' -> ('error', "error text', '')
        :param data:
        :return: (action:str, key:str, [value:str])
        """
        data_decoded = data.decode()
        m = re.match(r"(\w+)\s(\w+)\s*(.*)", data_decoded)
        if m is None:
            return "error", "value", f"Error while split data_decoded {data_decoded}"
        else:
            return m.group(1, 2, 3)

    def serve(self):
        while True:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)



