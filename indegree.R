library(data.table)
library(ggplot2)
library(gtable)
library(grid)
require(scales)

setwd("~/Desktop/Python/consensus/Files")


df <- fread("indegree.csv")
#df <- fread("indegree_id1-264_rc8.csv")


min(df$degree)



# a <- table(df$avg_count)


plt <- ggplot(data = df, aes(x = degree, y = count)) + geom_point(shape = 1)+ #+ geom_smooth(method=lm, se=FALSE)+
  #ggtitle("in-degree distribution log-log")+
  #stat_smooth(method = 'nls', formula = 'y~a*x^b', method.args = list(start= c(a = 1,b=1)),se=FALSE) + #geom_text(x = 600, y = 1, label = power_eqn(DD), parse = TRUE)+
  #geom_smooth(formula=y~x)+
  scale_x_log10("in-degree", breaks = c(1, 10, 100, 1000, 10000, 100000, 1000000)) + scale_y_log10("number of nodes", breaks = c(1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000))+
  #theme(axis.text=element_text(size=12), axis.title = element_text(size=15))
  theme(plot.title = element_text(hjust = 0.5), panel.background = element_blank(), axis.text=element_text(size=25),axis.title =element_text(size=25),
        legend.position = "bottom", legend.text=element_text(size=13),axis.line = element_line(size = 1), axis.ticks.length = unit(0.2, "cm") , plot.margin=grid::unit(c(0.5, 0.5, 0.5, 0.5), "cm"))
  #theme(plot.title = element_text(hjust = 0.5), panel.background = element_blank(), axis.text=element_text(size=12),axis.title =element_text(size=12),
   #      legend.position = "bottom", legend.text=element_text(size=13),axis.line = element_line(size = 0.5), plot.margin=grid::unit(c(0.5, 0.5, 0.5, 0.5), "cm")) #, aspect.ratio = 0.7

  
  
  #scale_x_continuous("in-degree")+
  #scale_y_continuous("number of nodes")







plt
ggsave("indegree_dist.pdf", path = "/Users/Torben/Desktop/thesis/pictures")

dev.off()











