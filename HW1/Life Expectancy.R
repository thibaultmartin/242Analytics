setwd("/Users/Thibault/Documents/Boulot/UC Berkeley/IEOR242/Material for students /Datasets/")
StateData <- read.csv("StateData.csv", header = TRUE, stringsAsFactors = FALSE)

#a) i) Scatterplot of the US
plot(StateData$Longitude,StateData$Latitude, pch='.', cex=5, xlab='Longitude',ylab='Latitude',main='Map of the states of the US')


#a) ii) Region with the highest graduation Average

av_high_school_region=aggregate(StateData$HighSchoolGrad~StateData$Region, FUN="mean")

colnames(av_high_school_region)=c('Region','HighSchoolGradMean')

#Returns Highest Mean
av_high_school_region[which.max(av_high_school_region$HighSchoolGradMean),]


#a) iii) Murder & Regions

boxplot(Murder~Region, data=StateData, main="Murder per Region", xlab="Region", ylab="Murder", cex.axis=0.8)



#b) i) Linear Model for Life expectancy
fit <- lm(LifeExp~Population+Income+Illiteracy+Murder+HighSchoolGrad+Frost+Area , data=StateData)
summary(fit)

#b) iii) Scatterplot of Life expectancy vs Income
plot(StateData$Income,StateData$LifeExp, pch='.', cex=7, main="Life Expectancy vs Income", xlab="Income", ylab="Life Expectancy", cex.axis=0.8)


#c)
fit1 <- lm(LifeExp~Population+Income+Illiteracy+Murder+HighSchoolGrad+Frost , data=StateData)
summary(fit1)

fit2 <- lm(LifeExp~Population+Income+Murder+HighSchoolGrad+Frost , data=StateData)
summary(fit2)

#The set we choose
fit3 <- lm(LifeExp~Population+Murder+HighSchoolGrad+Frost , data=StateData)
summary(fit3)

fit4 <- lm(LifeExp~Murder+HighSchoolGrad+Frost , data=StateData)
summary(fit4)

fit5 <- lm(LifeExp~Murder+HighSchoolGrad , data=StateData)
summary(fit5)


#c) Vector of predictions

predictions=predict(fit3, StateData[,-c(4)], type="response") 

StateData$Pred=predictions

#Prediction of minimum - actual minimum
StateData[which.min(StateData$Pred),]
StateData[which.min(StateData$LifeExp),]

#Prediction of maximum - actual maximum
StateData[which.max(StateData$Pred),]
StateData[which.max(StateData$LifeExp),]

state.name[1]
state.name[40]
state.name[47]
state.name[11]

#See how it compares with reality
plot(StateData$Pred,StateData$LifeExp, pch='.', cex=7, col="blue")
lines(StateData$LifeExp,StateData$LifeExp,col="green")
