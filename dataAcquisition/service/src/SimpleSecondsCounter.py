import time
class SecondCounter():
    def __init__(self):
        self.__firstInterval = None
        self.__counting = False

    def isCounting(self):
        return self.__counting

    def startCount(self):
        self.__firstInterval = time.time()
        self.__counting = True

    def finishCount(self, condition=2):
        if self.__counting:
            self.__counting = False
            # print("Count ", self.__firstInterval - time.time())
            return time.time() - self.__firstInterval >= condition
        return False

    def finished(self, condition=2):
        if self.__counting:
            # self.__counting = False
            # print("Count ", self.__firstInterval - time.time())
            return time.time() - self.__firstInterval >= condition
        return False
