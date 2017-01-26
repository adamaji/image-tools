import os
import sys
from PIL import Image, ImageTk
import Tkinter as tk

usage = "python manualBinaryImageClassifier.py [list of all img paths] [class name]"
_YES = "y"
_NO = "n"

class BinaryImageClassifier(tk.Frame):
  def __init__(self, root, img_path, class_name):
    self.img_list = []
    self.yes_list = []
    self.no_list = []
    with open(img_path, "r") as imgs:
      self.img_list = filter(None, imgs.read().split("\n"))

    self.img_index = 0

    self.root = root
    root.title("Manual binary image classifier")

    self.class_name = class_name
    self.img_path = img_path
    self.img = ImageTk.PhotoImage(file=self.img_list[0])
    self.label = tk.Label(root, text="Is this image a(n) "+class_name+"?")
    self.label.pack()
    self.directions = tk.Label(root, text="Press 'y' or 'n' to answer, or another key to go back")
    self.directions.pack()
    self.img_widget = tk.Label(root, image=self.img)
    self.img_widget.pack()

    self.root.bind("<KeyRelease>", self.keypress)

  def keypress(self, event):
    key = event.char.lower()
    if key == _YES or key == _NO:
      if key == _YES:
        self.yes_list.append(self.img_index)
        print("yes, classifying as " + self.class_name)
      elif key == _NO:
        self.no_list.append(self.img_index)
        print("no, not classifying")

      self.img_index += 1
      if self.img_index >= len(self.img_list):
        self.quit()
        sys.exit(1)

    else:
      if self.img_index > 0:
        print("retracting previous classification")
        self.img_index -= 1
        if self.img_index in self.yes_list:
          self.yes_list.remove(self.img_index)
        else:
          self.no_list.remove(self.img_index)

    self.img = ImageTk.PhotoImage(file=self.img_list[self.img_index])
    self.img_widget.configure(image= self.img)
    self.label.configure(text= str(self.img_index) + " Is this image a(n) " + self.class_name + "?")

  def quit(self):
    print("Done, now writing results to " + self.img_path + ".yes.txt and " + self.img_path + ".no.txt")
    yes_img = [self.img_list[i] for i in self.yes_list]
    no_img = [self.img_list[i] for i in self.no_list]
    with open(self.img_path + ".yes.txt", "w") as f:
      for img in yes_img:
        f.write(img + "\n")
    with open(self.img_path + ".no.txt", "w") as f:
      for img in no_img:
        f.write(img + "\n")

    self.root.destroy()

if __name__ == "__main__":
  if len(sys.argv) != 3:
    print usage
    sys.exit(-1)

  img_list_path = sys.argv[1]
  class_name = sys.argv[2]
  root = tk.Tk()
  classifier_gui = BinaryImageClassifier(root, img_list_path, class_name)
  root.mainloop()
