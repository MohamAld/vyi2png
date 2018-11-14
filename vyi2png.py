import json
import sys
import base64
from io import BytesIO
from PIL import Image
import math


def convert(file_name, file):
    data = json.load(my_file)['i'] # decode .vyi file

    max_rows = 10.0
    frames = []
    frame_width = 0
    frame_height = 0

    png_width = 0
    png_height = 0

    # Build frames from .vyi file decode
    for i in data:
        try: frames.append(Image.open(BytesIO(base64.b64decode(i[4])))) #Extracts the image of the icon
        except: pass

        #Extract frames for the current iconName if they exist
        if len(i) > 5:
            for j in i[5]:
                try: frames.append(Image.open(BytesIO(base64.b64decode(j[0])))) #Extracts the image of the icon
                except: pass
        
        #Extract other iconStates if they exist
        if len(i)>6:
            for k in i[6]:
                try: frames.append(Image.open(BytesIO(base64.b64decode(k[1])))) #Extracts the image of the icon
                except: pass
                if len(k) > 3:
                    print(k[3])
                    for j in k[3]:
                        try: frames.append(Image.open(BytesIO(base64.b64decode(j[0])))) #Extracts the image of the icon
                        except: pass

    frame_width = frames[0].size[0]
    frame_height = frames[0].size[1]


    #Calculate png output sizes
    if len(frames) > max_rows :
        png_width = frame_width * max_rows
        r = math.ceil(len(frames)/max_rows)
        png_height = frame_height * r
    else:
        png_width = frame_width*len(frames)
        png_height = frame_height
        

    png = Image.new("RGBA",(int(png_width), int(png_height)))

    for current_frame in frames :
        top = frame_height * math.floor((frames.index(current_frame))/max_rows)
        left = frame_width * (frames.index(current_frame) % max_rows)
        bottom = top + frame_height
        right = left + frame_width
        
        box = (left,top,right,bottom)
        box = [int(i) for i in box]
        cut_frame = current_frame.crop((0,0,frame_width,frame_height))
        
        png.paste(cut_frame, box)
        
    name = file_name.strip('.vyi')
    png.save(name + ".png", "PNG")
    print("Complete! Saved as: " + name + ".png")


if __name__ == '__main__':

    if not (sys.argv[1][-4:] == '.vyi'):
        print("Please use a .vyi file")
        sys.exit()
    with open(sys.argv[1], 'r') as my_file:
        convert(sys.argv[1],my_file)
