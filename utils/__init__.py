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
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
