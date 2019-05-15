# Meridian-prediction

This is for Meridian ( Traditional Chinese Medicine conception) prediction by machining learning mothod.
Plant-derived nature products, known as herb formulas, have been commonly used in Traditional Chinese Medicine (TCM) for disease prevention and treatment. The herbs have been traditionally classified into different categories according to their targeting organs known as Meridians. Despite the increasing knowledge on the active components of the herbs, the rationale of Meridian classification remains poorly understood. In this study, we took a machine learning approach to explore the molecular basis of Meridian. We determined the molecule features for 848 herbs and their active components including fingerprints and ADME properties (absorption, distribution, metabolism and excretion).

We extracted the information of TCM herbs including the Meridian and the chemical components from the newly published database called TCMID, contained 17738 herb-compound pairs including 735 herbs and 9,586 compounds. The canonical SMILES representations for the compound structures were determined using Open Babel. We used the PaDEL-Descriptor software to obtain the fingerprints. We determined the ADME properties of the compounds using the database SwissADME, which provides physicochemical properties, pharmacokinetics, drug-likeness and medicinal chemistry friendliness of compounds. If you want to know more about how we prepare the dataset for ML models, please read article. 

Here, we share the code and data for model. It mainly include one script and three original dataset files, including Meridian_prediction.R, Compound_meridian_features.csv, herb_level_after_filteration.csv and herb_level_without _filteration.csv.

## 1.	Meridian_prediction.R 

There are five parameters needed when running the scrip. 

#### 1.1 ‘m’ ( Machining learning method )

    •	1 = 'knn'
    •	2 = 'rf'
    •	3 = 'svmLinear'
    •	4 = ‘rpart’
    
#### 1.2 ‘d’ ( Features we use )

    •	1 = ‘ADMET’
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
    
#### 1.4 ‘f’ ( Output file name for the model evaluation )

#### 1.5 ‘i’ ( Input file name )

    •	1 = 'herb_feature.csv'
    •	2 = 'herb_feature_adme_filter.csv'
    •	3 = 'compound_feature.csv'

## 2. compound_feature.csv

This is compound level of Meridian classification and features. Here, as the file is too big, we have compressed it to compound_feature.7z file. You can uncompree it to Compound_meridian_features.csv.

## 3. herb_feature_adme_filter.csv

This is herb level of Meridian classification and features. The feature are calculated by adding all related compounds with good properties together.

## 4. herb_feature.csv

This is herb level of Meridian classification and features. The feature are calculated by adding all related compounds together nomatter it is with good properties or not.

# Example

For example, we give the value of the five parameters:

    •	m='c(1,3)'
    •	d='c(1,2)'
    •	o='c(3,4)'
    •	f='knn_admeExt_Lung.csv'
    •	i=1
    
Then run it with your own R script, and give four arguments by $m $d $o $f $i. It means that we want to use kNN and SVM as machining learning methods, use ADME and PuChem as features to  predict Meridian Heart and Stomach in herb before_filteration level. Finally, we export the predict evaluation result 'knn_svm_ADME_PubChem_Stomach_Heart.csv'.

In R teminal, we run like, 

 Rscript meridian_predict_new.R $m $d $o $f $i

