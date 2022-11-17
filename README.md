# synapse-analysis

ImageJ macros and python script for the assisted analysis of electron microscopy (EM) images from synapses. 

In imageJ:
1.	Install imageJ macros (Plugins > Macros > Install…)
2.	Open all EM images to be analyzed (ideally different conditions). Make sure that each image contains a proper file name. 
3.	Create a stack of all images. 
4.	Press the shortcut “s” once to randomly mix the order of images. 
5.	Note the pixel size or calculate the pixel size using the scale bar in the EM images.
6.	Remove the scale (Analyze > Set scale > Click to remove scale). Save the mixed stack. 
7.	Start with the analysis: 
      -	Use the freehand line tool to label the active zone membrane, press “n9” to save it in the ROI manager. 
      -	Use the straight line tool to label synaptic vesicles (“n1”) and docked synaptic vesicles (“n3”).
      -	Use the polygon selection or freehand selection tool to label endosome-like structures (“n6”).
      -	After labeling all structures, press the shortcut “p” to export the ROI manager information as a txt file.
      -	For reimporting a text file, use the shortcut “i”.
      -	With “7” and “8”, you may toggle between straight and freehand line.

In python: 
1.	Make sure that all txt files are saved in one folder. 
2.	Insert the pixel size of the EM images (nm/pixel) in line 14. 
3.	Add the path of the folder containing all txt files. 
4.	Run the script
5.	Note: every text file must contain a single active zone. 
