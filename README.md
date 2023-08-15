# Art_Boi

## Outline Generation Process

This readme provides a concise guide to the outline generation process, utilizing simple language for easy comprehension.

### Step 1: Rendering

1. Export Render: Save the primary rendered image.
2. Export Depth Map: Preserve the depth information of the render.
3. Export Normal Map: Capture the surface normal information of the render.
   - Note: Ensure that UV maps adhere to a specified color palette.

### Step 2: Image Downscaling

Reduce the size of all images for efficient processing.

### Step 3: Color Mapping

Map the rendered image to the nearest colours from the specified palette.

![Render image](res/test_render.png)
![Colour mapped render](res/output_colour_mapped.png)

### Step 4: Outline Creation

Apply the Sobel operation to the nearest colour, depth, and normal maps to generate outlines.

![Depth map](res/depth.png)
![Sobel effect](res/output_depth_sobel.png)

### Step 5: Layering Outlines

Layer the generated outlines on top of each other using the Python Imaging Library (PIL).

![Example_1](res/output_1.png)
![Example_2](res/output_2.png)

### Step 6 (Optional): Manual Layering

If necessary, create distinct layerings and manually mask them. This is particularly useful when working with text, as a colored Sobel outline might affect readability.

## Potential Enhancements

Enhance the outlined generation process with the following improvements:

- Implement a Sobel layering filter during rendering to automate the outline generation.
- Improve integration of normal maps to highlight faces perpendicular to the camera vector.
- Rewrite the code in a more structured and easily understandable programming language.
   - Enforcing strict typing for enhanced clarity.
   - Implement improved multi-threading for applying the process to multiple images, especially useful for animations.
   - Compile the code for increased processing speed.
- Develop Blender tools to streamline the rendering of all maps.
- Incorporate layering options for applying different colour palettes.
- Include an option to introduce dithering between shades to better emulate a pixel art appearance.
