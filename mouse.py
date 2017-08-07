import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo
from pymouse import PyMouse
from cell import Cell

LCLICK = 'n'
RCLICK = 'o'

mouse = PyMouse()

exit_action = None

cell_colors = (
    (0.09, 0.44, 0.93, 0.2),
    (0.56, 0.07, 0.94, 0.2),
    (0.29, 0.97, 0.01, 0.2),
    (1.00, 0.63, 0.01, 0.2),
)

class RootCell(Cell, Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        screen = self.get_screen()

        monitors = []
        for m in range(screen.get_n_monitors()):
            monitors.append(screen.get_monitor_geometry(m))

        rect = monitors[screen.get_monitor_at_window(screen.get_active_window())]
        w = rect.width
        h = rect.height
        self.x_offset = rect.x
        self.y_offset = rect.y

        Cell.__init__(self, 0, 0, w, h)
        print(self.w)

        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", self.delete)
        self.connect("focus-out-event", Gtk.main_quit)
        self.connect("key-press-event", self.handle_keypress)
        self.connect("draw", self.area_draw)

        self.set_size_request(w, h)
        self.set_border_width(0)

        self.set_title('mouse-something')

        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        if self.visual != None and self.screen.is_composited():
                self.set_visual(self.visual)

        self.set_app_paintable(True)
        self.show_all()

        self.focus = self
        self.cells = [self.divide()]


    def click(self, b):
        mouse.click(self.x_offset + self.focus.x + self.focus.w//2, self.y_offset + self.focus.y + self.focus.h//2, button=b)

    def lclick(self):
        return self.click(1)

    def rclick(self):
        return self.click(2)

    def delete(self, widget, event):
        Gtk.main_quit()

    def area_draw(self, widget, cr):
        cr.set_source_rgba(0.0, 0.0, 0.0, 0.0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
        cr.set_source_rgba(1, 1, 1, 1)
        cr.select_font_face('Arial')
        cr.set_font_size(32)
        self.grid(cr)

    def handle_keypress(self, widget, event):
        global exit_action
        print(event.keyval)
        if (event.string in self.cells[-1].keys()):
            cell = self.cells[-1].get(event.string)
            self.cells.append(cell.divide())
            self.focus = cell
            self.queue_draw()
        elif LCLICK == event.string:
            exit_action = self.lclick
            print(exit_action)
            self.close()
        elif RCLICK == event.string:
            exit_action = self.rclick
            self.close()
        # elif 65288 == event.keyval and len(self.cells) > 1:
        #     self.cells.pop()
        #     self.focus = self.cells[-1]
        #     self.queue_draw()
        elif 65307 == event.keyval or ' ' == event.string:
            self.close()



    def grid(self, cr):
        for xe in range(0, 2+1):
            x = self.focus.x + ((xe)/2) * self.focus.w
            self.v_line(cr, (1,1,1,1), 2, x)
            self.v_line(cr, (0,0,0,1), 1, x+1)
        for ye in range(0, 2+1):
            y = self.focus.y + ((ye)/2) * self.focus.h
            self.h_line(cr, (1,1,1,1), 2, y)
            self.h_line(cr, (0,0,0,1), 1, y+1)
        for i, cell in enumerate(self.cells[-1].values()):
            self.draw_cell(cr, cell, cell_colors[i])

    def draw_cell(self, cr, cell, color):
        cr.set_source_rgba(*color)
        cr.set_line_width(1)
        cr.move_to(cell.x, cell.y)
        cr.line_to(cell.x, cell.y + cell.h)
        cr.line_to(cell.x + cell.w, cell.y + cell.h)
        cr.line_to(cell.x + cell.w, cell.y)
        cr.move_to(cell.x, cell.y)
        cr.fill()

    def grid_label(self, cr, text, x, y):
        cr.set_source_rgba(1, 1, 1, 1)
        cr.select_font_face('Arial')
        cr.set_font_size(32)
        cr.move_to(x, y)
        cr.show_text(text)

    def v_line(self, cr, color, width, x):
        cr.set_source_rgba(*color)
        cr.set_line_width(width)
        cr.move_to(x, self.focus.y)
        cr.line_to(x, self.focus.y + self.focus.h - 1)
        cr.stroke()

    def h_line(self, cr, color, width, y):
        cr.set_source_rgba(*color)
        cr.set_line_width(width)
        cr.move_to(self.focus.x, y)
        cr.line_to(self.focus.x + self.focus.w - 1, y)
        cr.stroke()


RootCell()
Gtk.main()
if exit_action is not None:
    exit_action()
