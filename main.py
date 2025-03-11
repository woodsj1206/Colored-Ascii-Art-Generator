"""
Program Name: Colored Ascii Art Generator
Author: woodsj1206 (https://github.com/woodsj1206)
Description: This program converts an image into colored ascii art.
Date Created: 3/7/25
Last Modified: 3/11/25
"""

import argparse
from PIL import Image, ImageOps, ImageDraw, ImageFont
from progress_bar import ProgressBar

# ASCII character gradient from darkest (space) to lightest (0)
ASCII_CHARS = (
    "   ...,,,___---~~~```'''\"\"\"^^^***:::;;;!!!???<<<>>>+++((())){{{}}}[[[]]]///\\\\\\|||111iiilllffftttjjjCCCUUULLLIIIVVV77TTJJYY222SSSZZZvvvssszzzxxxrrrcccuuuoooeeeaaapppqqqyyygggnnnwwwmmmbbbdddkkkhhhDDDOOOQQQAAAFFFHHH334455XX66GGKKEEPPRR88BB99NNWWMM&&%%##@@@000"
)


def convert_image_to_colored_ascii(image: Image.Image) -> list[list[str]]:
    """
    Converts an image to colored ASCII art.

    Args:
        image (PIL.Image.Image): PIL Image object (RGB).
        
    Returns: 
        list[list[str]]: 2D list of ANSI-colored ASCII characters.
        
    """

    # Convert image to grayscale
    grayscale_img = ImageOps.grayscale(image)
    width, height = image.size

    grayscale_pixels = grayscale_img.load()
    color_pixels = image.load()

    # Create ASCII art array
    ascii_array = [[""] * width for _ in range(height)]
    
    # Create a progress bar
    progress_bar = ProgressBar("Coverting Image To Colored Ascii", total=height * width)

    for i in range(0, width):
      for j in range(0, height):
        grayscale_value = grayscale_pixels[i, j]
        r, g, b = color_pixels[i, j]
        ascii_array[j][i] = (ASCII_CHARS[int(grayscale_value % len(ASCII_CHARS))], r, g, b)
        progress_bar.update()

    return ascii_array


def display_colored_ascii(ascii_art: list[list[str]]) -> None:
    """
    Prints a colored ASCII image to the console using ANSI escape codes.

    Args:
        ascii_art (list[list[str]]): A 2D list where each element is a tuple (char, r, g, b).
                          - char: ASCII character.
                          - r, g, b: RGB color values (0-255).
                      
    Returns:
        None. Prints the colored ASCII image to the console.
        
    """
    
    for row in ascii_art:
        for char, r, g, b in row:
            print(rgb_char(char, r, g, b), end="")  # Print colored character without newline
        print()  # Move to the next line after printing a row


def rgb_char(char: str, r: int, g: int, b: int) -> str:
    """
    Colors an ASCII character using ANSI escape codes.

    Args:
        char (str): ASCII character.
        r (int): Red (0-255).
        g (int): Green (0-255).
        b (int): Blue (0-255).
        
    Returns: 
        str: ANSI-colored ASCII character string.
        
    """
    
    return f"\033[38;2;{r};{g};{b}m{char}\033[0m"


def save_ascii_as_image(image: Image.Image, ascii_array: list[list[str]], font_path: str, output_path="ascii_image", font_size=12, bg_color=(0, 0, 0), width_spacing=0, height_spacing=0) -> None:
    """
    Saves the colored ASCII output as an image.
    
    Args:
        image (PIL.Image.Image): PIL Image object (RGB).    
        ascii_array (list[list[str]]): 2D list of ANSI-colored ASCII characters to be rendered onto the output image.    
        font_path (str): Path to the TrueType (.ttf) font file to use for rendering the ASCII characters.    
        output_path (str, optional): Filename (without extension) for saving the output image (default: "ascii_image").  
        font_size (int, optional): Size of the font to be used when drawing each ASCII character (default: 12).    
        bg_color (tuple, optional): Background color of the output image, provided as an RGB tuple (default: black, (0, 0, 0)).   
        width_spacing (int, optional): Horizontal spacing between ASCII characters (default: 0).   
        height_spacing (int, optional): Vertical spacing between lines of ASCII characters (default: 0).
        
    Returns:
        None. The function saves the rendered image to the specified output path.
        
    """
    
    # Load a font
    font = ImageFont.truetype(font_path, font_size)
    
    max_char_width = 0
    max_char_height = 0

    # Get character dimensions
    for char in ASCII_CHARS:
      bbox = font.getbbox(char, anchor="mm")  # Bounding box (left, top, right, bottom)
      max_char_width = max(max_char_width, (bbox[2] - bbox[0]))  # Width
      max_char_height = max(max_char_height, bbox[3] - bbox[1] + 2)  # Height

    width, height = image.size
    
    # Create a new image with a solid background
    img = Image.new("RGB", 
                    (max_char_width + width * (max_char_width + width_spacing), max_char_height + height * (max_char_height + height_spacing)), 
                    bg_color)
    draw = ImageDraw.Draw(img)
    
    # Create a progress bar
    progress_bar = ProgressBar("Creating Image", total=height * width)
    
    # Draw ASCII characters
    for y, row in enumerate(ascii_array):
        for x, (char, r, g, b) in enumerate(row):  # row[x] contains (char, r, g, b)
            draw.text((max_char_width + x * (max_char_width + width_spacing), max_char_height + y * (max_char_height + height_spacing)), 
                      char, 
                      font=font, 
                      fill=(r, g, b), 
                      anchor="mm"
                      )
            progress_bar.update()

    
    # Save the image
    file_path = f"output_files/{output_path}_output.png"
    img.save(file_path)
    print(f"Done: ASCII image saved as {output_path}_output.png")


def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Convert an image into colored ASCII art.")
    parser.add_argument("--print", action="store_true", help="Display the ASCII art in the console.")
    parser.add_argument("--image", type=str, required=True, help="Path to the image file.")
    parser.add_argument("--font", type=str, required=True, help="Path to the font file.")
    parser.add_argument("--font-size", type=int, default=12, help="Font size for the ASCII image. (default: 12)")
    parser.add_argument("--width-spacing", type=int, default=0, help="Extra spacing between characters. (default: 0)")
    parser.add_argument("--height-spacing", type=int, default=0, help="Extra spacing between lines of characters. (default: 0)")
    parser.add_argument("--bg-color", type=str, default="0,0,0", help="Background color in R,G,B format. (default: 0,0,0)")
    
    # Parse arguments
    args = parser.parse_args()    # Load the image
    image_path = args.image
    image_name = image_path.split("/")[1].split(".")[0]
    image = Image.open(image_path)

    # Convert image to ASCII representation with color
    ascii_art = convert_image_to_colored_ascii(image)

    # Define font settings for image rendering
    font_path = args.font
    font_size = args.font_size
    width_spacing = args.width_spacing 
    height_spacing = args.height_spacing 
    background_color = tuple(map(int, args.bg_color.split(",")))  # (R, G, B)

    # Save the ASCII representation as an image
    save_ascii_as_image(
        image, 
        ascii_art, 
        font_path, 
        font_size=font_size, 
        output_path=image_name, 
        width_spacing=width_spacing, 
        height_spacing=height_spacing, 
        bg_color=background_color
        )

    # Display the ASCII art in the console with colors
    if args.print:
        display_colored_ascii(ascii_art)
        

if __name__ == "__main__":
    main()