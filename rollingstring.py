class RollingString:
    def __init__(self, rsize : int):
        self.rsize = rsize

        self.__head = 0
        self.__tail = -rsize
        self.__data = [""]*rsize

    def isfull(self) -> bool:
        return self.__tail >= 0
    
    def add(self, char : str):
        self.__data[self.__head] = char
        self.__head += 1
        self.__head %= self.rsize
        self.__tail += 1
        if self.__tail >= 0:
            self.__tail %= self.rsize

    def getStr(self) -> str:

        tail = self.__tail
        count = self.rsize
        if tail < 0:
            tail = 0
            count = self.__head

        out = []

        for i in range(tail, tail+count):
            i %= self.rsize
            out.append(self.__data[i])
        

        return "".join(out)

if __name__ == "__main__":
    A = RollingString(3)

    for i in range(10):
        A.add(str(i))
        A.getStr()
        print(A.getStr())