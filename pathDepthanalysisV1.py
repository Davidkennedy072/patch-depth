# -*- coding: utf-8 -*-
"""
Created on Fri May 11 11:06:14 2018

@author: David
"""
import numpy as np
import matplotlib.pyplot as plt
import operator
import os

file = open('result_DY_8.txt', 'r')
lines = file.readlines()
result = []
for x in lines:
    result.append(x.split(' ')) # Creates 2D list: 0 to 300 by 0 to 16
file.close() 

'''
Goal: Does accuracy increase with patch size
accuracy defined as average of depthCorrect
'''
# Pull depthCorrect data from list
accuracy = np.zeros(len(result)-1)
for row in range(len(result) -1):
    accuracy[row] = result[row+1][result[0].index('depthCorrect\t')]
    acc = np.mean(accuracy)
    
''' 
Goal: Confidence and accuracy
Plot accuracy as a funtion of confidence?
Maybe plot an histogram? # of rights for confidence
'''
confidence = np.zeros(len(result)-1)
for row in range(len(result) - 1):
    confidence[row] = abs(float(result[row+1][result[0].index('depthResp\t')]))
    
plt.figure(1)
# Sort confidence values in order
L = sorted(zip(confidence, accuracy), key = operator.itemgetter(0))
conf, accur = zip(*L)
plt.plot(conf, accur)