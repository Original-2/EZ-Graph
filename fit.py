import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class TrainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Make Model")
        self.values_list = {"optimizer":None, "loss":None, "metrics":None}

        self.box = Gtk.Box(spacing=6)
        self.add(self.box)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.box.pack_start(listbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox, True, True, 0)
        label1 = Gtk.Label(label="batch size (int - otherwise defaults to none)", xalign=0)
        vbox.pack_start(label1, True, True, 0)
        self.BatchSize = Gtk.Entry()
        self.BatchSize.props.valign = Gtk.Align.CENTER
        hbox.pack_start(self.BatchSize, False, True, 0)
        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox, True, True, 0)
        label1 = Gtk.Label(label="epochs (int - otherwise defaults to 1)", xalign=0)
        vbox.pack_start(label1, True, True, 0)
        self.EpochNum = Gtk.Entry()
        self.EpochNum.props.valign = Gtk.Align.CENTER
        hbox.pack_start(self.EpochNum, False, True, 0)
        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox, True, True, 0)
        label1 = Gtk.Label(label="validation split (float between 0 and 1 - otherwise defaults to 0)", xalign=0)
        vbox.pack_start(label1, True, True, 0)
        self.ValSplit = Gtk.Entry()
        self.ValSplit.props.valign = Gtk.Align.CENTER
        hbox.pack_start(self.ValSplit, False, True, 0)
        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label(label="verbose (visualisation of epochs)", xalign=0)
        self.verbose = Gtk.ComboBoxText()
        self.verbose.insert(0, "0", "Silent")
        self.verbose.insert(1, "1", "Progress bar")
        self.verbose.insert(2, "2", "1 line per epoch")
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(self.verbose, False, True, 0)
        listbox.add(row)

        buttonbox = Gtk.ListBox()
        buttonbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.box.pack_start(buttonbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=200)
        row.add(hbox)
        self.button1 = Gtk.Button(label="Save")
        self.button1.connect("clicked", self.on_button2_clicked)
        hbox.pack_start(self.button1, True, True, 0)
        buttonbox.add(row)

    def on_button2_clicked(self, widget):
        program = f""

        program += f"model.fit("

        batch = self.BatchSize.get_text()
        epoch = self.EpochNum.get_text()
        split = self.ValSplit.get_text()

        try:
            batch = int(batch)
        except:
            batch = None

        try:
            epoch = int(epoch)
        except:
            epoch = 1

        try:
            split = float(split)
        except:
            split = 0

        if self.verbose.get_active_text == "Silent":
            verbose = 0
        elif self.verbose.get_active_text == "Progress bar":
            verbose = 1
        else:
            verbose = 2


        program += f"x=x, y=y, batch_size={batch}, epochs={epoch}, validation_split={split}, verbose={verbose})"

        with open("train.txt", 'w') as f:
            f.write(program)
