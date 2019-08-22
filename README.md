# Meridian-prediction

This is for Meridian (Traditional Chinese Medicine conception) prediction by machining learning method.
Plant-derived nature products, known as herb formulas, have been commonly used in Traditional Chinese Medicine (TCM) for disease prevention and treatment. The herbs have been traditionally classified into different categories according to their targeting organs known as Meridians. Despite the increasing knowledge on the active components of the herbs, Meridian classification remains poorly understood. In this study, we apply machine learning approach to explore the molecular basis of Meridian. We determined the molecule features for 646 herbs and their active components including fingerprints and ADME properties (absorption, distribution, metabolism and excretion).

We extracted TCM Meridian and chemical components from the newly published database TCMID (http://119.3.41.228/tcmid/ingredient/41001/). Finally, 18140 herb-compound pairs were collected, including 646 herbs and 10053 compounds. PaDEL-Descriptor software was used to calculate compound fingerprints. Compounds ADME properties were obtained from database SwissADME (http://www.swissadme.ch/index.php#top), which provides physicochemical properties, pharmacokinetics, drug-likeness and medicinal chemistry friendliness of compounds. 

This is how the machining learning model works. It mainly includes one script and three original dataset files, including Meridian_prediction.R, compound_feature.csv, herb_feature.csv and herb_feature_adme_filter.csv. The details about dataset preparation can be found in folder 'data process' above.

## 1.	Meridian_prediction.R 

There are five parameters needed when running the scrip. 

#### 1.1 ‘m’ ( Machining learning method )

    •	1 = 'knn'
    •	2 = 'rf'
    •	3 = 'svmLinear'
    •	4 = ‘rpart’
    •	5 = ‘nnet’
    
#### 1.2 ‘d’ ( Features we use )

    •	1 = ‘ADME’
    •	2 = ‘PubChem’
    •	3 = ‘MACCS’
    •	4 = ‘Sub’
    •	5 = ‘Ext’
    •	6 = ‘ADME+Ext’
    •	7 = ‘ADME and all Fingerprints’
    
#### 1.3 ‘o’ ( Meridian )

    •	1 = ‘LUNG’
    •	2 = ‘SPLEEN’
    •	3 = ‘STOMACH’
    •	4 = ‘HEART’
    •	5 = ‘KIDNEY’
    •	6 = ‘LARGE INTESTINE’ 
    •	7 = ‘LIVER’
    
#### 1.4 ‘f’ ( Output file name for model evaluation )

#### 1.5 ‘i’ ( Input file name )

    •	1 = 'herb_feature.csv'
    •	2 = 'herb_feature_adme_filter.csv'
    •	3 = 'compound_feature.csv'

## 2. herb_feature.csv

This is herb level of Meridian classification and features. The feature are calculated by adding all related compounds together than average the it. We inculde all the related compounds no matter it is with good properties or not.

## 3. herb_feature_adme_filter.csv

The file is herb level of Meridian classification and features. Feature are calculated by adding all related compounds with good properties together and than average it.

## 4. compound_feature.csv

This is compound level of Meridian classification and features. As the file is too big, we have compressed it to compound_feature.7z file. You can uncompree it to Compound_meridian_features.csv.



# Example

Firstly, decide which kind of model result you want to get. Then, give the corresponding number to five parameters. For example, here I use these parameter setting:

    •	m='c(1,3)'
    •	d='c(1,2)'
    •	o='c(3,4)'
    •	f='model_prediction_result_output.csv'
    •	i=1
    
Then run it with your own R script, and give five arguments by the order of  $m $d $o $f $i. It means that we want to use kNN and SVM as machining learning methods, use ADME and PuChem as features to predict Meridian Heart and Stomach in herb level without filtering. Finally, we export the predict evaluation result 'model_prediction_result_output.csv'.

In R teminal, we run like, 

Rscript Meridian_prediction.R $m $d $o $f $i

