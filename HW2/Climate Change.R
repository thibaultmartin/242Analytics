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

library(lattice)
new.palette=colorRampPalette(c("black","red","yellow","white"),space="rgb") 
levelplot(corr_matrix, col.regions=new.palette)

#QUESTION B
fit2 <- lm(Temp~MEI+N2O+TSI+Aerosols, data=train)
summary(fit2)

#Choose the best model according to AIC selection
#fit3 = step(fit)

predictions <- predict(fit2,test[,-c(1,2,11)], type="response")
summary(predictions)

R_square<-cor(test[,"Temp"], predictions)^2
print(R_square)
# -> overfitting??


