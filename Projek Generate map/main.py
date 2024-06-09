import tkinter as tk
from tkinter import Scrollbar
from PIL import Image, ImageDraw, ImageTk
import random
import os

# Path assets
big_building_path = "D:/PAA/aset/bangunanbesar.jpg"
medium_building_path = "D:/PAA/aset/bangunansedang.jpg"
small_building_path = "D:/PAA/aset/bangunankecil.jpg"
house_path = "D:/PAA/aset/rumah.jpg"
tree_path = "D:/PAA/aset/pohon.jpg"

# Function to load images safely
def load_image(path):
    if os.path.exists(path):
        return Image.open(path)
    else:
        raise FileNotFoundError(f"File not found: {path}")

# Load images
try:
    big_building_img = load_image(big_building_path)
    medium_building_img = load_image(medium_building_path)
    small_building_img = load_image(small_building_path)
    house_img = load_image(house_path)
    tree_img = load_image(tree_path)
except FileNotFoundError as e:
    print(e)
    exit(1)

# Constants
MAP_WIDTH = 1500  # Ukuran peta besar untuk pengujian
MAP_HEIGHT = 1500
CELL_SIZE = 20
ZOOM_FACTOR = 1.0
MAP_SIZE_X = MAP_WIDTH // CELL_SIZE
MAP_SIZE_Y = MAP_HEIGHT // CELL_SIZE
BACKGROUND_COLOR = "#33a46c"

# Global variable to store city map
city_map = None

def create_city_map():
    global city_map
    city_map = Image.new('RGB', (MAP_WIDTH, MAP_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(city_map)

    def place_building(img, width, height, draw, num_buildings):
        attempts = 0
        while num_buildings > 0 and attempts < 1000:
            x = random.randint(0, MAP_SIZE_X - width)
            y = random.randint(0, MAP_SIZE_Y - height)
            if is_area_free(x, y, width, height) and is_next_to_road(x, y, width, height):
                city_map.paste(img.resize((width * CELL_SIZE, height * CELL_SIZE)), (x * CELL_SIZE, y * CELL_SIZE))
                mark_area_used(x, y, width, height)
                num_buildings -= 1
            attempts += 1

    def is_area_free(x, y, width, height):
        if x + width > MAP_SIZE_X or y + height > MAP_SIZE_Y:
            return False
        for i in range(y, y + height):
            for j in range(x, x + width):
                if map_grid[i][j] != 0:
                    return False
        return True

    def is_next_to_road(x, y, width, height):
        for i in range(max(0, y - 1), min(MAP_SIZE_Y, y + height + 1)):
            for j in range(max(0, x - 1), min(MAP_SIZE_X, x + width + 1)):
                if map_grid[i][j] == 2:
                    return True
        return False

    def mark_area_used(x, y, width, height):
        for i in range(y, y + height):
            for j in range(x, x + width):
                map_grid[i][j] = 1

    # Initialize map grid
    map_grid = [[0 for _ in range(MAP_SIZE_X)] for _ in range(MAP_SIZE_Y)]

    # Draw roads
    def draw_road():
        road_color = 'black'
        dashed_line_color = 'white'
        dash_length = 5

        # Main horizontal road
        y = MAP_SIZE_Y // 2
        for x in range(MAP_SIZE_X):
            map_grid[y][x] = 2
            draw.rectangle([x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE], fill=road_color)

        for x in range(0, MAP_SIZE_X * CELL_SIZE, dash_length * 2):
            draw.line([x, y * CELL_SIZE + CELL_SIZE // 2, x + dash_length, y * CELL_SIZE + CELL_SIZE // 2], fill=dashed_line_color)

        # Random vertical roads
        for _ in range(random.randint(3, 6)):
            x = random.randint(0, MAP_SIZE_X - 1)
            for yi in range(MAP_SIZE_Y):
                map_grid[yi][x] = 2
                draw.rectangle([x * CELL_SIZE, yi * CELL_SIZE, (x + 1) * CELL_SIZE, (yi + 1) * CELL_SIZE], fill=road_color)
            for yi in range(0, MAP_SIZE_Y * CELL_SIZE, dash_length * 2):
                draw.line([x * CELL_SIZE + CELL_SIZE // 2, yi, x * CELL_SIZE + CELL_SIZE // 2, yi + dash_length], fill=dashed_line_color)

        # Random horizontal roads
        for _ in range(random.randint(2, 4)):
            y = random.randint(0, MAP_SIZE_Y - 1)
            for xi in range(MAP_SIZE_X):
                map_grid[y][xi] = 2
                draw.rectangle([xi * CELL_SIZE, y * CELL_SIZE, (xi + 1) * CELL_SIZE, (y + 1) * CELL_SIZE], fill=road_color)
            for xi in range(0, MAP_SIZE_X * CELL_SIZE, dash_length * 2):
                draw.line([xi, y * CELL_SIZE + CELL_SIZE // 2, xi + dash_length, y * CELL_SIZE + CELL_SIZE // 2], fill=dashed_line_color)

    draw_road()

    # Draw rivers
    def draw_rivers():
        river_color = 'blue'

        def draw_vertical_river(x, start_y, end_y):
            for y in range(start_y, end_y):
                if map_grid[y][x] == 0:  # Cek jika sel kosong
                    map_grid[y][x] = 3
                    draw.rectangle([x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE], fill=river_color)

        def draw_horizontal_river(y, start_x, end_x):
            for x in range(start_x, end_x):
                if map_grid[y][x] == 0:  # Cek jika sel kosong
                    map_grid[y][x] = 3
                    draw.rectangle([x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE], fill=river_color)

        # Main horizontal river
        main_river_y = random.randint(1, MAP_SIZE_Y - 2)
        draw_horizontal_river(main_river_y, 0, MAP_SIZE_X)

        # Random vertical rivers connecting to the main river
        for _ in range(random.randint(2, 4)):
            x = random.randint(1, MAP_SIZE_X - 2)
            if map_grid[main_river_y][x] == 3:  # Ensure it connects to the main river
                if random.choice([True, False]):
                    draw_vertical_river(x, 0, main_river_y)  # From top to the main river
                else:
                    draw_vertical_river(x, main_river_y, MAP_SIZE_Y)  # From the main river to bottom

    draw_rivers()

    # Place buildings
    place_building(big_building_img, 10, 5, draw, 10)  # Increase to 10 large buildings
    place_building(medium_building_img, 5, 3, draw, 20)  # Increase to 20 medium buildings
    place_building(small_building_img, 2, 2, draw, 50)  # Increase to 50 small buildings
    place_building(house_img, 1, 2, draw, 60)  # Increase to 60 houses

    # Place trees with smaller size
    def place_trees(img, draw):
        tree_resized = img.resize((CELL_SIZE, CELL_SIZE))
        for y in range(MAP_SIZE_Y):
            for x in range(MAP_SIZE_X):
                if map_grid[y][x] == 0 and is_area_free(x, y, 1, 1):
                    city_map.paste(tree_resized, (x * CELL_SIZE, y * CELL_SIZE))
                    mark_area_used(x, y, 1, 1)

    place_trees(tree_img, draw)
    
    return city_map

def redraw_map():
    global city_map
    scaled_city_map = city_map.resize((int(MAP_WIDTH * ZOOM_FACTOR), int(MAP_HEIGHT * ZOOM_FACTOR)), Image.LANCZOS)
    city_map_tk = ImageTk.PhotoImage(scaled_city_map)
    canvas.create_image(0, 0, anchor='nw', image=city_map_tk)
    canvas.config(scrollregion=canvas.bbox(tk.ALL))
    canvas.image = city_map_tk

def on_mouse_wheel(event):
    # Shift key scrolls horizontally, otherwise scroll vertically
    if event.state & 0x0001:  # Shift key is pressed
        canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
    else:
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def on_scroll_start(event):
    canvas.scan_mark(event.x, event.y)

def on_scroll_move(event):
    canvas.scan_dragto(event.x, event.y, gain=1)

# Zoom in function
def zoom_in():
    global ZOOM_FACTOR
    ZOOM_FACTOR *= 1.2
    redraw_map()

# Zoom out function
def zoom_out():
    global ZOOM_FACTOR
    ZOOM_FACTOR /= 1.2
    redraw_map()

# Set up GUI
root = tk.Tk()
root.title("City Map Generator")

# Adjust the window size to ensure everything fits
root.geometry("1000x800")  # Make sure the window is large enough

# Create a frame for the canvas
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=1)

# Create a canvas and scrollbars
canvas = tk.Canvas(frame, width=800, height=600, bg="white")
scrollbar_y = Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar_x = Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
canvas.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Enable scrolling with mouse wheel and touchpad
canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # For Windows and MacOS
canvas.bind_all("<Shift-MouseWheel>", on_mouse_wheel)  # For horizontal scrolling
canvas.bind_all("<Button-4>", on_mouse_wheel)  # For Linux scroll up
canvas.bind_all("<Button-5>", on_mouse_wheel)  # For Linux scroll down

# Enable scrolling with dragging
canvas.bind("<ButtonPress-1>", on_scroll_start)
canvas.bind("<B1-Motion>", on_scroll_move)

# Create a button frame
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X)

# Add the generate button
generate_button = tk.Button(button_frame, text="Generate New Map", command=lambda: [create_city_map(), redraw_map()])
generate_button.pack(pady=10, padx=10, side=tk.LEFT)

# Add zoom in and zoom out buttons
zoom_in_button = tk.Button(button_frame, text="Zoom In", command=zoom_in)
zoom_in_button.pack(pady=10, padx=10, side=tk.LEFT)

zoom_out_button = tk.Button(button_frame, text="Zoom Out", command=zoom_out)
zoom_out_button.pack(pady=10, padx=10, side=tk.LEFT)

create_city_map()  # Generate initial map
redraw_map()  # Draw the map

root.mainloop()
