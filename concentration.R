#install.packages("data.table")
#install.packages("ggplot2")
library(data.table)
library(ggplot2)
library(gtable)
library(grid)
require(scales)

setwd("~/Desktop/Python/consensus/Scripts")


df <- fread("concentration_id1-1500_rc1.csv")
df

max(df$concentration)


plt <- ggplot(data = df, aes(x = concentration, y = prob)) + geom_point(shape = 1)+
  scale_x_log10("log concentration") + 
  scale_y_log10("Log PDF")+
  ggtitle("probability density function of concentration index")

plt






ggsave("concentration_PDF.png", width = 9, height = 7, path = "/Users/Torben/Desktop/thesis/pictures")

dev.off()




