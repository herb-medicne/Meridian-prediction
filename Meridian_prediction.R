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

#import data and data preparation

inputfilename_list = c('herb_feature.csv', 'herb_feature_adme_filter.csv', 'compound_feature.csv')

filename = inputfilename_list[as.numeric(args[5])]
mydata = read.csv(filename)
rownames(mydata)=mydata[,1]
mydata = select(mydata,'LUNG':'SubFP307')
uniquedata2= uniquecombs(mydata)
uniquedata2[is.na(uniquedata2)] <- 0
a=colSums(uniquedata2)
uniquedata2=uniquedata2[,which(a!=0)]

#training the model 
meridian1=function(data,organ,seednumber,methods)
{
  datanames= names(data)
  data = as.data.frame(data)
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
  model_fit <- train (training, trainingclass, method = methods, trControl=trctrl, metric = 'Accuracy')
  model_fit
  #parametertest=model_fit$result
  #filename_paragrid=paste(names(organ),datanames,methods,'para.csv',sep='_')
  #write.csv(parametertest,file= filename_paragrid)
  #Plot fit
  #filename_para=paste(names(organ),methods,'.png',sep='_')
  #png(filename_para)
  #plot(model_fit)
  #dev.off()
  
  ##SELELCT FEATURE
  importance <- varImp(model_fit, scale=FALSE)
  # summarize importance
  # plot importance
  filename_import_csv=paste(names(organ),datanames,methods,'import.csv',sep='_')
  write.csv(importance$importance,file=filename_import_csv)
  #filename_import_png=paste(names(organ),methods,datanames,'import.png',sep='_')
  #png(filename=filename_import_png)
  #plot(importance,top=10)
  #dev.off()
  
  
  # predict the testing data
 
 modelPredict = predict(model_fit, newdata = testing)
  #a=confusionMatrix(modelPredict,testingclass,positive='one')
  a=confusionMatrix(modelPredict,testingclass,positive='1')
  tocsv = data.frame(cbind(t(a$overall),t(a$byClass)))
  k=c(seednumber,datanames,methods,names(organ))
  names(k)=c('seed','Feature_type','Method','Meridians')
  tocsv1=data.frame(cbind(t(k),tocsv))
  return(tocsv1)
}


###2.1 different methods
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


##3.1 different organs

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
  for(i in 1:length(datalist))
  {
    datas = datalist[i]
    names(datas)= names(datalist[i])
	  d=meridian4(datas,organlist,seedlist,methodlist)
    d1= data.frame(rbind(d1, d))
  }
  write.csv(d1,file=filename_pre_csv)
  return(d1)
}

col_scale = colnames(select(uniquedata2,'MW':'Synthetic.Accessibility'))
uniquedata2 = uniquedata2 %>% mutate_at(col_scale,funs(c(scale(.))))
ADME=select(uniquedata2,MW:Synthetic.Accessibility)
PubChem= select(uniquedata2,colnames(uniquedata2)[startsWith(colnames(uniquedata2),'PubchemFP')])
MACCS= select(uniquedata2,colnames(uniquedata2)[startsWith(colnames(uniquedata2),'MACCSFP')])
Sub = select(uniquedata2,colnames(uniquedata2)[startsWith(colnames(uniquedata2),'SubFP')])
Ext=select(uniquedata2,colnames(uniquedata2)[startsWith(colnames(uniquedata2),'ExtFP')])
ADME_Ext=select(uniquedata2,MW:ExtFP1021)
ADME_Ext=cbind(ADME,Ext)
FourFinger=cbind(PubChem,MACCS,Sub,Ext)
ADME_all=cbind(ADME,FourFinger)

LIVER=as.data.frame(uniquedata2$LIVER)
LIVER[LIVER>1]='1'
names(LIVER)='LIVER'
SPLEEN=as.data.frame(uniquedata2$SPLEEN)
SPLEEN[SPLEEN>1]='1'
names(SPLEEN)='SPLEEN'
LUNG=as.data.frame(uniquedata2$LUNG)
names(LUNG)='LUNG'
LUNG[LUNG>1]='1'
HEART=as.data.frame(uniquedata2$HEART)
names(HEART)='HEART'
HEART[HEART>1]='1'
KIDNEY=as.data.frame(uniquedata2$KIDNEY)
names(KIDNEY)='KIDNEY'
KIDNEY[KIDNEY>1]='1'
LARGE.INTESTINE=as.data.frame(uniquedata2$LARGE.INTESTINE)
names(LARGE.INTESTINE)='LARGE.INTESTINE'
LARGE.INTESTINE[LARGE.INTESTINE>1]='1'
STOMACH=as.data.frame(uniquedata2$STOMACH)
names(STOMACH)='STOMACH'
STOMACH[STOMACH>1]='1'


datalistall=list(ADME = as.data.frame(ADME),PubChem = as.data.frame(PubChem),MACCS = as.data.frame(MACCS),Sub = (Sub),Ext = as.data.frame(Ext) ,ADME_Ext = as.data.frame( ADME_Ext), ADME_all = as.data.frame(ADME_all))
methodlistall=c('knn','rf', 'svmLinear','rpart')
organlistall=list(LUNG,SPLEEN,STOMACH,HEART,KIDNEY,LARGE.INTESTINE,LIVER)
methodlist=methodlistall[as.vector(eval(parse(text=args[1])))]
#methodlist=methodlistall
#methodlist=methodlistall[as.numeric(args[2])]
datalist=datalistall[as.vector(eval(parse(text=args[2])))]
#datalist=datalistall
#datalist=datalistall[as.numeric(args[3])]
seedlist=c(3333)
organlist=organlistall[as.vector(eval(parse(text=args[3])))]
#organlist=organlistall[as.numeric(args[3])]
filename_pre_csv=args[4]

meridian5(datalist,organlist,seedlist,methodlist,filename_pre_csv)

