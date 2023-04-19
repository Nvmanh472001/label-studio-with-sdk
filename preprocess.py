import os
import json
from math import dist
from pathlib import Path
from PIL import Image
import pandas as pd
import numpy as np
from uuid import uuid4


def create_image_url(image_path):
    return f"/data/local-files/?d={image_path}"


def read_data_from_path(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        data = f.readlines()
    data = [json.loads(line) for line in data]
    return data


def get_label_from_path(label_file_path):
    df = pd.read_csv(label_file_path, delimiter="\s", header=None, engine="python")
    id2labels = dict(zip(df[0].tolist(), df[1].tolist()))
    return id2labels


def convert_data_to_lbs_format(save_path, data, labels):
    """
    Convert Data to Label Studio Format
    """
    tasks = []
    for line in data:
        h = line["height"]
        w = line["width"]

        annotations = line["annotations"]
        result = []
        for annotation in annotations:
            annotation.update(
                {
                    "label": labels[annotation["label"]],
                    "image_size": (w, h),
                }
            )

            result.extend(annotation_fommater(annotation))

        lbs_format = {
            "data": {"ocr": create_image_url(line["file_name"])},
            "predictions": [
                {
                    "result": result,
                }
            ],
        }
        tasks.append(lbs_format)

    with open(save_path, mode="w") as buf:
        json.dump(tasks, buf, indent=2)


def annotation_fommater(annotation):
    w, h = annotation["image_size"]
    points = np.asarray(annotation["box"]).reshape((-1, 2))

    id_gen = str(uuid4())[:10]
    x = points[0][0]
    y = points[0][0]

    region_width = dist(points[0], points[1])
    region_height = dist(points[0], points[3])

    box_annotation = {
        "original_width": w,
        "original_height": h,
        "image_rotation": 0,
        "value": {
            "x": 100 * x / w,
            "y": 100 * y / h,
            "width": 100 * region_width / w,
            "height": 100 * region_height / h,
            "rotation": 0,
        },
        "id": id_gen,
        "from_name": "bbox",
        "to_name": "image",
        "type": "rectangle",
        "origin": "manual",
    }

    text_annotations = {
        "original_width": w,
        "original_height": h,
        "image_rotation": 0,
        "value": {
            "x": 100 * x / w,
            "y": 100 * y / h,
            "width": 100 * region_width / w,
            "height": 100 * region_height / h,
            "rotation": 0,
            "text": [annotation["text"]],
        },
        "id": id_gen,
        "from_name": "transcription",
        "to_name": "image",
        "type": "textarea",
        "origin": "manual",
    }

    label_annotation = {
        "original_width": w,
        "original_height": h,
        "image_rotation": 0,
        "value": {
            "x": 100 * x / w,
            "y": 100 * y / h,
            "width": 100 * region_width / w,
            "height": 100 * region_height / h,
            "rotation": 0,
            "labels": [annotation["label"]],
        },
        "id": id_gen,
        "from_name": "label",
        "to_name": "image",
        "type": "labels",
        "origin": "manual",
    }

    return [box_annotation, text_annotations, label_annotation]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="./data")

    args = parser.parse_args()
    fpath_pattern = f"{args.data_dir}/*.txt"

    test_fpath = f"{args.data_dir}/test.txt"
    train_fpath = f"{args.data_dir}/train.txt"
    label_fpath = f"{args.data_dir}/class_list.txt"

    labels = get_label_from_path(label_fpath)
    train_data = read_data_from_path(train_fpath)
    test_data = read_data_from_path(test_fpath)

    convert_data_to_lbs_format("train.json", train_data, labels)
    convert_data_to_lbs_format("test.json", test_data, labels)
