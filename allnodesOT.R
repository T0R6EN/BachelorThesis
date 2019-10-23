library(ggplot2)
library(data.table)
library(gtable)
library(grid)
require(scales)
library(lubridate)


#install.packages("lubridate")
setwd("~/Desktop/Python/consensus/Files/")

df <- fread("size_netOT.csv")

df[.N]

#colnames(df)[3] <- "IN"
df$date <- as.Date(df$date, "%Y-%m-%d")
str(df)

df
df = with(df, df[(date >= "2010-01-01"), ])
p1 <- ggplot(data = df, aes(x = date, y = size_net)) +geom_smooth() +
  scale_y_continuous("network size", breaks = scales::pretty_breaks(n = 5))+ #, limits = c(0,1), pretty(df$size_net, n = 10)
  scale_x_date('date',labels = date_format("%Y-%m"), breaks = date_breaks("years"))+
  #ggtitle("average network component sizes over time")+
 # guides(color=guide_legend(override.aes=list(fill=NA)))+ #because smooth makes legend keys grey
  theme(plot.title = element_text(hjust = 0.5), panel.background = element_blank(), axis.text=element_text(size=12),axis.title =element_text(size=12),
        legend.position = "bottom", legend.text=element_text(size=13),axis.line = element_line(size = 0.5), plot.margin=grid::unit(c(0.5, 0.5, 0.5, 0.5), "cm")) #, aspect.ratio = 0.7
  

p1
ggsave("NetSize.pdf", width = 10, height = 3.5, path = "/Users/Torben/Desktop/thesis/pictures")

