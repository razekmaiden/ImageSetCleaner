# Semi-supervised detection of wrong label in labeled data set
![demo_gui_cut](https://user-images.githubusercontent.com/25333848/33291972-e7f8c908-d3c7-11e7-8a32-95abc1d216e4.gif)

## Usage

This algorithm is well suited to validate labelled images obtained with web scrapping, user or colloborative generated labels.



## How does it work

This approach separate our image directory between two classes, inliers, and outliers, by describing the images with the bottlenecks
values generated by the end of the convolution phase of a pre-trained CNN like 'inception-v3' or a mobile net, for faster computation. These values are then fed to a clustering algorithm to get a prediction. To increase performance, some values of random images are precomputed, and added during the fit of our classifier.



## Basic Usage

Just run the ImageSetCleaner.py and pass the location of the directory you want to detect like so :
`python image_set_cleaner.py --image_dir=./foo/LocationLabelDir/`

You will then see a GUI pop up where you will be able to fine tune the detection and delete/move the selected outliers.


## Installation

`$ pip install -r requirements.txt`

## Options

* --image_dir: Path to the image directory you want to examine

* --clustering_method: Choose your method of clustering, between : kmeans, birch, gaussian_mixture, agglomerative_clustering

* --processing: You have the choice between 3 operations to handle the predictions of the clustering algorithm :
              - gui (default) : Will pop a gui that will let you delete the detected images directly
              - delete : Will simply delete the detected outliers
              - move : Will move the detected outliers to specified path given in --relocation_dir

* --relocation_dir: Path where you want the detected images to be moved, when the processing option move is selected

* --architecture:  The name of the pretrained architecture you want to use. I will advice to use a mobilenet, instead of inception-v3, unless you have a lot of image of one label, to prevent the effect of the curse of dimensionality:

 ['inception_v3', 'mobilenet_1.0_224', 'mobilenet_1.0_192', 'mobilenet_1.0_160', 'mobilenet_1.0_128','mobilenet_0.75_224', 'mobilenet_0.75_192', 'mobilenet_0.75_160', 'mobilenet_0.75_128', 'mobilenet_0.50_224', 'mobilenet_0.50_192', 'mobilenet_0.50_160', 'mobilenet_0.50_128', 'mobilenet_0.25_224', 'mobilenet_0.25_192', 'mobilenet_0.25_160', 'mobilenet_0.25_128']

 The mobilenet follow the pattern : mobilenet_<parameter size>_<input_size>

* --model_dir: Path where you want the weights and description to be downloaded, or if already done

* --pollution_dir: Path where the precomputed of random images are located.

* --pollution_percent: The percentage of bolltenecks that will be used for the prediction of the clustering algorithm in addition to the    values computed on your images.

## Creating your own noisy bottlenecks

You can create your own pollution values, that are more specefic to your problem by running the script Create_noise_bottlenecks.py. See further explanations, and option inside the file.

`python create_noise_bottlenecks.py --image_dir=./foo/LocationLabelDir/ --architecture=all`


### Some result

![cat_vs_dog](https://user-images.githubusercontent.com/25333848/33291975-ec609138-d3c7-11e7-952f-198eb827680c.png)

As expected this method works realy great, for images or labels that our pretrained CNN has seen. So if you have a need specific, or checking a constant data stream, with known outcome of images, I encourage you to use a custom CNN and adapt the code, and/or use the create_noise_bottlenecks script , for better performance.  We can also see that our estimator as a breaking point between 40-45 %. This is due to the process of normalizing the predictions, and choosing as inliers the smallest cluster. 

![google_test_graphic_card](https://user-images.githubusercontent.com/25333848/33580223-a11e9d70-d94c-11e7-8d71-013dd47df9c9.png)

![google_test_knife](https://user-images.githubusercontent.com/25333848/33580224-a13a624e-d94c-11e7-96b2-d1a79a55058b.png)

In these two graphs, we can see that that we can achieve a detection of up to 90 % of wrong labels from an unreliable data source, while minimizing false positives to under 10 % of our set. This can bring your data set, from unsalvageable or too expensive to correct or gather, to something that could be use for training despite residual noise ( see : [Here]:(https://arxiv.org/abs/1406.2080) )


## Visualisation

Here is a visualisation of this problem after different iso map transformations to validate the process, by looking at the separability of our two clusters and get an intuition of what is happening.

![iso_map](https://user-images.githubusercontent.com/25333848/33291978-ecb897ca-d3c7-11e7-8336-2c58f86e10f9.gif)


## What could be improved

As of right now, the unsupurvised algorithms used are still limited as they are only clustering data, instead of true semi-supervised, that could use the noise data as something that is not looked for, and reuse information from  the user that deleted/moved wrong labels with the GUI.


