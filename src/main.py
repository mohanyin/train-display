import cairo
import sys
import os

WIDTH, HEIGHT = 800, 480

def create_black_image(output_path):
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Create a new surface
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Fill the entire surface with black
    ctx.set_source_rgb(0, 0, 0)
    ctx.rectangle(0, 0, WIDTH, HEIGHT)
    ctx.fill()
    
    # Save the image
    surface.write_to_png(output_path)

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <output_path>")
        sys.exit(1)
        
    output_path = sys.argv[1]
    create_black_image(output_path)
    print(f"Black image saved to: {output_path}")

if __name__ == "__main__":
    main()