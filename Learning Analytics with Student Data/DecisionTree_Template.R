#this is a template file to help you get familiar with the R code for generating decision trees 
#----------------------

#set working directory - the directory where you store the file 
setwd("C:/Users/TABLET0007/Desktop/Research/UROP Summer 2017")

#read the csv file 
#the first line of the csv file can 
dd <- read.table( "./Data/HomeworkProblemsWeek8AggregateDataWithClass2.csv", 
                  sep=",", 
                  header=TRUE)

#import the rpart library 
#you may need to install it. 
# on the right panel in R studio, select packages -> install 
library(rpart)

# grow tree 
# the format is  targetvariable ~ predictorvariable1 + predictorvariable2
# cp is the complexity parameter, 
# adjust this value up and down until you get a tree of 2 or 3 levels 
fit <- rpart(dd$category ~  dd$Wk.8.5_averagedaysfromstart ,
             method="class", 
             data=dd,
             cp=0.01)

printcp(fit) # display the results 
plotcp(fit) # visualize cross-validation results 
summary(fit) # detailed summary of splits

plot(fit, uniform=TRUE, 
     main="Classification Tree for HomeworkProblem")
text(fit, use.n=TRUE, all=TRUE, cex=.8) 

post(fit, file = "tree2.ps", 
     title = "Classification Tree for HomeworkProblem")

#at this stage the tree might have several levels, which makes it hard to read 
#the objective is to reduce it until 2 or 3 levels. 
#one method to achieve this is to increase the complexity parameter until you get a tree you want
#you can stop here if it works fine 

#another method you can explore is to pruning the tree
pfit<- prune(fit, cp=fit$cptable[which.min(fit$cptable[,"xerror"]),"CP"])

# plot the pruned tree 
plot(pfit, uniform=TRUE, 
     main="Pruned Classification Tree for HomeworkProblem")
text(pfit, use.n=TRUE, all=TRUE, cex=.8)

post(fit, file = "tree3.ps", 
     title = "Classification Tree for HomeworkProblem")
