from visualization import *


def crop_circle_img(path: str):
    """Crop the image to a circle shape"""
    img = Image.open(path).convert("RGBA")
    background = Image.new("RGBA", img.size, (0,0,0,0))

    mask = Image.new("RGBA", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0,0, *img.size), fill='green', outline=None)

    new_img = Image.composite(img, background, mask)
    new_img.save(ROOT_DIR + "/src/images/tmp.png")

def fetch_img_from_url(url, crop=True):
    """Return the path for the fetched image."""
    response = requests.get(url, stream=True, headers=HEADERS)
    if response.status_code == 200:
        path = ROOT_DIR + "/src/images/tmp.jpg"
        f = open(path, 'wb')
        shutil.copyfileobj(response.raw, f)
        f.close()
        if crop: 
            crop_circle_img(path)
            return ROOT_DIR + '/src/images/tmp.png'
        else:
            return path
    else:
        return ROOT_DIR + "/src/images/player.png"