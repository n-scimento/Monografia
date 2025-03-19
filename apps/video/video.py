import cv2
import os

def png_to_mp4(input_folder, output_file, fps=30, quality=100):
    images = [img for img in os.listdir(input_folder) if img.endswith(".png")]
    images.sort()

    first_image_path = os.path.join(input_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    for image in images:
        image_path = os.path.join(input_folder, image)
        frame = cv2.imread(image_path)
        video.write(frame)

    video.release()
    print(f"Video saved as {output_file}")

# Example usage
input_folder = "plots"
output_file = "plots.mp4"
png_to_mp4(input_folder, output_file, fps=30)