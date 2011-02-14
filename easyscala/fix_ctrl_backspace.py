import re, pluggy, gedit, gtk

class FixCtrlBackspacePluggy(pluggy.Pluggy):
  def __init__(self, plugin, window):
    pluggy.Pluggy.__init__(self,plugin,window)
    self.register_handler(gedit.View,'key-press-event', self.on_key_press)

  def find_matching_pattern(self, patterns, text):
    for i in range(0, len(patterns)):
      if re.match(patterns[i],text)!=None:
        return patterns[i]

  def on_key_press(self, view, event):
    if event.keyval == gtk.keysyms.BackSpace and event.state & gtk.gdk.CONTROL_MASK:
      doc = self._window.get_active_document()
      end = doc.get_iter_at_mark(doc.get_insert())
      begin = doc.get_iter_at_mark(doc.get_insert())
      begin.backward_chars(1)
      patterns = [" {1,}", "[A-Z][a-z]{1,}|[a-z]{1,}","[A-Z]{1,}","[0-9]{1,}","[^a-zA-Z0-9 ]{1,}"]
      text = doc.get_text(begin,end,False)
      pattern = self.find_matching_pattern(patterns, text)
      if pattern!=None:
        while not (begin.starts_line() or (begin.ends_line() and end.starts_line())):
          text = doc.get_text(begin,end,False)
          if (re.match(pattern, text)==None):
            begin.forward_chars(1)
            doc.delete_interactive(begin,end,True)
            return True
          begin.backward_chars(1)
      doc.delete_interactive(begin,end,True)            
      return True
    return False

