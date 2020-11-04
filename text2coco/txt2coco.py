import json
import argparse
import os


def convert2coco(txt_path, submission_file): 
    # create a list of dictionaries
    json_info = []
    for item in os.listdir(txt_path):
        file_path = os.path.join(txt_path, item)
        f = open(file_path, "r")
        for line in f:
            line = line.split(" ")
            coord = list(map(float, line[1:])) 
            sign_info = {
                "image_id": 0,
                "category_id": 2,
                "bbox": [coord[0], coord[1], coord[2] - coord[0], coord[3] - coord[1]] 
            }
            json_info.append(sign_info)
    json_object = json.dumps(json_info, indent = 4) 
  
    # Writing to sample.json 
    with open(submission_file, "w") as outfile: 
        outfile.write(json_object) 
        

        

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-txt_path", "--text files location", required=True, help="text files location")
    ap.add_argument("-submission_file", "--submission file", required=True, help= "write the result to submission file")
    args = vars(ap.parse_args())
    files_path = args["text files location"]
    save_path = args["submission file"]
    print(files_path, save_path)
    convert2coco(files_path, save_path)