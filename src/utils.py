import matplotlib.font_manager as fm
from matplotlib.colors import LinearSegmentedColormap
import os

font_lora_path = os.path.join('..', 'fonts', 'Lora-VariableFont_wght.ttf')
font_lora_italic = os.path.join('..', 'fonts', 'Lora-Italic-VariableFont_wght.ttf')
font_oswald_bold_path = os.path.join('..', 'fonts', 'Oswald-VariableFont_wght.ttf')
font_robotomono_italic_path = os.path.join('..', 'fonts', 'RobotoMono-Italic-VariableFont_wght.ttf')
font_robotomono_bold_path = os.path.join('..', 'fonts', 'RobotoMono-VariableFont_wght.ttf')
font_robot_regular_path = os.path.join('..', 'fonts', 'Roboto-Regular.ttf')
font_robot_italic_path = os.path.join('..', 'fonts', 'Roboto-Italic.ttf')
font_robot_bold_path = os.path.join('..', 'fonts', 'Roboto-Bold.ttf')
font_sevillana_path = os.path.join('..', 'fonts', 'Sevillana-Regular.ttf')

FONT_LORA = fm.FontProperties(fname=font_lora_path)
FONT_LORA_ITALIC = fm.FontProperties(fname=font_lora_italic)
FONT_OSWALD = fm.FontProperties(fname=font_oswald_bold_path)
FONT_ROBOTMONO_ITALIC = fm.FontProperties(fname=font_robotomono_bold_path)
FONT_ROBOTMONO = fm.FontProperties(fname=font_robotomono_italic_path)
FONT_ROBOTO = fm.FontProperties(fname=font_robot_regular_path)
FONT_ROBOTO_BOLD = fm.FontProperties(fname=font_robot_bold_path)
FONT_ROBOTO_ITALIC = fm.FontProperties(fname=font_robot_italic_path)
FONT_SEVILLANA = fm.FontProperties(fname=font_sevillana_path)


COLORS_PALETTE_1 = {
    "bkg": "#092635",
    "color1": "#1B4242",
    "color2": "#5C8374",
    "color3": "#9EC8B9"
}

COLORS_PALETTE_2 = {
    "bkg": "#150485",
    "color1": "#590995",
    "color2": "#C62A88",
    "color3": "#03C4A1"
}

COLORS_PALETTE_3 =  {
    "bkg": "#351F39",
    "color1": "#726A95",
    "color2": "#719FB0",
    "color3": "#A0C1B8"
}


COLORS_PALETTE_4 = {
    "bkg": "#A9A9A9",
    "color1": "#FECDA6",
    "color2": "#FF9130",
    "color3": "#FF5B22"
}

COLORS_PALETTE_5 = {
    "bkg": "#A1CCD1",
    "color1": "#F4F2DE",
    "color2": "#E9B384",
    "color3": "#7C9D96"
}

COLORS_PALETTE_6 = {
    "bkg": "#F99B7D",
    "color1": "#E76161",
    "color2": "#B04759",
    "color3": "#8BACAA"
}

COLORS_PALETTE_7 = {
    "bkg": "#025464",
    "color1": "#E57C23",
    "color2": "#E8AA42",
    "color3": "#F8F1F1"
}

COLORS_PALETTE_8 = {
    "bkg": "#711DB0",
    "color1": "#C21292",
    "color2": "#EF4040",
    "color3": "#FFA732"
}

COLORS_PALETTE_9 = {
    "bkg": "#001B79",
    "color1": "#1640D6",
    "color2": "#ED5AB3",
    "color3": "#FF90C2"
}

COLORS_PALETTE_10 = {
    "bkg": "#756AB6",
    "color1": "#8DDFCB",
    "color2": "#82A0D8",
    "color3": "#EDB7ED"
}


COLORS_PALETTE_11 = {
    "bkg": "#0F0F0F",
    "color1": "#232D3F",
    "color2": "#005B41",
    "color3": "#008170"
}


COLORS_PALETTE_12 = {
    "bkg": "#000000",
    "color1": "#CEDEBD",
    "color2": "#4F6F52",
    "color3": "#3A4D39"
}


COLORS_PALETTE_13 = {
    "bkg": "#000000",
    "color1": "#150050",
    "color2": "#A91079",
    "color3": "#FB2576"
}

COLORS_PALETTE_14 = {
    "bkg": "#A9A9A9",
    "color1": "#FECDA6",
    "color2": "#FF9130",
    "color3": "#FF5B22"
}

COLORS_PALETTE_15 = {
    "bkg": "#E19898",
    "color1": "#A2678A",
    "color2": "#4D3C77",
    "color3": "#3F1D38"
}

custom_color = [(0, COLORS_PALETTE_12["color1"]), (0.5, COLORS_PALETTE_12["color2"]), (1, COLORS_PALETTE_12["color3"])]
CUSTOM_CMP_1 = LinearSegmentedColormap.from_list('custom_map', custom_color)
custom_color_2 = [(0, COLORS_PALETTE_13["color1"]), (0.5, COLORS_PALETTE_13["color2"]), (1, COLORS_PALETTE_13["color3"])]
CUSTOM_CMP_2 = LinearSegmentedColormap.from_list('custom_map', custom_color_2)
custom_color_3 = [(0, COLORS_PALETTE_14["color1"]), (0.5, COLORS_PALETTE_14["color2"]), (1, COLORS_PALETTE_14["color3"])]
CUSTOM_CMP_3 = LinearSegmentedColormap.from_list('custom_map', custom_color_3)
custom_color_4 = [(0, COLORS_PALETTE_15["color1"]), (0.5, COLORS_PALETTE_15["color2"]), (1, COLORS_PALETTE_15["color3"])]
CUSTOM_CMP_4 = LinearSegmentedColormap.from_list('custom_map', custom_color_4)