import cv2
import easygui
import numpy as np
import imageio
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Label, Button, TOP
from PIL import ImageTk, Image

def cartoonify(ImagePath):
    # Read the image
    original_image = cv2.imread(ImagePath)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    
    # Confirm that image is chosen
    if original_image is None:
        print("Cannot find any image. Choose an appropriate file.")
        sys.exit()
    
    resized_original = cv2.resize(original_image, (960, 540))

    # Convert image to grayscale
    gray_scale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    resized_gray = cv2.resize(gray_scale_image, (960, 540))

    # Apply median blur
    smooth_gray_scale = cv2.medianBlur(gray_scale_image, 5)
    resized_smooth_gray = cv2.resize(smooth_gray_scale, (960, 540))

    # Retrieve edges using adaptive threshold
    edges = cv2.adaptiveThreshold(smooth_gray_scale, 255, 
                                  cv2.ADAPTIVE_THRESH_MEAN_C, 
                                  cv2.THRESH_BINARY, 9, 9)
    resized_edges = cv2.resize(edges, (960, 540))

    # Apply bilateral filter
    color_image = cv2.bilateralFilter(original_image, 9, 300, 300)
    resized_color = cv2.resize(color_image, (960, 540))

    # Mask edges with the color image
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=edges)
    resized_cartoon = cv2.resize(cartoon_image, (960, 540))

    # Plot the images
    images = [resized_original, resized_gray, resized_smooth_gray, resized_edges, resized_color, resized_cartoon]
    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []}, gridspec_kw={'hspace': 0.1, 'wspace': 0.1})
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    
    save_button = Button(top, text="Save cartoon image", command=lambda: save_image(resized_cartoon, ImagePath), padx=30, pady=5)
    save_button.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
    save_button.pack(side=TOP, pady=50)
    
    plt.show()

def save_image(cartoon_image, ImagePath):
    # Save the image
    new_name = "cartoonified_Image"
    path = os.path.join(os.path.dirname(ImagePath), new_name + os.path.splitext(ImagePath)[1])
    cv2.imwrite(path, cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR))
    message = f"Image saved by name {new_name} at {path}"
    messagebox.showinfo(title=None, message=message)

def upload():
    image_path = easygui.fileopenbox()
    cartoonify(image_path)

# Setup Tkinter window
top = tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image!')
top.configure(background='white')

upload_button = Button(top, text="Cartoonify an Image", command=upload, padx=10, pady=5)
upload_button.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
upload_button.pack(side=TOP, pady=50)

top.mainloop()
