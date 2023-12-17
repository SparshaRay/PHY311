
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter as savgol
from scipy.signal import find_peaks
from scipy.interpolate import CubicSpline
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# Open the video file
cap = cv2.VideoCapture('processed.mp4')

# Initialize magnitude arrays
red_mags = []
blue_mags = []
green_mags = []

h = 50  # Minimum height of a peak or trough
d = 10  # Minimum distance between peaks or troughs

# Number of data points to use for the Savitzky-Golay filter
data_points = 15
# Degree of the polynomial to use for the Savitzky-Golay filter 
degree = 2

red_wavelength = 650
green_wavelength = 550
blue_wavelength = 450

# Loop through each frame in the video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Split the frame into its red, blue, and green color channels
    b, g, r = cv2.split(frame)
    
    # Initialize column magnitude arrays
    red_row_mags = []
    blue_row_mags = []
    green_row_mags = []
    
    # Loop through each column of pixels in the frame
    for row in range(36, 158):
        # Calculate the average color value for the column
        red_row_mags.append(np.mean(r[row, :]))
        blue_row_mags.append(np.mean(b[row, :]))
        green_row_mags.append(np.mean(g[row, :]))
    
    # Append the column magnitude arrays to the overall magnitude arrays
    red_mags.append(np.array(savgol(red_row_mags, data_points, degree)))
    blue_mags.append(np.array(savgol(blue_row_mags, data_points, degree)))
    green_mags.append(np.array(savgol(green_row_mags, data_points, degree)))

# Combine the red, blue, and green magnitude arrays into a single array for each frame
mags = np.array([np.array([red_mags[i], blue_mags[i], green_mags[i]]) for i in range(len(red_mags))])

# for i in range(len(mags)):
#     # Plot the magnitude of red, green, and blue in the last frame
#     last_frame_mags = mags[i]
#     red_peaks, _ = find_peaks(last_frame_mags[0], height=h, distance=d)
#     red_troughs, _ = find_peaks(256-last_frame_mags[0], height=h, distance=d)
#     blue_peaks, _ = find_peaks(last_frame_mags[1], height=h, distance=d)
#     blue_troughs, _ = find_peaks(256-last_frame_mags[1], height=h, distance=d)
#     green_peaks, _ = find_peaks(last_frame_mags[2], height=h, distance=d)
#     green_troughs, _ = find_peaks(256-last_frame_mags[2], height=h, distance=d)

#     profile = []

#     for i in range(len(red_peaks)):
#         profile.append([red_peaks[i], i*red_wavelength/2])

#     for i in range(len(red_troughs)):
#         profile.append([red_troughs[i], (i+1/2)*red_wavelength/2])

#     for i in range(len(blue_peaks)):
#         profile.append([blue_peaks[i], i*blue_wavelength/2])

#     for i in range(len(blue_troughs)):
#         profile.append([blue_troughs[i], (i+1/2)*blue_wavelength/2])

#     for i in range(len(green_peaks)):
#         profile.append([green_peaks[i], i*green_wavelength/2])

#     for i in range(len(green_troughs)):
#         profile.append([green_troughs[i], (i+1/2)*green_wavelength/2])

#     profile = np.transpose(profile)

#     # Check if there are any coordinates in profile with one x value and multiple y value
#     x_values = profile[0]
#     y_values = profile[1]
#     unique_x_values = np.unique(x_values)
#     new_profile = []

#     for x in unique_x_values:
#         indices = np.where(x_values == x)[0]
#         if len(indices) > 1:
#             avg_y = np.mean(y_values[indices])
#             new_profile.append([x, avg_y])
#         else:
#             new_profile.append([x, y_values[indices[0]]])

#     new_profile = np.transpose(new_profile)


#     plt.plot(new_profile[0], blue_wavelength/2+savgol(new_profile[1], data_points, degree), alpha=0.5)

# plt.show()


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for j in range(len(mags)):
    last_frame_mags = mags[j]
    red_peaks, _ = find_peaks(last_frame_mags[0], height=h, distance=d)
    red_troughs, _ = find_peaks(256-last_frame_mags[0], height=h, distance=d)
    blue_peaks, _ = find_peaks(last_frame_mags[1], height=h, distance=d)
    blue_troughs, _ = find_peaks(256-last_frame_mags[1], height=h, distance=d)
    green_peaks, _ = find_peaks(last_frame_mags[2], height=h, distance=d)
    green_troughs, _ = find_peaks(256-last_frame_mags[2], height=d, distance=d)

    profile = []

    for i in range(len(red_peaks)):
        profile.append([red_peaks[i], i*red_wavelength/2])

    for i in range(len(red_troughs)):
        profile.append([red_troughs[i], (i+1/2)*red_wavelength/2])

    for i in range(len(blue_peaks)):
        profile.append([blue_peaks[i], i*blue_wavelength/2])

    for i in range(len(blue_troughs)):
        profile.append([blue_troughs[i], (i+1/2)*blue_wavelength/2])

    for i in range(len(green_peaks)):
        profile.append([green_peaks[i], i*green_wavelength/2])

    for i in range(len(green_troughs)):
        profile.append([green_troughs[i], (i+1/2)*green_wavelength/2])

    profile = np.transpose(profile)

    x_values = profile[0]
    y_values = profile[1]
    unique_x_values = np.unique(x_values)
    new_profile = []

    for x in unique_x_values:
        indices = np.where(x_values == x)[0]
        if len(indices) > 1:
            avg_y = np.mean(y_values[indices])
            new_profile.append([x, avg_y])
        else:
            new_profile.append([x, y_values[indices[0]]])

    new_profile = np.transpose(new_profile)

    ax.plot(new_profile[0]/2, (green_wavelength/2+savgol(new_profile[1], data_points, degree))*3/4, zs=j*4, zdir='y', linewidth=1.0, alpha=0.9, c=cm.jet(j/len(mags)))
            
ax.set_xlabel('Distance from top of film (in mm)')
ax.set_zlabel('Thickness of film (in nanometers)')
ax.set_ylabel('Time (in seconds)')
plt.show()


for i in range(5):
    last_frame_mags = mags[i*round(len(mags)/4)]
    red_peaks, _ = find_peaks(last_frame_mags[0], height=h, distance=d)
    red_troughs, _ = find_peaks(256-last_frame_mags[0], height=h, distance=d)
    blue_peaks, _ = find_peaks(last_frame_mags[1], height=h, distance=d)
    blue_troughs, _ = find_peaks(256-last_frame_mags[1], height=h, distance=d)
    green_peaks, _ = find_peaks(last_frame_mags[2], height=h, distance=d)
    green_troughs, _ = find_peaks(256-last_frame_mags[2], height=d, distance=d)
    plt.plot(last_frame_mags[0], label='Red', color='red')
    plt.plot(red_peaks, last_frame_mags[0][red_peaks], "x", color='red')
    plt.plot(red_troughs, last_frame_mags[0][red_troughs], "x", color='red')
    plt.plot(last_frame_mags[1], label='Blue', color='blue')
    plt.plot(blue_peaks, last_frame_mags[1][blue_peaks], "x", color='blue')
    plt.plot(blue_troughs, last_frame_mags[1][blue_troughs], "x", color='blue')
    plt.plot(last_frame_mags[2], label='Green', color='green')
    plt.plot(green_peaks, last_frame_mags[2][green_peaks], "x", color='green')
    plt.plot(green_troughs, last_frame_mags[2][green_troughs], "x", color='green')
    plt.legend()
    plt.show()
