import unittest
import socket
import multiprocessing as mp
from mood.server import start_server


class TestServerCommands(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.proc = mp.Process(target=start_server, args=('localhost', 1337))
        self.proc.start()
        # Ждем запуска сервера
        self.client = socket.socket()
        self.client.connect(('localhost', 1337))

        self.client.send('test_player\n'.encode())
        print(self.client.recv(1024).decode())
        self.client.send('movemonsters off\n'.encode())
        print(self.client.recv(1024).decode())  

    @classmethod
    def tearDownClass(self):
        print('once')
        self.client.close()
        self.proc.terminate()

    def test_01_add_monster(self):
        self.client.send('addmon eyes 1 0 1000 0_0\n'.encode())
        response = self.client.recv(1024).decode()
        self.assertIn('Added monster eyes to (1, 0) saying 0_0', response)

    def test_02_move_to_monster(self):
        self.client.send('move 1 0\n'.encode())
        response = self.client.recv(1024).decode()
        assrt = 'Moved to (1, 0)\\n _____ \\n< 0_0 >\\n ----- \\n    \\\\n     \\\\n                                   .::!!!!!!!:.\\n  .!!!!!:.                        .:!!!!!!!!!!!!\\n  ~~~~!!!!!!.                 .:!!!!!!!!!UWWW$$$ \\n      :$$NWX!!:           .:!!!!!!XUWW$$$$$$$$$P \\n      $$$$$##WX!:      .<!!!!UW$$$$"  $$$$$$$$# \\n      $$$$$  $$$UX   :!!UW$$$$$$$$$   4$$$$$* \\n      ^$$$B  $$$$\\     $$$$$$$$$$$$   d$$R" \\n        "*$bd$$$$      \'*$$$$$$$$$$$o+#" \\n             """"          """"""" \n'
        self.assertIn(assrt, response)

    def test_03_attack_monster(self):
        self.client.send('attack eyes 15\n'.encode())
        response = self.client.recv(1024).decode()
        self.assertIn('Attacked eyes,  damage 15 hp\\neyes now has 985\n', response)
