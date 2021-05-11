# -*- coding: utf-8 -*-
"""
Created on Sun May  9 18:11:16 2021

@author: HP
"""
import numpy as np
from sklearn.svm import SVR
import pickle



class Predictor:
    
    def __init__(self,usermodel):
        self.modelpath="model.pkl"
        self.usermodel=usermodel
    def loadData(self):
        data=self.usermodel.admin_dash_purchase_trend()
        self.x=np.array([[i] for i in range(len(data))])
        self.y=np.array([t[1] for t in data])
        '''print(self.x)
        print(self.y)'''
    def buildModel(self):
        self.model=SVR(kernel="poly",degree=3,C=1.0)
        self.model=self.model.fit(self.x,self.y)
    def loadModel(self):
        dbfile = open(self.modelpath, 'rb')     
        self.model = pickle.load(dbfile)
    def saveModel(self):
        dbfile = open(self.modelpath, 'wb')
        pickle.dump(self.model, dbfile)
    def predict(self,x):
        self.loadModel()
        y=self.model.predict([[x]])
        return np.floor(y[0])
        
        
        