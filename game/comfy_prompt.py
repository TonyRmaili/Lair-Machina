import shutil
import os
from pathlib import Path 
import time
import json
import threading
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import urllib.request as request
from datetime import datetime

"""
This is the function used to generate the image for the character profile.
takes a promt as input and sends it to the comfy server - could generate mapts/items anything
"""

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


def get_file_info(folder_path):
    # List to store information of each file
    file_info_list = []
    
    # Loop through each file in the directory
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        # Check if it's a file, not a directory
        if os.path.isfile(file_path):
            # Get file stats
            file_stats = os.stat(file_path)
            
            # Gather the file's details as datetime objects for times
            file_info = {
                "name": file_name,
                "creation_time": datetime.fromtimestamp(file_stats.st_ctime)
            }

            file_info_list.append(file_info)
    return file_info_list

 
def scan_for_latest_img(source_folder,current_date):
    file_data = get_file_info(source_folder)
    for file in file_data:
        if current_date > file['creation_time']:
            continue  
        else:
            return file['name']

def move_and_rename_img(source_folder, file_name, char_name):
    source_file = os.path.join(source_folder, file_name)
    destination_file = os.path.join(f'./pics/{char_name}', 'profile_img.png')

    # Move and rename the file
    shutil.move(source_file, destination_file)
    print(f"File moved and renamed to {destination_file}")


def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req = request.Request("http://127.0.0.1:8188/prompt", data=data)
    response = request.urlopen(req)

def run_comfy(description, name):
    source_path = '/home/student/harry_and_tony_project/ComfyUI/output/'
    current_date = datetime.now()
    # Prepare the prompt and update it with the description
    prompt = json.loads(prompt_text)  # Assuming prompt_text is defined somewhere
    prompt["6"]["inputs"]["text"] = description

    # Queue the prompt
    queue_prompt(prompt)

    checking_img = True
    latest_file = None

    # Keep checking for the latest image
    while checking_img:
        latest_file = scan_for_latest_img(source_path,current_date)
        
        if latest_file:  # If a new file is found, exit the loop
            checking_img = False
        else:
            time.sleep(5)  # Wait for 5 seconds before checking again

    # Move and rename the latest image
    if latest_file:
        move_and_rename_img(source_path, latest_file, name)


  
if __name__=='__main__':
  # this wont happen as the game uses thread
    prompt = json.loads(prompt_text)
    art_description=input("what to generate?")
    #set the text prompt for our positive CLIPTextEncode
    prompt["6"]["inputs"]["text"] = f"{art_description}"
    print(prompt)
    queue_prompt(prompt)

