#install.packages("data.table")
#install.packages("ggplot2")
library(data.table)
library(ggplot2)
library(gtable)
library(grid)
require(scales)
library(lubridate)

setwd("~/Desktop/Python/consensus/Files")


df <- fread("cliques-table.csv")
df$date <- as.Date(df$date, "%Y-%m-%d")
str(df)
max(df$max_c)
df
#df$number <- seq(1,78)

mean(df$max_c)
plt <- ggplot(data = df, aes(x = date, y = max_c)) + geom_line()+#alpha = 0.8
 # geom_smooth(data = df, aes(x = date, y = max_c))+
  geom_hline(yintercept = mean(df$max_c), color="blue")+
  #ggtitle("size biggest fully connected subgraph over time")+
  scale_x_date('date',labels = date_format("%Y-%m"))+
  scale_y_discrete("number of nodes in largest clique", limits = c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,10))+ 
  theme(axis.title =element_text(size=12),axis.text=element_text(size=12),axis.ticks.x=element_blank())+theme(plot.title = element_text(hjust = 0.5), panel.background = element_blank(), axis.text=element_text(size=12),axis.title =element_text(size=12),
                                                                                                              legend.position = "bottom", legend.text=element_text(size=13),axis.line = element_line(size = 0.5), plot.margin=grid::unit(c(0.5, 0.5, 0.5, 0.5), "cm")) #, aspect.ratio = 0.7

plt
ggsave("max_cliquesize_OT.pdf", width = 10, height = 5, path = "/Users/Torben/Desktop/thesis/pictures")
#ggsave("max_cliquesize_OT_smooth.pdf", width = 9, height = 7, path = "/Users/Torben/Desktop/thesis/pictures")
#ggsave("max_cliquesize_OT_smoothandline.pdf", width = 9, height = 7, path = "/Users/Torben/Desktop/thesis/pictures")
