import gi
import pandas as pd

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

layers_list = []
CurrentLayerType = None

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.add(Gtk.Label(label=data))


class LabelWindow(Gtk.Window):
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
            if type == "Text data":
                self.CurrentLayerType = "Text data"

                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
                row.add(hbox)
                vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                hbox.pack_start(vbox, True, True, 0)
                label1 = Gtk.Label(label="File with data", xalign=0)
                vbox.pack_start(label1, True, True, 0)
                self.File = Gtk.FileChooserButton()
                self.File.props.valign = Gtk.Align.CENTER
                hbox.pack_start(self.File, False, True, 0)
                self.select = Gtk.Button(label="Select")
                self.select.connect("clicked", self.choose, listbox)
                hbox.pack_start(self.select, True, True, 0)
                listbox.add(row)

                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)
                label = Gtk.Label(label="Maximum length of text - only if padded", xalign=0)
                label1 = Gtk.Label(label="leave 0 if limit is maximum length", xalign=0)
                self.maxlen = Gtk.Entry()
                hbox.pack_start(label, True, True, 0)
                hbox.pack_start(label1, True, True, 0)
                hbox.pack_start(self.maxlen, False, True, 0)
                listbox.add(row)

                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)
                label = Gtk.Label(label="Pad sequences (y/n)", xalign=0)
                self.padd = Gtk.Entry()
                hbox.pack_start(label, True, True, 0)
                hbox.pack_start(self.padd, False, True, 0)
                listbox.add(row)

                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)
                label = Gtk.Label(label="Char level (y/n)", xalign=0)
                self.char = Gtk.Entry()
                hbox.pack_start(label, True, True, 0)
                hbox.pack_start(self.char, False, True, 0)
                listbox.add(row)

                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)
                label = Gtk.Label(label="Vocab size (0 for no limit)", xalign=0)
                self.vocab = Gtk.Entry()
                hbox.pack_start(label, True, True, 0)
                hbox.pack_start(self.vocab, False, True, 0)
                listbox.add(row)

                listbox.show_all()

        listbox_2 = Gtk.ListBox()
        items = ["Text data"]

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
        self.button1 = Gtk.Button(label="Save data")
        self.button1.connect("clicked", self.on_button2_clicked)
        hbox.pack_start(self.button1, True, True, 0)
        buttonbox.add(row)

    def choose(self, widget, list):
        self.data = pd.read_csv(self.File.get_filename())
        labels = self.data.columns.tolist()

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label(label="Row", xalign=0)
        self.row = Gtk.ComboBoxText()

        for i in range(len(labels)):
            self.row.insert(i, str(i), labels[i])

        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(self.row, False, True, 0)
        list.add(row)

        list.show_all()


    def on_button2_clicked(self, widget):
        if self.CurrentLayerType == "Text data":
            program = f"x = pd.read_csv('{self.File.get_filename()}')\n"
            program += f'x = x["{self.row.get_active_text()}"]\n\n'

            if self.CurrentLayerType == "Text data":
                if self.char.get_text() == "y":
                    char = "True"
                else:
                    char = "False"

                vocab = "None"
                try:
                    if int(self.vocab.get_text()) > 0:
                        vocab = int(self.vocab.get_text())
                except:
                    pass

                program += f"tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words={vocab}, char_level={char})\n"
                program += f"tokenizer.fit_on_texts(x)\n"
                program += f"total_words = len(tokenizer.word_index) + 1\n"
                program += f"x = tokenizer.texts_to_sequences(x)\n\n"

                if self.padd.get_text() == "y":
                    maxlen = "None"
                    try:
                        if int(self.maxlen.get_text()) > 0:
                            maxlen = int(self.maxlen.get_text())
                    except:
                        pass
                    program += f"x = tf.keras.preprocessing.sequence.pad_sequences(x, maxlen={maxlen})\n"
                    program += f"x = np.array(x)"
        with open("datax.txt", 'w') as f:
            f.write(program)
