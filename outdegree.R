library(data.table)
library(ggplot2)
library(gtable)
library(grid)
require(scales)

setwd("~/Desktop/Python/consensus/Files")


df <- fread("outdegree.csv")
min(df$degree)


plt <- ggplot(data = df, aes(x = degree, y = count)) + geom_point(shape = 1)+ #+ geom_smooth(method=lm, se=FALSE)+
 # ggtitle("out-degree distribution log-log")+
  scale_x_log10("out-degree", breaks = c(1, 10, 100, 1000, 10000, 100000, 1000000)) + scale_y_log10("number of nodes", breaks = c(1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000))+
  #theme(axis.text=element_text(size=12), axis.title = element_text(size=15))
  theme(plot.title = element_text(hjust = 0.5), panel.background = element_blank(), axis.text=element_text(size=25),axis.title =element_text(size=25),
         legend.position = "bottom", legend.text=element_text(size=13),axis.line = element_line(size = 1), axis.ticks.length = unit(0.2, "cm") , plot.margin=grid::unit(c(0.5, 0.5, 0.5, 0.5), "cm")) #, aspect.ratio = 0.7



#scale_x_continuous("in-degree")+
#scale_y_continuous("number of nodes")







plt
ggsave("outdegree_dist_max.pdf", path = "/Users/Torben/Desktop/thesis/pictures")

dev.off()














################################## old ############################
plt <- ggplot(data = df, aes(x = log10(degree), y = log10(avg_count))) + geom_point(shape = 1)+ 
  ggtitle("out-degree distribution")+
  scale_x_continuous("out-degree")+
  scale_y_continuous("number of nodes")




plt
ggsave("outdegree_dist.png", path = "/Users/Torben/Desktop/thesis/pictures")  
dev.off()
