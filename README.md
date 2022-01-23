# Taiko's GTK4 Python tutorial

Wanna make apps for Linux but not sure how to start with GTK? Frustrated with the style of GTK4 documentation. This guide will hopefully get you started!

Prerequisite: You have learnt the basics of Python

Topics:

 - A basic GTK window
 - Adding basic button widget
 - Introducing the box layout
 - Add check button, a switch and a slider
 - Add a custom header bar
 - Add a button with a menu
 - Custom drawing with Cairo
 - Handling input

For beginners, I suggest walking through each example and try to understand what each line is doing.

## A most basic program

```python
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

def on_activate(app):
    win = Gtk.ApplicationWindow(application=app)
    win.present()

app = Gtk.Application(application_id='com.example.GtkApplication')
app.connect('activate', on_activate)

app.run(None)

```

This should display a small blank window.

![A blank GTK window](blank.png)

For a serious app, you'll need to think of your own application id. It should be the reverse of a domain or page you control. If you don't have your own domain you can do like "com.github.me.myproject".

Right um... lets make that code into classes! 'Cause doing it functional style is a little awkward in Python.

Also, **Libawaita** is the new hotness, so lets switch to that!

Aaand we'll pass the app arguments in.

Here's what we got now:

## A better structured basic GTK4 + Adwaita


```python
import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Things will go here

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)

```

Soo we have an instance of an app class and a window which we extend! We run our app and it makes a window!

> **Tip:** Don't worry too much if you don't understand the `__init__(self, *args, **kwargs)` stuff for now.

### So! Whats next?

Well, we want to add something to our window. That would likely be a ***layout*** of some sort!

Most basic layout is a [Box](https://docs.gtk.org/gtk4/class.Box.html).

Lets add a box to the window! (Where the code comment "*things will go here*" is above)

```python
self.box = Gtk.Box()
self.set_child(self.box)
```

We make a new box, and attach it to the window. Simple. If you run the app now you'll see no difference, because there's nothing in the layout yet either.


## Add a button!

One of the most basic widgets is a [Button](https://docs.gtk.org/gtk4/class.Button.html). Let's make one and add it to the layout.

```python
self.button = Gtk.Button(label="Hello")
self.box1.append(self.button)
```

Now our app has a button! (The window will be small now)

But it does nothing when we click it. Let's connect it to a function! Make a new method that prints hello world, and we connect it! 

Here's our MainWindow so far:

```python
class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.box1)

        self.button = Gtk.Button(label="Hello")
        self.box1.append(self.button)
        self.button.connect('clicked', self.hello)

    def hello(self, button):
        print("Hello world")
```

Cool eh?

By the way the ***Box*** layout lays out widgets in like a vertical or horizontal order. We should set the orientation of the box. See the change:

```python
self.box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
```

### Quick intermission, lets set some window parameters

```python
self.set_default_size(600, 250)
self.set_title("MyApp")
```

## More boxes

You'll notice our button is stretched with the window. Let's add two boxes inside that first box we made. 

```python
self.box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
self.box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

self.button = Gtk.Button(label="Hello")
self.button.connect('clicked', self.hello)

self.set_child(self.box1)  # Horizontal box to window
self.box1.append(self.box2)  # Put vert box in that box
self.box1.append(self.box3)  # And another one, empty for now

self.box2.append(self.button) # But button in the first of the two vertial boxes
```

Now that's more neat!

## Add a check button!

So, we know about a button, next lets add a [Checkbutton](https://docs.gtk.org/gtk4/class.CheckButton.html).

```python
    ...
    self.check = Gtk.CheckButton(label="And goodbye?")
    self.box2.append(self.check)


def hello(self, button):
    print("Hello world")
    if self.check.get_active():
        print("Goodbye world!")
        self.close()
```

![Our window so far](twoitems.png)

When we click the button, we can check the state of the checkbox!

## Add a switch

For our switch, we'll want to put our switch in a ***Box***, otherwise it'll look all stretched.

```python
        ...
        self.switch_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.switch = Gtk.Switch()
        self.switch.set_active(True)  # Let's default it to on
        self.switch.connect("state-set", self.switch_switched) # Lets trigger a function

        self.switch_box.append(self.switch)
        self.box2.append(self.switch_box)

    def switch_switched(self, switch, state):
        print(f"The switch has been switched {'on' if state else 'off'}")
```

Try it out!

Our switch is looking rather nondescript, so lets add a label to it!
 

## Add a Label

A label is like a basic line of text

```python
self.label = Gtk.Label(label="A switch")
self.switch_box.append(self.switch)
self.switch_box.set_spacing(5) # Add some spacing

```

It should look like this now:

![Our window including switch and label](switch.png)

The file `part1.py` is an example of the code so far.

## Adding a slider (Aka scale)

Here's an example of adding a [Scale](https://docs.gtk.org/gtk4/ctor.Scale.new.html) with a range from 0 - 10

```python
        self.slider = Gtk.Scale()
        self.slider.set_digits(0)  # Number of decimal places to use
        self.slider.set_range(0, 10)
        self.slider.set_draw_value(True)  # Show a label with current value
        self.slider.set_value(5)  # Sets the current value/position
        self.slider.connect('value-changed', self.slider_changed)
        self.box2.append(self.slider)

    def slider_changed(self, slider):
        print(int(slider.get_value()))
```

## Adding a button into the header bar

First we need to make a header bar

```python
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)
```

Simple.

Now add a button

```python
        self.open_button = Gtk.Button(label="Open")
        self.header.pack_start(self.open_button)
```

We already know how to connect a function to the button, so i've omitted that.

Done! But... it would look nicer with an icon rather than text.

```python
        self.open_button.set_icon_name("document-open-symbolic")
```

This will be an icon name from the icon theme. 

For some defaults you can take a look at `/usr/share/icons/Adwaita/scalable/actions`.

If you were adding a new action icon it would go in `/usr/share/icons/hicolor/scalable/actions`

> **Help! Todo!** Is this the best way? How do icons work in a development environment?

# Adding a button with menu

For this there are multiple new concepts we need to introduce:

 - The [***MenuButton***](https://docs.gtk.org/gtk4/class.MenuButton.html) widget.
 - The [***Popover***](https://docs.gtk.org/gtk4/class.Popover.html), but here we will use a [***PopoverMenu***](https://docs.gtk.org/gtk4/class.PopoverMenu.html) which is built using an abstract menu model.
 - A [***Menu***](https://docs.gtk.org/gio/class.Menu.html). This is an abstract model of a menu.
 - [***Actions***](https://docs.gtk.org/gio/class.SimpleAction.html). An abstract action that can be connected to our abstract menu.

So, we click a MenuButton, which shows a Popover that was generated from a MenuModel that is composed of Actions.

```python
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

    def print_something(self, action, param):
        print("Something!")

```

![A basic menu in headerbar](menu1.png)

# Custom drawing area using Cairo

Here we use the [***DrawingArea***](https://docs.gtk.org/gtk4/class.DrawingArea.html) widget.

```python

        dw = Gtk.DrawingArea()

        # Make it fill the available space (It will stretch with the window)
        dw.set_hexpand(True)
        dw.set_vexpand(True)

        # Instead, If we didn't want it to fill the available space but wanted a fixed size
        #dw.set_content_width(100)
        #dw.set_content_height(100)

        dw.set_draw_func(self.draw, None)
        self.box3.append(dw)

    def draw(self, area, c, w, h, data):
        # c is a Cairo context

        # Fill background with a colour
        c.set_source_rgb(0, 0, 0)
        c.paint()

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

```

Further resources on Cairo:

 - [PyCairo Visual Documentation](https://seriot.ch/pycairo/)

Note that Cairo uses software rendering. For accelerated rendering, Gtk Snapshot can be used (todo)

## Input handling in our drawing area

### Handling a mouse / touch event

```python
        ...
        evk = Gtk.GestureClick.new()
        evk.connect("pressed", self.dw_click)  # could be "released"
        self.dw.add_controller(evk)

        self.blobs = []

    def dw_click(self, gesture, data):
        c, x, y = gesture.get_point()
        self.blobs.append((x, y))
        self.dw.queue_draw()  # Force a redraw

    def draw(self, area, c, w, h, data):
        # c is a Cairo context

        # Fill background
        c.set_source_rgb(0, 0, 0)
        c.paint()

        c.set_source_rgb(1, 0, 1)
        for x, y in self.blobs:
            c.arc(x, y, 10, 0, 2 * 3.1415926)
            c.fill()
        ...

```

![A drawing area with purple dots where we clicked](dots.png)

Ref: [GestureClick](https://docs.gtk.org/gtk4/class.GestureClick.html)

See also: [EventControllerKey](https://docs.gtk.org/gtk4/class.EventControllerKey.html)

See also: [EventControllerMotion](https://docs.gtk.org/gtk4/class.EventControllerMotion.html)

## Todo...


Text box: [Entry](https://docs.gtk.org/gtk4/class.Entry.html) 

Number changer: [SpinButton](https://docs.gtk.org/gtk4/class.SpinButton.html)




