import os
import shutil
import random

def remix_videos(video1_path, video2_path, output_dir):
    """
    Mock remixing function. In a real app, you'd combine/edit videos with ffmpeg or moviepy.
    For now, we just duplicate one of the inputs 5 times with new names.
    """
    base_name = "remix"
    for i in range(5):
        random_number = random.randint(0, 100)
        out_path = os.path.join(output_dir, f"{base_name}_{i}_{random_number}.mp3")
        try:
            shutil.copy(video1_path if i % 2 == 0 else video2_path, out_path)
        except shutil.SameFileError:
            pass
