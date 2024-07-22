import os
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from scipy import stats
import math
import pandas as pd
from mplsoccer import PyPizza, add_image
from highlight_text import fig_text
import warnings
import matplotlib.font_manager as fm
warnings.filterwarnings("ignore", category=FutureWarning)


class SoccerPlot:
    font_normal = os.path.join('..', 'fonts', 'Lora-VariableFont_wght.ttf')
    font_italic = os.path.join('..', 'fonts', 'Lora-Italic-VariableFont_wght.ttf')
    font_bold = os.path.join('..', 'fonts', 'Oswald-VariableFont_wght.ttf')
    font_normal_prop = fm.FontProperties(fname=font_normal)
    font_italic_prop = fm.FontProperties(fname=font_italic)
    font_bold_prop = fm.FontProperties(fname=font_bold)

    def __init__(self, df, cols_filter) -> None:
        self.df = df
        self.cols_filter = cols_filter

    def get_player(self, player_name, dataframe, cols_filter):
        player = dataframe.loc[(dataframe['Player'] == player_name)].reset_index()
        player = player[cols_filter]
        return list(player.loc[0])

    def calculate_percintiles(self, params, dataframe, player):
        values = []
        for x in range(len(params)):
            values.append(math.floor(stats.percentileofscore(dataframe[params[x]], player[x])))
        return values

    def get_params_list(self, df: pd.DataFrame, cols_filter):
        params_df = df[cols_filter]
        params = list(params_df.columns)
        return params
    
    def round_image(self, img):
        width, height = img.size

        # Create a circular mask with a perfect circle
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        min_dim = min(width, height)
        circle_radius = min_dim // 2
        circle_center = (width // 2, height // 2)
        
        draw.ellipse([(circle_center[0] - circle_radius, circle_center[1] - circle_radius),
                    (circle_center[0] + circle_radius, circle_center[1] + circle_radius)],
                    fill=255)
        result = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        result.paste(img, (0, 0), mask)

        return result
    
    def create_simple_pizza_plot(self, values, params, title, subtitle, data_credit, your_credit, player_image, team_image, color_palette:dict):

        # instantiate PyPizza class
        baker = PyPizza(
            params=params,                  # list of params
            background_color=color_palette["bkg"],
            straight_line_color="#000000",  # color for straight lines
            straight_line_lw=1,             # linewidth for straight lines
            last_circle_lw=1,               # linewidth of last circle
            other_circle_lw=1,              # linewidth for other circles
            other_circle_ls="-.",           # linestyle for other circles
            inner_circle_size=20            # increase the circle size
        )
        slice_colors = [color_palette["color2"]]*len(self.cols_filter)
        # plot pizza
        fig, ax = baker.make_pizza(
            values,              # list of values
            figsize=(8, 8),      # adjust figsize according to your need
            slice_colors=slice_colors,
            value_bck_colors=slice_colors,
            color_blank_space="same",
            param_location=110,  # where the parameters will be added
            kwargs_slices=dict(
                edgecolor="#000000",
                zorder=2, linewidth=1
            ),                   # values to be used when plotting slices
            kwargs_params=dict(
                color="#F2F2F2", fontsize=12,
                fontproperties=self.font_normal_prop,
                va="center"
            ),                   # values to be used when adding parameter
            kwargs_values=dict(
                color="#F2F2F2", fontsize=12,
                fontproperties=self.font_normal_prop,
                zorder=3,
                bbox=dict(
                    edgecolor="#000000", facecolor=color_palette['color2'],
                    boxstyle="round,pad=0.2", lw=1
                )
            )                    # values to be used when adding parameter-values
        )

        # add title
        fig.text(
            0.515, 0.975, title, size=16,
            ha="center", fontproperties=self.font_bold_prop, 
            color="#F2F2F2"
        )

        # add subtitle
        fig.text(
            0.515, 0.953,
            subtitle,
            size=13,
            ha="center", fontproperties=self.font_bold_prop,
            color="#F2F2F2"
        )

        fig.text(
            0.99, 0.02, f"{data_credit}\n{your_credit}", size=9,
            fontproperties=self.font_italic_prop,
            color="#F2F2F2",
            ha="right"
        )
        # add image
        if (player_image != None) and (team_image != None):
            player_image = self.round_image(player_image)
            ax_image = add_image(player_image, fig, left=0.4, bottom=0.38, width=0.224, height=0.228)
            ax_image = add_image(team_image, fig, left=0., bottom=0.9, width=0.1, height=0.1)

        return fig, ax
    
    
    def create_3_pilars_pizza_plot(self, values, params, title, subtitle, data_credit, your_credit, player_image, team_image, color_palette: dict):
        """
        Create a pizza plot with 3 categories with 5 Stats for each
        """
        # instantiate PyPizza class
        baker = PyPizza(
            params=params,                  # list of params
            background_color=color_palette["bkg"],
            straight_line_color="#000000",  # color for straight lines
            straight_line_lw=1,             # linewidth for straight lines
            last_circle_lw=1,               # linewidth of last circle
            other_circle_lw=1,              # linewidth for other circles
            other_circle_ls="-.",           # linestyle for other circles
            inner_circle_size=20            # increase the circle size
        )
        slice_colors = [color_palette["color1"]]*5 + [color_palette["color2"]]*5 + [color_palette["color3"]] * 5
        # plot pizza
        fig, ax = baker.make_pizza(
            values,              # list of values
            figsize=(8, 8),      # adjust figsize according to your need
            slice_colors=slice_colors,
            value_bck_colors=slice_colors,
            color_blank_space="same",
            param_location=110,  # where the parameters will be added
            kwargs_slices=dict(
                edgecolor="#000000",
                zorder=2, linewidth=1
            ),                   # values to be used when plotting slices
            kwargs_params=dict(
                color="#F2F2F2", fontsize=12,
                fontproperties=self.font_normal_prop,
                va="center"
            ),                   # values to be used when adding parameter
            kwargs_values=dict(
                color="#F2F2F2", fontsize=12,
                fontproperties=self.font_normal_prop,
                zorder=3,
                bbox=dict(
                    edgecolor="#000000",
                    boxstyle="round,pad=0.2", lw=1
                )
            )                    # values to be used when adding parameter-values
        )

        # add title
        fig.text(
            0.515, 0.975, title, size=16,
            ha="center", fontproperties=self.font_bold_prop, 
            color="#F2F2F2"
        )

        # add subtitle
        fig.text(
            0.515, 0.953,
            subtitle,
            size=13,
            ha="center", fontproperties=self.font_bold_prop,
            color="#F2F2F2"
        )

        fig.text(
            0.99, 0.02, f"{data_credit}\n{your_credit}", size=9,
            fontproperties=self.font_italic_prop,
            color="#F2F2F2",
            ha="right"
        )
        # add image
        if (player_image != None) and (team_image != None):
            player_image = self.round_image(player_image)
            ax_image = add_image(player_image, fig, left=0.4, bottom=0.38, width=0.224, height=0.228)
            ax_image = add_image(team_image, fig, left=0., bottom=0.9, width=0.1, height=0.1)

        return fig, ax
    
    def create_compare_pizza_plot(self, values, values_2, params, title, subtitle, data_credit, your_credit, player1_image, player2_image, color_palette: dict):

        # instantiate PyPizza class
        baker = PyPizza(
            params=params,                  # list of params
            background_color=color_palette["bkg"],
            straight_line_color="#000000",  # color for straight lines
            straight_line_lw=1,             # linewidth for straight lines
            last_circle_lw=1,               # linewidth of last circle
            other_circle_lw=1,              # linewidth for other circles
            other_circle_ls="-.",           # linestyle for other circles
            inner_circle_size=10           # increase the circle size
        )
        slice_colors_player1 = [color_palette["color1"]]*len(self.cols_filter)
        # plot pizza
        fig, ax = baker.make_pizza(
            values,              # list of values
            compare_values=values_2,
            figsize=(8, 8),      # adjust figsize according to your need
            slice_colors=slice_colors_player1,
            value_bck_colors=slice_colors_player1,
            param_location=110,  # where the parameters will be added
            kwargs_slices=dict(
                edgecolor="#000000",
                zorder=2, linewidth=1
            ),                   # values to be used when plotting slices
            kwargs_compare=dict(
                facecolor=color_palette["color2"], edgecolor="#000000",
                zorder=2, linewidth=1,
            ),
            kwargs_params=dict(
                color="#F2F2F2", fontsize=12,
                fontproperties=self.font_normal_prop,
                va="center"
            ),                   # values to be used when adding parameter
            kwargs_values=dict(
                color="#F2F2F2", fontsize=12,
                fontproperties=self.font_normal_prop,
                zorder=3,
                bbox=dict(
                    edgecolor="#000000", facecolor=color_palette["color1"],
                    boxstyle="round,pad=0.2", lw=1
                )
            ) ,                   # values to be used when adding parameter-values
            kwargs_compare_values=dict(
                color="#F2F2F2", fontsize=12,
                fontproperties=self.font_normal_prop,
                zorder=3,
                bbox=dict(
                    edgecolor="#000000", facecolor=color_palette["color2"],
                    boxstyle="round,pad=0.2", lw=1
                )
            )
        )

        # add title
        fig_text(
            0.515, 0.99, title, size=16, fig=fig,
            highlight_textprops=[{"color": color_palette["color1"]}, {"color": color_palette["color2"]}],
            ha="center", fontproperties=self.font_bold_prop, 
            color="#F2F2F2"
        )

        # add subtitle
        fig.text(
            0.515, 0.942,
            subtitle,
            size=13,
            ha="center", fontproperties=self.font_bold_prop,
            color="#F2F2F2"
        )

        fig.text(
            0.99, 0.02, f"{data_credit}\n{your_credit}", size=9,
            fontproperties=self.font_italic_prop,
            color="#F2F2F2",
            ha="right"
        )

        if (player1_image != None) and (player2_image != None):
            player1_image = self.round_image(player1_image)
            player2_image = self.round_image(player2_image)
            ax_image = add_image(player2_image, fig, left=0.8, bottom=0.8, width=0.224, height=0.228)
            ax_image = add_image(player1_image, fig, left=0., bottom=0.8, width=0.224, height=0.228)

        return fig, ax
    
    def generate_simple_pizza_plot(self, player_name, title, subtitle, data_credit, your_credit, player_image, team_image, color_palette:dict):
        params = self.get_params_list(self.df, self.cols_filter)
        player = self.get_player(player_name, self.df, self.cols_filter)
        values = self.calculate_percintiles(params, self.df, player)

        self.create_simple_pizza_plot(values, params, title, subtitle, data_credit, your_credit, player_image, team_image, color_palette)
        plt.show()

    def generate_3_pilars_pizza_plot(self, player_name, title, subtitle, data_credit, your_credit, player_image, team_image, color_palette:dict):
        params = self.get_params_list(self.df, self.cols_filter)
        player = self.get_player(player_name, self.df, self.cols_filter)
        values = self.calculate_percintiles(params, self.df, player)

        self.create_3_pilars_pizza_plot(values, params, title, subtitle, data_credit, your_credit, player_image, team_image, color_palette)
        plt.show()
    
    def generate_compare_pizza_plot(self, player_name1, player_name2, subtitle, data_credit, your_credit, player1_image, player2_image, color_palette: dict):
        params = self.get_params_list(self.df, self.cols_filter)
        player_1 = self.get_player(player_name1, self.df, self.cols_filter)
        values_1 = self.calculate_percintiles(params, self.df, player_1)

        player_2 = self.get_player(player_name2, self.df, self.cols_filter)
        values_2 = self.calculate_percintiles(params, self.df, player_2)

        title = f'<{player_name1}> vs <{player_name2}>'
        self.create_compare_pizza_plot(values_1, values_2,params, title, subtitle, data_credit, your_credit, player1_image, player2_image, color_palette)
        plt.show()
