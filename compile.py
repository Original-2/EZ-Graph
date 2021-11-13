import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.add(Gtk.Label(label=data))

class CompWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Make Model")
        self.values_list = {"optimizer":None, "loss":None, "metrics":None}

        self.box = Gtk.Box(spacing=6)
        self.add(self.box)

        Scrolled = Gtk.ScrolledWindow()
        Scrolled.props.min_content_width = 350
        self.box.pack_start(Scrolled, True, True, 0)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        Scrolled.add(listbox)

        def listboxset(type):
            children = listbox.get_children()
            for element in children:
                listbox.remove(element)
            if type == "optimizer":
                self.CurrentType = "optimizer"
                for i in ["Adadelta","Adagrad","Adam","Adamax","Ftrl","Nadam","RMSprop","SGD"]:
                    if self.values_list["optimizer"] != i:
                        self.ModelMake = Gtk.Button(label=i)
                        self.ModelMake.connect("clicked", self.set, i)
                        listbox.add(self.ModelMake)

                listbox.show_all()
            elif type == "loss":
                self.CurrentType = "loss"
                losses = {"BinaryCrossentropy":"the cross-entropy (2 categories - 1 and 0 - in 1 unit). Data is binary (0 - 1).",
                "CategoricalCrossentropy":"the cross-entropy (n categories between 1 and 0 in n units). Data is one hot.",
                "SparseCategoricalCrossentropy":"the cross-entropy (n categories in n units - typically saves memory). Data is not one hot.",
                "Poisson":"a categorical loss (y_pred - y_true * log(y_pred)). Data is one hot.",
                "KLDivergence":"categorical in 1 unit - y_true * log(y_true / y_pred). Data is one hot.",
                "LogCosh":"regressive loss (log((exp(x) + exp(-x))/2), where x is the error y_pred - y_true). Data is continuous.",
                "MeanAbsoluteError":"regressive loss (abs(y_true - y_pred)). Data is continuous.",
                "MeanAbsolutePercentageError":"regressive loss (loss = 100 * abs(y_true - y_pred) / y_true). Data is continuous.",
                "MeanSquaredError":"regressive loss (square(y_true - y_pred)). Data is continuous.",
                "MeanSquaredLogarithmicError":"regressive loss (square(log(y_true + 1.) - log(y_pred + 1.))). Data is continuous.",
                "SquaredHinge":"regressive loss (square(maximum(1 - y_true * y_pred, 0))). Data is continuous."}
                loss = losses.keys()
                for i in loss:
                    if self.values_list["optimizer"] != i:
                        self.ModelMake = Gtk.Button(label=f"{i}: {losses[i]}")
                        self.ModelMake.connect("clicked", self.set, i)
                        listbox.add(self.ModelMake)

                listbox.show_all()
            elif type == "metrics":
                self.CurrentType = "metrics"
                metrics = {"Accuracy":"a categorical metric: correct / total",
                "AUC":"Categorical. The AUC (Area under the curve) of the ROC (Receiver operating characteristic; default)",
                "Precision":"Categorical. True positives / true positives + false positives",
                "Recall":"Categorical. True positives / true positives + false negatives.",
                "Poisson":"Probabilistic. y_pred - y_true * log(y_pred).",
                "MeanSquaredError":"Regression. square(y_true - y_pred)",
                "RootMeanSquaredError":"Regression. square root of mean square error",
                "MeanAbsoluteError":"Regression. abs(y_true - y_pred)",
                "MeanAbsolutePercentageError":"Regression. 100 * abs(y_true - y_pred) / y_true",
                "logcosh":"Regression. log((exp(x) + exp(-x))/2), where x is the error (y_pred - y_true)"}
                metric = metrics.keys()
                for i in metric:
                    if self.values_list["metrics"] != i:
                        self.ModelMake = Gtk.Button(label=f"{i}: {metrics[i]}")
                        self.ModelMake.connect("clicked", self.set, i)
                        listbox.add(self.ModelMake)


                listbox.show_all()

        listbox_2 = Gtk.ListBox()
        items = ["optimizer","loss","metrics"]

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
        self.button1 = Gtk.Button(label="Save")
        self.button1.connect("clicked", self.on_button2_clicked)
        hbox.pack_start(self.button1, True, True, 0)
        buttonbox.add(row)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.props.min_content_height = 300
        scrolledwindow.props.min_content_width = 350
        #scrolledwindow.set_hexpand(True)
        #scrolledwindow.set_vexpand(True)
        self.label = Gtk.Label()
        scrolledwindow.add(self.label)

        buttonbox.add(scrolledwindow)

    def on_button2_clicked(self, widget):
        program = f""

        program += f"model.compile("

        opt = self.values_list["optimizer"]
        loss = self.values_list["loss"]
        metrics = self.values_list["metrics"]
        program += f"optimiser={opt}, loss={loss}, metrics={metrics})"

        with open("compile.txt", 'w') as f:
            f.write(program)

    def set(self, widget, val):
        if self.CurrentType in ["optimizer","loss"]:
            self.values_list[self.CurrentType] = val
        else:
            try:
                self.values_list[self.CurrentType].append(val)
                self.values_list[self.CurrentType] = list(set(self.values_list[self.CurrentType]))
            except:
                self.values_list[self.CurrentType] = []
                self.values_list[self.CurrentType].append(val)

        opt = self.values_list["optimizer"]
        loss = self.values_list["loss"]
        metrics = self.values_list["metrics"]
        self.label.set_text(f"optimizer: '{opt}'\n loss: '{loss}'\n metrics: {metrics}")
