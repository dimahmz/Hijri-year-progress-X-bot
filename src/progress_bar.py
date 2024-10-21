import os
from datetime import datetime
from PIL import Image, ImageDraw

# <generate a progress bar image and returns it's location
def generate_progress_bar(percent : float) -> str:
    if not 0 <= percent <= 100:
        raise ValueError("Percent must be between 0 and 100")

    # Create media directory if it doesn't exist
    os.makedirs('media', exist_ok=True)

    # Image dimensions and padding
    img_width, img_height = 2000, 350
    bar_width, bar_height = 1600, 220
    x_padding = (img_width - bar_width) // 2
    y_padding = (img_height - bar_height) // 2

    progress_width = int(bar_width * (percent / 100))

    # Create a blank image with a background color
    img = Image.new('RGB', (img_width, img_height),
                    color='#FFFFFF')  # Light pink background
    draw = ImageDraw.Draw(img)

    # Draw the progress bar background with rounded corners
    radius = 40
    draw.rounded_rectangle([x_padding, y_padding, x_padding + bar_width, y_padding+bar_height],
                           radius=radius, fill='#D3D3D3')

    # Draw the progress bar with rounded corners
    draw.rounded_rectangle([x_padding, y_padding, x_padding + progress_width, y_padding+bar_height],
                           radius=radius, fill='#000')

    # Get current datetime and format it
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save the image in the media directory with datetime and percent in filename
    filename = f"media\progress_{current_time}_{percent:.1f}.png"
    img.save(filename)
    return filename