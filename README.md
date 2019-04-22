# Meridian-prediction

This is for Meridian ( Traditional Chinese Medicine conception) prediction by machining learning mothod.
Plant-derived nature products, known as herb formulas, have been commonly used in Traditional Chinese Medicine (TCM) for disease prevention and treatment. The herbs have been traditionally classified into different categories according to their targeting organs known as Meridians. Despite the increasing knowledge on the active components of the herbs, the rationale of Meridian classification remains poorly understood. In this study, we took a machine learning approach to explore the molecular basis of Meridian. We determined the molecule features for 848 herbs and their active components including fingerprints and ADME properties (absorption, distribution, metabolism and excretion).

We extracted the information of TCM herbs including the Meridian and the chemical components from the newly published database called TCMID, contained 79,593 herb-compound pairs including 848 herbs and 9,586 compounds. The canonical SMILES representations for the compound structures were determined 113 using Open Babel. We used the PaDEL-Descriptor software to obtain the fingerprints. We determined the ADME properties of the compounds using the database SwissADME, which provides physicochemical properties, pharmacokinetics, drug-likeness and medicinal chemistry friendliness of compounds. If you want to know more about how we prepare the dataset for ML models, please read article: ??? 

Here, we share the ML code. It mainly include one script and three original dataset files, including Meridian_prediction.R, Compound_meridian_features.csv, herb_level_after_filteration.csv and herb_level_without _filteration.csv.

## 1.	Meridian_prediction.R 

There are five parameters needed when running the scrip. 

#### 1.1 ‘m’ ( Machining learning method )

    •	1 = 'knn'
    •	2 = 'rf'
    •	3 = 'svmLinear'
    •	4 = ‘rpart’
    
#### 1.2 ‘d’ ( Features we use )

    •	1 = ‘ADMET’
    •	2 = ‘Pubchem’
    •	3 = ‘MACCS’
    •	4 = ‘Sub’
    •	5 = ‘Ext’
    •	6 = ‘ADME+Ext’
    •	7 = ‘all the Four kind of Fingerprint’
    •	8 = ‘ADME and all Fingerprints’
    
#### 1.3 ‘o’ ( Meridian )

    •	1 = ‘Lung’
    •	2 = ‘Spleen’
    •	3 = ‘Stomach’
    •	4 = ‘Heart’
    •	5 = ‘Kidney’
    •	6 = ‘Larger Intestine’ 
    •	7 = ‘Liver’
    
#### 1.4 ‘f’ ( Output file name for the model evaluation )

#### 1.5 ‘i’ ( Input file name )

    •	1 = Compound_meridian_features.csv
    •	2 = herb_level_after_filteration.csv
    •	3 = herb_level_without_filteration.csv

## 2. Compound_meridian_features.csv

This is compound level of Meridian classification and features. Here, as the file is too big, we have compressed it to Compound_meridian_features.7z file. You can uncompree it to Compound_meridian_features.csv.

## 3. herb_level_after_filteration.csv

This is herb level of Meridian classification and features. The feature are calculated by adding all related compounds with good properties together.

## 4. herb_level_without _filteration.csv

This is herb level of Meridian classification and features. The feature are calculated by adding all related compounds together nomatter it is with good properties or not.

# Example

For example, we give the value of the five parameters:

    •	m=1
    •	d=6
    •	o=1
    •	f='knn_admeExt_Lung.csv'
    •	i=2
    
Then run it with your own R script, and give four arguments by $m $d $o $f $i. It means that we want to use KNN as machining learning method, use ADME and  Ext fingerprint combined together as features’ to  predict Meridian lung in herb after_filteration level. Finally, we export the predict evaluation result 'knn_admeExt_Lung.csv'.

In our sever, we run like, 

grun.py -n r_m"$m"_d"$d"_o"$o"_f"$f" -q hugemem.q -c "/apps/statistics2/R-3.4.3/bin/Rscript  Meridian_prediction.R $m $d $o $f $i.

