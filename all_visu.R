#VISUALIZE PREDCTION RESULTS
library(ggplot2)
require(ggplot2)
require(grid)

# Multiple plot function
#
# ggplot objects can be passed in ..., or to plotlist (as a list of ggplot objects)
# - cols:   Number of columns in layout
# - layout: A matrix specifying the layout. If present, 'cols' is ignored.
#
# If the layout is something like matrix(c(1,2,3,3), nrow=2, byrow=TRUE),
# then plot 1 will go in the upper left, 2 will go in the upper right, and
# 3 will go all the way across the bottom.
#
multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  require(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}


testrfr1_prediction <- as.data.frame(read.table("/home/axel/Documents/Final_res/30_rfr_pred_10.csv", sep = "," ,header = FALSE))
testrfr2_prediction <- as.data.frame(read.table("/home/axel/Documents/Final_res/30_rfr_pred_50.csv", sep = "," ,header = FALSE))
testrfr3_prediction <- as.data.frame(read.table("/home/axel/Documents/Final_res/30_rfr_pred_100.csv", sep = "," ,header = FALSE))

testsvr1_prediction <- as.data.frame(read.table("/home/axel/Documents/Final_res/30_lin_pred.csv", sep = "," ,header = FALSE))
testsvr2_prediction <- as.data.frame(read.table("/home/axel/Documents/Final_res/30_poly_pred.csv", sep = "," ,header = FALSE))

testnnr1_prediction <- as.data.frame(read.table("/home/axel/Documents/Final_res/30_nnr_pred_100.csv", sep = "," ,header = FALSE))
testnnr2_prediction <- as.data.frame(read.table("/home/axel/Documents/Final_res/30_nnr_pred_200.csv", sep = "," ,header = FALSE))
testnnr3_prediction <- as.data.frame(read.table("/home/axel/Documents/Final_res/30_nnr_pred_300.csv", sep = "," ,header = FALSE))

test_real <- as.data.frame(read.table("/home/axel/Documents/DATASET/final_model_data/30_pred_val.csv", sep = "," ,header = FALSE))

all <- test_real
all <- cbind(all,testrfr1_prediction[,1])
all <- cbind(all,testrfr2_prediction[,1])
all <- cbind(all,testrfr3_prediction[,1])
all <- cbind(all,testsvr1_prediction[,1])
all <- cbind(all,testsvr2_prediction[,1])
all <- cbind(all,testnnr1_prediction[,1])
all <- cbind(all,testnnr2_prediction[,1])
all <- cbind(all,testnnr3_prediction[,1])


colnames(all) <- c('real','predRFR1','predRFR2','predRFR3','predSVR1','predSVR2','predNNR1','predNNR2','predNNR3')

# err = 0
# for(i in 1:length(all$real)){
#   err = err + abs((all$predSVR1[i] - all$real[i]))
# }
# 
# 
# err_m = err/length(all$real)
# err_m

rfr1 <- ggplot(all, aes(y=all$`real`, x=all$`predRFR1`))+
  geom_point()+
  geom_smooth()+labs(y="Real",x="RFR 1 Predictions")+
  ggtitle("Predictions vs Real rotations")

rfr2 <- ggplot(all, aes(y=all$`real`, x=all$`predRFR2`))+
  geom_point()+
  geom_smooth()+labs(y="Real",x="RFR 2 Predictions")+
  ggtitle("Predictions vs Real rotations")

rfr3 <- ggplot(all, aes(y=all$`real`, x=all$`predRFR3`))+
  geom_point()+
  geom_smooth()+labs(y="Real",x="RFR 3 Predictions")+
  ggtitle("Predictions vs Real rotations")

svr1 <- ggplot(all, aes(y=all$`real`, x=all$`predSVR1`))+
  geom_point()+
  geom_smooth()+labs(y="Real",x="Linear SVR Predictions")+
  ggtitle("Predictions vs Real rotations")

svr2 <- ggplot(all, aes(y=all$`real`, x=all$`predSVR2`))+
  geom_point()+
  geom_smooth()+labs(y="Real",x="Poly SVR Predictions")+
  ggtitle("Predictions vs Real rotations")

nnr1 <- ggplot(all, aes(y=all$`real`, x=all$`predNNR1`))+
  geom_point()+
  geom_smooth()+labs(y="Real",x="NNR 1 Predictions")+
  ggtitle("Predictions vs Real rotations")

nnr2 <- ggplot(all, aes(y=all$`real`, x=all$`predNNR2`))+
  geom_point()+
  geom_smooth()+labs(y="Real",x="NNR 2 Predictions")+
  ggtitle("Predictions vs Real rotations")

nnr3 <- ggplot(all, aes(y=all$`real`, x=all$`predNNR3`))+
  geom_point()+
  geom_smooth()+labs(y="Real",x="NNR 3 Predictions")+
  ggtitle("Predictions vs Real rotations")


# Nouvelle page
#grid.newpage()
# Créer la mise en page : nrow = 2, ncol = 2
pushViewport(viewport(layout = grid.layout(3, 3)))
# Une fonction pour definir une region dans la mise en page
define_region <- function(row, col){
  viewport(layout.pos.row = row, layout.pos.col = col)
} 

print(rfr1, vp = define_region(1, 1))
print(rfr2, vp = define_region(1, 2))
print(rfr3, vp = define_region(1, 3))
print(svr1, vp = define_region(2, 1))
print(svr2, vp = define_region(2, 2))
print(nnr1, vp = define_region(3, 1))
print(nnr2, vp = define_region(3, 2))
print(nnr3, vp = define_region(3, 3))


