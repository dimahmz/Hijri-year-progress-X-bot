import os
from datetime import datetime
from PIL import Image, ImageDraw

def generate_progress_bar(percent: float, folder=None) -> str:
    #incalid percent range
    if not 0 <= percent <= 100:
        raise ValueError("Percent must be between 0 and 100")

    # create media directory if it doesn't exist
    if(folder==None):
      os.makedirs('media', exist_ok=True)
      folder = "media"
    else:    
      os.makedirs(folder, exist_ok=True)

    # image dimensions and padding
    img_width, img_height = 1900, 300
    bar_width, bar_height = 1300, 110
    x_padding = (img_width - bar_width) // 2
    y_padding = (img_height - bar_height) // 2

    progress_width = int(bar_width * (percent / 100))

    # create a blank image with a background color
    img = Image.new('RGB', (img_width, img_height),
                    color='#FFFFFF')  # Light pink background
    draw = ImageDraw.Draw(img)

    # draw the progress bar background with rounded corners
    radius = 0
    draw.rounded_rectangle([x_padding, y_padding, x_padding + bar_width, y_padding+bar_height],
                           radius=radius, fill='#D3D3D3')

    # draw the progress bar with rounded corners
    draw.rounded_rectangle([x_padding, y_padding, x_padding + progress_width, y_padding+bar_height],
                           radius=radius, fill='#000')

    # get current datetime and format it
    current_time = datetime.now().strftime(f"%Y-%m-%d_%H_%M")

    # save the image in the media directory with datetime and percent in filename
    filename = fr"{folder}\progress_{current_time}_{percent:.1f}.png"
    img.save(filename)
    return filename
