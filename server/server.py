import socket
import re
import selectors


class StraisServer:
    def __init__(self, host='', port=9999, db=None):
        self.sel = selectors.DefaultSelector()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()
        self.db = db
        self.socket.setblocking(False)
        print(f"Listen {host}:{port}")
        self._action_map={
            "get": self._get,
            "set": self._set
        }


    def exec_action(self, action:str):
        """
        exec function based on action_map dict, if action was not found return exec unhandled_action

        :param action:
        :return:
            function to exec
        example:
        exec_action('get') -> _get
        exec_action('unhandled') -> _unhandled_action
        """
        return self._action_map.get(action, self._unhandled_action)

    def _get(self, action, key, value) -> str:
        """
        get data action
        :param
            action: str,
            key: str,
            value: str
        :return:
            string
        """
        return self.db.get(key)

    def _set(self, action, key, value) -> bytes:
        """
        wrapper for set action
        :param
            action: str,
            key: str,
            value: str
        :return:
            string(ok or error)
        """
        if self.db.set(key, value):
            return b"Ok"
        else:
            return b"Error while setting data"


    def _unhandled_action(self, action, key, value) -> bytes:
        return f"Cant perform action={action}".encode()



    def register(self):
        self.sel.register(self.socket, selectors.EVENT_READ, self.accept)

    def read(self, conn, mask) -> None:
        data = conn.recv(1024)  # Should be ready
        if data:
            action, key, value = self.split_input_data(data)
            action_func = self.exec_action(action)
            conn.sendall(action_func(action=action, key=key, value=value))
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



