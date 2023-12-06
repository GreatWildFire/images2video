import cv2
import os
from pydub.utils import mediainfo
import ffmpeg

# Set relative paths
audio_file = os.path.join(os.getcwd(), 'audio.mp3')

# 1. Get audio file duration
audio_info = mediainfo(audio_file)
audio_length = round(float(audio_info['duration']))  # audio length in seconds

# 2. Create video based on audio duration
image_folder = os.path.join(os.getcwd(), "images", "png")
images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
images.sort()

# Read the first image file to determine video size
first_image_path = os.path.join(image_folder, images[0])
first_image = cv2.imread(first_image_path)
video_size = (first_image.shape[1], first_image.shape[0])  # (width, height)

frames_per_second = 1  # video frame rate
total_frames = frames_per_second * audio_length

# Calculate the number of frames each image should be shown for
frames_per_image = total_frames // len(images)

# Create a VideoWriter object with the determined video size
video = cv2.VideoWriter('temp_video.mp4', -1, frames_per_second, video_size)

# Think about the possibility that total_frames may not be perfectly divisible by len(images)
left_over_frames = total_frames % len(images)

for i, image in enumerate(images):
    img_path = os.path.join(image_folder, image)
    frame = cv2.imread(img_path)
    frames_for_this_image = frames_per_image

    # Add one more frame for this image to distribute left_over_frames evenly among images
    if i < left_over_frames:
       frames_for_this_image += 1

    for _ in range(frames_for_this_image):
        video.write(frame)

video.release()

# 3. Merge the newly created video with audio
input_video = ffmpeg.input('temp_video.mp4')
input_audio = ffmpeg.input(audio_file)

output = ffmpeg.output(input_video, input_audio, 'final_video.mp4', vcodec='copy', acodec='aac', strict='experimental')
output.run()
