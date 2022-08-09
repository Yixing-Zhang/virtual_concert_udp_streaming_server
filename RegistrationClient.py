#! /usr/bin/env python
from socket import *
import threading
from time import sleep
from sys import argv
import getopt
import select


class RegistrationClient:
    """
    This class controls client.
    This is a singleton class.
    """

    __species = None
    __first_init = True

    # UDP Networking
    localHost = '127.0.0.1'
    remoteIP = "16.162.92.84"
    pktLen = 8192

    # Ports
    remotePort = 1235
    localInPort = 1236
    localOutPort = 1237
    clientPort = 14043

    # Sockets
    remoteSock = socket(AF_INET, SOCK_DGRAM)
    localSock = socket(AF_INET, SOCK_DGRAM)

    # Threads
    accessThread = None
    forwardThread = None

    # Flags
    terminated = False

    def __new__(cls, *args, **kwargs):
        if cls.__species is None:
            cls.__species = object.__new__(cls)
        return cls.__species

    def __init__(self, host='127.0.0.1', remoteIP="16.162.92.84", pktLen=8192, remotePort=1235, localInPort=1236,
                 localOutPort=1237, clientPort=14043):
        if self.__first_init:
            self.localHost = host
            self.remoteIP = remoteIP
            self.pktLen = pktLen

            self.remotePort = remotePort
            self.localInPort = localInPort
            self.localOutPort = localOutPort
            self.clientPort = clientPort

            self.remoteSock = socket(AF_INET, SOCK_DGRAM)
            self.remoteSock.bind((self.localHost, self.localInPort))

            self.localSock = socket(AF_INET, SOCK_DGRAM)
            self.localSock.bind((self.localHost, self.localOutPort))

            self.accessThread = threading.Thread(target=self.Access)
            self.forwardThread = threading.Thread(target=self.Forward)

            self.terminated = False

            self.__class__.__first_init = False

    def Start(self):
        print("Starting Registration Client...")
        self.accessThread.start()
        self.forwardThread.start()
        print("Registration Client Started...")

    def Forward(self):
        print("Start Forwarding...\n", end='')
        while not self.terminated:
            ready = select.select([self.remoteSock], [], [], 1.0)
            if ready[0]:
                data, addr = self.remoteSock.recvfrom(self.pktLen)
                print("Received data from", addr, ":", data, "\n", end='')
                self.localSock.sendto(data, (self.localHost, self.clientPort))
                print("Forwarded the data to", self.localHost, self.clientPort, "\n", end='')
        print("Forwarding Stopped...\n", end='')

    def Access(self):
        count = 0
        print("Start Accessing Forward Server...\n", end='')
        while not self.terminated:
            if count % 5 == 0:
                self.remoteSock.sendto("access".encode(), (self.remoteIP, self.remotePort))
                print("Access Forward Server...\n", end='')
            count += 1
            count %= 5
            sleep(1)
        print("Stop Accessing Forward Server...\n", end='')

    def Terminate(self):
        print("Terminating Registration Client....\n", end='')
        self.terminated = True
        self.accessThread.join()
        self.forwardThread.join()
        self.remoteSock.close()
        self.localSock.close()
        print("Registration Client Terminated....\n", end='')
