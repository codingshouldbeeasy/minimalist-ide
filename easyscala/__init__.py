__all__ = ["pluggy", "fix_ctrl_backspace"]

import gtk
import gedit
import pluggy
import fix_ctrl_backspace


class EasyScalaPlugin(gedit.Plugin):
  def __init__(self):
    gedit.Plugin.__init__(self)
    self._instances = {}

  def activate(self, window):
    self._instances[window] = fix_ctrl_backspace.FixCtrlBackspacePluggy(self, window)

  def deactivate(self, window):
    self._instances[window].deactivate()
    del self._instances[window]

  def update_ui(self, window):
    self._instances[window].update_ui()

