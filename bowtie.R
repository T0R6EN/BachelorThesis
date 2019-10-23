library(ggplot2)
library(data.table)
library(gtable)
library(grid)
require(scales)
# install.packages("scales")
setwd("~/Desktop/Python/consensus/Scripts/")
#df <- fread("bowtie280k-300k.csv")
#df <- fread("bowtie380k-400k.csv")
#df
#df <- fread("bowtie380k-400ktest.csv")
#df

#df <- fread("newtable380k-400k.csv")
#df
df <- fread("newtable280k-300k.csv")
df
# -------------- Plot --------------- #

p1 <- ggplot(data = df, aes(x = Segment, y = SCC, color = "SCC", group = 1)) +geom_line() +
  geom_line(data = df, aes(y = WCC, color = "WCC", group = 6)) + 
  geom_line(data = df, aes(y = IN, color = "IN", group = 2)) + 
  geom_line(data = df, aes(y = OUT, color = "OUT", group = 3)) +
  geom_line(data = df, aes(y = Tendrils, color = "Tendrils", group = 4)) +
  geom_line(data = df, aes(y = Disconnected, color = "Disconnected", group = 5))+
  scale_y_continuous("component size in %", limits = c(0,100))+
  scale_x_discrete("window size", limits = c("1b", "2b", "4b", "8b", "16b", "32b", "64b", "128b", "256b", "512b", "1024b", "2048b", "4096b", "8192b"))+ # , "16384b"
  #ggtitle("average network component sizes by window size")+
  theme(plot.title = element_text(hjust = 0.5), panel.background = element_blank(), axis.text=element_text(size=12),axis.title =element_text(size=12),
        legend.position = "bottom", legend.text=element_text(size=13),axis.line = element_line(size = 0.5), plot.margin=grid::unit(c(0.5, 0.5, 0.5, 0.5), "cm"))+ #, aspect.ratio = 0.7
  
  scale_colour_manual("", breaks = c("SCC", "WCC", "IN", "OUT", "Tendrils", "Disconnected"), 
                      values = c("red", "aquamarine4",  "green", "blue", "orange2", "purple"))


  
p1
ggsave("BowtieWindowSize.pdf", width = 10, height = 7, path = "/Users/Torben/Desktop/thesis/pictures")

p2 <- ggplot(data = df, aes(x =Segment, y = AbsSizeCore, color = "Abs Core size"))+ geom_point()+
  theme(plot.title = element_text(hjust = 0.5), panel.background = element_blank(),axis.text=element_text(size=12),axis.title =element_text(size=12),
        legend.position = "none",axis.line = element_line(size = 0.5), plot.margin=grid::unit(c(0.5, 0.5, 0.5, 0.5), "cm"))+
  scale_x_discrete("window size", limits = c("1b", "2b", "4b", "8b", "16b", "32b", "64b", "128b", "256b", "512b", "1024b","2048b", "4096b", "8192b"))+
  scale_y_continuous("number of nodes",labels = comma)+
  scale_colour_manual("", breaks = "Abs Core size", values = "black")
  
p2
ggsave("AbsSizeCore.pdf", width = 10, height = 5, path = "/Users/Torben/Desktop/thesis/pictures")

#grid.newpage()
#pushViewport(viewport(layout = grid.layout(2, 1)))
#print(p2, vp = viewport(layout.pos.row = 2, layout.pos.col=1))
#print(p1, vp = viewport(layout.pos.row = 1, layout.pos.col=1))


#ggsave("bowtie380k-400k.png", width = 9, height = 7, path = "/Users/Torben/Desktop/thesis/pictures") #, dpi = 300
# ggsave("bowtie280k-300k.png", width = 9, height = 7, path = "/Users/Torben/Desktop/thesis/pictures") #, dpi = 300





