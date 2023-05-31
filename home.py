import tkinter
import tkinter as tk
import cv2
import numpy as np
import pygame
from keras.models import model_from_json
import mysql.connector
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.iconbitmap("E:/Emotion_detection_with_CNN-main/Emotion_detection_with_CNN-main/images/music.ico")
root.configure(background="#003366")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

# Set the size of the window to the width and height of your desktop
root.geometry(f"{width}x{height}")
root.title('Music Recommendation System')
# to display captured image
image_label = tk.Label(root, height=346, width=534)
image_label.place(x=499, y=246)

# # Load the image
camera_image = tk.PhotoImage(
    file="E:/Emotion_detection_with_CNN-main/Emotion_detection_with_CNN-main/images/camera.gif")
camera_image = camera_image.subsample(4, 4)
# Define the emotions as a list
emotions = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
is_playing = False
# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    port="3306",
    password="",
    database="song"
)
# Create a cursor object to execute SQL queries
mycursor = mydb.cursor()
with open('C:/Users/HP/Desktop/face_Detection/EmotionDetectionCNN-IITISoc2022-main/EmotionDetectionCNN'
          '-IITISoc2022-main/models/emotion_model.json', 'r') as f:
    model_json = f.read()

# Create a new Keras model from the JSON string
model = model_from_json(model_json)
face_detector = cv2.CascadeClassifier('C:/Users/HP/Desktop/face_Detection/EmotionDetectionCNN-IITISoc2022-main'
                                      '/EmotionDetectionCNN-IITISoc2022-main/haarcascade'
                                      '/haarcascade_frontalface_default.xml')
# Initialize pygame.mixer
pygame.mixer.init()
# Load the weights of the model from an HDF5 file
model.load_weights("C:/Users/HP/Desktop/face_Detection/EmotionDetectionCNN-IITISoc2022-main"
                   "/EmotionDetectionCNN-IITISoc2022-main/models/emotion_model_weights.h5")
current_emotion = 0
frames = []  # define frames in the outer scope


def load_frames(filename):
    global frames  # indicate that frames should be modified in the outer scope
    with Image.open(filename) as image:
        try:
            while True:
                frames.append(ImageTk.PhotoImage(image))
                image.seek(len(frames))
        except EOFError:
            pass
    return frames


current_song = ""


def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_input = None
    num_faces = face_detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h) in num_faces:
        cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (0, 255, 0), 4)
        roi_gray_frame = gray[y:y + h, x:x + w]
        img_input = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)
    if img_input is not None:
        pred = model.predict(img_input)
        emotion_idx = int(np.argmax(pred))
        emotion_label = emotions[emotion_idx]
    else:
        emotion_label = "Can't see..! Please Caputre Again"
    img = Image.fromarray(gray)
    img_tk = ImageTk.PhotoImage(image=img)
    image_label.configure(image=img_tk)
    image_label.image = img_tk
    image_label.lift()
    message = f"You seem's to be {emotion_label}"
    emotion_text = tk.Label(root, text=message, font=("Helvetica", 8), width=30, height=2)
    emotion_text.place(x=792, y=224, anchor="center")

    # Get the list of songs for the predicted emotion
    song_list = get_songs(emotion_label)
    global song_listbox
    song_listbox = tk.Listbox(root, font=("Helvetica", 10), width=50, height=10)
    song_scrollbar = tk.Scrollbar(root, command=song_listbox.yview)
    song_listbox.config(yscrollcommand=song_scrollbar.set)
    for song in song_list:
        song_listbox.insert(tk.END, song)
    song_listbox.bind("<Double-Button-1>", lambda event: play_selected_song(song_listbox))
    playlist_label = tk.Label(root, text="Playlist Generated", font=("Helvetica", 12))
    playlist_label.place(x=200, y=24, anchor="center")
    song_listbox.place(x=200, y=120, anchor="center")
    song_scrollbar.place(x=350, y=120, anchor="center", height=150)


def play_selected_song(song_listbox):
    # Get the selected song name
    song_name = song_listbox.get(song_listbox.curselection())
    # Retrieve the file path of the selected song
    mycursor.execute(f"SELECT file_path FROM songs WHERE name='{song_name}'")
    result = mycursor.fetchone()
    if result:
        song_path = result[0]
        # Load the song into the music mixer
        pygame.mixer.music.load(song_path)
        # Play the song
        pygame.mixer.music.play()


def update():
    global current_frame
    global frames
    current_frame = (current_frame + 1) % len(frames)
    gif_widget.configure(image=frames[current_frame])
    if current_frame == 0 and repeat == 0:
        return  # End of sequence
    gif_widget.after(delay, update)


def get_songs(emotion_label):
    # Select the name column from the songs table with the matching emotion label
    mycursor.execute(f"SELECT name FROM songs WHERE emotion LIKE '%{emotion_label}%'")
    results = mycursor.fetchall()
    if results:
        songs = [result[0] for result in results]
    else:
        songs = []
    return songs


def play_previous_song():
    # Get the index of the currently playing song
    current_song_idx = song_listbox.curselection()[0]
    # Select the previous song in the list
    previous_song_idx = current_song_idx - 1
    if previous_song_idx < 0:
        previous_song_idx = song_listbox.size() - 1  # wrap around to the end of the list
    # Play the selected song
    song_listbox.activate(previous_song_idx)
    song_listbox.selection_clear(0, tk.END)
    song_listbox.selection_set(previous_song_idx)
    play_selected_song(song_listbox)


def play_next_song():
    # Get the index of the currently playing song
    current_song_idx = song_listbox.curselection()[0]
    # Select the next song in the list
    next_song_idx = current_song_idx + 1
    if next_song_idx >= song_listbox.size():
        next_song_idx = 0  # wrap around to the beginning of the list
    # Play the selected song
    song_listbox.activate(next_song_idx)
    song_listbox.selection_clear(0, tk.END)
    song_listbox.selection_set(next_song_idx)
    play_selected_song(song_listbox)


def set_volume(value):
    # Set the volume of the mixer to the value of the volume slider
    pygame.mixer.music.set_volume(float(value) / 100)


def toggle_button_text(button):
    global is_playing
    if is_playing:
        # Pause the audio
        pygame.mixer.music.pause()
        button.config(text="Play")
        is_playing = False
    else:
        # Resume the audio from where it left off
        pygame.mixer.music.unpause()
        button.config(text="Pause")
        is_playing = True


# Load the frames of the animated GIF image
bgframes = load_frames('E:/Emotion_detection_with_CNN-main/Emotion_detection_with_CNN-main/images/canbebg.gif')

# Create a Label widget to display the animated GIF image
gif_widget = tk.Label(root, image=bgframes[0])
gif_widget.filename = "'E:/Emotion_detection_with_CNN-main/Emotion_detection_with_CNN-main/images/F.gif'"
current_frame = 0
delay = 100  # Milliseconds between frames
repeat = -1  # Number of times to repeat (0 = once, -1 = forever)
gif_widget.after(delay, update)
gif_widget.pack(fill="both", expand=True)

# Create the Capture Image button and place it in the top left corner
capture_btn = tk.Button(root, image=camera_image, command=capture_image, width=50, height=50)
capture_btn.place(x=760, y=117)

# Create the control buttons
play_button = tkinter.Button(root, width=6, height=3, bg="#2c2c2d", highlightbackground="#AD974f", text='PAUSE',
                             command=lambda: toggle_button_text(play_button), fg="#AD974f")
next_button = tk.Button(root, width=6, height=3, bg="#2c2c2d", fg="#AD974f", highlightbackground="#AD974f", text='NEXT',
                        command=play_next_song)
prev_button = tk.Button(root, width=6, height=3, bg="#2c2c2d", fg="#AD974f", highlightbackground="#AD974f",
                        text='PREV.', command=play_previous_song)

# Place the buttons and label on the GUI window
play_button.place(x=770, y=630)
next_button.place(x=930, y=630)
prev_button.place(x=600, y=630)

# Create the label for the volume slider
volume_label = tk.Label(root, text="Volume", font=("Arial", 14), fg="white",
                        bg="#2d2d2d")

# Place the volume label on the GUI window
volume_label.place(x=411, y=610)

# Create the volume slider
volume_slider = tk.Scale(root, from_=100, to=0, orient=tk.VERTICAL, command=set_volume, length=344, bg="#AD974f",
                         troughcolor="white")
volume_slider.set(30)

# Place the volume slider on the GUI window
volume_slider.place(x=429, y=250)

# Create the Music Recommendation System label
music_recommendation_label = tk.Label(root, text='“ Where words leave off, Music begins...”', font=("Arial", 20),
                                      fg="#000000",
                                      bg="#cccccc")
music_recommendation_label.place(x=580, y=8)

# Create the "Tap to click your image" label
tap_to_click_label = tk.Label(root, text="Let's Check Your Mood", font=("Arial", 14), fg="#000000",
                              bg="#cccccc")
tap_to_click_label.pack(side="top", pady=20)

# Center the "Tap to click your image" label below the "Music Recommendation System" label
tap_to_click_label.place(x=690, y=175)

# Run the main loop

root.mainloop()
