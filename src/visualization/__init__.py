import inquirer
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage,AnnotationBbox
import os
import pandas as pd
from pathlib import Path
from PIL import Image, ImageDraw
import requests
import shutil

from extraction.classes import SofaStats

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}

ROOT_DIR = str(Path(__file__).absolute().parent.parent.parent)
