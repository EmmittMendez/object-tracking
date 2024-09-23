# Import the required packages
import argparse
import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np


parser = argparse.ArgumentParser()

parser.add_argument("index_camera", help="index of the camera to read from", type=int)
args = parser.parse_args()

capture = cv2.VideoCapture(args.index_camera)

# Check if camera opened successfully
if capture.isOpened() is False:
    print("Error opening the camera")
    exit()
    
# Creamos la ventana de matplotlib
fig, ax = plt.subplots(1,2, figsize=(10, 5))
plt.subplots_adjust(bottom=0.35)
plt.title('Segmentación de objetos')

# Verificamos si la ventana esta cerrada
window_open = True

def on_close(event):
    global window_open
    window_open = False

fig.canvas.mpl_connect('close_event', on_close)

# Creamos los ejes minimos para los sliders h, s, v
axihmin = plt.axes([0.1, 0.2, 0.25, 0.03])
axismin = plt.axes([0.1, 0.15, 0.25, 0.03])
axivmin = plt.axes([0.1, 0.1, 0.25, 0.03])

# Creamos los ejes maximos para los sliders h, s, v
axihmax = plt.axes([0.6, 0.2, 0.25, 0.03])
axismax = plt.axes([0.6, 0.15, 0.25, 0.03])
axivmax = plt.axes([0.6, 0.1, 0.25, 0.03])

# Creamos lo slider para los minimos
hmin = Slider(axihmin, 'Hue min', 0.0, 179.0, valinit=0)
smin = Slider(axismin, 'Saturation min', 0.0, 255.0, valinit=0)
vmin = Slider(axivmin, 'Value min', 0.0, 255.0, valinit=0)

# Creamos lo slider para los maximos
hmax = Slider(axihmax, 'Hue max', 0.0, 179.0, valinit=179)
smax = Slider(axismax, 'Saturation max', 0.0, 255.0, valinit=255)
vmax = Slider(axivmax, 'Value max', 0.0, 255.0, valinit=255)

def update(val):
    ret, frame = capture.read()
    if ret is True:
        frame = cv2.resize(frame, None, fx=0.4, fy=0.4)
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        low_values = np.array([hmin.val, smin.val, vmin.val])
        high_values = np.array([hmax.val, smax.val, vmax.val])

        mask = cv2.inRange(hsv_frame, low_values, high_values)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        
        # Limpiamos los ejes
        ax[0].clear()
        ax[1].clear()
        
        # Mostrar el frame original en el primer subplot
        ax[0].imshow(rgb_frame)
        ax[0].set_title("Frame Original")
        ax[0].axis('off') 
        
        # Mostrar el resultado de la máscara en el segundo subplot
        ax[1].imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        ax[1].set_title("Mascara Generada")
        ax[1].axis('off') 
        
        plt.draw()
    else:
        capture.release()
        plt.close()

        
hmin.on_changed(update)
smin.on_changed(update)
vmin.on_changed(update)

hmax.on_changed(update)
smax.on_changed(update)
vmax.on_changed(update)
    
while window_open and capture.isOpened():
    update(None)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    plt.pause(0.1)
capture.release()
plt.show()
        
        
        
        
        
        