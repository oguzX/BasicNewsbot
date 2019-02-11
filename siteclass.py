class site:
    sitename = ""
    def __init__(self,_sitename,_siteurl,_contenttarget):
        self.sitename = _sitename
        self.siteurl = _siteurl
        self.contenttarget = _contenttarget
    
    def getsitename(self):
        return self.sitename
    
    def getsiteurl(self):
        return self.siteurl
    
    def getcontenttarget(self):
        return self.contenttarget