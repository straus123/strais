class DataBase:
    def __init__(self):
        self.global_data = {}

    def set(self, key:str, value:str) -> bool:
        self.global_data[key] = value
        return True

    def get(self, key:str) -> bytes:
        if key in self.global_data:
            return self.global_data[key].encode()
        else:
            return f"Key not found {key}".encode()