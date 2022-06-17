from abc import ABC, abstractmethod


class Util(ABC):

    @staticmethod
    def get_file_content_str(filename):
        with open(f"{filename}") as f:
            out = f.read()
        return out


class MUC(ABC):

    @staticmethod
    def on_model(m):
        print("GOT MODEL")
        print(type(m), m)

    @staticmethod
    def on_core(c):
        print("GOT UNSATISFIABLE CORE")
        print(type(c), c)
        if isinstance(c, list):
            for assumption in c:
                print(f"---{type(assumption)} : {assumption}")

    @staticmethod
    @abstractmethod
    def get_muc(c):
        pass


class MUCSimple(MUC):

    @staticmethod
    def get_muc(c):
        print(c)