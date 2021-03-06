setwd("/Users/Thibault/Documents/Boulot/UC Berkeley/IEOR242/Material for students /Datasets/")
ClimateData <- read.csv("ClimateChange.csv", header = TRUE, stringsAsFactors = FALSE)

#Splitting the data
train=ClimateData[ClimateData$Year<2007,]
test=ClimateData[ClimateData$Year>=2007,]

#QUESTION A
#Creating a linear model on training data
fit <- lm(Temp~MEI+CO2+CH4+N2O+CFC.11+CFC.12+TSI+Aerosols, data=train)
summary(fit)


#Showing correlation between variables
corr_matrix=cor(train[,-c(1,2,11)])
print(corr_matrix)

library(lattice)
new.palette=colorRampPalette(c("black","red","yellow","white"),space="rgb") 
levelplot(corr_matrix, col.regions=new.palette)

#QUESTION B
fit2 <- lm(Temp~MEI+N2O+TSI+Aerosols, data=train)
summary(fit2)

#Choose the best model according to AIC selection
#fit3 = step(fit)

#With the previous model
#pred_allvar <- predict(fit,test[,-c(1,2,11)], type="response")

predictions <- predict(fit2,test[,-c(1,2,11)], type="response")
summary(predictions)

#R_square
SSE = sum((test$Temp - predictions)^2)
#SSE = sum((test$Temp - pred_allvar)^2)
SST = sum((test$Temp - mean(train$Temp))^2)
print(1 - SSE/SST)

