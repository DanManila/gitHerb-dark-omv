import os

def de_info( msgtxt, titletxt ):
        pass

def fetch_textfile_value( pname, mykeyname ):
    # assumes pname has been vetted elsewhere, prior to calling this routine
    # assumes key-value pair are on a line of the form
    #     keyname = value
    myf = open( pname, 'r' )
    thisline = myf.readline()
    # return
    
    while( thisline ):
    
        if( "=" in thisline):
            lhs, rhs = thisline.split("=")
            lhs = (lhs.strip()).strip('\"')     # first strip whitespace, then strip quotes
            rhs = (rhs.strip()).strip('\"')
            
            if( lhs == mykeyname ):
                myvalue = rhs
                return myvalue
        
        thisline = myf.readline()
        
    return None
    
class MainForm():
    def __init__(self):
        self.InitializeComponent()
    
    def mainCancelClick(self,sender,e):        #   User clicked Cancel in Main Form.  Run away!!
        # EMK_finisher_GaN_jobglobals_v5.status = 'cancel'
        self.Close()
        
        y = int(5)
        y = y*y

    def setup_is_valid(self):
        pass
    
    def run_in_progress(self):
        pass

            
    def ButtonBClick(self, sender, e):
        pass

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        