'''
authors: Ben Scammell and Nick Fiacco
'''
import struct
import Tkinter as tk
from constants import *
from logo_thread import *
from pymol import cmd
import math
import tkFileDialog
from __init__ import *
from pymol.wizard import Wizard

class AutoScrollbar(tk.Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works with the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        tk.Scrollbar.set(self, lo, hi)

class WindowApp():
    
    def __init__(self, app):

        # Widget Parents
        self.win = tk.Toplevel(app.root)
        self.win.protocol("WM_DELETE_WINDOW", self.callback)
        self.win.title('MASTER Program')
        
        # Instance variables to be used in logos
        self.win.start = None
        self.win.textview = None
        self.win.sb = None
        self.win.sbv = None
        self.win.residue_list = None
        self.win.img = None
        self.win.logo = None
        self.win.canvas = None
        self.win.width = None
        self.win.coords = None
        self.win.linelist = []

        # Make a label for RMSD and entry box
        rmsd_label = tk.Label(self.win, text = "RMSD cut", width=1).grid(rowspan=2, sticky=N+E+S+W)
        self.win.rmsd = tk.StringVar(self.win)
        self.win.rmsd.set('0.5')
        rmsd_entry = tk.Entry(self.win, textvariable = self.win.rmsd, width=2).grid(row=0, column=1, rowspan=2, sticky=N+E+S+W)
        
        # Make a label for the Number of Structures value
        num_structs_label = tk.Label(self.win, text = "# matches", width=1).grid(row=2, column=0, rowspan=2, sticky=N+E+S+W)
        self.win.num_structs = tk.StringVar(self.win)
        self.win.num_structs.set('10')
        matches_entry = tk.Entry(self.win, textvariable = self.win.num_structs, width=2).grid(row=2, column=1, rowspan=2, sticky=N+E+S+W)
        

        # Make Label and menu selection for database type
        database_label = tk.Label(self.win, text = "Database").grid(row=4, column=0, rowspan=2, sticky=N+E+S+W)
        self.win.db = tk.StringVar(self.win)
        self.win.db.set("Test DB")
        database_select = tk.OptionMenu(self.win, self.win.db, "Test DB", "Full DB").grid(row=4, column=1, rowspan=2, sticky=N+E+S+W)
        
        # Make Label and menu selection for match type
        match_label = tk.Label(self.win, text = "Match type").grid(row=6, column=0, rowspan=2, sticky=N+E+S+W)
        self.win.fm = tk.StringVar(self.win)
        self.win.fm.set("Region")
        match_select = tk.OptionMenu(self.win, self.win.fm, "Region", "Full").grid(row=6, column=1, rowspan=2, sticky=N+E+S+W)

        # Add a search button that calls search when clicked
        search_button = tk.Button(self.win, text="Search", command=lambda: self.set_and_search()).grid(row=8, column=0, rowspan=2, columnspan=2, sticky=N+E+S+W)
        
        # Pick search
        self.win.search_id = tk.StringVar(self.win)
        self.win.search_id.set('Search IDs:')
        search_id_button = tk.OptionMenu(self.win, self.win.search_id, 'Search IDs:').grid(row=10, column=0, rowspan=2, sticky=N+E+S+W)

        # Info or freq checkbuttons
        logo_choice = tk.IntVar(self.win)
        logo_choice.set(1)
        info_check = tk.Radiobutton(self.win, text="info", variable=logo_choice, value=1).grid(row=10, column=1, sticky=N+E+S+W)
        freq_check = tk.Radiobutton(self.win, text="freq", variable=logo_choice, value=2).grid(row=11, column=1, sticky=N+E+S+W)
        

        # Make a button to run the Sequence Logo
        show_logo_button = tk.Button(self.win, text="Show Logo", command=lambda: self.set_and_display(int(logo_choice.get()), str(self.win.search_id.get()))).grid(row=12, column=0, rowspan=2, sticky=N+E+S+W)
        
        # Make a button to run Frequency Logo
        save_button = tk.Button(self.win, text="Save Logo", command=self.saveFile).grid(row=12, column=1, rowspan=2, sticky=N+E+S+W)
        
        # Label placeholding for logo graphic
        placeholder = tk.Label(self.win, background='white', text = "                                                                                                                 ").grid(row=0, column=2, rowspan=14, columnspan=5, sticky=N+E+S+W)

        # Start make id list
        self.make_ids()
    
    def callback(self):
        
        # Reset flag for making popup
        cmd.get_wizard().live_app = False
        self.win.destroy()
    

    # Remake ID menu after it been appended to searches
    def make_ids(self):
        
        if cmd.get_wizard().done_adding == True:

            # Set search options and current search
            searches = cmd.get_wizard().searches[0:]
            searches.insert(0, 'Search IDs: ')
            self.win.search_id.set(searches[0])
            
            # Remake window
            search_id = tk.OptionMenu(self.win, self.win.search_id, *searches).grid(row=10, column=0, rowspan=2, sticky=N+E+S+W)
            
            # Reset flag
            cmd.get_wizard().done_adding = False

    
    # Function to set flag and ID number
    def set_and_display(self, flag, id):

        # Set search
        cmd.get_wizard().set_search(int(id[-1])-1)

        # Show logo
        cmd.get_wizard().launch_logo_search(flag)


    # Function to set all values for searching
    def set_and_search(self):

        # Set RMSD cutoff
        if self.is_num(self.win.rmsd.get()):
            cmd.get_wizard().set_rmsd(float(self.win.rmsd.get()))
        else:
            cmd.get_wizard().status = 'rmsd not number'
            cmd.refresh_wizard()
            return

        # Set number of structures
        if self.is_num(self.win.num_structs.get()):
            cmd.get_wizard().set_num_structures(self.win.num_structs.get())
        else:
            cmd.get_wizard().status = 'num matches not number'
            cmd.refresh_wizard()
            return

        # Set Database
        if self.win.db == "Test DB":
            cmd.get_wizard().set_database("Test")
        elif self.win.db == "Full DB":
            cmd.get_wizard().set_database("Full")

        # Set Full matches
        if self.win.fm == "Region":
            cmd.get_wizard().set_full_matches(False)
        elif self.win.fm == "Full":
            cmd.get_wizard().set_full_matches(True)

        # Launch the search
        cmd.get_wizard().launch_search()

    def saveFile(self):

        extensions = [('PDF', '.pdf'), ('EPS', '.eps'), ('GIF', '.gif'), ('PNG', '.png')]
        f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".pdf", filetypes=extensions)

        # the user cancelled the save
        if f is None:
            cmd.get_wizard().status = 'Save Cancelled'
            cmd.refresh_wizard()
            return

        # get the EPS file from the server and write it
        self.getLogoFile(f.name)
        
        cmd.get_wizard().filename = f.name
        
        f.close()
        cmd.get_wizard().status = 'SequenceLogo saved'
        cmd.refresh_wizard()

    def getLogoFile(self, filepath):
        cmd.get_wizard().status = 'vector graphic requested'
        cmd.refresh_wizard()

        ext = filepath.split(".")[-1]

        logoThread = LogoThread(
            cmd.get_wizard().rmsd_cutoff,
            cmd.get_wizard().jobIDs[cmd.get_wizard().search],
            int(cmd.get_wizard().logo_flag),
            cmd.get_wizard().LOGOurl,
            cmd.get_wizard().cmd,
            filepath,
            ext)
            
        logoThread.start()
        logoThread.join()

        cmd.get_wizard().status = 'vector graphic received'
        cmd.refresh_wizard()

    
    def display_menu_logo(self, app, query, residues, rmsd_cutoff, LOGOurl, flag, plugin):
        """
        This method handles creating a SequenceLogo UI with Tkinter
        author = Ben + Nick
        """
        
        # placeholder for logo graphic
        placeholder = tk.Label(self.win, background='white', text = "                                                                                                                 ").grid(row=0, column=2, rowspan=14, columnspan=5, sticky=N+E+S+W)

        # Create the filepath name
        if flag == 1:
            logo_filepath = LOGO_CACHE + str(query)+"s.gif"
        elif flag == 2:
            logo_filepath = LOGO_CACHE + str(query)+"f.gif"
        
        # Set permanent flag (1/2)
        cmd.get_wizard().logo_flag = flag
        
        # Get the coordinates of the image
        self.win.coords = self.get_image_size(logo_filepath)
        self.win.width = self.win.coords[0]

        # Get the image
        self.win.img = tk.PhotoImage(file=logo_filepath)

        # Make a canvas, display the image, and save a reference
        self.win.canvas = tk.Canvas(self.win)
        self.win.canvas.create_image(self.win.width/2, 100, image=self.win.img)
        self.win.canvas.photo = self.win.img

        # Make the whole area scrollable
        self.win.canvas.config(bg='white', scrollregion = self.win.canvas.bbox("all"))

        # Place the canvas
        self.win.canvas.grid(row=0, column=2, rowspan=13, columnspan=4, sticky=N+E+S+W)
        
        #  Make window rescalable
        for p in range(13):
            self.win.grid_rowconfigure(p, weight=1)
        
        for q in range(2, 6):
            self.win.grid_columnconfigure(q, weight=1)
        
        # Create a scrollbar and link it with the canvas
        self.win.sb = AutoScrollbar(self.win, orient=tk.HORIZONTAL)
        self.win.sb.grid(row=13, column=2, columnspan=4, sticky=E+W)
        self.win.sb.config(bg='white', command=self.win.canvas.xview)
        
        self.win.sbv = AutoScrollbar(self.win, orient=tk.VERTICAL)
        self.win.sbv.grid(row=0, column=6, rowspan=12, sticky=N+S)
        self.win.sbv.config(bg='white', command=self.win.canvas.yview)
        
        #link scrollbars
        self.win.canvas.config(xscrollcommand=self.win.sb.set, yscrollcommand=self.win.sbv.set)
    
        # parse query, add residues to a list for later reference
        residues_str = residues.split()
        self.win.residue_list = []

        # Create residue list
        for residue_str in residues_str:
            residue = residue_str.split(',')
            self.win.residue_list.append(residue)
        
        # Write characters and underbar under residue
        x = 68
        for each_char in range(len(self.win.residue_list)):
            self.win.canvas.create_text(x, 180, text=str(self.win.residue_list[each_char][0]))
            self.win.linelist.append(self.win.canvas.create_line(x-4, 190, x+5.4, 190, width=2, fill='black'))
            self.binder(each_char)
            x += 18.8

        # set up empty initial selection object used by PyMol to group selections
        cmd.select("curPos", "none")


    
    def binder(self, p):
        """
        tag_binds each underbar canvas item
        """
        self.win.canvas.tag_bind(self.win.linelist[p], "<1>", lambda event, tag=self.win.linelist[p]: self.underbar_click(event, self.win.linelist[p]))
    
    def underbar_click(self, event, tag):
        """
        calls select or deselect on each residue when underbar is clicked
        """
        if self.win.canvas.itemcget(tag, 'fill') == 'black':
            self.win.canvas.itemconfigure(tag, fill='blue')
            self.residue_select(self.win.linelist.index(tag))
        else:
            self.win.canvas.itemconfigure(tag, fill='black')
            self.residue_deselect(self.win.linelist.index(tag))


    def residue_select(self, i):
        
        # Show selection message
        cmd.get_wizard().res_info = 'click search chain '+self.win.residue_list[i][1]+' num '+self.win.residue_list[i][2]
        cmd.get_wizard().status = 'residue selected'
        cmd.refresh_wizard()
        
        # Select residues
        cmd.select("curPos", "curPos or (chain " + self.win.residue_list[i][1] + " and resi " + self.win.residue_list[i][2] + ")")
        sys.stdout.flush()

    def residue_deselect(self, i):
        
        # Deselect residues
        cmd.select("curPos", "curPos and not (chain " + self.win.residue_list[i][1] + " and resi " + self.win.residue_list[i][2] + ")")

    def get_image_size(self, fname):
    
    #    Determine the image type of fhandle and return its size.
    #    http://stackoverflow.com/questions/8032642/how-to-obtain-image-size-using-standard-python-class-without-using-external-lib

        with open(fname, 'rb') as fhandle:
            head = fhandle.read(24)
            if len(head) != 24:
                return
            width, height = struct.unpack('<HH', head[6:10])
            return width, height

    def is_num(self, num):
        
        # Check to make sure input is only numerals and '.'
        for i in range(len(num)):
            if 48 <= ord(num[i]) <= 57 or ord(num[i]) == 46:
                pass
            else:
                return False
        return True

