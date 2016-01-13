import tkinter
import tkinter.filedialog
from PIL import ImageTk
import common


class GUI(object):

    RADIOBUTTON_LIST = [
        "Real",
        "Imaginary",
        "Phase",
        "Amplitude"
    ]

    SIZE_LIST = [
        "200%",
        "150%",
        "100%",
        "50%",
        "25%"
    ]

    def __init__(self, width, height):
        self._root = tkinter.Tk()
        self._root.geometry("%sx%s" % (width, height))
        self._l_label = tkinter.Label(self._root)
        self._r_label = tkinter.Label(self._root)
        self._l_label.grid(row=0, column=0)
        self._r_label.grid(row=0, column=1)
        self._l_img = None
        self._r_img = None

        self._value = tkinter.StringVar()
        self._old_val = "Real"
        self._value.set("Real")

        self._size_value = tkinter.StringVar()
        self._old_size_val = "100%"
        self._size_value.set("100%")

        self._oryg_file = None

        self._add_menu()

    def _add_menu(self):
        menubar = tkinter.Menu(self._root)

        file_menu = tkinter.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self._open_file)
        file_menu.add_command(label="Exit", command=self._root.destroy)

        show_menu = tkinter.Menu(menubar, tearoff=0)
        for text in GUI.RADIOBUTTON_LIST:
            show_menu.add_radiobutton(label=text, variable=self._value, value=text, command=self._change_fft)

        size_menu = tkinter.Menu(menubar, tearoff=0)
        for text in GUI.SIZE_LIST:
            size_menu.add_radiobutton(label=text, variable=self._size_value, value=text, command=self._change_size)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Show", menu=show_menu)
        menubar.add_cascade(label="size", menu=size_menu)

        self._root.config(menu=menubar)

    def _display_image_left(self, image):
        self._display_image(image, self._l_label)

    def _display_image_right(self, image):
        self._display_image(image, self._r_label)

    def _display_image(self, image, pane):
        tkimage = ImageTk.PhotoImage(image)

        pane.configure(image=tkimage)
        pane.tkimage = tkimage
        pane.image = image

    def start(self):
        self._root.mainloop()

    def _open_file(self):
        ftypes = [('Image Files', '*.tif *.jpg *.png')]
        dlg = tkinter.filedialog.Open(self._root, filetypes=ftypes)
        filename = dlg.show()

        try:
            self._oryg_file = common.open_image(filename)
            self._change_images()
        except AttributeError as ex:
            print("Choose a file! " + str(ex))

    def _change_fft(self):
        if self._value.get() == self._old_val:
            return

        self._old_val = self._value.get()
        try:
            im = common.FFT(self._oryg_file, self._value.get(), self._size_value.get())
            self._display_image_right(im)
        except Exception as e:
            print("An exception occurred while reloading images " + str(e))

    def _change_size(self):
        if self._size_value.get() == self._old_size_val:
            return

        self._old_size_val = self._size_value.get()
        self._change_images()

    def _change_images(self):
        try:
            im = common.resize(self._oryg_file, self._size_value.get())
            im2 = common.FFT(self._oryg_file, self._value.get(), self._size_value.get())
            self._display_image_left(im)
            self._display_image_right(im2)
            self._root.geometry("%sx%s" % (im.size[0]*2 + 8, im.size[1] + 4))
        except Exception as e:
            print("An exception occurred while reloading images! " + str(e))


