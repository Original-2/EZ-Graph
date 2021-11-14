import gi # used for GTK import
import pandas as pd # used for csv files

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk # used for gtk elements

CurrentLayerType = None # current input data type

class ListBoxRowWithData(Gtk.ListBoxRow): # creates list of all possible input data types
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.add(Gtk.Label(label=data))


class LabelWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Make Model")

        self.box = Gtk.Box(spacing=6) # box for the rest of the content to be contained in
        self.add(self.box)

        listbox = Gtk.ListBox() # left hand column, this contains all of the options for the current data type selected
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.box.pack_start(listbox, True, True, 0)

        def listboxset(type): # function that sets / resets the left hand column
            children = listbox.get_children()
            for element in children: # empties the listbox so new content can fill it
                listbox.remove(element)
            if type == "Regression data": # if the selected type is "Regression data"
                self.CurrentLayerType = "Regression data" # sets the variable for later usage

                row = Gtk.ListBoxRow() # a selection field for the the CSV file that will be used
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
                listbox.show_all()

            elif type == "Classification data": # if the selected type is "Classification data"
                self.CurrentLayerType = "Classification data" # sets the variable for later usage

                row = Gtk.ListBoxRow() # a selection field for the the CSV file that will be used
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

                row = Gtk.ListBoxRow() # a section describing what I meen by "sparse" and "dense" data
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)
                label = Gtk.Label(label="sparse data - data in labels is in 1 number e.g. 1,3,2", xalign=0)
                hbox.pack_start(label, True, True, 0)
                listbox.add(row)
                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)
                label = Gtk.Label(label="dense data - data in labels is in 1 number e.g. [1,0,0], [0,0,1], [0,1,0]", xalign=0)
                hbox.pack_start(label, True, True, 0)
                listbox.add(row)

                row = Gtk.ListBoxRow() # gives the selection on how the model will be trained
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)
                label = Gtk.Label(label="Model trained on Sparse or Regular data", xalign=0)
                self.sparse = Gtk.ComboBoxText()
                self.sparse.insert(0, "0", "Sparse")
                self.sparse.insert(1, "1", "Regular")
                hbox.pack_start(label, True, True, 0)
                hbox.pack_start(self.sparse, False, True, 0)
                listbox.add(row)

                row = Gtk.ListBoxRow() # explains what I mean by Uncategorised data
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)
                label = Gtk.Label(label="Uncategorised data - data is not put into categories e.g. dog, cat, snake", xalign=0)
                hbox.pack_start(label, True, True, 0)
                listbox.add(row)

                row = Gtk.ListBoxRow() # asks user what data they will provide
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)
                label = Gtk.Label(label="You will provide:", xalign=0)
                self.provided = Gtk.ComboBoxText()
                self.provided.insert(0, "0", "Sparse")
                self.provided.insert(1, "1", "Regular")
                self.provided.insert(2, "2", "Uncategorised")
                hbox.pack_start(label, True, True, 0)
                hbox.pack_start(self.provided, False, True, 0)
                listbox.add(row)

                listbox.show_all() # show the list box

        listbox_2 = Gtk.ListBox()
        items = ["Regression data", "Classification data"] # list of possible input data types

        for item in items:
            listbox_2.add(ListBoxRowWithData(item)) # displays all of the input data types

        def on_row_activated(listbox_widget, row):
            listboxset(row.data) # when a data type is selected, the corresponding row is shown

        listbox_2.connect("row-activated", on_row_activated)

        self.box.pack_start(listbox_2, True, True, 0)
        listbox_2.show_all() # make the middle row visible after configuring it


        buttonbox = Gtk.ListBox() # final row created
        buttonbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.box.pack_start(buttonbox, True, True, 0)

        row = Gtk.ListBoxRow() # create a txt file with selected information
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=200)
        row.add(hbox)
        self.button1 = Gtk.Button(label="Save data")
        self.button1.connect("clicked", self.on_button2_clicked)
        hbox.pack_start(self.button1, True, True, 0)
        buttonbox.add(row)

    def choose(self, widget, list): # reads the selected csv file and lets user select what row to use
        self.data = pd.read_csv(self.File.get_filename()) # read csv
        labels = self.data.columns.tolist() # list of all columns

        row = Gtk.ListBoxRow() # created a dropdown menu with all of the rows
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label(label="Row", xalign=0)
        self.row = Gtk.ComboBoxText()

        for i in range(len(labels)):
            self.row.insert(i, str(i), labels[i])

        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(self.row, False, True, 0)
        list.add(row)

        list.show_all() # make it visible

    def on_button2_clicked(self, widget): # save data
        if self.CurrentLayerType == "Regression data": # simply convert regression data into a numpy array
            program = f"y = pd.read_csv('{self.File.get_filename()}')\n"
            program += f'y = y["{self.row.get_active_text()}"]\n\n'
            program += f"y = np.array(y)"
        elif self.CurrentLayerType == "Classification data": # depending on the options selected, there are many ways that it can handle classification daya
            program = f"y = pd.read_csv('{self.File.get_filename()}')\n"
            program += f'y = y["{self.row.get_active_text()}"]\n\n'

            if self.provided.get_active_text() == self.sparse.get_active_text(): # same format as provided, no conversion needed
                pass
            elif self.provided == "Sparse": # sparse to regular conversion
                program += f"unique = pd.unique(y)\n"
                program += f"tempy = [[0 for i in range(len(unique))] for j in range(len(y))]\n"
                program += f"for i in range(len(tempy)):\n"
                program += f"\tfor j in range(len(tempy[i])):\n"
                program += f"\t\tif y[i] == j:\n"
                program += f"\t\t\ttempy[i][j] = 1\n"
                program += f"y = tempy\n"
                program += f"del(tempy)"
            elif self.provided == "Regular": # regular to sparse conversion
                program += f"unique = pd.unique(y)\n"
                program += f"tempy = [0 for i in range(len(y))]\n"
                program += f"for i in range(len(y)):\n"
                program += f"\tfor j in range(len(y[i])):\n"
                program += f"\t\tif y[i] == j:\n"
                program += f"\t\t\ttempy[i] = j\n"
                program += f"y = tempy\n"
                program += f"del(tempy)"
            else:
                program += f"unique = pd.unique(y)\n"
                if self.sparse == "Sparse": # uncategorised to sparse
                    program += f"tempy = [0 for i in range(len(y))]\n"
                    program += f"for i in range(len(tempy)):\n"
                    program += f"\ttempy[i] = unique.index(y[i])\n"
                    program += f"y = tempy\n"
                    program += f"del(tempy)"
                if self.sparse == "Regular": # uncategorised to dense
                    program += f"tempy = [[0 for i in range(len(unique))] for j in range(len(y))]\n"
                    program += f"for i in range(len(tempy)):\n"
                    program += f"\ttempy[i][unique.index(y[i])] = 1\n"
                    program += f"y = tempy\n"
                    program += f"del(tempy)"
            program += f"y = np.array(y)"

        with open("datay.txt", 'w') as f: # write all data to a txt file
            f.write(program)
