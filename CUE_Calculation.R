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



virocell_sta <- read.csv("Soil_Virocell_GEM_sta.csv")
host_sta <- read.csv("Soil_Host_GEM_sta.csv")
virocell_sta$Organism <- gsub("_vi\\d+","",virocell_sta$Model)
host_sta$Organism <- gsub("_host","",host_sta$Model)
all_sta <- merge(host_sta,virocell_sta,by="Organism")
all_sta$Gene.Count.dif <- all_sta$Gene.Count.y-all_sta$Gene.Count.x
all_sta$Metabolite.Count.dif <- all_sta$Metabolite.Count.y-all_sta$Metabolite.Count.x
all_sta$Reaction.Count.dif <- all_sta$Reaction.Count.y-all_sta$Reaction.Count.x
all_sta$Product.Count.dif <- all_sta$Product.Count.y-all_sta$Product.Count.x
all_sta$Carbon.Exchange.Reactions.dif <-  all_sta$Carbon.Exchange.Reactions.y-all_sta$Carbon.Exchange.Reactions.x
all_sta$Nitrogen.Exchange.Reactions.dif <- all_sta$Nitrogen.Exchange.Reactions.y - all_sta$Nitrogen.Exchange.Reactions.x
all_sta_sta <- all_sta[,grep(".dif",colnames(all_sta))]
colnames(all_sta_sta) <- c("Gene Count","Metabolite Count","Reaction Count","Product Count","Carbon Exchange Reactions","Nitrogen Exchange Reactions")
all_sta_sta <- melt(all_sta_sta)
all_sta_sta<-all_sta_sta[all_sta_sta$value!=0,]
table(all_sta_sta$variable)
ggplot(all_sta_sta,
       aes(x = variable, y = value, color = variable)) +
  geom_boxplot(alpha = 1, outlier.colour = NA,
               draw_quantiles = .5
  )+#geom_beeswarm(size = .5, alpha = .2)+
  theme_bw() + ylab("The difference between \nvirocell and the host") + xlab("") +
  #scale_y_log10()+
  scale_color_npg()+
  scale_y_continuous(limits = c(-50,50))+
  theme(legend.position = "none", 
        
        panel.grid = element_blank(),
        #aspect.ratio = 8,
        axis.text.x = element_text(angle = -65,
                                   vjust = 0.5, 
                                   hjust = 0,
                                   size = 9),
        strip.text.x = element_text(size=9),
        strip.text.y = element_text(vjust = 0),
        strip.placement = "outside",
        strip.background.y = element_rect(fill = NA, color = NA))

#CUE results
virocell <- read.csv("Soil_Virocell_xml_results.csv")
host <- read.csv("Soil_Host_xml_results.csv")
virocell_cue <- virocell %>%
  group_by(Model) %>%
  mutate(mean_value = ifelse(any(CUE < 0), NA, mean(CUE))) %>%
  slice(1) %>%
  ungroup()
  
host_cue <- host %>% 
  group_by(Model) %>%
  mutate(mean_value = ifelse(any(CUE < 0), NA, mean(CUE))) %>%
  slice(1) %>%
  ungroup()

virocell_cue$Organism <- gsub("_vi\\d+","",virocell_cue$Model)
host_cue$Organism <- gsub("_host","",host_cue$Model)
all <- merge(host_cue,virocell_cue,by="Organism")
plot(x=all$CUE.x,y=all$CUE.y)+abline(a=0,b=1)
all <- all[all$CUE.x > 0,]
all <- all[all$CUE.y > 0,]
plot(x=all$CUE.x,y=all$CUE.y)+abline(a=0,b=1)
ggplot(all,aes(x=CUE.x,y=CUE.y))+geom_point(color="lightblue")+
  geom_abline(intercept = 0, slope = 1, color = "grey", linetype = "dashed")+
  theme_bw()+
  theme(legend.position = "none", 
        panel.grid = element_blank(),
        axis.text = element_text(size = 10)
        )+
  xlab("CUE of host GEMs")+
  ylab("CUE of virocell GEMs")
all$dif <- all$CUE.x-all$CUE.y
all.dif <- all[all$dif>0,]

#gas emission
virocell_gas <- read.csv("Soil_Virocell_gas_emission.csv")
host_gas <- read.csv("Soil_Host_gas_emission.csv")
virocell_gas$Organism <- gsub("_vi\\d+","",virocell_gas$Filename)
host_gas$Organism <- gsub("_host","",host_gas$Filename)


all_gas <- merge(host_gas,virocell_gas,by="Organism")
all_gas$co2_dif <- all_gas$EX_co2_e.y-all_gas$EX_co2_e.x
all_gas$ch4_dif <- all_gas$EX_ch4s_e.y-all_gas$EX_ch4s_e.x
all_gas$nh4_dif <- all_gas$EX_nh4_e.y-all_gas$EX_nh4_e.x
all_gas$no2_dif <- all_gas$EX_no2_e.y-all_gas$EX_no2_e.x
all_gas$no3_dif <- all_gas$EX_no3_e.y-all_gas$EX_no3_e.x
all_gas_sta <- all_gas[,grep("_dif",colnames(all_gas))]
colnames(all_gas_sta) <- c("CO2","CH4","NH4","NO2","NO3-")
all_gas_sta <- melt(all_gas_sta)
all_gas_sta<-all_gas_sta[all_gas_sta$value!=0,]
table(all_gas_sta$variable)
ggplot(all_gas_sta,
       aes(x = variable, y = value, color = variable)) +
  geom_boxplot(alpha = 1, outlier.colour = NA,
               draw_quantiles = .5
  )+geom_beeswarm(size = .5, alpha = .2)+
  theme_bw() + ylab("The difference between \nvirocell and the host") + xlab("") +
  #scale_y_log10()+
  scale_color_npg()+
  # scale_y_continuous(breaks = seq(0,5,1),
  #                   limits = c(1,4),
  #labels = expression(10^0,10^1,10^2,10^3,10^4,10^5)
  #                  )+
  theme(legend.position = "none", 
        
        panel.grid = element_blank(),
        #aspect.ratio = 8,
        axis.text.x = element_text(angle = -65,
                                   vjust = 0.5, 
                                   hjust = 0,
                                   size = 9),
        strip.text.x = element_text(size=9),
        strip.text.y = element_text(vjust = 0),
        strip.placement = "outside",
        strip.background.y = element_rect(fill = NA, color = NA))

dim(all_gas_sta[all_gas_sta$value>0 & all_gas_sta$variable=="CO2",])
dim(all_gas_sta[all_gas_sta$value<0 & all_gas_sta$variable=="CO2",])
dim(all_gas_sta[all_gas_sta$value>0 & all_gas_sta$variable=="CH4",])
dim(all_gas_sta[all_gas_sta$value<0 & all_gas_sta$variable=="CH4",])
dim(all_gas_sta[all_gas_sta$value>0 & all_gas_sta$variable=="NO2",])
dim(all_gas_sta[all_gas_sta$value<0 & all_gas_sta$variable=="NO2",])
dim(all_gas_sta[all_gas_sta$value>0 & all_gas_sta$variable=="NH4",])
dim(all_gas_sta[all_gas_sta$value<0 & all_gas_sta$variable=="NH4",])
dim(all_gas_sta[all_gas_sta$value>0 & all_gas_sta$variable=="NO3-",])
dim(all_gas_sta[all_gas_sta$value<0 & all_gas_sta$variable=="NO3-",])






