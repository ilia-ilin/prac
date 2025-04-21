import unittest
import socket
import multiprocessing as mp
from mood.server import start_server


class TestServerCommands(unittest.TestCase):
    def setUp(self):
        self.proc = mp.Process(target=start_server, args=('localhost', 1337))
        self.proc.start()
        # Ждем запуска сервера
        self.client = socket.socket()
        self.client.connect(('localhost', 1337))

        self.client.send(b'movemonsters off\n')
        _ = self.client.recv(1024).decode()

    def tearDown(self):
        self.client.close()
        self.proc.terminate()

    def test_add_monster(self):
        self.client.send(b'addmon eyes coords 1 0 hello 0_0 hp 1000\n')
        response = self.client.recv(1024).decode()
        self.assertIn('Added monster eyes to (1, 0) saying 0_0', response)

    def test_move_to_monster(self):
        self.client.send(b'right\n')
        response = self.client.recv(1024).decode()

        assrt = '''
Moved to (1, 0)
 _____
< 0_0 >
 -----
    \\
     \\
                                   .::!!!!!!!:.
  .!!!!!:.                        .:!!!!!!!!!!!!
  ~~~~!!!!!!.                 .:!!!!!!!!!UWWW$$$
      :$$NWX!!:           .:!!!!!!XUWW$$$$$$$$$P
      $$$$$##WX!:      .<!!!!UW$$$$"  $$$$$$$$#
      $$$$$  $$$UX   :!!UW$$$$$$$$$   4$$$$$*
      ^$$$B  $$$$\\     $$$$$$$$$$$$   d$$R"
        "*$bd$$$$      '*$$$$$$$$$$$o+#"
             """"          """""""
'''
        self.assertIn(assrt, response)

    def test_attack_monster(self):
        self.client.send(b'attack sword\n')
        response = self.client.recv(1024).decode()
        self.assertRegex('Attacked eyes,  damage 15 hp\neyes now has 985', response)
