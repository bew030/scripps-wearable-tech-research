# Overview <img src="https://i.ytimg.com/vi/-nTwk1gqof8/maxresdefault.jpg" align="right" height="45">
_Created by Bernard Wong (bew030@ucsd.edu) in partnership with the [Scripps Research Translational Institute](https://www.scripps.edu/science-and-medicine/translational-institute/) and Giorgio Quer_

Over the summer, I had the great opportunity to intern under Giorgio Quer for Scripps Research Translational Institute. Oura, a wearable ring that tracks different health metrics, had shared the data with us and had given us the freedom to explore. Me and my mentor worked together to organize a series of questions that we aimed to answer by the end of the internship and then created weekly goals to help maintain productiveness. Throughout this research experience, I had the joy of collaborating with other data scientists at the institute, learn about working with real, messy data, and ultimately present my findings in front of a panel of well established doctors and health professionals. I would like to extend my thanks to the faculty at the institute for giving me such a valuable learning experience, and especially thank Giorgio for mentoring me through the process and making this exploration extremely rewarding. 

This repository has been organized for easy navigation. It contains a [writings](https://github.com/bew030/scripps-wearable-tech-research/tree/master/writings) which contains all the writing that I had done during my research, which includes my presentation, an exploratory paper about the impact of wearable technology, and my final research paper. The [final paper](https://github.com/bew030/scripps-wearable-tech-research/blob/master/writings/Scripps%20Research%20Project%20Overview.pdf) can be found and downloaded in this folder, but you can also find the results of my research throughout the rest of this README. There is also an [IBI_sleep_visualizations folder](https://github.com/bew030/scripps-wearable-tech-research/tree/master/IBI_sleep_visualizations) that contains all of the visualizations generated from the data: the code and notebooks used to explore the data and create these visualizations can also be found in the [python notebook workshops folder](https://github.com/bew030/scripps-wearable-tech-research). You can also take a look at the [final jupyter notebook](https://github.com/bew030/scripps-wearable-tech-research/blob/master/Final%20Notebook.ipynb) if you're interested in viewing the visualization code run. If you have data from an Oura wearable or data that fits the dataset criteria, you may also download the code from the [packages folder](https://github.com/bew030/scripps-wearable-tech-research/tree/master/packages). This code contains the packages for [ibi analysis](https://github.com/bew030/scripps-wearable-tech-research/tree/master/packages/ibisdk),[sleep analysis](https://github.com/bew030/scripps-wearable-tech-research/tree/master/packages/sleepsdk), and [motion analysis](https://github.com/bew030/scripps-wearable-tech-research/tree/master/packages/motionsdk). 

Out of respect of user privacy I've gone ahead and deleted the dataset used for my exploration. Explanations and snippets of the dataset have been scattered throughout the writings and the report, but if you have any questions or would like to learn more, please feel free to reach out by email or leave an issue. 

# Using the Code 

To make data analysis as neat as possible, all the methods have been organized into a well ordered package. Methods that analyze IBI, motion, and sleep have all been packaged in their own respective package. You can import all of these packages at once by importing the 'packages' package. 

__TL;DR:__ 

run the following code in your Jupyter Notebook: 

```python 
from packages import MotionAnalyzer
from packages import SleepAnalyzer
from packages import IBIAnalyzer
```

Run the following code in your Terminal: 

```python
pip install packages
```

The packages for IBI, motion, and sleep are primarily divided into methods that organize and clean the dataset and methods that visualize the data. The methods for [IBI](https://github.com/bew030/scripps-wearable-tech-research/blob/master/packages/ibisdk/wrapper.py), [motion](https://github.com/bew030/scripps-wearable-tech-research/blob/master/packages/motionsdk/wrapper.py), and [sleep](https://github.com/bew030/scripps-wearable-tech-research/blob/master/packages/sleepsdk/wrapper.py) are well documented, but if you have any issues please feel free to reach out. 


# The Data 


_IBI Dataset_ 

_Motion Dataset_ 

_Sleep Dataset_ 

__Data Analysis__ 

_IBI Dataset_ 

_Sleep Dataset_ 

__Conclusion__

## An Overview on Methods to be Used on Future Data ## 


# Badges 
[![GitHub issues](https://img.shields.io/github/issues/bew030/scripps-wearable-tech-research?color=purple)](https://github.com/bew030/scripps-wearable-tech-research/issues)
[![GitHub forks](https://img.shields.io/github/forks/bew030/scripps-wearable-tech-research?color=orange)](https://github.com/bew030/scripps-wearable-tech-research/network)
[![GitHub stars](https://img.shields.io/github/stars/bew030/scripps-wearable-tech-research)](https://github.com/bew030/scripps-wearable-tech-research/stargazers)
[![HitCount](http://hits.dwyl.io/bew030/scripps-wearable-tech-research.svg)](http://hits.dwyl.io/bew030/scripps-wearable-tech-research)
