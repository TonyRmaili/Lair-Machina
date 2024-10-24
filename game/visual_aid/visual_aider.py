import ollama
from PIL import Image, ImageDraw
import os


class VisualAider:
    def __init__(self):
        self.llava = 'llava:7b'
        self.llama = 'llama3.1'
        self.images_path = './images/'

        os.makedirs(self.images_path,exist_ok=True)


        self.system_coordinator = '''
You are a world map analysis assistant capable of identifying and returning locations on a map in response to user requests. Your goal is to accurately analyze the provided map and return the coordinates corresponding to the user's prompt.
Key Rules:
    1.Response Format: Only provide NORMALIZED coordinates in the format (x: int, y: int) based on the given map. Do not provide any other type of response or information. for example (0.43,0.21)
    2.Multiple Coordinates: If the prompt describes multiple locations, you must return several coordinate pairs, each separated by a comma.
    3.Precision: Ensure that the coordinates are as precise as possible in relation to the user's input.
    4.Limitations: Do not make any assumptions about the map beyond what is explicitly requested by the user. Only refer to the visible features of the map.
    5.Assistance: If the prompt is unclear or if no coordinates can be determined, return 'Coordinates not found'.

RESPOND using JSON.
'''


        self.coords = [
            (0.56,0.29),
             (0.73,0.41),
            (0.85,0.65)
        ]
        

    def coordinate_finder(self,prompt,images):
        resp = ollama.generate(
            model=self.llava,
            system=self.system_coordinator,
            prompt=prompt,
            images=images,
            format='json'
            )

        return resp['response']
    

    def place_circles_on_image(self,image_name, output_name, dot_radius=15, dot_color="red"):
        image_path = self.images_path + image_name
        output_path = self.images_path + output_name

        image = Image.open(image_path)
        width, height = image.size
        
        # Create a draw object
        draw = ImageDraw.Draw(image)

        # Loop through the coordinates and place a dot for each town
        for (x, y) in self.coords:
            # Convert normalized coordinates to pixel values
            x_pixel = int(x * width)
            y_pixel = int(y * height)
            
            # Draw a small circle (dot) at the coordinates
            draw.ellipse(
                (x_pixel - dot_radius, y_pixel - dot_radius, x_pixel + dot_radius, y_pixel + dot_radius),
                fill=dot_color
            )

        # Save the image with the dots
        image.save(output_path)
        print(f"Map saved with towns placed at {output_path}")
        print(f'image size {image.size}')

if __name__=='__main__':
    aider = VisualAider()
    prompt = 'Were are the deserts, anwser with a tuple (x:int,y:int)?'
    aider.place_circles_on_image(image_name='world_map.jpg',output_name='dots_world_map.jpg',dot_radius=40,dot_color='blue')

    path = aider.images_path + 'world_map.jpg'

    

    # resp = aider.coordinate_finder(prompt=prompt,images=[path])
    # print(resp)

