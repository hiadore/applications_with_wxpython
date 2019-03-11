# main.py

import os
import time
import wx

import wx.lib.agw.flatnotebook as fnb

class NewPage(wx.Panel):
    """
    Create a new page for each opened XML document. This is the
    top-level widget for the majority of the application
    """

    def __init__(self, parent, xml_path, size, opened_files):
        wx.Panel.__init__(self, parent)
        self.page_id = id(self)
        self.xml_root = None
        self.size = size
        self.opened_files = opened_files
        self.current_file = xml_path
        self.title = os.path.basename(xml_path)

        self.app_location = os.path.dirname(os.path.abspath( sys.argv[0] ))
        self.tmp_location = os.path.join(self.app_location, 'drafts')
        
        self.parse_xml(xml_path)
        
        current_time = time.strftime('%Y-%m-%d.%H.%M.%S', time.localtime())
        self.full_tmp_path = os.path.join(
                self.tmp_location,
                current_time + '-' + os.path.basename(xml_path))
    
        if not os.path.exists(self.tmp_location):
            try:
                os.makedirs(self.tmp_location)
            except IOError:
                raise IOError('Unable to create file at {}'.format(
                        self.tmp_location))
    
        if self.xml_root is not None:
            self.create_editor()
        


class Main(wx.Frame):
    
    def __init__(self):
        super().__init__(
            None, title="XML Editor",
            size=(800, 600))
        
        self.notebook = None
        self.opened_files = []
        self.current_page = None
        
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self)
        self.panel.SetSizer(self.main_sizer)
        
    def create_new_editor(self, xml_path):
        """
        Create the tree and xml editing widgets when the user loads
        an XML file
        """
        if not self.notebook:
            self.notebook = fnb.FlatNotebook(
                    self.panel)
            self.main_sizer.Add(self.notebook, 1, 
                                wx.ALL|wx.EXPAND, 5)
            style = self.notebook.GetAGWWindowStyleFlag()
            style |= fnb.FNB_X_ON_TAB
            self.notebook.SetAGWWindowStyleFlag(style)
            self.notebook.Bind(
                    fnb.EVT_FLATNOTEBOOK_PAGE_CLOSING, 
                    self.on_page_closing)
    
        if xml_path not in self.opened_files:
            self.current_page = NewPage(
                self.notebook, xml_path, self.size,
                self.opened_files)
            self.notebook.AddPage(self.current_page,
                                  os.path.basename(xml_path),
                                  select=True)
            self.last_opened_file = xml_path
    
            self.opened_files.append(self.last_opened_file)
    
        self.panel.Layout()
        
    def on_page_closing(self, event):
        pass