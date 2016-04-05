import Tkinter as tk
from features import mfcc
from features import logfbank
import scipy.io.wavfile as wav
import os
import math
class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # create a prompt, an input box, an output label,
        # and a button to do the computation
        self.prompt = tk.Label(self, text="Enter a number:", anchor="w")
        self.entry = tk.Entry(self)
        self.submit = tk.Button(self, text="Submit", command = self.process)
        self.output = tk.Label(self, text="")

        # lay the widgets out on the screen.
        self.prompt.pack(side="top", fill="x")
        self.entry.pack(side="top", fill="x", padx=20)
        self.output.pack(side="top", fill="x", expand=True)
        self.submit.pack(side="right")
    def readWaves(self):
        waves = []
        for dirname, dirnames, filenames in os.walk('audio'):
            for filename in filenames:
                name = (os.path.join(dirname, filename))
                (sig,rate) = wav.read(name)
                out = (sig,rate)
                waves.append(out)
        return waves
    def getCeps(self,waves):#pointwise multiply and subtract the average from all of it. Can compare on zero crossings too. can do length penaltiies.
        ceps = []
        for wave in waves:
            ceps.append(mfcc(wave[1],wave[0]))
        return ceps
    def getFBanks(self,waves):
        fbanks = []
        for wave in waves:
            fbanks.append(logfbank(wave[1],wave[0]))
        return fbanks
        '''
        cut the dtw to only sample smaller pieces for cepstrums and do the same for zero crossing. May need
        to normalize the cepstra otherwise the biggest one wins/loses. To normalize do zero mean and divide by st dev.
        '''
    def DTWDistance(self,s,t):#44100, divide signal into chunks. chunk into fixed sample sizes.
        n = len(s)#can do vectors or single values.
        m = len(t)
        DTW = [[]]
        for i in range(1,n):
            DTW[i, 0] = math.max
        for i in range(1,m):
            DTW[0, i] = math.max
        DTW[0, 0] = 0

        for i in range(1,n):
            for j in range(1,m):
                cost = math.abs(s[i]-t[j])# can put ssd here, normalized pointwise compare.
                DTW[i, j] = cost + math.minimum(DTW[i-1,j],DTW[i,j-1],DTW[i-1,j-1])

        return DTW[n, m]

    def process(self):
        # get the value from the input widget, convert
        # it to an int, and do a calculation

        waves = self.readWaves()
        cepstrums = self.getCeps(waves)
        fbanks = self.getFBanks(waves)
        for cep in cepstrums:
            print cep
        #waves.append(wav.read("audio/backup.wav"))
        #mfcc_feat = mfcc(sig,rate)
        #fbank_feat = logfbank(sig,rate)

        # set the output widget to have our result
        self.output.configure(text='stuff')
        print len(waves)
        print len(cepstrums)
        print len(fbanks)
        diffs = self.DTWDistance(cepstrums[0],cepstrums[1])

# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()
