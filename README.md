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

The data given to me was one sample selected from a pool of 223 people. There were 3 datasets with varying amounts of information, but each had well over 40,000 measurements. The goal was simple; I wanted to take the data and create methods that prepared the datasets for future manipulation such as visualization and machine learning, visualize the data to better understand it and discover patterns, and prepare methods that could be applied to future larger datasets in a similar format. However, I first needed to understand and clean the data before doing any analysis, and because this was new data that the company collected, I explored and cleaned the data while also creating a dictionary explaining what each of the datasets measured.

Overall, the process of understanding and cleaning the datasets was a long and tedious process. However, its importance cannot be stressed enough; through this organization, I was able to understand the data and get a better understanding on what information I was working with. Along with that, I was able to determine what data was truly useful and what wasn’t, which made the analytics and visualizations a much easier process in the future. This is just a quick summary of each of the datasets and what was done to clean it, but if you'd like a more in depth explanation of the datasets, a description of each of the columns in each dataset can be accessed [here](). 

_IBI Dataset_ 

<p align="center">
	<img src="https://github.com/bew030/scripps-wearable-tech-research/blob/master/read_me_images/Screen%20Shot%202019-10-19%20at%209.16.28%20PM.png" />
</p>
<p align="center">
  <i>The left image is the raw IBI data, while the right image is the raw data converted and organized into a dataframe</i>
</p>

Interbeat interval, or IBI, is the time interval between individual beats of the heart. It’s a useful measurement because it reflects how effective the brain’s communication with the heart is. A healthy body will have many varying IBIs due to the constant changes between the sympathetic and parasympathetic nervous system, so when IBI doesn’t vary this can be a warning sign to slowing neural communication or other neural issues. You can learn more about IBI [here](https://support.mindwaretech.com/2017/09/all-about-hrv-part-2-interbeat-intervals-and-time-domain-stats/). 
 
The dataset that we had contained almost 500,000 measurements of IBIs that occurred from 11.27.2018 to 12.12.2018, with a measurement occurring nearly every second (non inclusive of the time the wearable device was off or wasn’t running). The dataset contained information about when the IBI measurements were taken along with how valid the IBI measurement was. Overall, the dataset was relatively easy to clean and had no missing data. Because more than 95% of the data was clean, we only selected the most valid data and did an analysis on those.

_Motion Dataset_ 

<p align="center">
	<img src="https://github.com/bew030/scripps-wearable-tech-research/blob/master/read_me_images/Screen%20Shot%202019-10-19%20at%209.16.40%20PM.png"/>
</p>
<p align="center">
  <i>The left image is the raw motion data, while the right image is the raw data converted and organized into a dataframe</i>
</p>

This dataset was the simplest of the three datasets. It contained information about the date, time, how long motion occurred in seconds, the NTC temperature (the temperature of the internal components), ring state, number of low and high motions per minute, and average y and z motion during the duration of measurement. Due to the interests of the project being primarily related to sleep and heart rate, not much further analysis was done with the motion dataset. However, a dictionary explaining the columns of this dataset should make it easier for analysis in the future.

_Sleep Dataset_ 

<p align="center">
	<img src="https://github.com/bew030/scripps-wearable-tech-research/blob/master/read_me_images/Screen%20Shot%202019-10-19%20at%209.16.49%20PM.png"/>
</p>
<p align="center">
  <i>The left image is the raw sleep data, while the right image is the raw data converted and organized into a dataframe</i>
</p>

The sleep dataset was by far the most complicated due to a number of factors. One reason was that it had the most information and as a result took some deeper exploring to understand. For example, there were columns such as ‘is_longest’ and ‘​Lowest HR time minutes​’ which could mean a variety of things. There were more than 500 different measurements about sleep, but after some communication with the company we were able to make sense of what most of the columns meant. Along with that, not each data point had the same amount of information; due to the organization of the columns of the dataset, there were a few regarding the sleep cycles that occurred during sleep. Because not each sleep measurement lasted the same duration and therefore didn’t have the same number of sleep cycles, certain data points had measurements of sleep cycles while others didn’t. The data had naively just recorded no data whenever there weren’t sleep cycles and as a result formatting with the data was extremely poor. To resolve the issue, I replaced missing data with
placeholders representing nonexistent data, which enabled me to see full sleep cycles and make the data more readable.

Being such a big dataset, there were bound to be plenty of errors within the data. Time measurements were often slightly off, conditions were often erroneous, and sometimes software issues such as the wearable coming off or losing power would lead to errors in measuring sleep cycles and breathing rate. By sweeping the data and removing as many of these inaccurate data points, I was able to make the data a little more readable and easier to process later on. Even after the cleaning there were 1780 columns of data, making this dataset extremely informative.


# Visualizations

_IBI Dataset_ 

_Sleep Dataset_ 

# Conclusions



# Badges 
[![GitHub issues](https://img.shields.io/github/issues/bew030/scripps-wearable-tech-research?color=purple)](https://github.com/bew030/scripps-wearable-tech-research/issues)
[![GitHub forks](https://img.shields.io/github/forks/bew030/scripps-wearable-tech-research?color=orange)](https://github.com/bew030/scripps-wearable-tech-research/network)
[![GitHub stars](https://img.shields.io/github/stars/bew030/scripps-wearable-tech-research)](https://github.com/bew030/scripps-wearable-tech-research/stargazers)
[![HitCount](http://hits.dwyl.io/bew030/scripps-wearable-tech-research.svg)](http://hits.dwyl.io/bew030/scripps-wearable-tech-research)
