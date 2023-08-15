# Import library
from PIL import Image

def color_distance(c1,c2):
    r1,g1,b1 = c1
    r2,g2,b2 = c2
    return ((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)**0.5

def extract_colors_from_image(image_path):
    image = Image.open(image_path)
    image = image.convert("RGB")

    pixel_values = list(image.getdata())

    unique_colors = []

    for rgb_tuple in pixel_values:
        is_unique = True
        for existing_color in unique_colors:
            if color_distance(rgb_tuple, existing_color) < 1:
                is_unique = False
                break
        if is_unique:
            r,g,b = rgb_tuple
            unique_colors.append((r,g,b))
        #print(unique_colors)

    return unique_colors

color_palette = extract_colors_from_image("colour_pallete.png")

print(color_palette)

def to_grey(red, green, blue) -> float:
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue

def gray_scale_img(image):
    image_clone = image.copy()
    pixels = image_clone.load()
    
    # Loop through the pixels and map them to the closest color from the list
    width,height = image.size
    for x in range(width):
        for y in range(height):
            pixel = pixels[x,y]
            #help(pixel)
            closest_color = to_grey(pixel[0], pixel[1], pixel[2])
            
            closest_color = (int(closest_color), int(closest_color), int(closest_color))

            pixels[x,y] = closest_color
    
    return image_clone

def map_closet_colour_img(image):
    image_clone = image.copy()
    pixels = image_clone.load()
    
    width,height = image.size
    for x in range(width):
        for y in range(height):
            pixel = pixels[x,y]
            
            closest_color = min(color_palette, key=lambda c:color_distance(c,pixel))
            
            pixels[x,y] = closest_color
    
    return image_clone

sobel_filters = {
    "h":[-1, -2, -1, 0, 0, 0, 1, 2, 1],
    "v":[-1, 0, 1, -2, 0, 2, -1, 0, 1]
}

def sobel_value(pixel_value, sobel_filter):
    value = 0

    for i in range(len(pixel_value)):
        value += pixel_value[i] * sobel_filter[i]

    return value

def sobel_filter_img(image, map = lambda val: val):
    image_clone = image.copy()
    sobel_pixels = image_clone.load()

    pixels = image.load()

    width,height = image.size
    for x in range(width):
        for y in range(height):

            col_value = []
            for delta_x in range(-1,2):
                for delta_y in range(-1,2):
                    pixel = 0
                    try:
                        pixel = pixels[x+delta_x, y+delta_y][0]
                    except Exception as e:
                        pass

                    col_value.append(pixel)

            sobel_x = sobel_value(col_value, sobel_filters["h"])
            sobel_y = sobel_value(col_value, sobel_filters["v"])

            value = (sobel_x**2 + sobel_y**2)**0.5

            value = int(map(value))

            sobel_pixels[x,y] = (value, value, value)
    
    return image_clone

def calculate_scale_factor(initial_size, final_size):
    initial_width, initial_height = initial_size
    final_width, final_height = final_size

    scale_factor_width = final_width / initial_width
    scale_factor_height = final_height / initial_height

    return min(scale_factor_width, scale_factor_height)

def downscale_image(image, scale_factor):
    image_clone = image.copy()
    
    original_width, original_height = image.size
    
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)
    
    downscaled_image = image_clone.resize((new_width, new_height), Image.ANTIALIAS)

    return downscaled_image

def overlay_image(img_1, img_2, overlay_cond, img_2_col_map= lambda col_1, col_2: col_2):

    width_1, height_1 = img_1.size
    width_2, height_2 = img_2.size

    width = min(width_1, width_2)
    height = min(height_1, height_2)

    new_image = Image.new("RGB", (width, height))

    pixels_1 = img_1.load()
    pixels_2 = img_2.load()

    output_pixel = new_image.load()

    for x in range(width):
        for y in range(height):
            pixel_1 = pixels_1[x,y]
            pixel_2 = pixels_2[x, y]

            if overlay_cond(pixel_1, pixel_2):
                output_pixel[x,y] = img_2_col_map(pixel_1, pixel_2)
            else:
                output_pixel[x,y] = pixel_1

    return new_image

def split_image_vertically(image):
    width, height = image.size
    
    mid_point = width // 2
    
    left = image.crop((0, 0, mid_point, height))
    right = image.crop((mid_point, 0, width, height))

    return (left, right)

def resize_image_point(image, scale_factor):
    original_width, original_height = image.size
    
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)
    
    resized_image = image.resize((new_width, new_height), Image.NEAREST)
    
    return resized_image

if __name__ == "__main__":
    pixel_art_size = (2**8 * 2, 2**8)#(256,256)#(512,512)

    # loading_images
    colour_image = Image.open("test_render.png")
    colour_image = colour_image.convert("RGB")
    colour_image = downscale_image(
        colour_image,
        calculate_scale_factor(colour_image.size, pixel_art_size)
    )
    
    depth_image = Image.open("depth.png")
    depth_image = depth_image.convert("RGB")
    depth_image = downscale_image(
        depth_image,
        calculate_scale_factor(depth_image.size, pixel_art_size)
    )

    normal_image = Image.open("normal.png")
    normal_image = normal_image.convert("RGB")
    normal_image = downscale_image(
        normal_image,
        calculate_scale_factor(normal_image.size, pixel_art_size)
    )

    colour_mapped = map_closet_colour_img(colour_image)

    # generating edges from source images
    grey_sobel = sobel_filter_img(gray_scale_img(colour_image), lambda v: v*v-32000)
    grey_sobel.save("output_grey_sobel.png")

    colour_mapped = overlay_image(
        colour_mapped,
        grey_sobel,
        lambda col_1, col_2: col_2[0] > 100,
        lambda col_1, col_2: (0, 0, 0)
    )

    depth_sobel = sobel_filter_img(depth_image, lambda v: v ** 0.75)
    depth_sobel.save("output_depth_sobel.png")

    colour_mapped = overlay_image(
        colour_mapped,
        depth_sobel,
        lambda col_1, col_2: col_2[0] > 50,
        lambda col_1, col_2: (0, 0, 0)
    )

    normal_sobel = sobel_filter_img(normal_image, lambda v: 0.5*v)
    normal_sobel.save("output_normal_sobel.png")

    colour_mapped = overlay_image(
        colour_mapped,
        normal_sobel,
        lambda col_1, col_2: col_2[0] > 100,
        lambda col_1, col_2: (0, 0, 0)
    )
    colour_mapped.save("output_colour_mapped.png")

    # colour_image = Image.open("output_colour_mapped.png")
    # colour_image = colour_image.convert("RGB")

    left,right = split_image_vertically(colour_mapped)

    #left.save("post_1.png")
    #right.save("post_2.png")

    left = Image.open("post_1.png")
    left = left.convert("RGB")

    right = Image.open("post_2.png")
    right = right.convert("RGB")

    resize_image_point(left, 4)
    resize_image_point(right, 4)

    left.save("post_1.png")
    right.save("post_2.png")

