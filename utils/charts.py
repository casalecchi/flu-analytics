from utils import *


def crop_img(path):
    img = Image.open(path).convert("RGBA")
    background = Image.new("RGBA", img.size, (0,0,0,0))

    mask = Image.new("RGBA", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0,0,150,150), fill='green', outline=None)

    new_img = Image.composite(img, background, mask)
    new_img.save('image.png')

def fetch_img(url, crop=True):
    response = requests.get(url, stream=True, headers=HEADERS)
    if response.status_code == 200:
        f = open('image.jpg', 'wb')
        shutil.copyfileobj(response.raw, f)
        f.close()
        if crop: 
            crop_img('image.jpg')
            return 'image.png'
        else:
            return 'image.jpg'
    else:
        path = os.getcwd() + "/img/player.png"
        return path

def get_text_y(value, max_value):
    return value - 0.13 * max_value
    
def get_badge_y(value, max_value):
    if max_value < 2:
        return value - 0.5 * max_value
    else:
        return value - 0.27 * max_value
    
def get_avatar_y(max_value):
    return -max_value * 0.2
    
def generate_bar_from_data(data, column, title, isInt=True, k=10):
    plt.figure(figsize=(24,6), facecolor="#EEE9E4") 
    ax = plt.axes()
    ax.set_facecolor("#EEE9E4")
    filtered_data = data.sort_values(column, ascending=False).head(k)
    max_value = filtered_data.iloc[0][column]

    plt.bar(
        filtered_data["name"], filtered_data[column],
        color=filtered_data["primary_color"],
        edgecolor=filtered_data["secondary_color"],
        width=0.5,
        linewidth=5,
    )

    for i in range(k):
        value = filtered_data.iloc[i][column]
        if isInt:
            value = int(value)
        plt.text(x=i,
                y=get_text_y(value, max_value),
                s = str(value),
                backgroundcolor='#EEE9E4',
                ha='center',
                # weight='bold',
                fontsize=16,
                )
        
        badge_path = fetch_img(filtered_data.iloc[i]['badge_url'], crop=False)
        badge = plt.imread(badge_path)
        offset_badge = OffsetImage(badge, zoom=0.28)
        offset_badge.image.axes = ax
        ab = AnnotationBbox(offset_badge, (i, 0),  xybox=(i, get_badge_y(value, max_value)), frameon=False,
                            xycoords='data', pad=0)
        ax.add_artist(ab)

        img_path = fetch_img(filtered_data.iloc[i]['avatar_url'])
        avatar = plt.imread(img_path)
        offset_avatar = OffsetImage(avatar, zoom=0.4)
        offset_avatar.image.axes = ax
        ab = AnnotationBbox(offset_avatar, (i, 0),  xybox=(i, get_avatar_y(max_value)), frameon=True,
                        xycoords='data', pad=0, bboxprops={'boxstyle': 'circle', 
                                                           'ec': filtered_data.iloc[i]["primary_color"],
                                                           'linewidth': 3})
        ax.add_artist(ab)
        
    def format_names(x, _):
        name = filtered_data.iloc[x]['name']
        separated_name = name.split()
        if len(name) > 13:
            len_first = len(separated_name[0])
            len_second = len(separated_name[1])
            if len_first > len_second:
                separated_name[0] = f"{name[0]}."
            else:
                separated_name[1] = f"{separated_name[1][0]}."
        return " ".join(separated_name[0:2])
    
    plt.xticks(fontsize=19)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(format_names))
    ax.set_yticks([])
    plt.title(title, fontsize=24)
    plt.savefig(f'{title}.png', bbox_inches = 'tight')
    os.remove('image.jpg')
    os.remove('image.png')
