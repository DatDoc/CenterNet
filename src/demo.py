from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import _init_paths

import os
import cv2

from opts import opts
from detectors.detector_factory import detector_factory

image_ext = ['jpg', 'jpeg', 'png', 'webp']
video_ext = ['mp4', 'mov', 'avi', 'mkv']
time_stats = ['tot', 'load', 'pre', 'net', 'dec', 'post', 'merge']
dictionary = {
  2: 'bicycle',
  3: 'car',
  4: 'motorcycle',
  6: 'bus',
  8: 'truck',
  -1: 'xebagac'
}
def demo(opt):
  os.environ['CUDA_VISIBLE_DEVICES'] = opt.gpus_str
  opt.debug = max(opt.debug, 1)
  Detector = detector_factory[opt.task]
  detector = Detector(opt)

  if opt.demo == 'webcam' or \
    opt.demo[opt.demo.rfind('.') + 1:].lower() in video_ext:
    cam = cv2.VideoCapture(0 if opt.demo == 'webcam' else opt.demo)
    detector.pause = False
    while True:
        _, img = cam.read()
        cv2.imshow('input', img)
        ret = detector.run(img)
        time_str = ''
        for stat in time_stats:
          time_str = time_str + '{} {:.3f}s |'.format(stat, ret[stat])
        print(time_str)
        if cv2.waitKey(1) == 27:
            return  # esc to quit
  else:
    if os.path.isdir(opt.demo):
      image_names = []
      ls = os.listdir(opt.demo)
      for file_name in sorted(ls):
          ext = file_name[file_name.rfind('.') + 1:].lower()
          if ext in image_ext:
              image_names.append(os.path.join(opt.demo, file_name))
    else:
      image_names = [opt.demo]
    
    for (image_name) in image_names:
      ret = detector.run(image_name)
      time_str = ''
      for stat in time_stats:
        time_str = time_str + '{} {:.3f}s |'.format(stat, ret[stat])
      # print(time_str)
      dets = ret['results']
      txt_path = '/content/cp/{}.xml'.format(image_name.split('.')[0])
      try: 
          os.makedirs('/'.join(map(str, txt_path.split('/')[:-1])))
      except: 
          pass
      f = open(txt_path,'w')
      for key in dets.keys():
        if key in dictionary.keys():
          for i in range(len(dets[key])):
            f.write('{} {} {} {} {}\n'.format(dictionary[key],int(dets[key][i , 0]),int(dets[key][i , 1]),int(dets[key][i , 2]),int(dets[key][i , 3])))
      f.close()



if __name__ == '__main__':
  opt = opts().init()
  demo(opt)
