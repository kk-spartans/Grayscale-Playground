from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps

def update_image(image, weights):
    # Convert to grayscale using weighted average with user-defined weights
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert image to numpy array
    img_array = np.array(image)
    
    # Apply weights to each channel and sum
    r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
    grayscale = weights[0] * r + weights[1] * g + weights[2] * b
    
    # Convert back to PIL Image
    return Image.fromarray(grayscale.astype('uint8'))
    def update_sliders(sliders, changed_index):
        weights = [slider.get() for slider in sliders]
        total = sum(weights)
        if total > 0:
            remaining = 1.0 - weights[changed_index]
            if remaining >= 0:
                # Distribute remaining weight proportionally among other sliders
                other_total = sum(weights[i] for i in range(len(weights)) if i != changed_index)
                if other_total > 0:
                    ratio = remaining / other_total
                    for i in range(len(weights)):
                        if i != changed_index:
                            sliders[i].set(weights[i] * ratio)
                else:
                    # If other sliders are 0, distribute evenly
                    equal_share = remaining / (len(weights) - 1)
                    for i in range(len(weights)):
                        if i != changed_index:
                            sliders[i].set(equal_share)
def on_slider_change(image, sliders, canvas, img_label):
    weights = [slider.get() for slider in sliders]
    total = sum(weights)
    if total != 0:
        weights = [w / total for w in weights] 
    result_image = update_image(image, weights)
    result_image_tk = ImageTk.PhotoImage(result_image)
    img_label.config(image=result_image_tk)
    img_label.image = result_image_tk

def main():
    root = tk.Tk()
    root.title("Image Grayscale Converter")

    # Load the image
    image_path = filedialog.askopenfilename()
    image = Image.open(image_path)
    image_tk = ImageTk.PhotoImage(image)

    # Create a canvas to display the image
    canvas = tk.Canvas(root, width=image.width, height=image.height)
    canvas.pack(side=tk.LEFT)
    img_label = tk.Label(canvas, image=image_tk)
    img_label.image = image_tk
    img_label.pack()

    # Create sliders for weights
    sliders_frame = tk.Frame(root)
    sliders_frame.pack(side=tk.RIGHT, fill=tk.Y)

    sliders = []
    for color in ['Red', 'Green', 'Blue']:
        label = tk.Label(sliders_frame, text=f"Weight for {color}")
        label.pack()
        slider = tk.Scale(sliders_frame, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
        slider.set(0.33)  # Default value
        slider.pack()
        sliders.append(slider)

    # Update image when sliders change
    for slider in sliders:
        slider.config(command=lambda _: on_slider_change(image, sliders, canvas, img_label))

    root.mainloop()

if __name__ == "__main__":
    main()
