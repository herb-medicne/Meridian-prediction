#!/usr/bin/env Script
library(ranger)
library(lattice)
library(purrr)
library(tidyverse)
library(mgcv)
library('e1071')
library(caret)
library(nlme)
library(nycflights13)
library(car)
library(mlbench)
library('randomForest')

args = commandArgs(trailingOnly=TRUE)


#import data and data prepare it
filename_input_csv=args[5]
mydata<- read.csv(filename_input_csv, header =T,sep=',')
uniquedata2= uniquecombs(mydata)
uniquedata2[is.na(uniquedata2)] <- 0
#delete whose feature that all compounds is 'NA' 
a=colSums(uniquedata2)
combin <- data.frame(rbind(t(data.frame(a)),data.frame(uniquedata2)))
uniquedata2=combin[,which(a!=0)][-1,]
rownames(uniquedata2)=uniquedata2[,1]
uniquedata2=uniquedata2[,-1]

#training the model 
meridian1=function(data,organ,seednumber,methods)
{
  set.seed(seednumber)
  intrain = createDataPartition(y = organ[,1], p= 0.7, list = FALSE)
  training = data[intrain,]
  testing = data[-intrain,]
  databin=cbind(organ,data)
  trainingclass=databin[intrain,][,1]
  trainingclass=factor(trainingclass)
  testingclass=databin[-intrain,][,1]
  testingclass=factor(testingclass)
  
  
  # train model
  set.seed(3333)
  trctrl <- trainControl(method = "cv", number = 5)
  model_fit <- train (training, trainingclass, method = methods,trControl=trctrl, preProcess = c("center", "scale"),tuneLength = 10)
 model_fit
  parametertest=model_fit$result
  filename_paragrid=paste(names(organ),methods,'para.csv',sep='_')
  write.csv(parametertest,file= filename_paragrid)
  #Plot fit
  #filename_para=paste(names(organ),methods,'.png',sep='_')
  #png(filename_para)
  #plot(model_fit)
  #dev.off()
  
  ##SELELCT FEATURE
  importance <- varImp(model_fit, scale=FALSE)
  # summarize importance
  #print(importance)
  # plot importance
  filename_import_csv=paste(names(organ),methods,'import.csv',sep='_')
  write.csv(importance$importance,file=filename_import_csv)
  filename_import_png=paste(names(organ),methods,'import.png',sep='_')
  #png(filename=filename_import_png)
  #plot(importance,top=10)
  #dev.off()
  
  
  # KNN for Liver
 
 modelPredict = predict(model_fit, newdata = testing)
  a=confusionMatrix(modelPredict,testingclass,positive='1')
  tocsv = data.frame(cbind(t(a$overall),t(a$byClass)))
  k=c(seednumber,deparse(substitute(data)),methods,names(organ))
  names(k)=c('seed','data','method','organ')
  tocsv1=data.frame(cbind(t(k),tocsv))
  return(tocsv1)
}


###2.1 differente methods
meridian2=function(data,organ,seednumber,methodlist)
{
  m1=data.frame()
  for(methods in methodlist)
  {
    m=meridian1(data,organ,seednumber,methods)
    m1= data.frame(rbind(m1, m))
  }
  return(m1)
}


##3.1 differente organs

meridian3=function(data,organlist,seednumber,methodlist)
{
  r1=data.frame()
  for(organs in organlist)
  {
    r=meridian2(data,organs,seednumber,methodlist)
    r1= data.frame(rbind(r1, r))
  }
  return(r1)
}


##4.1 different seeds
meridian4=function(data,organlist,seedlist,methodlist)
{
  s1=data.frame()
  for(seeds in seedlist)
  {
    s=meridian3(data,organlist,seeds,methodlist)
    s1= data.frame(rbind(s1, s))
  }
  return(s1)
}


##5.1 different feature
meridian5=function(datalist,organlist,seedlist,methodlist,filename_pre_csv='')
{
  d1=data.frame()
  for(datas in datalist)
  {
    d=meridian4(datas,organlist,seedlist,methodlist)
    d1= data.frame(rbind(d1, d))
  }
  write.csv(d1,file=filename_pre_csv)
  return(d1)
}

ADMET=scale(select(uniquedata2,MW:SyntheticAccessibility))
Pubchem= select(uniquedata2,colnames(uniquedata2)[startsWith(colnames(uniquedata2),'PubchemFP')])
MACCS= select(uniquedata2,colnames(uniquedata2)[startsWith(colnames(uniquedata2),'MACCSFP')])
Sub = select(uniquedata2,colnames(uniquedata2)[startsWith(colnames(uniquedata2),'SubFP')])
Ext=select(uniquedata2,colnames(uniquedata2)[startsWith(colnames(uniquedata2),'ExtFP')])
ADMEText=scale(select(uniquedata2,MW:ExtFP1021))
FourFinger=scale(select(uniquedata2,ExtFP1:MACCSFP165))
ADMETFinger=scale(select(uniquedata2,MW:MACCSFP165))
allorgan=select(uniquedata2,Lung:Liver)

Liver=as.data.frame(uniquedata2$Liver)
Liver[Liver>1]='1'
names(Liver)='Liver'
Spleen=as.data.frame(uniquedata2$Spleen)
Spleen[Spleen>1]='1'
names(Spleen)='Spleen'
Lung=as.data.frame(uniquedata2$Lung)
names(Lung)='Lung'
Lung[Lung>1]='1'
Heart=as.data.frame(uniquedata2$Heart)
names(Heart)='Heart'
Heart[Heart>1]='1'
Kidney=as.data.frame(uniquedata2$Kidney)
names(Kidney)='Kidney'
Kidney[Kidney>1]='1'
LargeIntestine=as.data.frame(uniquedata2$LargeIntestine)
names(LargeIntestine)='LargeIntestine'
LargeIntestine[LargeIntestine>1]='1'
Stomach=as.data.frame(uniquedata2$Stomach)
names(Stomach)='Stomach'
Stomach[Stomach>1]='1'


datalistall=list(ADMET,Pubchem,MACCS,Sub,Ext,ADMEText,FourFinger,ADMETFinger)
methodlistall=c('knn','rf', 'svmLinear','rpart')
organlistall=list(Lung,Spleen,Stomach,Heart,Kidney,LargeIntestine,Liver)
methodlist=methodlistall[as.numeric(args[1])]
datalist=datalistall[as.numeric(args[2])]
seedlist=c(3333)
organlist=organlistall[as.numeric(args[3])]
filename_pre_csv=args[4]

meridian5(datalist,organlist,seedlist,methodlist,filename_pre_csv)
