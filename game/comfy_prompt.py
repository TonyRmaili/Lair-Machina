import shutil
import os
from pathlib import Path 

import json
from urllib import request
import threading

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
image_generation_event = threading.Event()

# # WORKS######################
def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    request.urlopen(req)

def move_and_rename_latest_image(source_folder, destination_folder, new_filename):
    # Get a list of all image files (jpg, png, etc.) in the source folder
    image_extensions = ('.png')  # Add more extensions if needed
    images = [file for file in Path(source_folder).glob('*') if file.suffix.lower() in image_extensions]

    # Check if there are any images in the folder
    if not images:
        print("No images found in the source folder.")
        return

    # Find the latest image by modification time
    latest_image = max(images, key=os.path.getmtime)

    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Create the destination path with the new filename and the same extension
    destination_path = Path(destination_folder) / (new_filename + latest_image.suffix)

    # Move the file (instead of copying)
    shutil.move(str(latest_image), str(destination_path))

    print(f"Moved and renamed the latest image: {latest_image} to {destination_path}")
    
    image_generation_event.set()


def run_in_thread(art_description, character_name):
    prompt = json.loads(prompt_text)
    prompt["6"]["inputs"]["text"] = art_description


    # Reset the event before starting the image generation
    image_generation_event.clear()

    # Run the text generation in a separate thread, pass the argument using args
    thread1 = threading.Thread(target=queue_prompt, args=(prompt,))
    thread1.start()
    
    # move_and_rename_latest_image(source_folder='/home/student/harry_and_tony_project/ComfyUI/output/', destination_folder=f'./pics/{character_name}', new_filename='profile_img' )

    thread2 = threading.Thread(
        target=move_and_rename_latest_image,
        args=('/home/student/harry_and_tony_project/ComfyUI/output/', f'./pics/{character_name}', 'profile_img')
    )
    thread2.start()

    thread1.join()
    thread2.join()

    # Set the event to indicate the image generation is done
    image_generation_event.set()


if __name__=='__main__':
  # this wont happen as the game uses thread
    prompt = json.loads(prompt_text)
    art_description=input("what to generate?")
    #set the text prompt for our positive CLIPTextEncode
    prompt["6"]["inputs"]["text"] = f"{art_description}"
    print(prompt)
    queue_prompt(prompt)

