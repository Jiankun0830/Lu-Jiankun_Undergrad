dd <- read.table( "./Output_Final_forR.csv", 
                  sep=",", 
                  header=TRUE)


library(rpart)


fit <- rpart(dd$FinalB ~  dd$number_of_exercises_done ,
             method="class", 
             data=dd,
             cp=0.01)

printcp(fit) # display the results 
plotcp(fit) # visualize cross-validation results 
summary(fit) # detailed summary of splits

plot(fit, uniform=TRUE, 
     main="Classification Tree for Exercises")
text(fit, use.n=TRUE, all=TRUE, cex=.8) 

post(fit, file = "tree2.ps", 
     title = "Classification Tree for Ecercises")

pfit<- prune(fit, cp=fit$cptable[which.min(fit$cptable[,"xerror"]),"CP"])


plot(pfit, uniform=TRUE, 
     main="Pruned Classification Tree for Exercises")
text(pfit, use.n=TRUE, all=TRUE, cex=.8)

post(fit, file = "tree3.ps", 
     title = "Classification Tree for Exercises")

