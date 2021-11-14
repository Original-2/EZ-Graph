import gi # used for GTK import

import layers # other pages
import compile
import fit
import datax
import datay

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk # used to make windows for GUI

# add main menu + model compilation section
class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Make Model")

        self.box = Gtk.Box(spacing=6) # create a box which will contain all buttons
        self.add(self.box)

        list = Gtk.ListBox() # create a box inside the box for proper formatting
        self.box.pack_start(list, True, True, 0)

        self.InputData = Gtk.Button(label="input data (x)") # create a button for input data
        self.InputData.connect("clicked", self.newWin, datax.LabelWindow()) # link function to
        list.add(self.InputData) # add button to box (make it visible)

        self.OutData = Gtk.Button(label="output data (y)") # see "input data" field
        self.OutData.connect("clicked", self.newWin, datay.LabelWindow())
        list.add(self.OutData)

        self.ModelMake = Gtk.Button(label="Make model") # see "input data" field
        self.ModelMake.connect("clicked", self.newWin, layers.LayerWindow())
        list.add(self.ModelMake)

        self.CompModel = Gtk.Button(label="Compile model") # see "input data" field
        self.CompModel.connect("clicked", self.newWin, compile.CompWindow())
        list.add(self.CompModel)

        self.ModelTrain = Gtk.Button(label="Train model") # see "input data" field
        self.ModelTrain.connect("clicked", self.newWin, fit.TrainWindow())
        list.add(self.ModelTrain)

        self.PyScriptMake = Gtk.Button(label="Make it into a python script") # creats a button to make a python script
        self.PyScriptMake.connect("clicked", self.makePyScript) # make function run on click - turns all inputed data into a .py script
        list.add(self.PyScriptMake) # add button to box (make it visible)

    def newWin(self, widget, window):
        layerwin = window
        layerwin.show_all() # opens a new window predetermined in the "connect" function

    def makePyScript(self, widget): # creates a python script that can be run to train the neural network
        program = f"import tensorflow as tf\n" # manage imports - these are the common libraries that may be needed
        program += f"import numpy as np\n"
        program += f"import pandas as pd\n\n"

        # the following files are written in other windows, accessed by the the "newWin" buttons

        try: # if the "datax.txt" file exists, it will be read and added to the program
            with open("datax.txt", "r") as file:
                program += f"# x data (inputs)\n"
                program += file.read()
                program += f"\n\n"
        except:
            program += "#No inputs defined\n\n"

        try: # if the "datay.txt" file exists, it will be read and added to the program
            with open("datay.txt", "r") as file:
                program += f"# y data (labels)\n"
                program += file.read()
                program += f"\n\n"
        except:
            program += "#No labels defined\n\n"

        try: # if the "model.txt" file exists, it will be read and added to the program
            with open("model.txt", "r") as file:
                program += f"# model\n"
                program += file.read()
                program += f"\n\n"
        except:
            program += "#No model defined\n\n"

        try: # if the "compile.txt" file exists, it will be read and added to the program
            with open("compile.txt", "r") as file:
                program += f"# compilation\n"
                program += file.read()
                program += f"\n\n"
        except:
            program += "#No compilation defined\n\n"

        try: # if the "train.txt" file exists, it will be read and added to the program
            with open("train.txt", "r") as file:
                program += f"# training\n"
                program += file.read()
                program += f"\n\n"
        except:
            program += "#No training defined\n\n"

        with open("training.py", 'w') as f: # write the program to a python file in the current directory
            f.write(program)


win = MyWindow() # creates the window
win.connect("destroy", Gtk.main_quit) # closing the main window closes all other ones
win.show_all() # make the elements (buttons, boxes etc.) visible
Gtk.main() # run the program
