from socket import *
import select
import threading
from time import sleep


class ForwardServer:
    """
    This class controls server.
    This is a singleton class.
    """

    __species = None
    __first_init = True

    # UDP Networking
    host = '0.0.0.0'
    TTL = 20
    pktLen = 2048

    # Ports
    inPort = 1234
    outPort = 1235

    # Sockets
    inSock = socket(AF_INET, SOCK_DGRAM)
    outSock = socket(AF_INET, SOCK_DGRAM)

    # Threads
    registrationThread = None
    forwardThread = None
    timerThread = None

    # Flags
    terminated = False

    # addresses pool
    addrList = {}

    def __new__(cls, *args, **kwargs):
        if cls.__species is None:
            cls.__species = object.__new__(cls)
        return cls.__species

    def __init__(self, host='0.0.0.0', TTL=20, pktLen=2048, inPort=1234, outPort=1235):
        if self.__first_init:
            self.host = host
            self.TTL = TTL
            self.pktLen = pktLen

            self.inPort = inPort
            self.outPort = outPort

            self.inSock = socket(AF_INET, SOCK_DGRAM)
            self.inSock.bind((self.host, self.inPort))

            self.outSock = socket(AF_INET, SOCK_DGRAM)
            self.outSock.bind((self.host, self.outPort))

            self.registrationThread = threading.Thread(target=self.AcceptRegistration)
            self.forwardThread = threading.Thread(target=self.Forward)
            self.timerThread = threading.Thread(target=self.Timer)

            self.terminated = False

            self.addrList = {}

            self.__class__.__first_init = False

    def Start(self):
        print("Starting Server...")
        self.registrationThread.start()
        self.forwardThread.start()
        self.timerThread.start()
        print("Server Started...")

    def Forward(self):
        print("Start Forwarding...\n", end='')
        while not self.terminated:
            ready = select.select([self.inSock], [], [], 1.0)
            if ready[0]:
                data, inAddr = self.inSock.recvfrom(self.pktLen)
                for addr in self.addrList.keys():
                    self.outSock.sendto(data, addr)
        print("Forward Stopped....\n", end='')

    def AcceptRegistration(self):
        print("Start Accepting Client Registration...\n", end='')
        while not self.terminated:
            ready = select.select([self.outSock], [], [], 1.0)
            if ready[0]:
                data, clientAddr = self.outSock.recvfrom(self.pktLen)
                self.AddAddrList(clientAddr)
        print("Stop Accepting Client Registration...\n", end='')

    def AddAddrList(self, addr):
        if addr not in self.addrList.keys():
            print("New Client Registered: ", addr, "\n", end='')
        self.addrList[addr] = 0

    def IncTime(self):
        self.addrList = {k: v + 1 for k, v in self.addrList.items()}

    def DelTimeOut(self):
        newAddrList = {k: v for k, v in self.addrList.items() if v <= self.TTL}
        # stat timeout addrlist
        diff = [k for k in self.addrList.keys() if k not in newAddrList.keys()]
        if len(diff) != 0:
            print("Client Timeout: ", diff, '\n', end='')
        self.addrList = newAddrList

    def Timer(self):
        print("Start Timer....\n", end='')
        count = 0
        while not self.terminated:
            if count % 5 == 0:
                print("Running....\n", end='')
            sleep(1)
            self.DelTimeOut()
            self.IncTime()
            count += 1
            count %= 5
        print("Timer Stopped....\n", end='')

    def Terminate(self):
        print("Terminating Server....\n", end='')
        self.terminated = True
        self.registrationThread.join()
        self.forwardThread.join()
        self.timerThread.join()
        self.inSock.close()
        self.outSock.close()
        print("Server Terminated....\n", end='')
