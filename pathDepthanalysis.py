# -*- coding: utf-8 -*-
"""
Created on Fri May 11 11:06:14 2018

@author: David
"""
import numpy as np
import matplotlib.pyplot as plt
import operator
import os
import re
subjectinital = 'RA'
amountofbins = 10

plt.figure(1)
#plt.clf()

filelist = []
for root, dirs, files in os.walk('C:/Users/zae/Documents/summer2018/patchDepth_results'):
    for Datei in files:
        if Datei.endswith('.txt'):
            if subjectinital in Datei:
                filelist.append(Datei)
binaveragesall = np.zeros([len(filelist), amountofbins]) # Used for acc vs conf average
genau = np.zeros([len(filelist),2])   
figureaccuracy = np.zeros([len(filelist), 2])   
for Datei in filelist: 
    file = open(Datei, 'r')
    lines = file.readlines()
    result = [] # Result is changing in each iteration 
    for x in lines:
        result.append(x.split(' ')) # Creates 2D list: 0 to 300 by 0 to 16
    imagesize = int(re.search(r'\d+', Datei).group())
    # Pull depthCorrect data from list
    accuracy = np.zeros(len(result)-1)
    labeldepth = np.zeros(len(result)-1)
    figurecorrect = np.zeros(len(result)-1)
    for row in range(len(result) -1):
        accuracy[row] = result[row+1][result[0].index('depthCorrect\t')]
        labeldepth[row] = result[row+1][result[0].index('labelDepth\t')]
        figurecorrect[row] = result[row+1][result[0].index('figureCorrect\t')]
    acc = np.mean(accuracy)
    genau[filelist.index(Datei), 0] = imagesize
    genau[filelist.index(Datei), 1] = acc

    Summen = 0
    for responseindex in range(len(figurecorrect)): # Each patch has 300 responses
        if labeldepth[responseindex] == 1 and accuracy[responseindex] == 1:
            Summen = Summen + figurecorrect[responseindex]
    figureaccuracy[filelist.index(Datei), 0] = imagesize 
    figureaccuracy[filelist.index(Datei), 1] = Summen / sum(labeldepth)
    
    confidence = np.zeros(len(result)-1)
    for row in range(len(result) - 1):
        confidence[row] = abs(float(result[row+1][result[0].index('depthResp\t')]))
    
    # Sort confidence values in order
    L = sorted(zip(confidence, accuracy), 
               key = operator.itemgetter(0))
    L = np.array(L)
    binrange = [(100/amountofbins)*x+(100/amountofbins) for x in range(amountofbins)]
    binaverages = np.zeros(len(binrange))
    for binrangeindex in range(len(binrange)):
        for confaccu in L:
             if confaccu[0] < binrange[binrangeindex]:
                 binaverages[binrangeindex] = np.mean([binaverages[binrangeindex], 
                                                      confaccu[1]])
    binaveragesall[filelist.index(Datei), :] = binaverages
    plt.figure(1) 
    plt.plot([x-len(binrange)/2 for x in binrange], binaverages, 
              label = '{} Patch size {}'.format(subjectinital, imagesize))
    
plt.xlabel('Confidence')
plt.ylabel('Accuracy') 
plt.suptitle('Accuracy(depth) with increasing confidence for all patches')
plt.title('Confidence bin interval: {}'.format(len(binrange)))
plt.legend()

plt.figure(2)
Mittelwert = binaveragesall.mean(axis=0)
plt.plot([x-len(binrange)/2 for x in binrange], Mittelwert, 
          label = 'Overall {}'.format(subjectinital)) 
plt.xlabel('Confidence')
plt.ylabel('Accuracy') 
plt.suptitle('Accuracy(depth) with increasing confidence')
plt.title('Confidence bin interval: {}'.format(len(binrange)))
plt.legend()

plt.figure(3)
# Reorganizing genau x data to plot 
genau = genau[genau[:,0].argsort()]
figureaccuracy = figureaccuracy[figureaccuracy[:,0].argsort()]
#Plot accuracy across different image sizes 
plt.plot(genau[:,0], genau[:,1], label = '{}: Depth'.format(subjectinital))
plt.plot(figureaccuracy[:,0], figureaccuracy[:, 1], 
         label = '{}: Figure'.format(subjectinital))
plt.legend()
plt.ylabel('Accuracy')
plt.xlabel('Imagesize')
plt.title('Accuracy (depth) with Increasing Patch Size')

file.close() 