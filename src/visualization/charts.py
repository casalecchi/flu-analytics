from visualization import *
from visualization.imageProcessing import fetch_img_from_url

def get_text_y(value, max_value):
    return value - 0.13 * max_value
    
def get_badge_y(value, max_value):
    return value - 0.27 * max_value
    
def get_avatar_y(max_value):
    return -max_value * 0.2
    
def generate_bar_from_data(data, column, title, isInt=True, k=10):
    plt.figure(figsize=(k * 2.4, 6), facecolor="#EEE9E4") 
    ax = plt.axes()
    ax.set_facecolor("#EEE9E4")
    filtered_data = data.sort_values(column, ascending=False).head(k)
    max_value = filtered_data.iloc[0][column]

    plt.bar(
        filtered_data["player_name"], filtered_data[column],
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
                 # if the value is too low, the label will be lower.
                 # with max we fixed the mininum value for y
                 y=max(get_text_y(value, max_value), 0.07 * max_value),
                 s = str(value),
                 backgroundcolor='#EEE9E4',
                 ha='center',
                 # weight='bold',
                 fontsize=16,
                )
        
        if value >= 0.35 * max_value:
            # if less will be no room for the badge
            badge_path = fetch_img_from_url(filtered_data.iloc[i]['badge_url'], crop=False)
            badge = plt.imread(badge_path)
            offset_badge = OffsetImage(badge, zoom=0.28)
            offset_badge.image.axes = ax
            ab = AnnotationBbox(offset_badge, (i, 0),  xybox=(i, get_badge_y(value, max_value)), frameon=False,
                                xycoords='data', pad=0)
            ax.add_artist(ab)

        img_path = fetch_img_from_url(filtered_data.iloc[i]['avatar_url'])
        avatar = plt.imread(img_path)
        offset_avatar = OffsetImage(avatar, zoom=0.4)
        offset_avatar.image.axes = ax
        ab = AnnotationBbox(offset_avatar, (i, 0),  xybox=(i, get_avatar_y(max_value)), frameon=True,
                        xycoords='data', pad=0, bboxprops={'boxstyle': 'circle', 
                                                           'ec': filtered_data.iloc[i]["primary_color"],
                                                           'linewidth': 3})
        ax.add_artist(ab)
        
    def format_names(x, _):
        name = filtered_data.iloc[x]['player_name']
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
    path = ROOT_DIR + "/src/examples/"
    plt.savefig(path + f'{title}.png', bbox_inches = 'tight')
    os.remove(ROOT_DIR + '/src/images/tmp.jpg')
    os.remove(ROOT_DIR + '/src/images/tmp.png')

def get_bar_chart_inputs():
    choices = []
    for attr in SofaStats.Player_Stats_For_Tournament:
        choices.append(attr)
    choices.sort()

    questions = [
        inquirer.Text('fname', message="Type the file name with data (with .csv)"),
        inquirer.List('attr', message="What attribute you want to create the ranking?",
                        choices=choices,),
        inquirer.Text('title', message="Inform the title of your chart"),
        inquirer.Text('k', message="K-value"),
        inquirer.Text('isInt', message="Attribute should be presented as integer? [y]|[n]")
    ]

    answers = inquirer.prompt(questions)
    return answers