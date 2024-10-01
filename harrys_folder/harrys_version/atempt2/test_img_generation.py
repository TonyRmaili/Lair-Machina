# # # import os
# # # import requests
# # # import json

# # # # Function to create directory if it doesn't exist
# # # def create_output_dir(directory):
# # #     if not os.path.exists(directory):
# # #         os.makedirs(directory)

# # # # Function to generate image using ComfyUI
# # # def generate_image(prompt, output_path):
# # #     # Define the URL where ComfyUI is running
# # #     comfyui_url = "http://localhost:8188/generate"  # Adjust if needed

# # #     # Define the input payload for ComfyUI
# # #     payload = {
# # #         "prompt": prompt,
# # #         "model": "flux1-schnell",  # Specify the model (Flux Schnell)
# # #         "output_path": output_path,
# # #         # Add other configurations (steps, image size, etc.)
# # #     }

# # #     # Send the request to generate the image
# # #     response = requests.post(comfyui_url, json=payload)
    
# # #     # Check if the request was successful
# # #     if response.status_code == 200:
# # #         print(f"Image generated successfully: {output_path}")
# # #     else:
# # #         print(f"Failed to generate image: {response.status_code}")
# # #         print(response.text)



# # # character_description = "Uthgar the mountain dwarf cleric of light"
# # # # Example usage
# # # prompt = "A portrait of {character_description}"
# # # output_dir = "./generated_images"
# # # create_output_dir(output_dir)
# # # output_path = os.path.join(output_dir, "city_skyline.png")

# # # generate_image(prompt, output_path)















# # import websocket
# # import json
# # import random
# # import os

# # # WebSocket server address
# # server_address = "ws://localhost:8188"  # This is the WebSocket URL for ComfyUI

# # # Function to load the workflow from a saved JSON file
# # def load_workflow(workflow_path):
# #     try:
# #         with open(workflow_path, 'r') as file:
# #             workflow = json.load(file)
# #             return workflow
# #     except FileNotFoundError:
# #         print(f"The file {workflow_path} was not found.")
# #         return None
# #     except json.JSONDecodeError:
# #         print(f"The file {workflow_path} contains invalid JSON.")
# #         return None

# # # Function to update the workflow with a new prompt and regenerate the seed
# # def update_workflow_with_prompt(workflow, positive_prompt, negative_prompt=''):
# #     # Find the KSampler node
# #     for node_id, node in workflow.items():
# #         if node.get('class_type') == 'KSampler':
# #             # Set a new random seed
# #             node['inputs']['seed'] = random.randint(10**14, 10**15 - 1)
            
# #             # Update the positive prompt
# #             positive_input_id = node['inputs']['positive'][0]
# #             workflow[positive_input_id]['inputs']['text'] = positive_prompt
            
# #             # Update the negative prompt if provided
# #             if negative_prompt:
# #                 negative_input_id = node['inputs']['negative'][0]
# #                 workflow[negative_input_id]['inputs']['text'] = negative_prompt

# #     return workflow

# # # Function to establish a WebSocket connection
# # def open_websocket_connection():
# #     ws = websocket.WebSocket()
# #     ws.connect(server_address)
# #     return ws

# # # Function to send the updated workflow through WebSocket and track progress
# # def send_workflow_and_track(ws, workflow, output_dir='./output/'):
# #     prompt_id = None
    
# #     # Send the workflow via WebSocket
# #     ws.send(json.dumps(workflow))
    
# #     # Track progress
# #     while True:
# #         result = ws.recv()
# #         result = json.loads(result)

# #         # Check for progress updates
# #         if 'type' in result and result['type'] == 'progress':
# #             data = result['data']
# #             print(f"In KSampler -> Step: {data['value']} of {data['max']}")
        
# #         # Check if execution is complete
# #         if 'type' in result and result['type'] == 'execution_cached':
# #             prompt_id = result['prompt_id']
# #             break

# #     # After execution is complete, fetch images
# #     get_images(ws, prompt_id, output_dir)

# # # Function to get generated images from the WebSocket API
# # def get_images(ws, prompt_id, output_dir):
# #     # Get the image history from ComfyUI
# #     ws.send(json.dumps({"type": "history", "prompt_id": prompt_id}))

# #     result = ws.recv()
# #     result = json.loads(result)

# #     # Fetch images
# #     for node_id, output in result.get('outputs', {}).items():
# #         if 'images' in output:
# #             for image in output['images']:
# #                 save_image(ws, image['filename'], output_dir)

# # # Function to save an image to disk
# # def save_image(ws, filename, output_dir):
# #     # Create output directory if it doesn't exist
# #     os.makedirs(output_dir, exist_ok=True)

# #     # Fetch the image from ComfyUI
# #     ws.send(json.dumps({"type": "view", "filename": filename, "subfolder": "output"}))
    
# #     # Save the image to the output directory
# #     image_data = ws.recv()
# #     with open(os.path.join(output_dir, filename), 'wb') as img_file:
# #         img_file.write(image_data)
# #     print(f"Saved image: {filename}")

# # # Main function to handle the entire process
# # def generate_image(prompt, workflow_path, output_dir='./output/', negative_prompt=''):
# #     # Load the workflow
# #     workflow = load_workflow(workflow_path)
# #     if workflow is None:
# #         return

# #     # Update the workflow with the new prompt
# #     workflow = update_workflow_with_prompt(workflow, prompt, negative_prompt)

# #     # Establish a WebSocket connection
# #     ws = open_websocket_connection()

# #     try:
# #         # Send the workflow and track progress
# #         send_workflow_and_track(ws, workflow, output_dir)
# #     finally:
# #         ws.close()

# # player_character = "Uthgar the mountaion dwarf cleric of light"
# # # Example usage
# # # workflow_path = "~/harry_and_tony_project/Lair-Machina/harrys_folder/harrys_version/atempt2/workflow_api.json"
# # workflow_path = "workflow_api.json"
# # positive_prompt = f"A portrait of {player_character}"
# # output_dir = "./generated_images/"

# # generate_image(positive_prompt, workflow_path, output_dir)


# # atempt 3 - on the computer -  websockets was fail

# import subprocess
# import os

# def generate_image_with_comfyui(workflow_json_path, output_dir):
#     # Ensure the output directory exists
#     os.makedirs(output_dir, exist_ok=True)

#     # Command to run ComfyUI from the command line
#     # command = f"python path/to/ComfyUI/main.py --workflow {workflow_json_path} --output {output_dir}"
#     command = f"~/harry_and_tony_project/ComfyUI/main.py --workflow {workflow_json_path} --output {output_dir}"
    
#     # Run the command and wait for it to finish
#     result = subprocess.run(command, shell=True, capture_output=True)

#     if result.returncode == 0:
#         print(f"Image generation successful. Check the output directory: {output_dir}")
#     else:
#         print(f"Error generating image: {result.stderr.decode()}")

# # Example usage
# generate_image_with_comfyui("workflow_api.json", "./output")



import json
from urllib import request, parse
import random

#This is the ComfyUI api prompt format.

#If you want it for a specific workflow you can "enable dev mode options"
#in the settings of the UI (gear beside the "Queue Size: ") this will enable
#a button on the UI to save workflows in api format.

#keep in mind ComfyUI is pre alpha software so this format will change a bit.

#this is the one for the default workflow
# prompt_text = """
# {
#     "3": {
#         "class_type": "KSampler",
#         "inputs": {
#             "cfg": 8,
#             "denoise": 1,
#             "latent_image": [
#                 "5",
#                 0
#             ],
#             "model": [
#                 "4",
#                 0
#             ],
#             "negative": [
#                 "7",
#                 0
#             ],
#             "positive": [
#                 "6",
#                 0
#             ],
#             "sampler_name": "euler",
#             "scheduler": "normal",
#             "seed": 8566257,
#             "steps": 20
#         }
#     },
#     "4": {
#         "class_type": "CheckpointLoaderSimple",
#         "inputs": {
#             "ckpt_name": "v1-5-pruned-emaonly.safetensors"
#         }
#     },
#     "5": {
#         "class_type": "EmptyLatentImage",
#         "inputs": {
#             "batch_size": 1,
#             "height": 512,
#             "width": 512
#         }
#     },
#     "6": {
#         "class_type": "CLIPTextEncode",
#         "inputs": {
#             "clip": [
#                 "4",
#                 1
#             ],
#             "text": "dwarf warrior"
#         }
#     },
#     "7": {
#         "class_type": "CLIPTextEncode",
#         "inputs": {
#             "clip": [
#                 "4",
#                 1
#             ],
#             "text": "bad hands"
#         }
#     },
#     "8": {
#         "class_type": "VAEDecode",
#         "inputs": {
#             "samples": [
#                 "3",
#                 0
#             ],
#             "vae": [
#                 "4",
#                 2
#             ]
#         }
#     },
#     "9": {
#         "class_type": "SaveImage",
#         "inputs": {
#             "filename_prefix": "ComfyUI",
#             "images": [
#                 "8",
#                 0
#             ]
#         }
#     }
# }
# """

prompt_text = """
{
  "5": {
    "inputs": {
      "width": 1024,
      "height": 1024,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Empty Latent Image"
    }
  },
  "6": {
    "inputs": {
      "text": "Fantasy artwork",
      "clip": [
        "11",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "13",
        0
      ],
      "vae": [
        "10",
        0
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "9": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  },
  "10": {
    "inputs": {
      "vae_name": "ae.safetensors"
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "Load VAE"
    }
  },
  "11": {
    "inputs": {
      "clip_name1": "t5xxl_fp16.safetensors",
      "clip_name2": "clip_l.safetensors",
      "type": "flux"
    },
    "class_type": "DualCLIPLoader",
    "_meta": {
      "title": "DualCLIPLoader"
    }
  },
  "12": {
    "inputs": {
      "unet_name": "flux1-schnell.safetensors",
      "weight_dtype": "default"
    },
    "class_type": "UNETLoader",
    "_meta": {
      "title": "Load Diffusion Model"
    }
  },
  "13": {
    "inputs": {
      "noise": [
        "25",
        0
      ],
      "guider": [
        "22",
        0
      ],
      "sampler": [
        "16",
        0
      ],
      "sigmas": [
        "17",
        0
      ],
      "latent_image": [
        "5",
        0
      ]
    },
    "class_type": "SamplerCustomAdvanced",
    "_meta": {
      "title": "SamplerCustomAdvanced"
    }
  },
  "16": {
    "inputs": {
      "sampler_name": "euler"
    },
    "class_type": "KSamplerSelect",
    "_meta": {
      "title": "KSamplerSelect"
    }
  },
  "17": {
    "inputs": {
      "scheduler": "simple",
      "steps": 4,
      "denoise": 1,
      "model": [
        "12",
        0
      ]
    },
    "class_type": "BasicScheduler",
    "_meta": {
      "title": "BasicScheduler"
    }
  },
  "22": {
    "inputs": {
      "model": [
        "12",
        0
      ],
      "conditioning": [
        "6",
        0
      ]
    },
    "class_type": "BasicGuider",
    "_meta": {
      "title": "BasicGuider"
    }
  },
  "25": {
    "inputs": {
      "noise_seed": 550096394834419
    },
    "class_type": "RandomNoise",
    "_meta": {
      "title": "RandomNoise"
    }
  }
}
"""

import os
import time
import json
from urllib import request
import os
import time
from PIL import Image
import glob

# # WORKS######################
def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    request.urlopen(req)

def show_images_in_folder(folder_path):
    # Find all PNG files in the specified folder
    image_files = glob.glob(os.path.join(folder_path, "*.png"))
    
    # Loop through each PNG file and open it
    for image_file in image_files:
        print(f"Opening image: {image_file}")
        img = Image.open(image_file)
        img.show()

prompt = json.loads(prompt_text)
art_description=input("what to generate?")
#set the text prompt for our positive CLIPTextEncode
prompt["6"]["inputs"]["text"] = f"{art_description}"

# #set the seed for our KSampler node
# prompt["3"]["inputs"]["seed"] = 5

queue_prompt(prompt)

folder_path="/home/student/harry_and_tony_project/ComfyUI/output/"
# Show all PNG images in the output folder
show_images_in_folder(folder_path)



###################################


# def queue_prompt(prompt):
#     p = {"prompt": prompt}
#     data = json.dumps(p).encode('utf-8')
#     req =  request.Request("http://127.0.0.1:8188/prompt", data=data, headers={'Content-Type': 'application/json'})
#     request.urlopen(req)

# def wait_for_image(output_path, timeout=60):
#     # Wait for the image to be generated
#     for _ in range(timeout):
#         if os.path.exists(output_path):
#             return True
#         time.sleep(1)
#     return False

# def show_image(image_path):
#     # Open and display the image using Pillow
#     img = Image.open(image_path)
#     img.show()

# # Your existing prompt workflow
# prompt = json.loads(prompt_text)
# prompt["6"]["inputs"]["text"] = "elf cleric fantasy portrait"

# # Queue the prompt
# queue_prompt(prompt)

# # Define the path where ComfyUI saves the generated image
# output_image_path = "ComfyUI/output/ComfyUI_00008_.png"  # Adjust this path as needed

# # Wait for the image to be generated (adjust the timeout if necessary)
# if wait_for_image(output_image_path):
#     print(f"Image generated successfully at {output_image_path}")
#     # Open and display the image
#     show_image(output_image_path)
# else:
#     print("Image generation timed out or the file was not found.")

