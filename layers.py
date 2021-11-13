import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

layers_list = []
CurrentLayerType = None

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.add(Gtk.Label(label=data))


class LayerWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Make Model")

        self.box = Gtk.Box(spacing=6)
        self.add(self.box)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.box.pack_start(listbox, True, True, 0)

        def listboxset(type):
            children = listbox.get_children()
            for element in children:
                listbox.remove(element)
            if type == "Input":
                self.CurrentLayerType = "Input"

                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)
                vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                hbox.pack_start(vbox, True, True, 0)
                label1 = Gtk.Label(label="shape of input in brackets - like np.shape", xalign=0)
                label2 = Gtk.Label(label="will be padded / truncated", xalign=0)
                vbox.pack_start(label1, True, True, 0)
                vbox.pack_start(label2, True, True, 0)
                self.InputShape = Gtk.Entry()
                self.InputShape.props.valign = Gtk.Align.CENTER
                hbox.pack_start(self.InputShape, False, True, 0)
                listbox.add(row)

                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)
                label = Gtk.Label(label="Advanced: ragged / sparse input", xalign=0)
                label = Gtk.Label(label="ragged: Variable length inputs, often used with embedding", xalign=0)
                label = Gtk.Label(label="sparse: ragged / sparse input", xalign=0)
                self.misc = Gtk.ComboBoxText()
                self.misc.insert(0, "0", "None")
                self.misc.insert(1, "1", "ragged")
                self.misc.insert(2, "2", "sparse")
                hbox.pack_start(label, True, True, 0)
                hbox.pack_start(self.misc, False, True, 0)
                listbox.add(row)

                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)
                vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                hbox.pack_start(vbox, True, True, 0)
                label1 = Gtk.Label(label="ragged rank - only applicable to ragged input", xalign=0)
                label2 = Gtk.Label(label="k dimentional ragged input", xalign=0)
                vbox.pack_start(label1, True, True, 0)
                vbox.pack_start(label2, True, True, 0)
                self.RaggedRank = Gtk.Entry()
                self.RaggedRank.props.valign = Gtk.Align.CENTER
                hbox.pack_start(self.RaggedRank, False, True, 0)
                listbox.add(row)

                listbox.show_all()
            elif type == "Dense / Fully connected":
                self.CurrentLayerType = "Dense / Fully connected"

                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)
                vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                hbox.pack_start(vbox, True, True, 0)
                label1 = Gtk.Label(label="Number of layers (int)", xalign=0)
                vbox.pack_start(label1, True, True, 0)
                self.Layers = Gtk.Entry()
                self.Layers.props.valign = Gtk.Align.CENTER
                hbox.pack_start(self.Layers, False, True, 0)
                listbox.add(row)

                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)
                label = Gtk.Label(label="Activation function", xalign=0)
                self.activ = Gtk.ComboBoxText()
                self.activ.insert(0, "0", "None")
                self.activ.insert(1, "1", "exponential")
                self.activ.insert(2, "2", "gelu")
                self.activ.insert(3, "3", "hard_sigmoid")
                self.activ.insert(4, "4", "elu")
                self.activ.insert(5, "5", "relu")
                self.activ.insert(6, "6", "selu")
                self.activ.insert(7, "7", "sigmoid")
                self.activ.insert(8, "8", "softmax")
                self.activ.insert(9, "9", "softplus")
                self.activ.insert(10, "10", "softsign")
                self.activ.insert(11, "11", "swish")
                self.activ.insert(12, "12", "tanh")
                hbox.pack_start(label, True, True, 0)
                hbox.pack_start(self.activ, False, True, 0)
                listbox.add(row)

                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)
                label = Gtk.Label(label="Use Bias (y/n)", xalign=0)
                self.bias = Gtk.Entry()
                hbox.pack_start(label, True, True, 0)
                hbox.pack_start(self.bias, False, True, 0)
                listbox.add(row)

                listbox.show_all()
            elif type == "Flatten":
                self.CurrentLayerType = "Flatten"

                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
                row.add(hbox)
                vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                hbox.pack_start(vbox, True, True, 0)
                label1 = Gtk.Label(label="No parameters for this layer", xalign=0)
                vbox.pack_start(label1, True, True, 0)
                listbox.add(row)

                listbox.show_all()
            elif type == "Dropout":
                self.CurrentLayerType = "Dropout"

                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
                row.add(hbox)
                vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                hbox.pack_start(vbox, True, True, 0)
                label1 = Gtk.Label(label="Dropout (fraction set to zero) - must be 0 to 1", xalign=0)
                vbox.pack_start(label1, True, True, 0)
                self.Rate = Gtk.Entry()
                self.Rate.props.valign = Gtk.Align.CENTER
                hbox.pack_start(self.Rate, False, True, 0)
                listbox.add(row)

                listbox.show_all()

        listbox_2 = Gtk.ListBox()
        items = ["Input", "Dense / Fully connected", "Flatten", "Dropout"]

        for item in items:
            listbox_2.add(ListBoxRowWithData(item))

        def on_row_activated(listbox_widget, row):
            listboxset(row.data)

        listbox_2.connect("row-activated", on_row_activated)

        self.box.pack_start(listbox_2, True, True, 0)
        listbox_2.show_all()


        buttonbox = Gtk.ListBox()
        buttonbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.box.pack_start(buttonbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=200)
        row.add(hbox)
        self.button1 = Gtk.Button(label="Add layer")
        self.button1.connect("clicked", self.on_button1_clicked)
        hbox.pack_start(self.button1, True, True, 0)
        buttonbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=200)
        row.add(hbox)
        self.button1 = Gtk.Button(label="Save Model")
        self.button1.connect("clicked", self.on_button2_clicked)
        hbox.pack_start(self.button1, True, True, 0)
        buttonbox.add(row)


        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.props.min_content_height = 300
        scrolledwindow.props.min_content_width = 350
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        buttonbox.add(scrolledwindow)

        self.grid = Gtk.Grid()

        scrolledwindow.add(self.grid)


    def on_button1_clicked(self, widget):
        if self.CurrentLayerType == "Input":
            I = ""
            if self.misc.get_active_text() == "None":
                I = f"tf.keras.Input({self.InputShape.get_text()}),"
            elif self.misc.get_active_text() == None:
                I = f"tf.keras.Input({self.InputShape.get_text()}),"
            elif self.misc.get_active_text() == "sparse":
                I = f"tf.keras.Input({self.InputShape.get_text()}, sparse=True),"
            elif self.misc.get_active_text() == "ragged":
                none = ["None" for i in range(int(self.RaggedRank.get_text()))]
                I = f"tf.keras.Input({none}, ragged=True, ragged_rank={self.RaggedRank.get_text()}),"
            layers_list.append(I)
        elif self.CurrentLayerType == "Dense / Fully connected":
            try:
                bias = False
                if self.bias.get_text() == "y":
                    bias = True
                DF = f'tf.keras.layers.Dense(units={int(self.Layers.get_text())}, activation="{self.activ.get_active_text()}", use_bias={bias}),'
                layers_list.append(DF)
            except:
                pass
        elif self.CurrentLayerType == "Flatten":
            F = "tf.keras.layers.Flatten(),"
            layers_list.append(F)
        elif self.CurrentLayerType == "Dropout":
            rate = self.Rate.get_text()
            try:
                if float(rate) >= 0 and float(rate) <= 1:
                    D = f"tf.keras.layers.Dropout({float(self.Rate.get_text())}),"
                    layers_list.append(D)
            except:
                pass
        else:
            pass
        self.refresh()
    def on_button2_clicked(self, widget):
        program = f""
        program += f"model = tf.keras.Sequential([\n"

        for i in layers_list:
            program += f"{i}\n"

        program += "])"

        with open("model.txt", 'w') as f:
            f.write(program)

    def refresh(self):
        children = self.grid.get_children()
        for element in children:
            self.grid.remove(element)

        buttons = [[Gtk.Button(label="Delete"), Gtk.Button(label="Down"), Gtk.Button(label="Up"), i] for i in range(len(layers_list))]
        for i in range(len(layers_list)):
            textview = Gtk.TextView()
            textbuffer = textview.get_buffer()
            textbuffer.set_text(layers_list[i])
            self.grid.attach(textview, 1, i, 2, 1)
            self.grid.show_all()
            buttons[i][0].connect("clicked", self.delete, i)
            self.grid.attach_next_to(buttons[i][0], textview, Gtk.PositionType.LEFT, 1, 1)
            self.grid.show_all()
            buttons[i][1].connect("clicked", self.down, i)
            self.grid.attach_next_to(buttons[i][1], buttons[i][0], Gtk.PositionType.LEFT, 1, 1)
            self.grid.show_all()
            buttons[i][2].connect("clicked", self.up, i)
            self.grid.attach_next_to(buttons[i][2], buttons[i][1], Gtk.PositionType.LEFT, 1, 1)
            self.grid.show_all()

    def delete(self, widget, num):
        layers_list.pop(num)
        self.refresh()
    def up(self, widget, num):
        if num == len(layers_list):
            pass
        else:
            layers_list.insert(num+2, layers_list[num])
            layers_list.pop(num)
        self.refresh()
    def down(self, widget, num):
        if num == 0:
            pass
        else:
            layers_list.insert(num-1, layers_list[num])
            layers_list.pop(num+1)
        self.refresh()
