import Tkinter as tk
from features import mfcc
from features import logfbank
import scipy.io.wavfile as wav
import os
import math
import sys
import random

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # create a prompt, an input box, an output label,
        # and a button to do the computation
        self.prompt = tk.Label(self, text="Enter a number:", anchor="w")
        self.entry = tk.Entry(self)
        #self.submit = tk.Button(self, text="Submit", command = self.process)
        self.output = tk.Label(self, text="")
        self.hello = tk.Button(self, text="hello", command = self.hello)
        self.do = tk.Button(self, text="do", command = self.do)
        self.delete = tk.Button(self, text="delete", command = self.delete)
        self.edit = tk.Button(self, text="edit", command = self.edit)
        self.exit = tk.Button(self, text="exit", command = self.exit)
        self.paste = tk.Button(self, text="paste", command = self.paste)
        self.put = tk.Button(self, text="put", command = self.put)
        self.bye = tk.Button(self, text="bye", command = self.bye)
        self.backup = tk.Button(self, text="backup", command = self.backup)
        self.list = tk.Button(self, text="list", command = self.list)


        # lay the widgets out on the screen.
        self.prompt.pack(side="top", fill="x")
        self.entry.pack(side="top", fill="x", padx=20)

        self.hello.pack(side="bottom")
        self.do.pack(side="bottom")
        self.delete.pack(side="bottom")
        self.edit.pack(side="bottom")
        self.exit.pack(side="bottom")
        self.paste.pack(side="bottom")
        self.put.pack(side="bottom")
        self.bye.pack(side="bottom")
        self.backup.pack(side="bottom")
        self.list.pack(side="bottom")
        self.output.pack(side="top", fill="x", expand=True)

    def hello(self):
        self.process("hello")
    def do(self):
        self.process("do")
    def delete(self):
        self.process("delete")
    def edit(self):
        self.process("edit")
    def exit(self):
        self.process("exit")
    def paste(self):
        self.process("paste")
    def put(self):
        self.process("put")
    def bye(self):
        self.process("bye")
    def backup(self):
        self.process("backup")
    def list(self):
        self.process("list")

    def readWaves(self):
        waves = []
        for dirname, dirnames, filenames in os.walk('audio'):
            for filename in filenames:
                name = (os.path.join(dirname, filename))
                (sig,rate) = wav.read(name)
                out = (sig,rate)
                waves.append(out)
        return waves,filenames
    def readWavesTest(self,test):
        waves = []
        test = "test/"+test
        for dirname, dirnames, filenames in os.walk(test):
            for filename in filenames:
                name = (os.path.join(dirname, filename))
                (sig,rate) = wav.read(name)
                out = (sig,rate)
                waves.append(out)
        return waves,filenames

    def getCeps(self,waves):#pointwise multiply and subtract the average from all of it. Can compare on zero crossings too. can do length penaltiies.
        ceps = []
        for i in range(0,len(waves)):
            ceps.append(mfcc(waves[i][1],waves[i][0]))
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
        DTW  = []
        for i in range(0,n):
            new = []
            for j in range(0,m):
                new.append(0)
            DTW.append(new)
        for i in range(0,n):
            DTW[i][0] = float("inf")
        for i in range(0,m):
            DTW[0][i] = float("inf")
        DTW[0][0] = 0
        for i in range(1,n):
            for j in range(1,m):
                #print len(s[i]), len(t[j])
                cost = self.dist3(s[i],t[j])# can put ssd here, normalized pointwise compare.
                DTW[i][j] = cost + min(DTW[i-1][j],DTW[i][j-1],DTW[i-1][j-1])

        return DTW[n-1][m-1]

    def dist(self,s,t):
        totalDiff = 0
        means = self.getMean(s)
        meant = self.getMean(t)
        stDevSums = 0
        stDevSumt = 0
        for i in range(0,len(s)):
            stDevSums += abs(s[i]-means)
            stDevSumt += abs(t[i]-meant)
            s[i] = s[i] - means
            t[i] = t[i] - meant
        stDevs = stDevSums/len(s)
        stDevt = stDevSumt/len(t)
        diffs = []
        for i in range(0,len(s)):
            s[i] = s[i]/stDevs
            t[i] = t[i]/stDevt
            diffs.append(abs(s[i]-t[i]))
        diffmean = self.getMean(diffs)
        for i in diffs:
            i = i - diffmean
            totalDiff += (i - diffmean)

        return totalDiff/len(diffs)

    def dist2(self,s,t):
        sumDiff = 0
        mean1 = self.getMean(s)
        mean2 = self.getMean(t)
        for i in range(0,len(s)):
            sumDiff += pow(((s[i])-(t[i])),2)
        return sumDiff

    def dist3(self,s,t):
        diffs = []
        for i in range(0,len(s)):
            diffs.append((s[i])-(t[i]))
        diffmean = self.getMean(diffs)
        variance = 0
        for i in diffs:
            variance += pow(i - diffmean,2)
        return variance

    def process(self,file):
        # get the value from the input widget, convert
        # it to an int, and do a calculation

        results = self.readWaves()
        waves = results[0]
        names = results[1]
        cepstrums = self.getCeps(waves)
        fbanks = self.getFBanks(waves)
        tResults = self.readWavesTest(file)
        tWaves = tResults[0]
        tNames = tResults[1]
        tCeps = self.getCeps(tWaves)
        n = random.randint(0,len(tWaves)-1)
        '''zero crossings kind of muddying the water. will not use these'''
        '''
        zeroCrossings = []
        for i in range(0,len(waves)):
            count = 0
            pos = True
            for point in waves[i][1]:
                #print point
                avg = ((point[0] + point[1])/2)
                if avg < 0 and pos:
                    count += 1
                    pos = False
                if avg > 0 and not(pos):
                    count += 1
                    pos = True
            zeroCrossings.append(count)
            print count


        zeroDiffs = []
        for j in range(0,len(cepstrums)):
            temp = abs(zeroCrossings[n]-zeroCrossings[j]),n,j,names[n],names[j]
            zeroDiffs.append(temp)
        print zeroDiffs
        if zeroDiffs[1] != 0:
            minimum = zeroDiffs[1]
        else:
            minimum = zeroDiffs[2]
        for diff in zeroDiffs:
            if diff[0] < minimum[0] and diff[0] != 0:
                minimum = diff
        print minimum
        '''
        # set the output widget to have our result


        differences = []

        for j in range(0,len(cepstrums)):
            temp = self.DTWDistance(tCeps[n],cepstrums[j]),n,j,tNames[n],names[j]
            differences.append(temp)

        #diffs = self.DTWDistance(cepstrums[0],cepstrums[1])
        #print differences
        for d in differences:
            print d
        if differences[1] != 0:
            minimum = differences[1]
        else:
            minimum = differences[2]
        for diff in differences:
            if diff[0] < minimum[0] and diff[0] != 0:
                minimum = diff
        out = minimum[3],minimum[4]
        self.output.configure(text=out)

    def getMean(self,list):
        sum = 0
        for item in list:
            sum += item
        return sum/len(list)
# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()
