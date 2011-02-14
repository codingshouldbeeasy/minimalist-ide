from gettext import gettext as _

class Pluggy:
  def __init__(self, plugin, window):
    self._window = window
    self._plugin = plugin
    self._handlers = {}
  
  def register_handler(self, view_type, signal, handler):
    type_handlers = self._handlers.get(view_type,[])
    type_handlers+=(signal, handler)
    self._handlers[view_type] = type_handlers
    self.register_handler_with_all_views(view_type, signal, handler)
  
  def register_handler_with_view(self, view, signal, handler):
    handlers = getattr(view, 'pluggy_handlers', [])
    handler_id = view.connect(signal, handler)
    setattr(view, 'pluggy_handlers', handlers+[handler_id])

  def register_handler_with_all_views(self, view_type, signal, handler):
    for view in self._window.get_views():
      if isinstance(view, view_type):
        self.register_handler_with_view(view,signal, handler)
        
  def register_all_handlers_with_view(self, view):
    for view_type in self._handlers:
      if isinstance(view, view_type):
        signal_handler = self._handlers[view_type]
        self.register_handler_with_view(view, signal_handler[0], signal_handler[1])
  
  def deactivate(self):
    print "DEACTIVATE"
    for view in self._window.get_views():
      for handler_id in getattr(view, 'pluggy_handlers', []):
        print handler_id
        view.disconnect(handler_id)
      setattr(view, 'pluggy_handlers', [])
    self._window = None
    self._plugin = None
    
  def update_ui(self):
    active_view = self._window.get_active_view()
    active_doc = self._window.get_active_document()
    if getattr(active_view, 'pluggy_handlers', None)==None:
      self.register_all_handlers_with_view(view)
    self.ui_updated(active_view, active_doc)
    
  def ui_updated(self, active_view, active_doc):
    pass

