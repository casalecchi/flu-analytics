import inquirer
import matplotlib.pyplot as plt
import pandas as pd
import requests
import os
import numpy as np
import shutil
from matplotlib.offsetbox import OffsetImage,AnnotationBbox
from PIL import Image, ImageDraw

from utils.Statistics import *
from utils.Team import *

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}
