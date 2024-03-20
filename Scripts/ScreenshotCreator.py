import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import ImageClip
from PIL import Image

def create_images_folder():
    images_folder = "images"
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

def take_screenshot(video_path, output_path):
    clip = VideoFileClip(video_path)
    screenshot = clip.get_frame(20)  # Capture frame at 10th second
    clip.close()

    image_name = os.path.basename(video_path).replace("-video", "").replace(".mp4", "-image.png")
    image_path = os.path.join(output_path, image_name)

    screenshot_image = ImageClip(screenshot, duration=clip.duration)
    screenshot_image = screenshot_image.set_pos((0, 0))

    # Resize using Pillow's Image.resize
    screenshot_image.img = Image.fromarray(screenshot_image.img)
    screenshot_image.img = screenshot_image.img.resize((screenshot_image.w // 200, screenshot_image.h // 200), Image.BILINEAR)
    
    screenshot_image.save_frame(image_path)

def main():
    videos_folder = "videos"
    images_folder = "images"

    create_images_folder()

    for filename in os.listdir(videos_folder):
        if filename.endswith(".mp4"):
            video_path = os.path.join(videos_folder, filename)
            take_screenshot(video_path, images_folder)

if __name__ == "__main__":
    main()
