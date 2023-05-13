from ultralytics import YOLO
import cv2
import numpy as np
import yaml
import os
import math

os.environ['CLEARML_CONFIG_FILE'] = "clearml.conf"

from clearml import Task, InputModel

with open('config.yaml','r') as f:
    configModel = yaml.safe_load(f)

task = Task.init(project_name=configModel["clearml-project-config"]["project-name"], task_name=configModel["clearml-project-config"]["task-name"],
                 task_type=configModel["clearml-project-config"]["task-type"], reuse_last_task_id=configModel["clearml-project-config"]["id"])

inputModel = InputModel(project=configModel["clearml-project-config"]["project-name"], name=configModel["model-config"]["YOLO-model"],
                        only_published=configModel["model-config"]["published"], tags=configModel["model-config"]["tags"])

task.connect(inputModel)
pathToModel = inputModel.get_local_copy()

model = YOLO(pathToModel)
imgSize = configModel["model-config"]["image-size"]

def extractValue(img, latitude, zoomLevel):
    scalingH, scalingW = img.shape[0]/imgSize, img.shape[1]/imgSize
    data = cv2.resize(img, (imgSize, imgSize))

    results = model.predict(data, imgsz = imgSize,
                            conf = configModel["model-config"]["conf"], iou = configModel["model-config"]["iou"],
                            save = configModel["model-config"]["save-mode"], save_conf = configModel["model-config"]["save-mode"],
                            save_crop = configModel["model-config"]["save-mode"], save_txt = configModel["model-config"]["save-mode"],
                            device = configModel["model-config"]["device-mode"],
                            show_labels=True, show_conf=True)
    
    METERS_PER_PX = (156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoomLevel))
    RATIO_PIXEL_TO_SQUARE_M = METERS_PER_PX * METERS_PER_PX
    AREA_METER_LIST = {}
    ORDER = 1
    for i in range(len(results)):
        for j in range(len(results[i].masks)):
            segmenPoly = results[i].masks[j].xy
            
            x1 = int(results[i].boxes[j].xyxy[0][0]*scalingW)
            y1 = int(results[i].boxes[j].xyxy[0][1]*scalingH)
            x2 = int(results[i].boxes[j].xyxy[0][2]*scalingW)
            y2 = int(results[i].boxes[j].xyxy[0][3]*scalingH)

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            for x in segmenPoly:
                for y in x:
                    y[0] = round(y[0]*scalingH)
                    y[1] = round(y[1]*scalingW)

            pts = np.array(segmenPoly[0], np.int32)
            pts = pts.reshape((-1, 1, 2))

            img = cv2.polylines(img, [pts], True, (255, 0, 0), 2)
            img = cv2.putText(img, f"{ORDER}", (center_x, center_y), cv2.FONT_HERSHEY_PLAIN, 3 , (255,255,255), 5)
            areaPX = cv2.contourArea(pts,)
            areaM = (round(areaPX * RATIO_PIXEL_TO_SQUARE_M, 3))
            AREA_METER_LIST.update({ORDER:areaM})
            ORDER = ORDER + 1
    
    totalTambakIkan = len(results[0].boxes.cls)

    return img, AREA_METER_LIST, totalTambakIkan