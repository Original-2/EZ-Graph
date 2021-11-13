import gi
import layers
import compile
import fit
import datax
import datay

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# add main menu + model compilation section
class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Make Model")

        self.box = Gtk.Box(spacing=6)
        self.add(self.box)

        list = Gtk.ListBox()
        self.box.pack_start(list, True, True, 0)

        self.ModelMake = Gtk.Button(label="input data (x)")
        self.ModelMake.connect("clicked", self.newWin, datax.LabelWindow())
        list.add(self.ModelMake)

        self.ModelMake = Gtk.Button(label="output data (y)")
        self.ModelMake.connect("clicked", self.newWin, datay.LabelWindow())
        list.add(self.ModelMake)

        self.ModelMake = Gtk.Button(label="Make model")
        self.ModelMake.connect("clicked", self.newWin, layers.LayerWindow())
        list.add(self.ModelMake)

        self.ModelMake = Gtk.Button(label="Compile model")
        self.ModelMake.connect("clicked", self.newWin, compile.CompWindow())
        list.add(self.ModelMake)

        self.ModelMake = Gtk.Button(label="Train model")
        self.ModelMake.connect("clicked", self.newWin, fit.TrainWindow())
        list.add(self.ModelMake)

        self.ModelMake = Gtk.Button(label="Make it into a python script")
        self.ModelMake.connect("clicked", self.makePyScript)
        list.add(self.ModelMake)

    def newWin(self, widget, window):
        layerwin = window
        layerwin.show_all()

    def makePyScript(self, widget):
        program = f"import tensorflow as tf\n"
        program += f"import numpy as np\n"
        program += f"import pandas as pd\n\n"

        try:
            with open("datax.txt", "r") as file:
                program += f"# x data (inputs)\n"
                program += file.read()
                program += f"\n\n"
        except:
            program += "#No inputs defined\n\n"

        try:
            with open("datay.txt", "r") as file:
                program += f"# y data (labels)\n"
                program += file.read()
                program += f"\n\n"
        except:
            program += "#No labels defined\n\n"

        try:
            with open("model.txt", "r") as file:
                program += f"# model\n"
                program += file.read()
                program += f"\n\n"
        except:
            program += "#No model defined\n\n"

        try:
            with open("compile.txt", "r") as file:
                program += f"# compilation\n"
                program += file.read()
                program += f"\n\n"
        except:
            program += "#No compilation defined\n\n"

        try:
            with open("train.txt", "r") as file:
                program += f"# training\n"
                program += file.read()
                program += f"\n\n"
        except:
            program += "#No training defined\n\n"

        with open("training.py", 'w') as f:
            f.write(program)


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
