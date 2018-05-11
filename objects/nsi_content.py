#!/usr/bin/python

class nsi_content:
    def __init__(self):
        self.id=""
        self.name=""
        self.description=""
        self.nstId=""
        self.vendor=""
        self.nstInfoId=""
        self.flavorId=""
        self.sapInfo=""
        self.nsiState=""
        self.instantiateTime=""
        self.terminateTime=""
        self.scaleTime=""
        self.updateTime=""
        self.netServInstance_Uuid = []
               
    def getID(self):
        return self.id

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getNSTId(self):
        return self.nstId
    
    def getVendor(self):
        return self.vendor

    def getInfoId(self):
        return self.nstInfoId

    def getFlavorIds(self):
        return self.flavorId

    def getSapInfo(self):
        return self.sapInfo

    def getNSIState(self):
        return self.nsiState
    
    def getInstatiateTime(self):
        return self.instantiateTime
    
    def getTerminateTime(self):
        return self.terminateTime
    
    def getScaleTime(self):
        return self.scaleTime
    
    def getUpdateTime(self):
        return self.updateTime
        
    def getNetServInstance_Uuid(self):
        return self.netServInstance_Uuid