import tkinter as tk
import os
import random
from PIL import Image, ImageTk
from playsound import playsound

WINDOW_TITLE = "My Wardrobe"
WINDOW_HEIGHT = 350
WINDOW_WIDTH = 600
IMG_WIDTH = 250
IMG_HEIGHT = 250

#Store all the tops in the file we can access & skip the hidden files
ALL_TOPS = [str('tops/') + imagefile for imagefile in os.listdir("tops/") if not imagefile.startswith('.')]
ALL_BOTTOMS = [str('bottoms/') + imagefile for imagefile in os.listdir("bottoms/") if not imagefile.startswith('.')]

class wardrobeApp:
    def __init__(self, root):
        self.root = root

        #show top/bottoms image in the window
        self.tops_images = ALL_TOPS
        self.bottoms_images = ALL_BOTTOMS

        #Save single top & bottom image
        self.top_image_path = self.tops_images[0]
        self.bottom_image_path = self.bottoms_images[0]

        #create and add top & bottom image into frame
        self.tops_frame = tk.Frame(self.root)
        self.top_image_label = self.create_photo(self.top_image_path, self.tops_frame)

        self.bottoms_frame = tk.Frame(self.root)
        self.bottom_image_label = self.create_photo(self.bottom_image_path, self.bottoms_frame)


        #add it to the pack
        self.top_image_label.pack(side=tk.TOP)
        self.bottom_image_label.pack(side=tk.TOP)

        #Create background
        self.create_background()

    def create_background(self):
        self.root.title(WINDOW_TITLE)
        self.root.geometry('{0}x{1}'.format(WINDOW_HEIGHT, WINDOW_WIDTH))

        #add all buttons
        self.create_buttons()

        #add clothing
        self.tops_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.bottoms_frame.pack(fill=tk.BOTH, expand=tk.YES)

    def create_buttons(self):
        tops_prev_btn = tk.Button(self.tops_frame, text="PREV", command= self.get_next_top)
        tops_prev_btn.pack(side=tk.LEFT)

        create_outfit_btn = tk.Button(self.bottoms_frame, text="CREATE OUTFIT", command= self.create_outfit)
        create_outfit_btn.pack(side=tk.LEFT)

        tops_next_btn = tk.Button(self.tops_frame, text="NEXT", command= self.get_prev_top)
        tops_next_btn.pack(side=tk.RIGHT)

        bottoms_prev_btn = tk.Button(self.bottoms_frame, text="PREV", command= self.get_prev_bottom)
        bottoms_prev_btn.pack(side=tk.LEFT)
        bottoms_next_btn = tk.Button(self.bottoms_frame, text="NEXT", command= self.get_next_bottom)
        bottoms_next_btn.pack(side=tk.RIGHT)


    #general function to change images prev and next
    def _get_next_item(self, current_item, category, increment=True):

        # if we know the current position, then we can find the before/after it
        item_index = category.index(current_item)
        final_index = len(category) - 1
        next_index = 0

        #consider the edge cases
        if increment and item_index==final_index:
            # add the end, and need to up, cycle back to the beginning
            next_index=0
        elif not increment and item_index==0:
            #cycle back to end
            next_index= final_index
        else:
            #regular up and down
            #increment by 1
            increment=1 if increment else -1
            next_index = item_index + increment

        next_image = category[next_index]
        # reset and update the image based on the next image path
        if current_item in self.tops_images:
            image_label = self.top_image_label
            self.top_image_path = next_image
        else:
            image_label = self.bottom_image_label
            self.bottom_image_path = next_image

        #use update function to change the image
        self.update_image(next_image, image_label)

    def get_next_top(self):
        self._get_next_item(self.top_image_path, self.tops_images)

    def get_prev_top(self):
        self._get_next_item(self.top_image_path, self.tops_images, increment=False)

    def get_next_bottom(self):
        self._get_next_item(self.bottom_image_path, self.bottoms_images)

    def get_prev_bottom(self):
        self._get_next_item(self.bottom_image_path, self.bottoms_images, increment=False)

    def update_image(self, new_image_path, image_label):
        image_file = Image.open(new_image_path)
        image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
        tk_photo = ImageTk.PhotoImage(image_resized)

        #update based on the provided image label
        image_label.configure(image=tk_photo)

        #weird tkinter quirk
        image_label.image = tk_photo


    def create_photo(self, image_path, frame):
        image_file = Image.open(image_path)
        image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
        tk_photo = ImageTk.PhotoImage(image_resized)
        image_label = tk.Label(frame, image=tk_photo, anchor=tk.CENTER)

        #weird tkinter quirk
        image_label.image = tk_photo

        # so we can add later
        return image_label

    def create_outfit(self):
        #select top and bottom
        new_top_index = random.randint(0, len(self.tops_images)-1)
        new_bottom_index = random.randint(0, len(self.bottoms_images)-1)

        # add the clothes onto the screen
        self.update_image(self.tops_images[new_top_index], self.top_image_label)
        self.update_image(self.bottoms_images[new_bottom_index], self.bottom_image_label)

        #add noise


root = tk.Tk()
app = wardrobeApp(root)
print(ALL_TOPS)
root.mainloop()
