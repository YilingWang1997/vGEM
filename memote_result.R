library(dplyr)
library(reshape2)
library(Hmisc)
library(data.table)
library(ggcorrplot)
library(igraph)
library(shapefiles)
library(ggbeeswarm)
library(tidyverse)
library(ggraph)
library(ggsci)
library(colorspace)
library(ggpubr)
soil_host <- read.csv("memote_soil_host_result.csv")
soil_virocell <- read.csv("memote_soil_virocell_result.csv")
paddy_host <- read.csv("memote_paddysoil_host_result.csv")
paddy_virocell <- read.csv("memote_paddysoil_virocell_result.csv")

soil_all <- rbind(soil_host,soil_virocell)
paddy_all <- rbind(paddy_host,paddy_virocell)

stoichiometric_consistency.df <- data.frame(table(paddy_all$test_stoichiometric_consistency))
ggplot(stoichiometric_consistency.df,aes(x="",y=Freq,fill=Var1))+
  geom_bar(stat="identity",width=1)+
  scale_fill_npg()+
  coord_polar("y",start=0)+
  theme_minimal()+
  theme(panel.grid = element_blank(),
        axis.title=element_blank(),
        axis.ticks=element_blank(),
        axis.text = element_blank(),
        legend.title = element_blank())

all <- rbind(data.frame(paddy_all,type=rep("Original",2714)),data.frame(soil_all,type=rep("Refined",2035)))

ggplot(all,
       aes(x = type, y = test_reaction_mass_balance, color = type)) +
  geom_boxplot(alpha = 1, outlier.colour = NA,
               draw_quantiles = .5,width=.4
  )+
  scale_y_continuous(limits = c(0,0.003))+
  theme_bw() + ylab("Proportion of reactions \nwith mass imbalance") + xlab("") +
  scale_color_npg()+
  theme(legend.position = "none",panel.grid = element_blank())
t.test(soil_all$test_reaction_mass_balance,paddy_all$test_reaction_mass_balance)


                   