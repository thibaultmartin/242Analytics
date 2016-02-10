setwd("/Users/Thibault/Documents/Boulot/UC Berkeley/IEOR242/Material for students /Datasets/")
Parole <- read.csv("Parole.csv", header = TRUE, stringsAsFactors = FALSE)

attach(Parole)

Count_violator= as.data.frame(table(Violator))
print(Count_violator)


#Test of table function...
print(table(Parole$Violator[Parole$Age>50]))
aggregate(Violator,by=list(State),FUN='sum')


#Creating a training and test set
smp_size <- floor(0.7 * nrow(Parole))

## set the seed to make your partition reproductible
set.seed(123)
train_ind <- sample(nrow(Parole),replace=F, size=smp_size)
train <- Parole[train_ind, ]
test <- Parole[-train_ind, ]

#Other method
#install.packages("caTools")
#library(caTools)
#spl = sample.split(Parole$Male, SplitRatio = 0.7)
#train <- Parole[spl, ]
#test <- Parole[-spl, ]


#Fitting a logistic model
fit=glm(Violator~.,data=train,family=binomial)
summary(fit)
test=coef(fit)
print(test)

glm.probs=predict(fit,test,type="response")
#glm.pred = rep(0, nrow(test))
#glm.pred[glm.probs > 0.5] = 1


# Produce a confusion matrix

table(test$Violator, glm.probs > 0.8)

#table(glm.pred, test$Violator)
#8.4% of false negative, 4.4% of false positive, total accuracy= 87.2%

glm.baseline=rep(0,nrow(test))
table(glm.baseline,test$Violator)
#Ratio of 22/203=10.8% 

#Lowering the threshold will reduce the number of "false negative"

#Computing the AUC
#install.packages('ROCR')
library(ROCR)

ROCRpred = prediction(glm.baseline, test$Violator)
#ROCRpred=prediction(glm.random,test$Violator)
ROCCurve = performance(ROCRpred, "tpr", "fpr")
plot(ROCCurve)
plot(ROCCurve, colorize=TRUE, print.cutoffs.at=seq(0,1,0.1), text.adj=c(-0.1,2))

#Computing the AUC
as.numeric(performance(ROCRpred, "auc")@y.values)

#Prediction accuracy of 86%
