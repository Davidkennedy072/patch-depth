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
subjectinital = 'KE'

filelist = []
for root, dirs, files in os.walk('C:/Users/zae/Documents/summer2018/patchDepth_results'):
    for Datei in files:
        if Datei.endswith('.txt'):
            if subjectinital in Datei:
                filelist.append(Datei)
genau = np.zeros([len(filelist),2])       
for Datei in filelist: 
    file = open(Datei, 'r')
    
    lines = file.readlines()
    result = [] # Result is changing in each iteration 
    for x in lines:
        result.append(x.split(' ')) # Creates 2D list: 0 to 300 by 0 to 16
    imagesize = int(re.search(r'\d+', Datei).group())
    # Pull depthCorrect data from list
    accuracy = np.zeros(len(result)-1)
    for row in range(len(result) -1):
        accuracy[row] = result[row+1][result[0].index('depthCorrect\t')]
    acc = np.mean(accuracy)
    genau[filelist.index(Datei), 0] = imagesize
    genau[filelist.index(Datei), 1] = acc
    
    confidence = np.zeros(len(result)-1)
    for row in range(len(result) - 1):
        confidence[row] = abs(float(result[row+1][result[0].index('depthResp\t')]))
    
    # Sort confidence values in order
    L = sorted(zip(confidence, accuracy), 
               key = operator.itemgetter(0))
    #conf, accur = zip(*L)
    #plt.plot(conf, accur)
    L = np.array(L)
    amountofbins = 10
    binrange = [10*x+10 for x in range(amountofbins)]
    binaverages = np.zeros(len(binrange))
    for binrangeindex in range(len(binrange)):
        for confaccu in L:
             if confaccu[0] < binrange[binrangeindex]:
                 binaverages[binrangeindex] = np.mean([binaverages[binrangeindex], 
                                                      confaccu[1]])
    plt.figure(1)
    #plt.bar(binrange, binaverages, len(binrange)) 
    #plt.figure(4)
    plt.plot([x-len(binrange)/2 for x in binrange], binaverages,
              label = 'Patch size {}'.format(imagesize))
    plt.legend()
    
    '''
    Idea: Plot average accuracy vs confidence for all patches 
    '''

plt.xlabel('Confidence')
plt.ylabel('Accuracy') 
plt.suptitle('Accuracy with increasing confidence for all patches')
plt.title('Confidence bin interval: {}'.format(len(binrange)))

plt.figure(2)
# Reorganizing genau x data to plot 
genau = genau[genau[:,0].argsort()]
#Plot accuracy across different image sizes 
plt.plot(genau[:,0], genau[:,1])
plt.ylabel('Accuracy')
plt.xlabel('Imagesize')
plt.title('Accuracy with Increasing Patch Size')
file.close() 