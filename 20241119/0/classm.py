class Sender:
    isfst = True

    @classmethod
    def report(self):
        if self.isfst:
            print("Greetings!")
            self.isfst = False
        else:
            print("Get away!")

class Asker:
    @staticmethod
    def askall(lst):
        for i in lst:
            i.report()
