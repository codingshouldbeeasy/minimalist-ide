import gedit, gtk, sys, traceback

import easyscala
ui_str = """
<ui>
  <toolbar name="ToolBar">
    <separator />
    <toolitem name="ReloadPlugins" action="ReloadPlugins" />
  </toolbar>
</ui>
"""


# define the plugin helper class
class ReloadPluginsHelper:
  def handle_exception(self, operation):
    print "****************** ERROR "+operation+" PLUGIN **************"
    (t,v,tb) = sys.exc_info()
    traceback.print_tb(tb)
    print t
    sys.exc_clear()
    sys.excepthook(t,v,tb)
    print "EXCEPTION CLEARED"

  def reload_modules(self):
    reload(easyscala)      
    reload(easyscala.pluggy)
    reload(easyscala.fix_ctrl_backspace)
  
  def __init__(self, plugin, window):
    self._window = window
    self._plugin = plugin    
    self._insert_ui_items()
    self._impl = None
    try:
      self.reload_modules()
      self._impl = easyscala.EasyScalaPlugin()
      self._impl.activate(window)
    except:
      self.handle_exception( "LOADING")
      
  def deactivate(self):
    try:
      self._impl.deactivate(self._window)  
    except:
      self.handle_exception( "DEACTIVATING")
 
    self._remove_ui_items()
    self._window = None
    self._plugin = None


  def _insert_ui_items(self):
    self._manager = self._window.get_ui_manager()
    self._action_group = gtk.ActionGroup("PluginActions")
    
    self._action_group.add_actions([(
            "ReloadPlugins", 
            gtk.STOCK_OK, 
            _("Text Wrap"), 
            "<Ctrl><Shift>R", 
            _("Reload Plugins"), 
            self.on_reload_plugins)])
    self._manager.insert_action_group(self._action_group, -1)
    self._ui_id = self._manager.add_ui_from_string(ui_str)

  def _remove_ui_items(self):
    self._manager.remove_ui(self._ui_id)
    self._ui_id = None
    self._manager.remove_action_group(self._action_group)
    self._action_group = None
    self._manager.ensure_update()

  def on_reload_plugins(self, action):
    if self._impl != None:
      try:
        self._impl.deactivate(self._window)  
      except:
        self.handle_exception( "DEACTIVATING")
    self._impl=None
    try:
      self.reload_modules()
      self._impl=easyscala.EasyScalaPlugin()
      self._impl.activate(self._window)  
    except:
      self.handle_exception( "LOADING")
      
  def update_ui(self):
    if self._impl!=None:
      self._impl.update_ui(self._window)

#class EasyScalaPluginWrapper(gedit.Plugin):
#  def activate(self, window):
#    print "LOADING"

#  def deactivate(self, window):
#    self._impl.deactivate(window)

#  def update_ui(self, window):
#    self._impl.update_ui(window)
    
    
    
class ReloadPluginsWrapperPlugin(gedit.Plugin):
  def __init__(self):
    ReloadPluginsWrapperPlugin.instance = self
    print ReloadPluginsWrapperPlugin.instance
    gedit.Plugin.__init__(self)
    self._instances = {}


  def activate(self, window):
    self._instances[window] = ReloadPluginsHelper(self, window)


  def deactivate(self, window):
    self._instances[window].deactivate()
    del self._instances[window]


  def update_ui(self, window):
    self._instances[window].update_ui()

def rr():
  oldplugin = ReloadPluginsWrapperPlugin.instance
  for window in oldplugin._instances.keys():
    oldplugin.deactivate(window)
  import reloadplugin
  reload(reloadplugin)
  ReloadPluginsWrapperPlugin.instance = oldplugin
  for window in oldplugin._instances:
    oldplugin.activate(window)


