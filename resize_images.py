'''
1. Buat folder batik_m dan batik_p yang berisi gambar-gambar batik. (masing-masing ada 4 subfolder: aksesoris, atasan, bawahan, polos)
2. Lalu jalankan script ini untuk meresize semua gambar menjadi 224x224 pixels.
3. Gambar yang sudah diresize akan disimpan di folder baru dengan suffix '_resized'. 
    NOTE: gambar akan replace file yg sudah ada jika filename sama.
    RECCOMMENDED: hapus folder '_resized' sebelum run script ini
'''

import os
from PIL import Image
import glob

def resize_images_in_folder(source_folder_path, target_folder_path, target_size=(224, 224)):
    """
    Resize all images in a folder to target size and save in new folder.
    Print file paths of non-square images before resizing.
    
    Args:
        source_folder_path (str): Path to the source folder containing images
        target_folder_path (str): Path to the target folder to save resized images
        target_size (tuple): Target size as (width, height)
    """
    # Supported image extensions
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.tif']
    
    # Create target directory if it doesn't exist
    os.makedirs(target_folder_path, exist_ok=True)
    
    # Get all image files in the source folder
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(source_folder_path, ext)))
        image_files.extend(glob.glob(os.path.join(source_folder_path, ext.upper())))
    
    non_square_count = 0
    processed_count = 0
    
    print(f"\nProcessing folder: {source_folder_path}")
    print(f"Saving to: {target_folder_path}")
    print(f"Found {len(image_files)} images")
    
    for image_path in image_files:
        try:
            # Open the image
            with Image.open(image_path) as img:
                original_size = img.size
                
                # Check if image is square
                if original_size[0] != original_size[1]:
                    print(f"Non-square image: {image_path} (size: {original_size[0]}x{original_size[1]})")
                    non_square_count += 1
                
                # Resize the image to target size
                resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
                
                # Convert to RGB if necessary (for JPEG compatibility)
                if resized_img.mode in ('RGBA', 'LA', 'P'):
                    resized_img = resized_img.convert('RGB')
                
                # Create target file path
                filename = os.path.basename(image_path)
                target_image_path = os.path.join(target_folder_path, filename)
                
                # Save the resized image to new location
                resized_img.save(target_image_path, quality=95)
                processed_count += 1
                
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")
    
    print(f"Processed: {processed_count} images")
    print(f"Non-square images found: {non_square_count}")
    return processed_count, non_square_count

def main():
    """
    Main function to resize images in all batik folders
    """
    # Base directory - current working directory
    base_dir = os.getcwd()
    
    # Define the folder structure
    batik_types = ['batik_m', 'batik_p']
    categories = ['aksesoris', 'atasan', 'bawahan', 'polos']
    
    total_processed = 0
    total_non_square = 0
    
    print("=" * 60)
    print("IMAGE RESIZING SCRIPT - Resizing to 224x224 pixels")
    print("=" * 60)
    
    # Process each folder
    for batik_type in batik_types:
        for category in categories:
            source_folder_path = os.path.join(base_dir, batik_type, category)
            target_folder_path = os.path.join(base_dir, f"{batik_type}_resized", category)
            
            if os.path.exists(source_folder_path):
                processed, non_square = resize_images_in_folder(source_folder_path, target_folder_path)
                total_processed += processed
                total_non_square += non_square
            else:
                print(f"Source folder not found: {source_folder_path}")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total images processed: {total_processed}")
    print(f"Total non-square images found: {total_non_square}")
    print("All images have been resized to 224x224 pixels")
    print(f"Resized images saved in folders with '_resized' suffix")

if __name__ == "__main__":
    # Check if PIL is available
    try:
        from PIL import Image
        main()
    except ImportError:
        print("Error: PIL (Pillow) is not installed.")
        print("Please install it using: pip install Pillow")