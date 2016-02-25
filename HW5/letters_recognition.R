setwd("/Users/Thibault/Documents/Boulot/UC Berkeley/IEOR242/HW5/")
letters=read.csv(file="letters.csv")

#a)
letters$IsB=letters$Letter=='B'

set.seed(123)
sampsize=floor(0.5*nrow(letters))
samp_ind=sample(nrow(letters),size=sampsize,replace=F)
train=letters[samp_ind,]
test=letters[-samp_ind,]


#i) accuracy =75.42%
answer=rep(FALSE,nrow(test))
table(test$IsB,answer)
print(sum(test$IsB==answer)/length(answer))

library(rpart)
library(rpart.plot)
library(randomForest)

#ii) Building a CART
notB_tree=rpart(IsB~. ,data=train[,-1],method='class', minbucket=1,cp=0.01)
prp(notB_tree)
printcp(notB_tree)
plotcp(notB_tree)

#newtree=prune(notB_tree,cp=0.018)
#prp(newtree)
prediction=predict(notB_tree,newdata=test,type='class')
print(sum(test$IsB==prediction)/length(prediction))

#plotting the tree
prp(notB_tree)

#Validation
#set.seed(123)
#samp_ind2=sample.split(train$IsB,SplitRatio = 0.5)
#validatetrain=train[samp_ind2,]
#validatetest=train[!samp_ind2,]

accuracies=list()
range=1:50

for (i in range){
  notB_tree2=rpart(IsB~. ,data=validatetrain[,-c(1)],method='class',minbucket=i)
  prediction=predict(notB_tree2,newdata=validatetest,type="class")
  predddd=as.data.frame(prediction)
  lol=table(prediction,validatetest$IsB)
  print(lol)
  acc=sum(validatetest$IsB==prediction)/length(prediction)
  accuracies=c(accuracies,acc)
  }

plot(range,accuracies,type='l',main='Accuracies vs number of elements in buckets')



#RANDOM FOREST

train$IsB=as.factor(train$IsB)
test$IsB=as.factor(test$IsB) 

accuracies=list()
for (i in 1:10){
  notB_forest=randomForest(IsB~., data = train[,-c(1)], ntree=200, nodesize=i)
  prediction=predict(notB_forest,newdata=test,type="class")
  lol=table(prediction,test$IsB)
  print(lol)
  acc=sum(test$IsB==prediction)/length(prediction)
  accuracies=c(accuracies,acc)
}

accuracies=as.data.frame(accuracies)
print(accuracies[which.max(accuracies)])
plot(1:10,accuracies, type='l')

notB_forest_best=randomForest(IsB~., data = train[,-c(1)], ntree=200, nodesize=1)
predictions_forest=predict(notB_forest_best,test,type="class")
print(sum(test$IsB==predictions_forest)/length(predictions_forest))

#a)iv)accuracy is more important since there is nothing to interpret


#a)bis=> using logistic regression
fit=glm(IsB~.,data=train[,-1],family='binomial')
summary(fit)
fit=step(fit)

predictions_logistic=predict(fit,test,type="response")
table(test$IsB, predictions_logistic > 0.5)

#Creating the ROC curve
library(ROCR)
ROCRpred=prediction(predictions_logistic,test$IsB)
ROCCurve = performance(ROCRpred, "tpr", "fpr")
plot(ROCCurve, colorize=TRUE, print.cutoffs.at=seq(0,1,0.1), text.adj=c(-0.1,2))
as.numeric(performance(ROCRpred, "auc")@y.values)
print(sum(test$IsB==(as.data.frame(predictions_logistic)>0.5))/length(predictions_logistic))



#b)i) Baseline model
table(train$Letter)
which.max(table(train$Letter))
train$baseline='A'
test$baseline='A'

table(test$Letter,test$baseline)
print(sum(test$Letter==test$baseline)/length(test$baseline))

#b)ii)
tree=rpart(Letter~.,data=train[,-c(18,19)],method='class', cp=0.01)
printcp(tree)
plotcp(tree)

prp(tree)

#ATTENTION: METTRE "NEWDATA"
predictions_tree=predict(tree,newdata=test,type='class')
table(predictions_tree,test$Letter)

#plotting the confusion matrix
library(corrplot)
corrplot(matrix,is.corr=FALSE,method='number')

#Printing the accuracy - 85.75%
print(sum(test$Letter==predictions_tree)/length(predictions_tree))


#b)iii)
total_forest=randomForest(Letter~., data = train[,-c(18,19)], ntree=200, nodesize=10)
total_predictions_forest=predict(total_forest,test,type="class")
print(sum(test$Letter==total_predictions_forest)/length(total_predictions_forest))


print(table(test$Letter,total_predictions_forest))

#plotting the confusion matrix
library(corrplot)
corrplot(matrix,is.corr=FALSE,method='number')


#Using k-nearest neighbors
library(class)

set.seed(123)
sampsize=floor(0.5*nrow(letters))
samp_ind=sample(nrow(letters),size=sampsize,replace=F)
train=letters[samp_ind,]
test=letters[-samp_ind,]

#Printing results
predict_KNN=knn(train[,-1], test[,-1], cl=train$Letter, k = 1, l = 0, prob = FALSE, use.all = TRUE)
print(sum(test$Letter==predict_KNN)/length(predict_KNN))


matrix=table(test$Letter,predict_KNN)

#plotting the confusion matrix
library(corrplot)
print(matrix)
corrplot(matrix,is.corr=FALSE,method='number')



range=1:20
accuracies=list()
for (i in 1:20) {
  predict_KNN=knn(train[,-1], test[,-1], cl=train$Letter, k = i, l = 0, prob = FALSE, use.all = TRUE)
  acc=sum(test$Letter==predict_KNN)/length(predict_KNN)
  accuracies=c(accuracies,acc)
}
plot(range,accuracies,type='l',main="accuracies")

