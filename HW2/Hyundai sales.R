setwd("/Users/Thibault/Documents/Boulot/UC Berkeley/IEOR242/Material for students /Datasets/")
CarData <- read.csv("Elantra.csv", header = TRUE, stringsAsFactors = FALSE)

train <- CarData[CarData$Year<2013,]
test <- CarData[CarData$Year>=2013,]

xtrain <- train[,-c(1:2)]

#a) without seasons
fit <- lm(ElantraSales~.,data=xtrain)
summary(fit)
#Model is clearly underfitting - RSquared of 0.3544, no significant variable

#b) with seasons
xtrain2 <- train[,-c(2)]
fit2 <- lm(ElantraSales~.,data=xtrain2)
summary(fit2)
#Does poorly because months are not categorical values

#c)i) Months as a factor value
xtrain3<- xtrain2
xtrain3$Month <- factor(xtrain3$Month)

#Prove that it is a categorical value - separates into different months
levels(xtrain3$Month)

fit3 <- lm(ElantraSales~.,data=xtrain3)
summary(fit3)

#c)ii)Predicting the sales
test$Month<-factor(test$Month)

predictions <-predict(fit3,test[,-c(2,3)],type="response")
print(predictions)

Rsquare=cor(predictions,test$ElantraSales)^2
print(Rsquare)
