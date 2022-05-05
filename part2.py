import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, Gdk, Graphene, GLib

class Custom(Gtk.Widget):
    def __init__(self):
        super().__init__()
        self.set_size_request(30, 30)

    def do_snapshot(self, s):
        #s.save()
        print("sn")
        red = Gdk.RGBA()
        # red.red = 1.
        # red.green = 0.
        # red.blue = 0.
        # red.alpha = 1.
        r = Graphene.Rect()
        r.init(0, 0, 70, 70)
        print(r)
        print(r.get_height())
        red.red = 1
        red.alpha = 1
        print(red.to_string())
        s.append_color(red, r)
        #s.restore()


    def do_measure(self, orientation, for_size):
        print("m")
        return 50, 50, -1, -1
        pass

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_default_size(600, 250)
        self.set_title("MyApp")

        # Main layout containers
        self.box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.box2.set_spacing(10)
        self.box2.set_margin_top(10)
        self.box2.set_margin_bottom(10)
        self.box2.set_margin_start(10)
        self.box2.set_margin_end(10)

        self.set_child(self.box1)  # Horizontal box to window
        self.box1.append(self.box2)  # Put vert box in that box
        self.box1.append(self.box3)  # And another one, empty for now

        # Add a button
        self.button = Gtk.Button(label="Hello")
        self.button.connect('clicked', self.hello)
        self.box2.append(self.button)  # But button in the first of the two vertical boxes

        # Add a check button
        self.check = Gtk.CheckButton(label="And goodbye?")
        self.box2.append(self.check)

        # Add a box containing a switch and label
        self.switch_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.switch_box.set_spacing(5)

        self.switch = Gtk.Switch()
        self.switch.set_active(True)  # Let's default it to on
        self.switch.connect("state-set", self.switch_switched)  # Lets trigger a function on state change

        self.label = Gtk.Label(label="A switch")

        self.switch_box.append(self.switch)
        self.switch_box.append(self.label)
        self.box2.append(self.switch_box)

        self.slider = Gtk.Scale()
        self.slider.set_digits(0)  # Number of decimal places to use
        self.slider.set_range(0, 10)
        self.slider.set_draw_value(True)  # Show a label with current value
        self.slider.set_value(5)  # Sets the current value/position
        self.slider.connect('value-changed', self.slider_changed)
        self.box2.append(self.slider)

        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        self.open_button = Gtk.Button(label="Open")
        self.header.pack_start(self.open_button)
        self.open_button.set_icon_name("document-open-symbolic")

        self.open_dialog = Gtk.FileChooserNative.new(title="Choose a file",
                                                     parent=self, action=Gtk.FileChooserAction.OPEN)

        self.open_dialog.connect("response", self.open_response)
        self.open_button.connect("clicked", self.show_open_dialog)

        f = Gtk.FileFilter()
        f.set_name("Image files")
        f.add_mime_type("image/jpeg")
        f.add_mime_type("image/png")
        self.open_dialog.add_filter(f)


        # Create a new "Action"
        action = Gio.SimpleAction.new("something", None)
        action.connect("activate", self.print_something)
        self.add_action(action)  # Here the action is being added to the window, but you could add it to the
        # application or an "ActionGroup"

        # Create a new menu, containing that action
        menu = Gio.Menu.new()
        menu.append("Do Something", "win.something")  # Or you would do app.grape if you had attached the
        # action to the application

        # Create a popover
        self.popover = Gtk.PopoverMenu()  # Create a new popover menu
        self.popover.set_menu_model(menu)

        # Create a menu button
        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(self.popover)
        self.hamburger.set_icon_name("open-menu-symbolic")  # Give it a nice icon

        # Add menu button to the header bar
        self.header.pack_start(self.hamburger)

        # set app name
        GLib.set_application_name("My App")

        # Add an about dialog
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.show_about)
        self.add_action(action)  # Here the action is being added to the window, but you could add it to the
        menu.append("About", "win.about")

        self.dw = Gtk.DrawingArea()

        # Make it fill the available space (It will stretch with the window)
        self.dw.set_hexpand(True)
        self.dw.set_vexpand(True)

        # Instead, If we didn't want it to fill the available space but wanted a fixed size
        #dw.set_content_width(100)
        #dw.set_content_height(100)

        self.dw.set_draw_func(self.draw, None)
        self.box3.append(self.dw)

        #evc = Gtk.EventController.key_new()
        evk = Gtk.GestureClick.new()
        evk.connect("pressed", self.dw_click)  # could be "released"
        self.dw.add_controller(evk)

        evk = Gtk.EventControllerKey.new()
        evk.connect("key-pressed", self.key_press)
        self.add_controller(evk)

        self.blobs = []

        self.cursor_crosshair = Gdk.Cursor.new_from_name("crosshair")
        self.dw.set_cursor(self.cursor_crosshair)

        app = self.get_application()
        sm = app.get_style_manager()
        sm.set_color_scheme(Adw.ColorScheme.PREFER_DARK)

        custom = Custom()
        #self.box3.append(custom)
        custom.set_hexpand(True)
        custom.set_vexpand(True)

    def show_about(self, action, param):
        self.about = Gtk.AboutDialog()
        self.about.set_transient_for(self)
        self.about.set_modal(self)

        self.about.set_authors(["Your Name"])
        self.about.set_copyright("Copyright 2022 Your Full Name")
        self.about.set_license_type(Gtk.License.GPL_3_0)
        self.about.set_website("http://example.com")
        self.about.set_website_label("My Website")
        self.about.set_version("1.0")
        self.about.set_logo_icon_name("org.example.example")

        self.about.show()

    def key_press(self, event, keyval, keycode, state):
        if keyval == Gdk.KEY_q and state & Gdk.ModifierType.CONTROL_MASK:
            self.close()

    def show_open_dialog(self, button):
        self.open_dialog.show()

    def open_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            file = dialog.get_file()
            filename = file.get_path()
            print(filename)

    def dw_click(self, gesture, data, x, y):
        self.blobs.append((x, y))
        self.dw.queue_draw()  # Force a redraw

    def draw(self, area, c, w, h, data):
        # c is a Cairo context

        # Fill background
        c.set_source_rgb(0, 0, 0)
        c.paint()

        c.set_source_rgb(1, 0, 1)
        for x, y in self.blobs:
            c.arc(x, y, 10, 0, 2 * 3.1215)
            c.fill()

        # Draw a line
        c.set_source_rgb(0.5, 0.0, 0.5)
        c.set_line_width(3)
        c.move_to(10, 10)
        c.line_to(w - 10, h - 10)
        c.stroke()

        # Draw a rectangle
        c.set_source_rgb(0.8, 0.8, 0.0)
        c.rectangle(20, 20, 50, 20)
        c.fill()

        # Draw some text
        c.set_source_rgb(0.1, 0.1, 0.1)
        c.select_font_face("Sans")
        c.set_font_size(13)
        c.move_to(25, 35)
        c.show_text("Test")


    def print_something(self, action, param):
        print("Something!")

    def slider_changed(self, slider):
        print(int(slider.get_value()))

    def switch_switched(self, switch, state):
        print(f"The switch has been switched {'on' if state else 'off'}")

    def hello(self, button):
        print("Hello world")
        if self.check.get_active():
            print("Goodbye world!")
            self.close()


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()


app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
