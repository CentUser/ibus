import gtk
import gtk.gdk as gdk
import gobject
from image import Image
from handle import Handle

class LanguageBar (gtk.Toolbar):
	def __init__ (self):
		gtk.Toolbar.__init__ (self)
		self.set_property ("icon-size", gtk.ICON_SIZE_MENU)
		# self.set_orientation (gtk.ORIENTATION_VERTICAL)
		self._create_items ()
	
	def insert (self, toolitem, pos):
		gtk.Toolbar.insert (self, toolitem, pos)
		self.check_resize ()

	def _add_items (self):
		btn = gtk.ToolButton (gtk.STOCK_NEW)
		btn.connect ("clicked", lambda x: self._add_items ())
		self.insert (btn, -1)
		self.insert (gtk.ToolButton (gtk.STOCK_APPLY), -1)
		self.insert (gtk.SeparatorToolItem (), -1)
		self.show_all ()
		
	def _create_items (self):
		handle = Handle ()
		item = gtk.ToolItem ()
		item.add (handle)
		self.insert (item, -1)

		self._add_items ()
		
	def do_realize (self):
		gtk.Toolbar.do_realize (self)
		self.check_resize ()
	
	def do_check_resize (self):
		width = 0
		for item in self:
			w, h = item.size_request ()
			width += w
		self.set_size_request (width + 2, -1)
		
gobject.type_register (LanguageBar, "IBusLanguageBar")

class LanguageBarWindow (gtk.Window):
	def __init__ (self):
		gtk.Window.__init__ (self, gtk.WINDOW_POPUP)
		self._language_bar = LanguageBar ()
		self._language_bar.connect ("size-request", self._size_request_cb)
		self.add (self._language_bar)
		self.show_all ()

	def _size_request_cb (self, widget, size):
		self.resize (size.width, size.height)

	def do_size_allocate (self, allocation):
		gtk.Window.do_size_allocate (self, allocation)
		root = gdk.get_default_root_window ()
		workarea = root.property_get ("_NET_WORKAREA")[2]
		x, y = workarea[2] - allocation.width - 40, workarea[1] + workarea[3] - allocation.height
		self.move (x, y)
		
	def do_destroy (self):
		gtk.main_quit ()
		gtk.Window.do_destroy (self)

gobject.type_register (LanguageBarWindow, "IBusLanguageBarWindow")

