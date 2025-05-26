import os
from PIL import Image
import sys

def optimize_image(image_path):
    """
    Optimize and resize an image while maintaining aspect ratio
    """
    try:
        with Image.open(image_path) as img:
            # Get original dimensions
            width, height = img.size
            
            # Calculate new dimensions while maintaining aspect ratio
            if width > height:  # Landscape
                if width > 1280:
                    new_width = 1280
                    new_height = int(height * (1280 / width))
                else:
                    new_width = width
                    new_height = height
            else:  # Portrait
                if height > 960:
                    new_height = 960
                    new_width = int(width * (960 / height))
                else:
                    new_width = width
                    new_height = height
            
            # Only resize if needed
            if new_width != width or new_height != height:
                print(f"Resizing {image_path} from {width}x{height} to {new_width}x{new_height}")
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Save optimized image
            img.save(
                image_path,
                optimize=True,
                quality=85,
                progressive=True,
                subsampling=2
            )
            print(f"Optimized {image_path}")
            
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")

def main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Process all image files in the assets/img directory and its subdirectories
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    
    # Walk through all directories
    for root, dirs, files in os.walk(os.path.join(current_dir, 'assets', 'img')):
        for file in files:
            if file.lower().endswith(image_extensions):
                image_path = os.path.join(root, file)
                optimize_image(image_path)

if __name__ == "__main__":
    main()
