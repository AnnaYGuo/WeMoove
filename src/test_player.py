import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

class VideoPlayer(tk.Tk):
    def __init__(self, video1_path, video2_path, start_frame1=0, start_frame2=0):
        super().__init__()
        self.title("Side-by-Side Video Player")

        self.video1_path = video1_path
        self.video2_path = video2_path

        self.video1 = cv2.VideoCapture(video1_path)
        self.video2 = cv2.VideoCapture(video2_path)

        self.current_frame1 = start_frame1
        self.current_frame2 = start_frame2

        self.create_widgets()
        self.play_videos()

    def create_widgets(self):
        self.video_frame1 = tk.Label(self)
        self.video_frame1.pack(side=tk.LEFT)

        self.video_frame2 = tk.Label(self)
        self.video_frame2.pack(side=tk.RIGHT)

        self.frame_num_label1 = tk.Label(self, text="Frame Number 1:")
        self.frame_num_label1.pack()
        self.frame_num_entry1 = tk.Entry(self)
        self.frame_num_entry1.insert(0, str(self.current_frame1))
        self.frame_num_entry1.pack()

        self.frame_num_label2 = tk.Label(self, text="Frame Number 2:")
        self.frame_num_label2.pack()
        self.frame_num_entry2 = tk.Entry(self)
        self.frame_num_entry2.insert(0, str(self.current_frame2))
        self.frame_num_entry2.pack()

        self.switch_button = tk.Button(self, text="Switch Videos", command=self.switch_videos)
        self.switch_button.pack()

        self.create_trackbars()

    def create_trackbars(self):
        self.trackbar1 = tk.Scale(self, from_=0, to=self.video1.get(cv2.CAP_PROP_FRAME_COUNT)-1,
                                  orient=tk.HORIZONTAL, command=self.on_trackbar_change1)
        self.trackbar1.pack()
        self.trackbar1.set(self.current_frame1)

        self.trackbar2 = tk.Scale(self, from_=0, to=self.video2.get(cv2.CAP_PROP_FRAME_COUNT)-1,
                                  orient=tk.HORIZONTAL, command=self.on_trackbar_change2)
        self.trackbar2.pack()
        self.trackbar2.set(self.current_frame2)

    def on_trackbar_change1(self, value):
        self.current_frame1 = int(value)
        self.frame_num_entry1.delete(0, tk.END)
        self.frame_num_entry1.insert(0, str(self.current_frame1))
        self.update_video_frames()

    def on_trackbar_change2(self, value):
        self.current_frame2 = int(value)
        self.frame_num_entry2.delete(0, tk.END)
        self.frame_num_entry2.insert(0, str(self.current_frame2))
        self.update_video_frames()

    def update_video_frames(self):
        self.video1.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame1)
        self.video2.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame2)
        self.play_videos()

    def play_videos(self):
        ret1, frame1 = self.video1.read()
        ret2, frame2 = self.video2.read()

        if ret1 and ret2:
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            frame1 = Image.fromarray(frame1)
            frame1 = ImageTk.PhotoImage(image=frame1)
            self.video_frame1.configure(image=frame1)
            self.video_frame1.image = frame1

            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            frame2 = Image.fromarray(frame2)
            frame2 = ImageTk.PhotoImage(image=frame2)
            self.video_frame2.configure(image=frame2)
            self.video_frame2.image = frame2

            self.trackbar1.set(self.current_frame1)
            self.trackbar2.set(self.current_frame2)

            self.after(30, self.play_videos)
        else:
            self.video1.release()
            self.video2.release()

    def switch_videos(self):
        new_video1_path = filedialog.askopenfilename(title="Select Video 1", filetypes=[("Video files", "*.mp4;*.avi")])
        new_video2_path = filedialog.askopenfilename(title="Select Video 2", filetypes=[("Video files", "*.mp4;*.avi")])

        if new_video1_path and new_video2_path:
            self.video1_path = new_video1_path
            self.video2_path = new_video2_path

            self.video1 = cv2.VideoCapture(new_video1_path)
            self.video2 = cv2.VideoCapture(new_video2_path)

            self.current_frame1 = 0
            self.current_frame2 = 0

            self.create_trackbars()
            self.play_videos()

if __name__ == "__main__":
    app = VideoPlayer("Chinese12.mp4", "Chinese13.mp4", start_frame1=100, start_frame2=50)
    app.mainloop()
