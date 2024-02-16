import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import statistics
from scipy.stats import norm   
import numpy as np
from statsmodels.graphics.gofplots import qqplot
from matplotlib import pyplot

class Plotter:
    '''
    Class for plotting graph
    
    Methods:
        bar_chart_plot(index, values, xlabel=str, ylabel=str, title=str, rotation=0, grid=bool, bar_width=0.8): prints a bar chart 
        hist_plotter(data, bins): prints a histogram
        is_data_skew(data, column_name): prints skew of the data
        qq_plotter(data, column_name): prints a qq-plo
        box_plot(data, column_name): prints a box plo
        scatter_plot(data): prints a scatter plot
    '''

    def bar_chart_plot(self, index, values, xlabel='', ylabel='', title='', rotation=0, grid=bool, bar_width=0.8):
        '''
        Function to plot a bar chart.

        Args:
            index (list or array-like): The x-axis values.
            values (list or array-like): The y-axis values.
            xlabel (str, optional): Label for the x-axis. Defaults to ''.
            ylabel (str, optional): Label for the y-axis. Defaults to ''.
            title (str, optional): Title of the plot. Defaults to ''.
            rotation (int, optional): Rotation angle of x-axis labels. Defaults to 0.
            grid (bool, optional): Whether to display grid lines. Defaults to False.
            bar_width (float, optional): Width of the bars. Defaults to 0.8.

        Returns:
            A graph
        '''
        plt.bar(index, values, width=bar_width)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.xticks(rotation=rotation)
        plt.grid(grid)
        plt.show()

    def hist_plotter(self, data, bins):
        '''
        Function to plot a histogram and density plot.

        Args:
            data (Series or array-like): The data to be plotted.
            bins (int or sequence of scalars or str, optional): Specification of histogram bins. Defaults to 10.

        Returns:
            A histogram
        '''
        data.hist(bins=bins, density=True)
        data.plot.density()

    def is_data_skew(self, data, column_name):
        '''
        Fucntion xomputes the skew of data in the column
        
        Args:
            data (pd.Dataframe): dataframe containing the column.
            column_name (str): name of the column that you want inspect the skew of.
        
        Return:
            str: the skew of {column_name} is : {skew}
        '''
        skew = data[column_name].skew()
        return f'the skew of {column_name} is : {skew}'

    def qq_plotter(self, data, column_name):
        '''
        Function to plot a QQ plot for a specified column in the dataset.

        Args:
            data (DataFrame): The input dataset.
            column_name (str): The name of the column to plot the QQ plot for.

        Returns:
            A qq-plot
        '''
        filtered_data = data[column_name].dropna()
        qqplot(filtered_data , scale=1 ,line='q', fit=True)
        pyplot.show()

    def box_plot(self, data, column_name):
        '''
        Function to plot a boxplot for a specified column in the dataset.

        Args:
            data (DataFrame): The input dataset.
            column_name (str): The name of the column to plot the boxplot for.

        Returns:
            A box plot
        '''
        plt.title(f'{column_name}')
        sns.boxplot(data[column_name])
        plt.show()

    def scatter_plot(self, data):
        '''
        Function to plot a scatter plot for two columns in the dataset.

        Args:
            data (DataFrame): The input dataset.

        Returns:
            A scatter graph
        '''
        sns.scatterplot(data)
    
      