#install.packages("data.table")
#install.packages("ggplot2")
library(data.table)
library(ggplot2)
library(gtable)
library(grid)
require(scales)
library(lubridate)

#setwd("~/Desktop/Python/consensus/Scripts")
setwd("~/Desktop/Python/consensus/Files")

df <- fread("avgClustering.csv")
df
#df$number <- seq(1,78)
df$date <- as.Date(df$date, "%Y-%m-%d")
df = with(df, df[(date >= "2015-01-01"), ])

mean(df$avg_clust)
plt <- ggplot(data = df, aes(x = date, y = avg_clust)) + geom_line()+
  geom_hline(yintercept = mean(df$avg_clust), color="blue")+
  #ggtitle("average clustering over time")+
  scale_x_date('date',labels = date_format("%Y-%m"), breaks = date_breaks("years"))+
  scale_y_continuous("average clustering", limits = c(0,0.25))+theme(plot.title = element_text(hjust = 0.5), panel.background = element_blank(), axis.text=element_text(size=12),axis.title =element_text(size=12),
                                                                    legend.position = "bottom", legend.text=element_text(size=13),axis.line = element_line(size = 0.5), plot.margin=grid::unit(c(0.5, 0.5, 0.5, 0.5), "cm")) #, aspect.ratio = 0.7
  
#+ theme(axis.title.x=element_blank(), axis.text.x=element_blank(),axis.ticks.x=element_blank())
plt
ggsave("avg_clustering.pdf", width = 10, height = 5, path = "/Users/Torben/Desktop/thesis/pictures") #, width = 9, height = 7
