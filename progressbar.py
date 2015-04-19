#Progress Bar
import sys

class Progress:
    orig = "[----------]"

    def __init__(self, total):
        self.total = total
        self.completed = 0
        self._DrawProgress
        self.laststring = ""

    def Increment(self, sincelast = 1):
        self.completed += sincelast
        self._DrawProgress()

    def _DrawProgress(self):
        ratio = self.completed / float(self.total)
        percent = ratio*100 - ratio*100 % 1
        posS = percent % 10
        posB = (percent - percent % 10)/10
        posS, posB = int(posS), int(posB)
        newstring = self.orig[0] + posB*"X" + self.orig[posB + 1: 12]
        newstring += self.orig[0] + posS*"x" + self.orig[posS + 1: 12]
        self.laststring = newstring
        backs = "\b"*len(newstring)
        newstring = backs + newstring
        sys.stdout.write(newstring)
        sys.stdout.flush()

    def End(self):
        sys.stdout.write("\b"*len(self.laststring))
        sys.stdout.write(" "*len(self.laststring))
        sys.stdout.write("\b"*len(self.laststring))

