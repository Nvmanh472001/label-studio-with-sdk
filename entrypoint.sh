#!/bin/bash
echo "---------Start loading dataset to Label Studio Project!---------"
python3 load_to_lbs.py || exit 1
echo "---------Finish load to LBS---------"
echo "---------End this container---------"