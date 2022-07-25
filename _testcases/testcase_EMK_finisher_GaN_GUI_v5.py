# import ScriptEnv
import ScriptEnv
import os
import sys
import collections
import datetime
import string
import math
import inspect

# NOTE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#      Current GUI module implementation does not use "Ansoft.ElectronicsDesktop"
#      CONSEQUENTLY: AddMessage is not available. use MessageBox instead 
#                    (gives a pop-up, can't send msg to Message Manager)
#
# Explicitly, it does not use any of the following commented-out stuff:
#
#       global oAnsoftApp
#       ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
#       oAnsoftApp      = CreateObject("Ansoft.ElectronicsDesktop")
#       oDesktop        = oAnsoftApp.GetAppDesktop()
#       oProject        = oDesktop.GetActiveProject()
#       oDesign         = oProject.GetActiveDesign()
#       oEditor         = oDesign.SetActiveEditor("3D Modeler")
#       initialAutoSave = oDesktop.GetAutoSaveEnabled()
#
#       ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
#       oProject = oDesktop.GetActiveProject()
#       oDesign = oProject.GetActiveDesign()
#       oEditor = oDesign.SetActiveEditor("3D Modeler")
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import clr
clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")

import System.Drawing
import System.Windows.Forms
import System.IO
from System.Drawing import *
from System.Windows.Forms import *

# MessageBox.Show( "import EMK_finisher_GaN_config_v5" )
import EMK_finisher_GaN_config_v5

# MessageBox.Show( "import EMK_finisher_GaN_jobglobals_v5" )
import EMK_finisher_GaN_jobglobals_v5

# MessageBox.Show( "import EMK_viewTextFile" )
import EMK_viewTextFile


def de_info( msgtxt, titletxt ):
        MessageBox.Show( msgtxt, titletxt )

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
    
class MainForm(Form):
    def __init__(self):
        self.InitializeComponent()
    
    def mainCancelClick(self,sender,e):        #   User clicked Cancel in Main Form.  Run away!!
        # EMK_finisher_GaN_jobglobals_v5.status = 'cancel'
        EMK_finisher_GaN_jobglobals_v5.user_ok = False
        self.Close()
        
        y = int(5)
        y = y*y

    def setup_is_valid(self):
        # oDesktop.AddMessage( "","",0,"^  setup_is_valid = " )
        setup_pathname   = EMK_finisher_GaN_jobglobals_v5.setup_pathname
        setupfile_exists = os.path.isfile( setup_pathname )
        # MessageBox.Show( "setup_pathname = "   + setup_pathname,   "fcn: setup_is_valid" )
        # MessageBox.Show( "setupfile_exists = " + repr(setupfile_exists), "fcn: setup_is_valid" )
        if setupfile_exists:
            EMK_finisher_GaN_jobglobals_v5.setup_ok = True
        else:
            EMK_finisher_GaN_jobglobals_v5.setup_ok = False
    
    def run_in_progress(self):
        setup_pathname   = EMK_finisher_GaN_jobglobals_v5.setup_pathname
        setupfile_exists = os.path.isfile( setup_pathname )
        # MessageBox.Show( "setup_pathname = "   + setup_pathname,   "fcn: setup_is_valid" )
        # MessageBox.Show( "setupfile_exists = " + repr(setupfile_exists), "fcn: setup_is_valid" )
        if setupfile_exists:
            EMK_finisher_GaN_jobglobals_v5.setup_ok = True
        else:
            EMK_finisher_GaN_jobglobals_v5.setup_ok = False

            
    def str2int_BrPnt( self, in_str ):
        if   in_str == "Start":
            iBrPnt = 0
        elif in_str == "Finish":
            iBrPnt = 1000
        else:
            iBrPnt = int( in_str )
        return iBrPnt


    def read_setup_from_files( self, setupfile ):
        # NOTE: THIS FUNCTION IS NOT CALLED DURING A RESUME OPERATION
        #       SO NO ALLOWANCE IS MADE HERE FOR THE CASE OF A RESUMING JOB
        #
        # OBJECTIVE: READ SETUP FROM INPUT FILES
        #            STORE INFORMATION IN GLOBALS MODULE
        #            ERROR REPORTING IS HANDLED BY SEPARATE ROUTINE: self.errorcheck_setup_and_populate_GUI
        #            ERROR REPORTING IS THE SAME WHETHER STARTING FROM FILES OR RESUMING A JOB
        #         

        # self._textBoxA.Text = ''        
        # self._textBoxB.Text = ''        
        # self._textBoxC.Text = ''
        # self._textBoxIconn.Text = ''
        # self._textBoxTopo.Text  = ''
        
        ok_so_far = True
        setup_ok  = True
        
        specified_dir = False
        specified_gds = False
        specified_mat = False
        specified_ild = False
        
        have_dir = False
        have_gds = False
        have_mat = False
        have_ild = False

        found_interconnect = False
        found_topography   = False
        
        EMK_finisher_GaN_jobglobals_v5.tech_dir = ''
        EMK_finisher_GaN_jobglobals_v5.gds_defn_file = ''
        EMK_finisher_GaN_jobglobals_v5.ild_defn_file = ''
        EMK_finisher_GaN_jobglobals_v5.mat_defn_file = ''
        
        
        # ------------------------
        # 1. verify specified setup file: if error, return to GUI loop
        # mySetupfilePathName = self._openSetupFileDialog.FileName
        # EMK_finisher_GaN_jobglobals_v5.setup_pathname = mySetupfilePathName        # store in globals even though we haven't checked it. error reporting routine will
        # if ( os.path.isfile(mySetupfilePathName) ):
            # pass
        # else:
            # ok_so_far = False
            # setup_ok  = False
            # msg_content = "Specified Setup file pathname does not point to a file."
            # msg_title   = "Error"
            # MessageBox.Show( msg_content, msg_title )
            # return
        
        
        # mySetupfilePathName = self.fetchSetupFile.FileName
        mySetupfilePathName = setupfile
        EMK_finisher_GaN_jobglobals_v5.setup_pathname = mySetupfilePathName        # store in globals even though we haven't checked it. error reporting routine will
        if ( os.path.isfile(mySetupfilePathName) ):
            pass
        else:
            ok_so_far = False
            setup_ok  = False
            msg_content = "Specified Setup file pathname does not point to a file."
            msg_title   = "Error"
            MessageBox.Show( msg_content, msg_title )
            # return
        
        
        # ------------------------
        # 2. open specified setup file: if error, return to GUI loop
        if( ok_so_far ):
            # self._textBoxSetupFileBrowse.Text = mySetupfilePathName
            try:
                fsetupfile = open( mySetupfilePathName, 'r' )
            except:
                # tell user the setup file is messed up
                # TBD TBD TBD TBD TBD
                ok_so_far = False
                setup_ok  = False
                msg_content = "Unable to open Setup file."
                msg_title   = "Error"
                MessageBox.Show( msg_content, msg_title )
                # return
        
        
        # ------------------------
        # 3. get techdir
        if( ok_so_far ):
            EMK_finisher_GaN_jobglobals_v5.setup_pathname = os.path.abspath( mySetupfilePathName )
            EMK_finisher_GaN_jobglobals_v5.setup_path     = os.path.dirname( mySetupfilePathName )
            # EMK_finisher_GaN_jobglobals_v5.progress_bar   = 0
            # if( EMK_finisher_GaN_jobglobals_v5.iStart == 0 ):
                # EMK_finisher_GaN_jobglobals_v5.escape_mode = False
        
        
        # ------------------------
        # 4. parse setup file and error check
        if( ok_so_far ):
        
            setup_file_pathname = EMK_finisher_GaN_jobglobals_v5.setup_pathname
            setup_f = open( setup_file_pathname, 'r' )
            
            # debug -----------------
            # msg_content2 = "read_setup_files::setup_pathname = " + setup_file_pathname
            # msg_title2   = "read_setup_files::setup_file_pathname"
            # MessageBox.Show( msg_content2, msg_title2 )
            # debug -----------------

            thisline = setup_f.readline()
            # specified_dir = False
            # specified_gds = False
            # specified_mat = False
            # specified_ild = False
            # EMK_finisher_GaN_jobglobals_v5.tech_dir = ''
            # EMK_finisher_GaN_jobglobals_v5.gds_defn_file = ''
            # EMK_finisher_GaN_jobglobals_v5.ild_defn_file = ''
            # EMK_finisher_GaN_jobglobals_v5.mat_defn_file = ''

            while( thisline ):
                # //debug -----------------
                # msg_content3 = "thisline >>" + thisline
                # msg_title3   = "read_setup_files::thisline"
                # MessageBox.Show( msg_content3, msg_title3 )
                # //debug -----------------
                
                # first scan entire file for keywords and their values (so order within file doesn't matter)
                if '=' in thisline:
                
                    lhs, rhs = thisline.split("=")
                    lhs = (lhs.strip()).strip('\"')     # first strip whitespace, then strip quotes
                    rhs = (rhs.strip()).strip('\"')
                    rhs =  rhs.strip('\\')              # rhs also needs strip backslash
                    rhs =  rhs.strip('/' )              # rhs also needs strip forwardslash

                    # //debug -----------------
                    # msg_content4 = "lhs,rhs >>" + repr(lhs) + ", " + repr(rhs)
                    # msg_title4   = "read_setup_files::lhs,rhs"
                    # MessageBox.Show( msg_content4, msg_title4 )
                    # //debug -----------------
                    
                    if( lhs == "tech_dir" ):
                        # //debug -----------------
                        msg_content = "tech_dir line >>" + repr(thisline)
                        msg_content = msg_content + "\n\r   os.getcwd() = " + repr( os.getcwd() )
                        msg_content = msg_content + "\n\r   rhs = " + repr(rhs)
                        msg_content = msg_content + "\n\r   os.path.isdir(rhs) = " + repr( os.path.isdir(rhs) )
                        msg_title   = "read_setup_from_files. lhs"
                        # MessageBox.Show( msg_content, msg_title )
                        # //debug -----------------
                        EMK_finisher_GaN_jobglobals_v5.tech_dir = rhs
                        specified_dir = True
                    elif( lhs == "gds_defn_file" ):
                        EMK_finisher_GaN_jobglobals_v5.gds_defn_file = rhs
                        specified_gds = True
                    elif( lhs == "ild_defn_file" ):
                        EMK_finisher_GaN_jobglobals_v5.ild_defn_file = rhs
                        specified_ild = True
                    elif( lhs == "mat_defn_file" ):
                        EMK_finisher_GaN_jobglobals_v5.mat_defn_file = rhs
                        specified_mat = True
                
                thisline = setup_f.readline()
        
       
        # ------------------------
        # 5.  error check definition file specifications
        
        # //error checks
        err_msg = ""
        nl = "\r\n"
        if (not specified_dir):
            err_msg = err_msg + nl + "Setup file does not specify 'tech_dir'."
        
        if (specified_dir and not specified_gds):
            err_msg = err_msg + nl + "Setup file does not specify gds_defn_file."
            
        if (specified_dir and not specified_ild):
            err_msg = err_msg + nl + "Setup file does not specify ild_defn_file."
            
        if (specified_dir and not specified_mat):
            err_msg = err_msg + nl + "Setup file does not specify mat_defn_file."
            
        tech_dir = EMK_finisher_GaN_jobglobals_v5.tech_dir
        gds_defn_pname = tech_dir + '/' + EMK_finisher_GaN_jobglobals_v5.gds_defn_file
        ild_defn_pname = tech_dir + '/' + EMK_finisher_GaN_jobglobals_v5.ild_defn_file
        mat_defn_pname = tech_dir + '/' + EMK_finisher_GaN_jobglobals_v5.mat_defn_file
        
        # specified_dir = False
        # specified_gds = False
        # specified_mat = False
        # specified_ild = False

        # if ( not os.path.isdir(tech_dir) ):
            # err_msg = err_msg + nl + "Valid tech_dir path not found."
        # if ( not os.path.isfile(gds_defn_pname) ):
            # err_msg = err_msg + nl + "Valid gds_defn_file pathname not found."
        # if ( not os.path.isfile(ild_defn_pname) ):
            # err_msg = err_msg + nl + "Valid ild_defn_pname pathname not found."
        # if ( not os.path.isfile(mat_defn_pname) ):
            # err_msg = err_msg + nl + "Valid mat_defn_pname pathname not found."


        if ( os.path.isdir(tech_dir) ):
            EMK_finisher_GaN_jobglobals_v5.tech_dir = tech_dir
            EMK_finisher_GaN_jobglobals_v5.have_dir = True
            have_dir = True
        else:
            err_msg = err_msg + nl + "Valid tech_dir path not found."
        
        if ( os.path.isfile(gds_defn_pname) ):
            EMK_finisher_GaN_jobglobals_v5.gds_defn_pname = gds_defn_pname
            have_gds = True
        else: 
            err_msg = err_msg + nl + "Valid gds_defn_file pathname not found."
            
        if ( os.path.isfile(ild_defn_pname) ):
            EMK_finisher_GaN_jobglobals_v5.ild_defn_pname = ild_defn_pname
            have_ild = True
        else:
            err_msg = err_msg + nl + "Valid ild_defn_pname pathname not found."
            
        if ( os.path.isfile(mat_defn_pname) ):
            EMK_finisher_GaN_jobglobals_v5.mat_defn_pname = mat_defn_pname
            have_mat = True
        else:
            err_msg = err_msg + nl + "Valid mat_defn_pname pathname not found."
        
        if (have_dir and have_gds):
            try:
                test_gds_defn = open( gds_defn_pname, 'r' )
                test_gds_defn.close()
                have_gds = True
                EMK_finisher_GaN_jobglobals_v5.have_gds = True
            except:
                err_msg = err_msg + nl + "Unable to open file at specified gds_defn_file pathname."
                have_gds = False
            
        if (have_dir and have_ild):
            try:
                test_ild_defn = open( ild_defn_pname, 'r' )
                test_ild_defn.close()
                have_ild = True
                EMK_finisher_GaN_jobglobals_v5.have_ild = True
            except:
                err_msg = err_msg + nl + "Unable to open file at specified ild_defn_file pathname."
                have_ild = False

        if (have_dir and have_mat):
            try:
                test_mat_defn = open( mat_defn_pname, 'r' )
                test_mat_defn.close()
                have_mat = True
                EMK_finisher_GaN_jobglobals_v5.have_mat = True
            except:
                err_msg = err_msg + nl + "Unable to open file at specified mat_defn_file pathname."
                have_mat = False

        msg_title = "Error"
        if ( err_msg != "" ):
            # err_msg = "marker 1232\n\r" + err_msg
            err_msg = "" + err_msg
            MessageBox.Show( err_msg, msg_title )
            EMK_finisher_GaN_jobglobals_v5.setup_ok = False
            return err_msg
        
        
        # ------------------------
        # 6. read INTERCONNECT and TOPOGRAPHY from gds_defn_file
        # msg_content = "marker 5555\n\r"
        # msg_content = msg_content + "have_dir = " + repr(EMK_finisher_GaN_jobglobals_v5.have_dir) + "\n\r"
        # msg_content = msg_content + "have_gds = " + repr(EMK_finisher_GaN_jobglobals_v5.have_gds) + "\n\r"
        # msg_title   = "process/topo"
        # MessageBox.Show( msg_content, msg_title )

        iProcesses  = EMK_finisher_GaN_config_v5.iProcesses
        iTopography = EMK_finisher_GaN_config_v5.iTopography
        if (have_dir and have_gds):
            topo    = fetch_textfile_value( gds_defn_pname, "TOPOGRAPHY" )
            connect = fetch_textfile_value( gds_defn_pname, "INTERCONNECT" )
            if( connect in iProcesses ):
                EMK_finisher_GaN_jobglobals_v5.interconnect = connect
                found_interconnect = True
                # //debug -----------------
                # msg_content = "INTERCONNECT. iProcesses = " + repr(iProcesses) + "\n\r"
                # msg_content = msg_content  + "INTERCONNECT. connect = " + repr(connect)
                # msg_title   = "iProcesses"
                # MessageBox.Show( msg_content, msg_title )
                # //debug -----------------
            else:
                EMK_finisher_GaN_jobglobals_v5.interconnect = None
                found_interconnect = False
            
            if( topo in iTopography ):
                EMK_finisher_GaN_jobglobals_v5.topography   = topo
                found_topography = True
                # //debug -----------------
                # msg_content = "TOPOGRAPHY. iTopography = " + repr(iTopography) + "\n\r"
                # msg_content = msg_content  + "TOPOGRAPHY. topo = " + repr(topo)
                # msg_title   = "iProcesses"
                # MessageBox.Show( msg_content, msg_title )
                # //debug -----------------
            else:
                EMK_finisher_GaN_jobglobals_v5.topography   = None
                found_topography = False
            
        setup_ok = ok_so_far  
        setup_ok = setup_ok and have_gds and have_mat and have_ild 
        setup_ok = setup_ok and found_interconnect and found_topography
        
        EMK_finisher_GaN_jobglobals_v5.setup_ok = setup_ok
        
        # if setup_ok != True:
        if True:
            # //debug -----------------
            msg_content = "setup_ok = " + repr(setup_ok)
            msg_content = msg_content + "\n\r have_gds = " + repr(EMK_finisher_GaN_jobglobals_v5.have_gds)
            msg_content = msg_content + "\n\r have_mat = " + repr(EMK_finisher_GaN_jobglobals_v5.have_mat)
            msg_content = msg_content + "\n\r have_ild = " + repr(EMK_finisher_GaN_jobglobals_v5.have_ild)
            msg_content = msg_content + "\n\r"
            msg_content = msg_content + "\n\r found_interconnect = " + repr(found_interconnect)
            msg_content = msg_content + "\n\r found_topography   = " + repr(found_topography)
            msg_title   = "ERROR: read_setup_from_files"
            # MessageBox.Show( msg_content, msg_title )
            # //debug -----------------
                
        return setup_ok
        
# *************************************************************************************************
        
        # return
        
        if( EMK_finisher_GaN_jobglobals_v5.setup_ok):
            tech_dir = EMK_finisher_GaN_jobglobals_v5.tech_dir
            gds_defn_pname = tech_dir + '\\' + EMK_finisher_GaN_jobglobals_v5.gds_defn_file
            ild_defn_pname = tech_dir + '\\' + EMK_finisher_GaN_jobglobals_v5.ild_defn_file
            mat_defn_pname = tech_dir + '\\' + EMK_finisher_GaN_jobglobals_v5.mat_defn_file

            self._textBoxA.Text = gds_defn_pname        
            self._textBoxB.Text = ild_defn_pname        
            self._textBoxC.Text = mat_defn_pname
            
            self._textBoxIconn.Text   = EMK_finisher_GaN_jobglobals_v5.interconnect
            self._textBoxTopo.Text = EMK_finisher_GaN_jobglobals_v5.topography
            
            if ( EMK_finisher_GaN_jobglobals_v5.topography == "Planar" ):
                self._comboBoxEncap.FormattingEnabled  = True
                self._comboBoxEstyle.Enabled           = False 
                self._comboBoxEstyle.FormattingEnabled = True
                self._comboBoxEstyle.SelectedIndex     = 0              # square corners - cannot be modified
            elif ( EMK_finisher_GaN_jobglobals_v5.topography == "Conformal" ):
                self._comboBoxEncap.FormattingEnabled  = True
                self._comboBoxEstyle.Enabled           = False 
                self._comboBoxEstyle.FormattingEnabled = True
                self._comboBoxEstyle.SelectedIndex     = 0              # chamfered corners, cannot be modified
                # if( EMK_finisher_GaN_jobglobals_v5.iStart == 0 ):
                    # self._checkBoxEsc.Checked = True
                # else:
                    # self._checkBoxEsc.Checked = False
            # else:
                # self._checkBoxEsc.Checked = False
                # set Edge Style = Square
                
        else:
            pass
            # originally was putting MessageBox error display here, but that is now in read_setup_files
            #   where the user can still recover by chosing a different setup file 
            # msg_contentC = err_msg
            # msg_titleC   = "Error"
            # MessageBox.Show( msg_contentC, msg_titleC )
        return



    def InitializeComponent( self ):
        # de_info("initializing main\n\rgds_defn_file = " + EMK_finisher_GaN_jobglobals_v5.gds_defn_file,"dbg")
        # de_info( "init start, EMK_finisher_GaN_jobglobals_v5.ild_defn_pname = " + EMK_finisher_GaN_jobglobals_v5.ild_defn_pname, "after stuffing testBoxB" )
        # de_info( "init start, EMK_finisher_GaN_jobglobals_v5.ild_defn_file = " + EMK_finisher_GaN_jobglobals_v5.ild_defn_file, "after stuffing testBoxB" )

        
        self._openSetupFileDialog    = System.Windows.Forms.OpenFileDialog()
        self._buttonSetupFileBrowse  = System.Windows.Forms.Button()
        self._textBoxSetupFileBrowse = System.Windows.Forms.TextBox()
        self._labelBrowse            = System.Windows.Forms.Label()

        self._labelA   = System.Windows.Forms.Label()
        self._labelB   = System.Windows.Forms.Label()
        self._labelC   = System.Windows.Forms.Label()
        self._buttonA  = System.Windows.Forms.Button()
        self._buttonB  = System.Windows.Forms.Button()
        self._buttonC  = System.Windows.Forms.Button()
        self._textBoxA = System.Windows.Forms.TextBox()
        self._textBoxB = System.Windows.Forms.TextBox()
        self._textBoxC = System.Windows.Forms.TextBox()

        self._buttonExe      = System.Windows.Forms.Button()
        self._buttonCancel   = System.Windows.Forms.Button()
        self._labelIconn     = System.Windows.Forms.Label()
        self._textBoxIconn   = System.Windows.Forms.TextBox()
        self._labelEncap     = System.Windows.Forms.Label()
        self._comboBoxEncap  = System.Windows.Forms.ComboBox()
        self._labelEstyle    = System.Windows.Forms.Label()
        self._comboBoxEstyle = System.Windows.Forms.ComboBox()
        self._panelPhyStruct = System.Windows.Forms.Panel()
        self._panelModel     = System.Windows.Forms.Panel()
        self._labelPhyStruct = System.Windows.Forms.Label()
        self._labelModel     = System.Windows.Forms.Label()
        self._textBoxTopo    = System.Windows.Forms.TextBox()
        self._labelTopo      = System.Windows.Forms.Label()
        self._panelEscape    = System.Windows.Forms.Panel()
        self._checkBoxEsc    = System.Windows.Forms.CheckBox()
        self._textBoxEntry   = System.Windows.Forms.TextBox()
        self._comboBoxEscape = System.Windows.Forms.ComboBox()
        self._labelEntry     = System.Windows.Forms.Label()
        self._labelEscape    = System.Windows.Forms.Label()
        
        self._panelPhyStruct.SuspendLayout()
        self._panelModel.SuspendLayout()
        self._panelEscape.SuspendLayout()
        self.SuspendLayout()
        #
        iProcesses    = EMK_finisher_GaN_config_v5.iProcesses
        iEncapsulant  = EMK_finisher_GaN_config_v5.iEncapsulant
        iEdgeType     = EMK_finisher_GaN_config_v5.iEdgeType
        iTopography   = EMK_finisher_GaN_config_v5.iTopography
        iBreakpoints  = EMK_finisher_GaN_config_v5.iBreakpoints
        #
        escape_mode_on = EMK_finisher_GaN_jobglobals_v5.escape_mode
        
       
        # OPENFILEDIALOGBROWSE - SETUP_FILE WIDGETS ================================================
        # 
        # openFileDialogBrowse   -   Setup file dialog initialization
        # 
        if( EMK_finisher_GaN_jobglobals_v5.escape_mode ):
            browse_pname = EMK_finisher_GaN_jobglobals_v5.start_dir
        else:
            browse_pname = EMK_finisher_GaN_jobglobals_v5.setup_pathname
        self._openSetupFileDialog.Filter           = "Setup files|*.setup|All files|*.*"
        self._openSetupFileDialog.InitialDirectory = browse_pname
        self._openSetupFileDialog.Title            = "Select setup file"
        self._openSetupFileDialog.FileOk          += self.OpenFile_SetupFilePickOk
        # self._openSetupFileDialog.FileOk          += self.OpenFile_SetupFilePickOk
        # self._openSetupFileDialog.FileCancel      += self.OpenFile_FilePickCancel
        # 
        # _buttonSetupFileBrowse   -   "browse for Setup file" button
        # 
        self._buttonSetupFileBrowse.Anchor   = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right
        self._buttonSetupFileBrowse.Location = System.Drawing.Point(600, 50)
        self._buttonSetupFileBrowse.Name     = "browsebutton_setupFilePathName"
        self._buttonSetupFileBrowse.Size     = System.Drawing.Size(60, 23)
        self._buttonSetupFileBrowse.TabIndex = 0
        self._buttonSetupFileBrowse.Text     = "Browse..."
        self._buttonSetupFileBrowse.UseVisualStyleBackColor = True
        self._buttonSetupFileBrowse.Click   += self.Button_SetupBrowseClick
        # self._buttonSetupFileBrowse.ButtonClick   += self.Button_SetupBrowseClick
        # 
        # textBoxBrowse   -   Setup file textbox
        # 
        self._textBoxSetupFileBrowse.Anchor   = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
        self._textBoxSetupFileBrowse.Location = System.Drawing.Point(34, 50)
        self._textBoxSetupFileBrowse.Name     = "textbox_setupFilePathName"
        self._textBoxSetupFileBrowse.Size     = System.Drawing.Size(550, 23)
        self._textBoxSetupFileBrowse.TabStop  = False
        # self._textBoxSetupFileBrowse.Text     = browse_pname
        self._textBoxSetupFileBrowse.Text     = EMK_finisher_GaN_jobglobals_v5.setup_pathname
        self._textBoxSetupFileBrowse.ReadOnly = True
        self._textBoxSetupFileBrowse.TextChanged += self.TextBoxBrowseTextChanged
        # 
        # labelBrowse   -   Setup file label
        # 
        self._labelBrowse.Location = System.Drawing.Point(34, 30)
        self._labelBrowse.Name     = "labelBrowse"
        self._labelBrowse.Size     = System.Drawing.Size(100, 15)
        self._labelBrowse.Text     = "Setup file"
        
        
        # INIT FILE VIEWERS  =======================================================================
        # 
        # labelA
        # 
        self._labelA.Location = System.Drawing.Point(45, 104)
        self._labelA.Name     = "labelA"
        self._labelA.Size     = System.Drawing.Size(100, 23)
        self._labelA.Text     = "GDS defn file"
        # self._labelA.Click   += self.LabelAClick
        # 
        # labelB
        # 
        self._labelB.Location = System.Drawing.Point(45, 139)
        self._labelB.Name     = "labelB"
        self._labelB.Size     = System.Drawing.Size(100, 23)
        self._labelB.Text     = "ILD defn file"
        # 
        # labelC
        # 
        self._labelC.Location = System.Drawing.Point(45, 174)
        self._labelC.Name     = "labelC"
        self._labelC.Size     = System.Drawing.Size(100, 23)
        self._labelC.Text     = "Material defn"
        # 
        # buttonA
        # 
        self._buttonA.Anchor       = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right
        self._buttonA.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
        self._buttonA.Enabled      = True
        self._buttonA.Location     = System.Drawing.Point(560, 98)
        self._buttonA.Name         = "buttonA"
        self._buttonA.Size         = System.Drawing.Size(100, 23)
        self._buttonA.TabIndex     = 1
        self._buttonA.Text         = "View GDS defn"
        self._buttonA.UseVisualStyleBackColor = True
        self._buttonA.Click       += self.ButtonAClick
        # 
        # buttonB
        # 
        self._buttonB.Anchor       = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right
        self._buttonB.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
        self._buttonB.Enabled      = True
        self._buttonB.Location     = System.Drawing.Point(560, 133)
        self._buttonB.Name         = "buttonB"
        self._buttonB.Size         = System.Drawing.Size(100, 23)
        self._buttonB.TabIndex     = 2
        self._buttonB.Text         = "View ILD defn"
        self._buttonB.UseVisualStyleBackColor = True
        self._buttonB.Click       += self.ButtonBClick
        # 
        # buttonC
        # 
        self._buttonC.Anchor       = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right
        self._buttonC.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
        self._buttonC.Enabled      = True
        self._buttonC.Location     = System.Drawing.Point(560, 168)
        self._buttonC.Name         = "buttonC"
        self._buttonC.Size         = System.Drawing.Size(100, 23)
        self._buttonC.TabIndex     = 3
        self._buttonC.Text         = "View Mat'l defn"
        self._buttonC.UseVisualStyleBackColor = True
        self._buttonC.Click       += self.ButtonCClick
        # 
        # textBoxA
        # 
        self._textBoxA.Anchor      = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
        self._textBoxA.Enabled     = True
        self._textBoxA.Location    = System.Drawing.Point(125, 100)
        self._textBoxA.Name        = "textBoxA"
        self._textBoxA.Size        = System.Drawing.Size(425, 20)
        self._textBoxA.ReadOnly    = True
        self._textBoxA.Text        = EMK_finisher_GaN_jobglobals_v5.gds_defn_pname
        # 
        # textBoxB
        # 
        self._textBoxB.Anchor      = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
        self._textBoxB.Enabled     = True
        self._textBoxB.Location    = System.Drawing.Point(125, 135)
        self._textBoxB.Name        = "textBoxB"
        self._textBoxB.Size        = System.Drawing.Size(425, 20)
        self._textBoxB.ReadOnly    = True
        self._textBoxB.Text        = EMK_finisher_GaN_jobglobals_v5.ild_defn_pname
        
        # de_info( "textBoxB = " + EMK_finisher_GaN_jobglobals_v5.ild_defn_pname, "after stuffing testBoxB" )
        
        # 
        # textBoxC
        # 
        self._textBoxC.Anchor      = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
        self._textBoxC.Enabled     = True
        self._textBoxC.Location    = System.Drawing.Point(125, 170)
        self._textBoxC.Name        = "textBoxC"
        self._textBoxC.Size        = System.Drawing.Size(425, 20)
        self._textBoxC.ReadOnly    = True
        self._textBoxC.Text        = EMK_finisher_GaN_jobglobals_v5.mat_defn_pname        
        
        # 
        # PHYSICAL STRUCTURE PANEL:      ===========================================================
        #     Metal system (display only) and Encapsulant ComboBox   
        # 
        # 
        # _labelPhyStruct - PHYSICAL STRUCTURE panel label
        # 
        self._labelPhyStruct.Location = System.Drawing.Point(34, 225)
        self._labelPhyStruct.Name     = "labelPhyStruct"
        self._labelPhyStruct.Size     = System.Drawing.Size(100, 23)
        self._labelPhyStruct.Text     = "Physical Structure"
        # self._labelPhyStruct.Click   += self.labelPhyStructClick
        # 
        # _labelIconn - INTERCONNECT PROCESS label
        # 
        self._labelIconn.ForeColor = System.Drawing.SystemColors.ControlText
        self._labelIconn.Location  = System.Drawing.Point(21, 14)
        self._labelIconn.Name      = "labelIconn"
        self._labelIconn.Size      = System.Drawing.Size(140, 18)
        self._labelIconn.Text      = "Interconnect Process"
        # self._labelIconn.Click    += self.labelIconnClick
        # 
        # _textBoxIconn - INTERCONNECT PROCESS (DISPLAY ONLY)
        # 
        self._textBoxIconn.Anchor   = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left
        self._textBoxIconn.Enabled  = False
        self._textBoxIconn.Location = System.Drawing.Point(21, 28)
        self._textBoxIconn.Name     = "textBoxIconn"
        self._textBoxIconn.Size     = System.Drawing.Size(140, 21)
        self._textBoxIconn.ReadOnly = True
        self._textBoxIconn.Text     = EMK_finisher_GaN_jobglobals_v5.interconnect
        # 
        # _labelEncap - ENCAPSULANT
        # 
        self._labelEncap.ForeColor = System.Drawing.SystemColors.ControlText
        self._labelEncap.Location  = System.Drawing.Point(21, 70)
        self._labelEncap.Name      = "labelEncap"
        self._labelEncap.Size      = System.Drawing.Size(140, 18)
        self._labelEncap.Text      = "Encapsulant"
        # self._labelEncap.Click    += self.Label2Click
        # 
        # _comboBoxEncap - ENCAPSULANT
        # 
        self._comboBoxEncap.DisplayMember     = "0"
        self._comboBoxEncap.DropDownStyle     = System.Windows.Forms.ComboBoxStyle.DropDownList
        self._comboBoxEncap.FormattingEnabled = True
        self._comboBoxEncap.Items.AddRange(System.Array[System.Object](iEncapsulant))
        self._comboBoxEncap.Location          = System.Drawing.Point(21, 84)
        self._comboBoxEncap.Name              = "comboBoxEncap"
        self._comboBoxEncap.Size              = System.Drawing.Size(140, 21)
        self._comboBoxEncap.TabIndex          = 6
        self._comboBoxEncap.SelectedIndex     = EMK_finisher_GaN_config_v5.iEncapsulant.index( EMK_finisher_GaN_jobglobals_v5.encapsulant )
        self._comboBoxEncap.SelectedIndexChanged += self.comboBoxEncapSelectedIndexChanged
        # 
        # _panelPhyStruct - PHYSICAL DEFN PANEL
        # 
        self._panelPhyStruct.BackColor            = System.Drawing.SystemColors.Control
        self._panelPhyStruct.BorderStyle          = System.Windows.Forms.BorderStyle.Fixed3D
        self._panelPhyStruct.Controls.Add(self._textBoxIconn)
        self._panelPhyStruct.Controls.Add(self._comboBoxEncap)
        self._panelPhyStruct.Controls.Add(self._labelIconn)
        self._panelPhyStruct.Controls.Add(self._labelEncap)
        self._panelPhyStruct.Controls.Add(self._labelPhyStruct)
        self._panelPhyStruct.ForeColor            = System.Drawing.SystemColors.MenuHighlight
        self._panelPhyStruct.Location             = System.Drawing.Point(34, 240)
        self._panelPhyStruct.Name                 = "panelPhyStruct"
        self._panelPhyStruct.Size                 = System.Drawing.Size(180, 132)
        self._panelPhyStruct.TabIndex             = 4

        # 
        # HFSS MODEL DEFINITION PANEL:      ========================================================
        #     {Planar|Conformal} (display only), and Edge Type ComboBox   
        # 
        # _labelModel - HFSS MODEL
        # 
        self._labelModel.Location = System.Drawing.Point(255, 225)
        self._labelModel.Name     = "labelModel"
        self._labelModel.Size     = System.Drawing.Size(146, 20)
        self._labelModel.Text     = "HFSS Model"
        # self._labelModel.Click   += self.labelModelClick
        # 
        # _labelTopo - STRUCTURE
        # 
        self._labelTopo.ForeColor = System.Drawing.SystemColors.ControlText
        self._labelTopo.Location  = System.Drawing.Point(21, 14)
        self._labelTopo.Name      = "labelTopo"
        self._labelTopo.Size      = System.Drawing.Size(140, 18)
        self._labelTopo.Text      = "Topography"
        # self._labelTopo.Click    += self.Label6Click
        # 
        # _textBoxTopo - display TOPOGRAPHY type
        # 
        self._textBoxTopo.Anchor   = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left
        self._textBoxTopo.Enabled  = False
        self._textBoxTopo.Location = System.Drawing.Point(21, 28)
        self._textBoxTopo.Name     = "textBoxTopo"
        self._textBoxTopo.Size     = System.Drawing.Size(140, 21)
        self._textBoxTopo.ReadOnly = True
        self._textBoxTopo.Text     = EMK_finisher_GaN_jobglobals_v5.topography
        # 
        # _labelEstyle - EDGE STYLE
        # 
        self._labelEstyle.ForeColor = System.Drawing.SystemColors.ControlText
        self._labelEstyle.Location  = System.Drawing.Point(21, 70)
        self._labelEstyle.Name      = "labelEstyle"
        self._labelEstyle.Size      = System.Drawing.Size(140, 18)
        self._labelEstyle.Text      = "Edge Style"
        # self._labelEstyle.Click    += self.Label2Click
        # 
        # _comboBoxEstyle - EDGE STYLE
        # 
        # self._comboBoxEstyle.DisplayMember     = "2"
        self._comboBoxEstyle.DropDownStyle     = System.Windows.Forms.ComboBoxStyle.DropDownList
        self._comboBoxEstyle.FormattingEnabled = False
        self._comboBoxEstyle.Items.AddRange(System.Array[System.Object](iEdgeType))
        self._comboBoxEstyle.Location          = System.Drawing.Point(21, 84)
        self._comboBoxEstyle.Name              = "comboBoxEstyle"
        self._comboBoxEstyle.Size              = System.Drawing.Size(140, 21)
        self._comboBoxEstyle.TabIndex          = 9
        self._comboBoxEstyle.SelectedIndex     = 0
        self._comboBoxEstyle.SelectedIndex     = EMK_finisher_GaN_config_v5.iEdgeType.index( EMK_finisher_GaN_jobglobals_v5.edge_style )
        self._comboBoxEstyle.Enabled           = False
        self._comboBoxEstyle.SelectedIndexChanged += self.comboBoxEncapSelectedIndexChanged
        # 
        # _panelModel - HFSS MODEL PANEL
        # 
        self._panelModel.BackColor   = System.Drawing.SystemColors.Control
        self._panelModel.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        self._panelModel.Controls.Add(self._comboBoxEstyle)
        self._panelModel.Controls.Add(self._textBoxTopo)
        self._panelModel.Controls.Add(self._labelEstyle)
        self._panelModel.Controls.Add(self._labelTopo)
        self._panelModel.ForeColor   = System.Drawing.SystemColors.MenuHighlight
        self._panelModel.Location    = System.Drawing.Point(255, 240)
        self._panelModel.Name        = "panelModel"
        self._panelModel.Size        = System.Drawing.Size(180, 132)
        self._panelModel.TabIndex    = 7
        
        # 
        # _panelEscape - ESCAPE MODE panel ===============================================================
        # 
        self._panelEscape.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        self._panelEscape.Controls.Add(self._comboBoxEscape)
        self._panelEscape.Controls.Add(self._textBoxEntry)
        self._panelEscape.Controls.Add(self._labelEscape)
        self._panelEscape.Controls.Add(self._labelEntry)
        self._panelEscape.Enabled  = False
        self._panelEscape.Location = System.Drawing.Point(475, 240)
        self._panelEscape.Name     = "panelEscape"
        self._panelEscape.Size     = System.Drawing.Size(180, 132)
        self._panelEscape.TabIndex = 10
        # 
        # checkBox1      --- TOGGLE ESCAPE MODE
        # 
        #   evaluate Q_debug_mode_on
        #       read progress parameters from design
        #   if debug_mode AND progress_ok
        #       init debug mode 
        #           determine exit breakpoint range
        #           update gui
        #   elif debug_mode AND (NOT progress_ok)
        #       reset debug mode
        #           update gui
        self._checkBoxEsc.Location        = System.Drawing.Point(475, 218 )      # self._checkBoxEsc.Checked
        self._checkBoxEsc.Name            = "checkBoxEscapeMode"
        self._checkBoxEsc.Size            = System.Drawing.Size( 120, 28)
        self._checkBoxEsc.TabIndex        = 11
        self._checkBoxEsc.Text            = "Escape Mode"
        self._checkBoxEsc.UseVisualStyleBackColor = True
        self._checkBoxEsc.Checked         = EMK_finisher_GaN_jobglobals_v5.escape_mode
        self._checkBoxEsc.CheckedChanged += self.CheckBoxEscCheckedChanged
        
        # de_info( "checkBoxEsc = " + repr( self._checkBoxEsc.Checked ), "dbg" )

        # 
        # textBox5 - ESCAPE MODE ENTRY POINT
        # 
        self._textBoxEntry.Location = System.Drawing.Point(21,28)
        self._textBoxEntry.Name     = "textBoxEntryPoint"
        self._textBoxEntry.Size     = System.Drawing.Size(64,21)
        self._textBoxEntry.TabIndex = 12
        self._textBoxEntry.Text     = repr( EMK_finisher_GaN_jobglobals_v5.iStart )
        self._textBoxEntry.ReadOnly = True
        self._textBoxEntry.TextChanged += self.TextBoxEntryTextChanged      #   is this necessary? might even be a problem.
                                                                            #   looks bogus - filed only set by this script, not the user
        # 
        # comboBox6 - ESCAPE MODE STOP POINT
        # 
        # de_info( "init comboBox for escape mode","dbg")
        self._comboBoxEscape.AllowDrop         = True
        self._comboBoxEscape.DropDownStyle     = System.Windows.Forms.ComboBoxStyle.DropDownList
        self._comboBoxEscape.Enabled           = True
        self._comboBoxEscape.FormattingEnabled = True
        # stopPointList = iBreakpoints[1:]
        # mystartpnt = self.str2int_BrPnt( EMK_finisher_GaN_jobglobals_v5.iStart )
        mystartpnt = str(EMK_finisher_GaN_jobglobals_v5.iStart)
        # de_info( "init 2 comboBox for escape mode\n\riBreakpoints = " + repr( iBreakpoints ) + "\n\rmystartpnt = " + repr(mystartpnt),"dbg")
        IstartPnt = iBreakpoints.index( mystartpnt )
        Ifirstavailstop = IstartPnt + 1
        newStopPointList = iBreakpoints[Ifirstavailstop:]
        # de_info( "init 3 comboBox for escape mode\n\rnewStopPointList = " + repr( newStopPointList ) + "\n\rmystartpnt = " + repr(mystartpnt),"dbg")
        self._comboBoxEscape.Items.AddRange(System.Array[System.Object](newStopPointList) )
        self._comboBoxEscape.Location          = System.Drawing.Point(21,84)
        self._comboBoxEscape.Name              = "comboBoxEscapePoint"
        self._comboBoxEscape.Size              = System.Drawing.Size(64,60)
        # self._comboBoxEscape.Sorted          = True
        self._comboBoxEscape.TabIndex          = 13
        self._comboBoxEscape.SelectedIndex     = len(newStopPointList)-1
        self._comboBoxEscape.SelectedIndexChanged += self.ComboBoxEscapeSelectedIndexChanged
        # de_info( "after init comboBox for escape mode","dbg")
        # 
        # _labelEntry - ESCAPE MODE ENTRY POINT
        # 
        self._labelEntry.ForeColor = System.Drawing.SystemColors.ControlText
        self._labelEntry.Location  = System.Drawing.Point(21,14)
        self._labelEntry.Name      = "labelEntry"
        self._labelEntry.Size      = System.Drawing.Size(140,18)
        self._labelEntry.Text      = "Entry Point"
        # self._labelEntry.Click    += self.Label7Click
        # 
        # label8 - ESCAPE MODE STOP POINT
        # 
        self._labelEscape.ForeColor = System.Drawing.SystemColors.ControlText
        self._labelEscape.Location  = System.Drawing.Point( 21,70)
        self._labelEscape.Name      = "labelEscape"
        self._labelEscape.Size      = System.Drawing.Size(140,18)
        self._labelEscape.Text      = "Exit Point"
        # self._labelEscape.Click    += self.Label7Click
        
        # 
        # JOB CONTROL BUTTONS: Cancel & Execute   ==================================================
        # 
        # _buttonExe  -  EXECUTE
        # 
        self._buttonExe.Anchor   = System.Windows.Forms.AnchorStyles.Bottom
        self._buttonExe.Location = System.Drawing.Point(400, 430)
        self._buttonExe.Enabled  = False
        self._buttonExe.Name     = "buttonExe"
        self._buttonExe.Size     = System.Drawing.Size(75, 23)
        self._buttonExe.TabIndex = 15
        self._buttonExe.Text     = "Execute"
        self._buttonExe.UseVisualStyleBackColor = True
        self._buttonExe.Click   += self.mainExecuteClick
        # 
        # _buttonCancel  -  CANCEL    Run Away!! Run Away!!
        # 
        self._buttonCancel.Anchor   = System.Windows.Forms.AnchorStyles.Bottom
        self._buttonCancel.Location = System.Drawing.Point(200, 430)
        self._buttonCancel.Name     = "buttonCancel"
        self._buttonCancel.Size     = System.Drawing.Size(75, 23)
        self._buttonCancel.TabIndex = 14
        self._buttonCancel.Text     = "Cancel"
        self._buttonCancel.UseVisualStyleBackColor = True
        self._buttonCancel.Click   += self.mainCancelClick
        # 
        # HANDLE ESCAPE MODE    ====================================================================
        
        # de_info( "init @ HANDLE ESCAPE MODE","dbg")
        
        if( EMK_finisher_GaN_jobglobals_v5.escape_mode == True ):
            
            # de_info( "inside HANDLE ESCAPE MODE\n\rcalling set_escape_mode","dbg")
            
            self.set_escape_mode( )
            #
            #
            # ERROR CHECK SETUP GOES HERE
            #
            #
            self._buttonExe.Enabled  = True
        else:
            self.clear_escape_mode( )

        # 
        # AND NOW ... THE MAIN EVENT    ============================================================
        # 
        # MainForm
        # 
        
        # de_info( "init @ THE MAIN EVENT","dbg")
        
        self.ClientSize = System.Drawing.Size(700, 500)
        self.Controls.Add(self._buttonSetupFileBrowse)
        self.Controls.Add(self._textBoxSetupFileBrowse)
        self.Controls.Add(self._labelBrowse)
        self.Controls.Add(self._buttonCancel)
        self.Controls.Add(self._buttonExe)
        self.Controls.Add(self._panelModel)
        self.Controls.Add(self._labelModel)
        self.Controls.Add(self._panelPhyStruct)
        self.Controls.Add(self._labelPhyStruct)
        self.Controls.Add(self._panelEscape)
        self.Controls.Add(self._checkBoxEsc)
        
        self.Controls.Add(self._textBoxA)
        self.Controls.Add(self._textBoxB)
        self.Controls.Add(self._textBoxC)
        self.Controls.Add(self._buttonA)
        self.Controls.Add(self._buttonB)
        self.Controls.Add(self._buttonC)
        self.Controls.Add(self._labelA)
        self.Controls.Add(self._labelC)
        self.Controls.Add(self._labelB)
        
        # self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog
        self.Name = "MainForm"
        script_ID_version = EMK_finisher_GaN_config_v5.script_name + " " + EMK_finisher_GaN_config_v5.script_version
        self.Text = script_ID_version
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.MaximumSize = System.Drawing.Size(1200, 800)
        self.MinimumSize = System.Drawing.Size(700, 500)
        self.CenterToScreen()
        
        self._panelPhyStruct.ResumeLayout(False)
        self._panelModel.ResumeLayout(False)
        self._panelEscape.ResumeLayout(False)
        self.ResumeLayout(False)
        
        # de_info("here we go...","dbg")
        
        
        
        
    def errorcheck_setup_and_populate_GUI( self ):  
        # - THIS ROUTINE DOES ERROR CHECKING ON THE SETUP THAT EXISTS IN THE VARIABLES OF THE GLOBALS 
        #     MODULE.
        # - THIS ROUTINE BELONGS TO 'MAIN_FORM', SO THERE IS ALWAYS AN ACTIVE GUI WHENEVER THIS RUNS.
        # - ERRORS FOUND BY THIS CHECK ARE REPORTED USING CHANGES TO THE GUI DISPLAY ITSELF, AND/OR 
        #     POP-UP MESSAGE BOXES.
        # - THIS ROUTINES OPERATES ON THE DATA IN THE GLOBALS & CONFIG MODULES; IT'S INTENDED TO BE 
        #     CALLED AFTER THE START-UP OF A NEW JOB (i.e. after self.read_setup_from_files), OR AFTER  
        #     READING DESIGN VARIABLES WHEN RESUMING A JOB (i.e. after __MAIN__.sendvars_actdsn2globals)
        # - REMEMBER: THIS ROUTINE EXECUTES AFTER READ FROM FILES, OR DURING A RESUME. SOME ERROR CHECKS  
        #     MAY NOT MAKE SENSE IF YOU CONSIDER ONLY ONE OF THOSE SCENARIOS. DON'T ASS.U.ME
        
        # de_info("Milepost 0","dbg")
        ok_so_far = True
        setup_ok  = True
        
        specified_dir = False
        specified_gds = False
        specified_ild = False
        specified_mat = False
        
        have_dir = False
        have_gds = False
        have_mat = False
        have_ild = False

        found_interconnect = False
        found_topography   = False

        # //debug -----------------
        # MessageBox.Show( "Entered", "errorcheck_setup_and_populate_GUI" )
        # //debug -----------------
        
        msg_title   = "Setup Error"
        nl = "\n\r"
        SETUP_ERROR = 1
                
        matchesA = self.Controls.Find("textBoxA", True);
        matchesB = self.Controls.Find("textBoxB", True);
        matchesC = self.Controls.Find("textBoxC", True);
        wtf_textBoxA = matchesA[0]
        wtf_textBoxB = matchesB[0]
        wtf_textBoxC = matchesC[0]
        wtf_textBoxA.Text = ''
        wtf_textBoxB.Text = ''
        wtf_textBoxC.Text = ''

        # //debug -----------------
        # MessageBox.Show( "Mark1", "errorcheck_setup_and_populate_GUI" )
        # //debug -----------------

        matchesSUF         = self.Controls.Find("textbox_setupFilePathName", True);
        textBox_setupfile  = matchesSUF[0]
        matches_buttonExe  = self.Controls.Find("buttonExe", True);
        wtf_buttonExe      = matches_buttonExe[0];
        wtf_buttonExe.Enabled = False

        # de_info("Milepost 1","dbg")
        # ------------------------
        # 1. verify specified setup file: in case of error - return to GUI loop immediately
        mySetupfilePathName = EMK_finisher_GaN_jobglobals_v5.setup_pathname
        # self._textBoxSetupFileBrowse = mySetupfilePathName
        if ( os.path.isfile(mySetupfilePathName) ):
            textBox_setupfile.ForeColor = System.Drawing.SystemColors.ControlText
            textBox_setupfile.BackColor = System.Drawing.SystemColors.Control
            pass
        else:
            EMK_finisher_GaN_jobglobals_v5.setup_ok = False
            textBox_setupfile.ForeColor = Color.Red
            textBox_setupfile.BackColor = Color.LemonChiffon
            msg_content = "Specified Setup file pathname does not point to a file."
            MessageBox.Show( msg_content, msg_title )
            return SETUP_ERROR

            
        # de_info("Milepost 2","dbg")
        # ------------------------
        # 2. open specified setup file: in case of error - return to GUI loop immediately
        try:
            fsetupfile = open( mySetupfilePathName, 'r' )
        except:
            EMK_finisher_GaN_jobglobals_v5.setup_ok = False
            textBox_setupfile.ForeColor   = Color.Red
            textBox_setupfile.BackColor   = Color.LemonChiffon
            msg_content = "Unable to open specified Setup file."
            MessageBox.Show( msg_content, msg_title )
            return SETUP_ERROR

        
        # ERRORS ENCOUNTERED UP TO THIS POINT TRIGGERED AN ESCAPE FROM THIS ROUTINE.
        # SO IF WE ARE STILL HERE, NO ERRORS.
        # FROM THIS POINT ON, WILL ACCUMULATE WITHOUT EXITING. 
        # THEN REPORT THE ERRORS AS A GROUP    
    
                            # matches = self.Controls.Find("textBoxA", True);
                            # wtf_textBoxA = matches[0]

        # de_info("Milepost 3","dbg")
        # ------------------------
        # 3. get techdir, verify that it is a directory 
        err_msg = ''
        if( os.path.isdir(EMK_finisher_GaN_jobglobals_v5.tech_dir) ):
            have_dir = True
            tech_dir = EMK_finisher_GaN_jobglobals_v5.tech_dir
            textBox_setupfile.ForeColor = System.Drawing.SystemColors.ControlText
            textBox_setupfile.BackColor = System.Drawing.SystemColors.Control
            wtf_textBoxA.ForeColor = System.Drawing.SystemColors.ControlText
            wtf_textBoxA.BackColor = System.Drawing.SystemColors.Control
            wtf_textBoxB.ForeColor = System.Drawing.SystemColors.ControlText
            wtf_textBoxB.BackColor = System.Drawing.SystemColors.Control
            wtf_textBoxC.ForeColor = System.Drawing.SystemColors.ControlText
            wtf_textBoxC.BackColor = System.Drawing.SystemColors.Control
            # de_info("its a dir alright!","tech dir check: good")
        else:
            textBox_setupfile.ForeColor = Color.Red
            textBox_setupfile.BackColor = Color.LemonChiffon
            wtf_textBoxA.ForeColor = Color.Red
            wtf_textBoxA.BackColor = Color.LemonChiffon
            wtf_textBoxB.ForeColor = Color.Red
            wtf_textBoxB.BackColor = Color.LemonChiffon
            wtf_textBoxC.ForeColor = Color.Red
            wtf_textBoxC.BackColor = Color.LemonChiffon
            err_msg = err_msg + nl + "Bad tech directory specified."
            # de_info("whazzit?","tech dir check: bad")
            MessageBox.Show( err_msg, "Setup error(s)" )
            return SETUP_ERROR
            

        # de_info("Milepost 4.a","dbg")
        # ------------------------
        # 4.a. verify that files have been specified 
        err_msg = ''
        if have_dir:
        
            if( len( EMK_finisher_GaN_jobglobals_v5.gds_defn_file ) > 0 ):
                specified_gds = True
            if( len( EMK_finisher_GaN_jobglobals_v5.ild_defn_file ) > 0 ):
                specified_ild = True
            if( len( EMK_finisher_GaN_jobglobals_v5.mat_defn_file ) > 0 ):
                specified_mat = True
            
            if( specified_gds ):
                # gds_defn_pname = tech_dir + '\\' + EMK_finisher_GaN_jobglobals_v5.gds_defn_file
                gds_defn_pname = EMK_finisher_GaN_jobglobals_v5.gds_defn_pname
                
                wtf_textBoxA.Text = gds_defn_pname
                wtf_textBoxA.ForeColor = System.Drawing.SystemColors.ControlText
                wtf_textBoxA.BackColor = System.Drawing.SystemColors.Control
                # de_info("have gds","defn files check: good")
            else:
                wtf_textBoxA.ForeColor = Color.Red
                wtf_textBoxA.BackColor = Color.LemonChiffon
                err_msg = err_msg + nl + "Valid gds_defn_file pathname not found."
                # de_info("no gds defn for you","defn files check: bad")
    
            if( specified_ild ):
                ild_defn_pname = tech_dir + '\\' + EMK_finisher_GaN_jobglobals_v5.ild_defn_file
                wtf_textBoxB.Text = ild_defn_pname
                wtf_textBoxB.ForeColor = System.Drawing.SystemColors.ControlText
                wtf_textBoxB.BackColor = System.Drawing.SystemColors.Control
                # de_info("have ild","defn files check: good")
            else:
                wtf_textBoxB.ForeColor = Color.Red
                wtf_textBoxB.BackColor = Color.LemonChiffon
                err_msg = err_msg + nl + "Valid ild_defn_file pathname not found."
                # de_info("no ild defn for you","defn files check: bad")
    
            if( specified_mat ):
                mat_defn_pname = tech_dir + '\\' + EMK_finisher_GaN_jobglobals_v5.mat_defn_file
                wtf_textBoxC.Text = mat_defn_pname
                wtf_textBoxC.ForeColor = System.Drawing.SystemColors.ControlText
                wtf_textBoxC.BackColor = System.Drawing.SystemColors.Control
                # de_info("have mats","defn files check: good")
            else:
                wtf_textBoxC.ForeColor = Color.Red
                wtf_textBoxC.BackColor = Color.LemonChiffon
                err_msg = err_msg + nl + "Valid mat_defn_file pathname not found."
                # de_info("no mats defn for you","defn files check: bad")
    
            # MessageBox.Show( msg_content, msg_title )
            if ( not ( have_dir and specified_gds and specified_ild and specified_mat ) ):
                MessageBox.Show( err_msg, "Setup file error(s)" )
                return SETUP_ERROR
            

        # de_info("Milepost 4.b","dbg")
        # ------------------------
        # 4.b. verify that specified files exist 
        if have_dir:
            
            if( os.path.isfile(gds_defn_pname) ):
                have_gds = True
                tech_dir = EMK_finisher_GaN_jobglobals_v5.tech_dir
                wtf_textBoxA.ForeColor = System.Drawing.SystemColors.ControlText
                wtf_textBoxA.BackColor = System.Drawing.SystemColors.Control
                # de_info("have gds","defn files check: good")
            else:
                have_gds = False
                wtf_textBoxA.ForeColor = Color.Red
                wtf_textBoxA.BackColor = Color.LemonChiffon
                err_msg = err_msg + nl + "Valid gds_defn_file pathname not found."
                # de_info("no gds defn for you","defn files check: bad")
    
            if( os.path.isfile(ild_defn_pname) ):
                have_ild = True
                wtf_textBoxB.ForeColor = System.Drawing.SystemColors.ControlText
                wtf_textBoxB.BackColor = System.Drawing.SystemColors.Control
                # de_info("have ild","defn files check: good")
            else:
                have_ild = False
                wtf_textBoxB.ForeColor = Color.Red
                wtf_textBoxB.BackColor = Color.LemonChiffon
                err_msg = err_msg + nl + "Valid ild_defn_file pathname not found."
                # de_info("no ild defn for you","defn files check: bad")
    
            if( os.path.isfile(mat_defn_pname) ):
                have_mat = True
                wtf_textBoxC.ForeColor = System.Drawing.SystemColors.ControlText
                wtf_textBoxC.BackColor = System.Drawing.SystemColors.Control
                # de_info("have mats","defn files check: good")
            else:
                have_mat = False
                wtf_textBoxC.ForeColor = Color.Red
                wtf_textBoxC.BackColor = Color.LemonChiffon
                err_msg = err_msg + nl + "Valid mat_defn_file pathname not found."
                # de_info("no mats defn for you","defn files check: bad")
    
            # MessageBox.Show( msg_content, msg_title )
            if ( not ( have_dir and have_gds and have_ild and have_mat ) ):
                MessageBox.Show( err_msg, "Setup file error(s)" )
                return SETUP_ERROR

        
        # de_info("Milepost 5","dbg")
        # ------------------------
        # 5. verify that specified definition files can be opened 
        err_msg = ''
        if (have_dir and have_gds):
            try:
                test_gds_defn = open( gds_defn_pname, 'r' )
                test_gds_defn.close()
                have_gds = True
            except:
                err_msg = err_msg + nl + "Unable to open file at specified gds_defn_file pathname."
                have_gds = False
            
        if (have_dir and have_ild):
            try:
                test_ild_defn = open( ild_defn_pname, 'r' )
                test_ild_defn.close()
                have_ild = True
            except:
                err_msg = err_msg + nl + "Unable to open file at specified ild_defn_file pathname."
                have_ild = False

        if (have_dir and have_mat):
            try:
                test_mat_defn = open( mat_defn_pname, 'r' )
                test_mat_defn.close()
                have_mat = True
            except:
                err_msg = err_msg + nl + "Unable to open file at specified mat_defn_file pathname."
                have_mat = False

        if ( not ( have_dir and have_gds and have_ild and have_mat ) ):
            MessageBox.Show( err_msg, "Setup error(s)" )
            return SETUP_ERROR
            
            
        # de_info("Milepost 6","dbg")
        # ------------------------
        # 6. read INTERCONNECT and TOPOGRAPHY from gds_defn_file
        err_msg = ''
        iProcesses  = EMK_finisher_GaN_config_v5.iProcesses
        iTopography = EMK_finisher_GaN_config_v5.iTopography
        if (have_dir and have_gds):
            topo    = fetch_textfile_value( gds_defn_pname, "TOPOGRAPHY" )
            connect = fetch_textfile_value( gds_defn_pname, "INTERCONNECT" )
            if( connect in iProcesses ):
                self._textBoxIconn.Text = connect
                found_interconnect = True
            else:
                self._textBoxIconn.Text = None
                err_msg = err_msg + nl + "gds_defn_file should specify interconnect type. Not found."
                found_interconnect = False
            
            if( topo in iTopography ):
                self._textBoxTopo.Text = topo
                found_topography = True
            else:
                self._textBoxTopo.Text = None
                err_msg = err_msg + nl + "gds_defn_file should specify topography type. Not found."
                found_topography = False

            # de_info("found_interconnect = " + repr(found_interconnect), "dbg")
            # de_info("found_topography = "   + repr(found_topography),   "dbg")
            
            if ( not ( found_interconnect and found_topography ) ):
                wtf_textBoxA.ForeColor = Color.Red
                wtf_textBoxA.BackColor = Color.LemonChiffon
                MessageBox.Show( err_msg, "Setup error(s)" )
                return SETUP_ERROR

                
        setup_ok = True  
        setup_ok = setup_ok and have_gds and have_mat and have_ild 
        setup_ok = setup_ok and found_interconnect and found_topography
        
        EMK_finisher_GaN_jobglobals_v5.setup_ok = setup_ok
        
        # fill remainder of GUI form
        # de_info("here is. setting textBoxIconn","dbg")
        matches_textBoxIconn   = self.Controls.Find("textBoxIconn", True);
        wtf_textBoxIconn       = matches_textBoxIconn[0];
        wtf_textBoxIconn.Text  = EMK_finisher_GaN_jobglobals_v5.interconnect
        
        matches_comboBoxEncap  = self.Controls.Find("comboBoxEncap", True);
        wtf_comboBoxEncap      = matches_comboBoxEncap[0];
        wtf_comboBoxEncap.Text = EMK_finisher_GaN_jobglobals_v5.encapsulant
        
        matches_textBoxTopo    = self.Controls.Find("textBoxTopo", True);
        wtf_textBoxTopo        = matches_textBoxTopo[0];
        wtf_textBoxTopo.Text   = EMK_finisher_GaN_jobglobals_v5.topography
        
        matches_comboBoxEstyle  = self.Controls.Find("comboBoxEstyle", True);
        wtf_comboBoxEstyle      = matches_comboBoxEstyle[0];
        estyle = EMK_finisher_GaN_jobglobals_v5.edge_style
        Istyle = EMK_finisher_GaN_config_v5.iEdgeType.index( estyle )
        
        nl = "\n\r"
        # de_info( 
            # "estyle = " + repr(estyle) + nl +
            # "Istyle = " + repr(Istyle) + nl
            # , "dbg" )
        
        
        # de_info("Milepost 9","dbg")
        if( wtf_textBoxTopo.Text == "Planar" ):
            estyle = "Square"
            Istyle = EMK_finisher_GaN_config_v5.iEdgeType.index( estyle )
            wtf_comboBoxEstyle.Enabled           = False 
            wtf_comboBoxEstyle.FormattingEnabled = False
            wtf_comboBoxEstyle.SelectedIndex     = Istyle         # square corners, user locked out
            # de_info( 
                # "estyle = " + repr(estyle) + nl +
                # "Istyle = " + repr(Istyle) + nl
                # , "wtf_textBoxTopo == Planar" )
            
            
        elif ( wtf_textBoxTopo.Text == "Conformal" ):
            estyle = "Chamfered"
            Istyle = EMK_finisher_GaN_config_v5.iEdgeType.index( estyle )
            wtf_comboBoxEstyle.Enabled           = False 
            wtf_comboBoxEstyle.FormattingEnabled = False
            wtf_comboBoxEstyle.SelectedIndex     = Istyle         # chamfered corners, only option available for GaN
            # de_info( 
                # "estyle = " + repr(estyle) + nl +
                # "Istyle = " + repr(Istyle) + nl
                # , "wtf_textBoxTopo == Conformal" )
            
                
        escmode = EMK_finisher_GaN_jobglobals_v5.escape_mode
        if (escmode == 0):
            self.clear_escape_mode(  )
        else:
            self.set_escape_mode(  )
        
        matches_buttonExe  = self.Controls.Find("buttonExe", True);
        wtf_buttonExe      = matches_buttonExe[0];
        if setup_ok:
            wtf_buttonExe.Enabled = True
            return 0
        else:
            wtf_buttonExe.Enabled = False
            return SETUP_ERROR        
        return 0        
        
        
    def clear_escape_mode( self ):
        self._panelEscape.Enabled    = False  
        self._textBoxIconn.Enabled   = True     # Enabled, but not editable
        self._comboBoxEncap.Enabled  = True
        EMK_finisher_GaN_jobglobals_v5.escape_mode = False
        # is_planar = (self._textBoxTopo.Text == "Planar")
        is_conformal = (self._textBoxTopo.Text == "Conformal")
        if is_conformal:
            self._comboBoxEstyle.Enabled = True
            # de_info("is_conformal == True","dbg")
        else:
            self._comboBoxEstyle.Enabled = False
            # de_info("is_conformal == False","dbg")
        self._textBoxTopo.Enabled    = True     # Enabled, but not editable
        self._buttonSetupFileBrowse.Enabled  = True
        # self._textBoxSetupFileBrowse.Enabled = False          ## DOESN'T WORK!??! sumpin hinky about this
        # matches_testBox_SUF = self.Controls.Find("textbox_setupFilePathName", True);
        # wtf_testBox_SUF     = matches_testBox_SUF[0];
        # wtf_testBox_SUF.Enabled = True
        return 0    
    
    
    def set_escape_mode( self ):
        self._panelEscape.Enabled    = True   
        self._textBoxIconn.Enabled   = False
        self._comboBoxEncap.Enabled  = False
        self._comboBoxEstyle.Enabled = False
        self._textBoxTopo.Enabled    = False
        self._buttonSetupFileBrowse.Enabled  = False
        EMK_finisher_GaN_jobglobals_v5.escape_mode = True
        # read progress bar and convert to breakpoint
        # set iStart and iStop
        # de_info( "iBreakpoints = " + repr(EMK_finisher_GaN_config_v5.iBreakpoints),"dbg" )
        Ibp = EMK_finisher_GaN_config_v5.iBreakpoints
        PBtxt = str(EMK_finisher_GaN_jobglobals_v5.progress_bar)
        Indx_resume_istart = Ibp.index( PBtxt )
        # de_info( "Indx_resume_istart = " + repr(Indx_resume_istart) + "\n\rIbp[ Indx_resume_istart ] = " + repr(Ibp[ Indx_resume_istart ]),"dbg" )
        self._textBoxEntry.Text = Ibp[ Indx_resume_istart ]
        # de_info( "self._textBoxEntry.Text = " + repr(self._textBoxEntry.Text), "dbg" )
        Indx_firstavailstop  = Indx_resume_istart + 1
        # de_info( "set_escape_mode\n\rIndx_firstavailstop = " + repr(Indx_firstavailstop),"dbg")        
        newStopPointList = Ibp[ Indx_firstavailstop: ]
        # de_info( "set_escape_mode\n\rnewStopPointList = " + repr(newStopPointList),"dbg")
        
        self._comboBoxEscape.Items.Clear()
        self._comboBoxEscape.Items.AddRange(System.Array[System.Object](newStopPointList) )  
        self._comboBoxEscape.SelectedIndex = len( newStopPointList ) - 1
        # if (iBPstop <= resume_istart):
            # self._comboBoxEscape.SelectedItem = resume_istart + 1
        self._textBoxEntry.Enabled   = True     # Enabled, but not editable
        self._comboBoxEscape.Enabled = True
        return 0        
        
        
    def mainExecuteClick(self, sender, e):                          #   =================== Execute
        EMK_finisher_GaN_jobglobals_v5.edge_style    = self._comboBoxEstyle.Text 
        EMK_finisher_GaN_jobglobals_v5.encapsulant   = self._comboBoxEncap.Text
        # EMK_finisher_GaN_jobglobals_v5.interconnect  = self._textBoxIconn.Text
        # EMK_finisher_GaN_jobglobals_v5.topography    = self._textBoxTopo.Text 
        EMK_finisher_GaN_jobglobals_v5.user_ok       = True        #   == need user_ok AND setup_ok to proceed
        breakpoint1 = self._textBoxEntry.Text
        breakpoint2 = self._comboBoxEscape.Text
        EMK_finisher_GaN_jobglobals_v5.iStart         = self.str2int_BrPnt( breakpoint1 )
        EMK_finisher_GaN_jobglobals_v5.iStop          = self.str2int_BrPnt( breakpoint2 )
        # EMK_finisher_GaN_jobglobals_v5.setup_pathname = self._textBoxSetupFileBrowse.Text
        
        self.Close()

 
    def CheckBoxEscCheckedChanged(self, sender, e):               #   =================== Escape Mode Checkbox
        # if checkbox is now checked 
        #      if ( (setup_is_valid) AND (progbar == 0) )
        #           set debug_mode
        #      elif ( (setup_is_valid) AND (progbar != 0) )
        #           reverse checkbox
        #           message 'no can do'
        #      elif ( NOT setup_is_valid )
        #           reverse checkbox
        #           message 'no can do'
        # elif checkbox is NOT checked
        #      if ( (debug_mode) AND (progbar == 0) )
        #           clear debug mode
        #           disable panel
        #      elif ( (setup_is_valid) AND (progbar != 0) )
        #           reverse checkbox
        #           message 'no can do, cannot exit debug mode, job in progress'
        #      elif ( NOT setup_is_valid )
        #           reverse checkbox
        #           message 'no can do'
        # if (not self._checkBoxEsc.Focused):
            # return
        if( not sender is self._checkBoxEsc ):    # otherwise changes from code cause inf loop
            return
        currentCheckBoxState = self._checkBoxEsc.Checked
        self.setup_is_valid()
        self.run_in_progress()
        # iStart = EMK_finisher_GaN_jobglobals_v5.iStart
        if ( currentCheckBoxState and not EMK_finisher_GaN_jobglobals_v5.setup_ok ):
        # if ( currentCheckBoxState ):
            msg_content = "Cannot enter escape mode because setup is not valid."
            msg_title   = "Error"
            MessageBox.Show( msg_content, msg_title )
            self._checkBoxEsc.Checked = False
        elif ( (not currentCheckBoxState) and ( EMK_finisher_GaN_jobglobals_v5.progress_bar != 0 ) ):
            msg_content = "Cannot exit escape mode. Script has already been started."
            msg_title   = "Error"
            MessageBox.Show( msg_content, msg_title )
            self._checkBoxEsc.Checked = True
        elif ( not currentCheckBoxState ):
            self.clear_escape_mode(  )
            # self._panelEscape.Enabled = False  
            # self._textBoxIconn.Enabled = True
            # self._comboBoxEncap.Enabled = True
            # self._comboBoxEstyle.Enabled = True
            # self._textBoxTopo.Enabled = True
            # self._buttonSetupFileBrowse.Enabled  = True
            # self._textBoxSetupFileBrowse.Enabled = True
        elif ( currentCheckBoxState ):    
            self.set_escape_mode(  )
            # self._panelEscape.Enabled = True   
            # self._textBoxIconn.Enabled = False
            # self._comboBoxEncap.Enabled = False
            # self._comboBoxEstyle.Enabled = False
            # self._textBoxTopo.Enabled = False
            # self._buttonSetupFileBrowse.Enabled  = False
            # self._textBoxSetupFileBrowse.Enabled = False
        else:
            msg_content = "Error 74911 in routine CheckBoxEscCheckedChanged"
            msg_title   = "Programming error"
            MessageBox.Show( msg_content, msg_title )

            
    def comboBoxEncapSelectedIndexChanged(self, sender, e):
        pass

        
    def TextBoxEntryTextChanged(self, sender, e):
        pass
 

    def ComboBoxEscapeSelectedIndexChanged(self, sender, e):
        global iBreakpoints
        if (not self._comboBoxEscape.Focused):
            return
        pass
        #
        # when i was setting start and stop:
        #
        # currentStartValue = self._comboBox5.SelectedItem
        # newStopValue      = self._comboBoxEscape.SelectedItem
        # newStartRange     = iBreakpoints[ :iBreakpoints.index(newStopValue) ]     #  python code asymmetry (compare newStopRange)
        # indexOfStartInNewStartRange = newStartRange.index(currentStartValue)
        # self._comboBox5.Items.Clear()
        # self._comboBox5.Items.AddRange( System.Array[System.Object](newStartRange) )
        # self._comboBox5.SelectedIndex = indexOfStartInNewStartRange
        
    def OpenFile_SetupFilePickOk(self, sender, e):
        # this routine reads the input files and sets up the variables in the globals module
        # it is expected to be called for a new run only - not resumed runs
        #
        # this routine gets called when the user presses the OK button in the setup file browser dialog box.
        # the job here is to 
        #   1.  verify specified setup file: if error, set so_far_ok to False
        #   2.  open specified setup file: if error, set so_far_ok to False
        #   3.  read definition filenames, techdir
        #   4.  open gdsii definition file: if error, incr Nerr, append notice to errmsg
        #   5.  Parse GDS definition file for
        #       5a. INTERCONNECT  2LM|2LM-no_airbridge
        #       5b. TOPOGRAPHY    Planar|conformal
        #       5c. UNITS         nm
        #       5d. populate GUI form with INTERCONNECT, TOPOGRAHY
        #   6.  open ILD definition file: if error, incr Nerr, append notice to errmsg
        #   7.  open MAT definition file: if error, incr Nerr, append notice to errmsg
        #   8.  if error, display errmsg and return to GUI loop
        #   9.  populate globals
        #   10. return to GUI loop

        if( self._openSetupFileDialog.ShowDialog() == DialogResult.OK):
            self._textBoxA.Text = ''        
            self._textBoxB.Text = ''        
            self._textBoxC.Text = ''
            self._textBoxIconn.Text   = ''
            self._textBoxTopo.Text = ''
            self._textBoxSetupFileBrowse.Text = self._openSetupFileDialog.FileName
            
            setup_ok = self.read_setup_from_files( )
            self.errorcheck_setup_and_populate_GUI( )
        else:
            self._openSetupFileDialog.Dispose()

            
    def evaluate_setup( self ):
        # starting from global variables module, evaluate setup:
        #       setup_file exists?
        #       setup_file valid?
        #       tech_dir exists?
        #       gds_defn_file exists?
        #       ild_defn_file exists?
        #       mat_defn_file exists?
        #       gds_defn_file specifies TOPOLOGY?
        #       gds_defn_file specifies INTERCONNECT?
        #       
        dmy = EMK_finisher_GaN_jobglobals_v5.escape_mode
        return [0, "setup OK"]
        # return [1, "yo, Macbeth, your breath smells like death"]
        
    def Button_SetupBrowseClick(self, sender, e):
        # fetchSetupFile = self._openSetupFileDialog.ShowDialog()
        fetchSetupFile = OpenFileDialog()
        fetchSetupFile.Filter = "Setup files|*.setup|All files|*.*"
        # msg_content = "At  Button_SetupBrowseClick.\n\rfetchSetupFile = " + repr(fetchSetupFile)
        # msg_title   = "dbg"
        # MessageBox.Show( msg_content, msg_title )
        
        # if( fetchSetupFile == System.Windows.Forms.DialogResult.OK ):
        if fetchSetupFile.ShowDialog(self) == DialogResult.OK:
            # assuming setup_file selection is valid
            
            # not sure why i need to do this, but I do.
            # problems arose if the user choose a file, then choose again before executing.
            # the first pass, I could use this >>    self._textBoxSetupFileBrowse.Text = setupfilepathname         
            # but on the second pass this lead to errors.
            # f me
            matches = self.Controls.Find("textbox_setupFilePathName", True);
            textBox_setupfile = matches[0]

            textBox_setupfile.ForeColor = System.Drawing.SystemColors.WindowText
            textBox_setupfile.BackColor = System.Drawing.SystemColors.Control
            setupfilepathname = fetchSetupFile.FileName
            # msg_content = "After browse for setup file pick.\n\rclicked OK.\n\rsetupfilepathname = " + setupfilepathname
            # msg_content = msg_content + "\n\r self = " + repr(self)
            # msg_title   = "dbg"
            # MessageBox.Show( msg_content, msg_title )
            textBox_setupfile.Text = setupfilepathname
            
            
            
            
            # de_info( "before read_setup_from_files.\n\rsetupfilepathname = " + setupfilepathname,"dbg")
            setup_ok = self.read_setup_from_files( setupfilepathname )
            # de_info( "after read_setup_from_files\n\rbefore errorcheck_setup_and_populate_GUI","dbg")
            self.errorcheck_setup_and_populate_GUI( )
        else:
            fetchSetupFile.Dispose()
            msg_content = "User canceled setup file selection"
            # msg_content = msg_content + "\n\r self = " + repr(self)
            msg_title   = "dbg"
            # MessageBox.Show( msg_content, msg_title )
            # return   # for now

            
        # err_flag, err_mess = self.read_setup()
        err_flag, err_mess = self.evaluate_setup()
        if( err_flag == 0 ):
            pass
            # msg_content = err_mess
            # msg_title   = "dbg"
            # MessageBox.Show( msg_content, msg_title )
        else:
            msg_content = err_mess
            msg_title   = "dbg"
            MessageBox.Show( msg_content, msg_title )
           
        # check setup.
        
    def TextBoxBrowseTextChanged(self, sender, e):
        pass
    

    def ButtonAClick( self, sender, e ):        
        fA_pname = self._textBoxA.Text
        if ( os.path.isfile(fA_pname) ):        #   <- real programmers would go nuts if they saw this. here's hoping they dont see it
            fAstream = open( fA_pname, 'r' )
            fAtxt = fAstream.readlines()
            fA = EMK_viewTextFile.Form1()
            nl = "\r\n"
            fA._fileInfo.Text = "File: " + fA_pname
            fA._textBox1.Text = nl.join( fAtxt )
            fA._textBox1.Select(0,0)
            fA.Text = "GDSII definition file"
            fA.Show()
        else:
            msg_content = "   Unable to open GDSII definition file for viewing."
            msg_title   = "Error"
            MessageBox.Show( msg_content, msg_title )

            
    def ButtonBClick(self, sender, e):
        fB_pname = self._textBoxB.Text
        if ( os.path.isfile(fB_pname) ):
            fBstream = open( fB_pname, 'r' )
            fBtxt = fBstream.readlines()
            fB = EMK_viewTextFile.Form1()
            nl = "\r\n"
            fB._fileInfo.Text = "File: " + fB_pname
            fB._textBox1.Text = nl.join( fBtxt )
            fB._textBox1.Select(0,0)
            fB.Text = "Inter-Layer Dielectric (ILD) definition file"
            fB.Show()
        else:
            msg_content = "   Unable to open ILD definition file for viewing."
            msg_title   = "Error"
            MessageBox.Show( msg_content, msg_title )

            
    def ButtonCClick(self, sender, e):
        fC_pname = self._textBoxC.Text
        if ( os.path.isfile(fC_pname) ):
            fCstream = open( fC_pname, 'r' )
            fCtxt = fCstream.readlines()
            fC = EMK_viewTextFile.Form1()
            nl = "\r\n"
            fC._fileInfo.Text = "File: " + fC_pname
            fC._textBox1.Text = nl.join( fCtxt )
            fC._textBox1.Select(0,0)
            fC.Text = "Materials definition file"
            fC.Show()
        else:
            msg_content = "   Unable to open Materials definition file for viewing."
            msg_title   = "Error"
            MessageBox.Show( msg_content, msg_title )
        # the end

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        