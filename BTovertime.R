library(ggplot2)
library(data.table)
library(gtable)
library(grid)
require(scales)
library(lubridate)


#install.packages("lubridate")
setwd("~/Desktop/Python/consensus/Files/")

df <- fread("BSovertime.csv")
mean(df[['IN']])
mean(df[['SCC']])
mean(df[['OUT']])
mean(df[['TEN']])
mean(df[['DIS']])

df[.N]
df

#colnames(df)[3] <- "IN"
df$date <- as.Date(df$date, "%Y-%m-%d")
str(df)
df[1:7]



p1 <- ggplot(data = df, aes(x = date, y = SCC, color = "SCC", group = 1)) +geom_smooth() +
  geom_smooth(data = df, aes(y = WCC, color = "WCC", group = 6)) + 
  geom_smooth(data = df, aes(y = IN, color = "IN", group = 2)) + 
  geom_smooth(data = df, aes(y = OUT, color = "OUT", group = 3)) +
  geom_smooth(data = df, aes(y = TEN, color = "Tendrils", group = 4)) +
  geom_smooth(data = df, aes(y = DIS, color = "Disconnected", group = 5))+
  
  geom_line(data = df, aes(y=SCC, color = "SCC", group = 1), alpha = 0.3)+
  geom_line(data = df, aes(y = WCC, color = "WCC", group = 6), alpha = 0.3) + 
  geom_line(data = df, aes(y = IN, color = "IN", group = 2), alpha = 0.3) + 
  geom_line(data = df, aes(y = OUT, color = "OUT", group = 3), alpha = 0.3) +
  geom_line(data = df, aes(y = TEN, color = "Tendrils", group = 4), alpha = 0.3) +
  geom_line(data = df, aes(y = DIS, color = "Disconnected", group = 5), alpha = 0.3)+
    
  scale_y_continuous("component size in %", limits = c(0,1))+
  scale_x_date('date',labels = date_format("%Y-%m"), breaks = date_breaks("years"))+
  #ggtitle("average network component sizes over time")+
  guides(color=guide_legend(override.aes=list(fill=NA)))+ #because smooth makes legend keys grey
  theme(plot.title = element_text(hjust = 0.5), panel.background = element_blank(), axis.text=element_text(size=12),axis.title =element_text(size=12),
        legend.position = "bottom", legend.text=element_text(size=13),axis.line = element_line(size = 0.5), plot.margin=grid::unit(c(0.5, 0.5, 0.5, 0.5), "cm"))+ #, aspect.ratio = 0.7
  
  scale_colour_manual("", breaks = c("SCC", "WCC", "IN", "OUT", "Tendrils", "Disconnected"), 
                      values = c("red", "aquamarine4",  "green", "blue", "orange2", "purple"))




p1
ggsave("Bowtie_over_time.pdf", width = 10, height = 7, path = "/Users/Torben/Desktop/thesis/pictures")
