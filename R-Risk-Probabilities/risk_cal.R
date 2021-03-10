library(survival)
library(mstate)
library("colorspace")


tmat <- transMat(x = list(c(2, 3, 4, 8), c(5,6,8), c(5,7,8), c(6,7,8),c(8),c(8),c(8),c()),
                 names = c("health", "IA", "IS", "DM", "IA+IS","IA+DM","IS+DM","death"))
cmdata <- read.csv("save_m_df.csv")

tmat

cmdata_30 <- subset(cmdata, tea_year=="4" & age_5g == "5")

mscm_30 <- msprep(time = c(NA, "IA_date", "IS_date","DM_date", "IA_IS_date","IA_DM_date","IS_DM_date","death_date"),
                  status = c(NA, "IA", "IS", "DM","IA_IS","IA_DM","IS_DM","is_death"),
                  data = cmdata_30 , trans = tmat,id=cmdata_30$THJID)
mscm_30[, c("Tstart", "Tstop", "time")] <- mscm_30[, c("Tstart","Tstop", "time")]/365.25
events(msf0_30)
write.csv(mscm_30, "tea_year_mscm.csv")

mscm <- read.csv("tea_year_mscm.csv")
mscm_30 <- subset(mscm, tag = 1)

c0_30 <- coxph(Surv(Tstart, Tstop, status) ~ strata(trans), data = mscm_30,method = "breslow")
msf0_30 <- msfit(object = c0_30, vartype = "aalen", trans = tmat)

## 画图
temp <- msf0_30$Haz
# temp_2 <- temp[which(temp$trans == 1 | temp$trans == 2 | temp$trans == 3 | temp$trans == 4),]
temp_1 <- temp[which(temp$trans == 1),]
temp_2 <- temp[which(temp$trans == 2),]
temp_3 <- temp[which(temp$trans == 3),]
temp_4 <- temp[which(temp$trans == 4),]
plot(x = temp_1$time, y = temp_1$Haz, type = 'l',
     col = "deepskyblue", lwd = 3,
     xlab = "Years", ylab = "Probability", main = "Probability through years")
lines(x = temp_2$time, y = temp_2$Haz, col = "DarkTurquoise", lwd = 3)
lines(x = temp_3$time, y = temp_3$Haz, col = "DeepPink", lwd = 3)
lines(x = temp_4$time, y = temp_4$Haz, col = "RosyBrown", lwd = 3)
legend("topleft", c("IA", "IS", "DM", "Death"),
       col = c("deepskyblue", "DarkTurquoise", "DeepPink", "RosyBrown"),
       lty = c(1,1,1,1), lwd = c(3, 3, 3, 3))


pt <- probtrans(msf0_30, predt = 0)

pt1_30 <- probtrans(msf0_30, predt = 0)[[1]]
pt2_30 <- probtrans(msf0_30, predt = 0)[[2]]
pt3_30 <- probtrans(msf0_30, predt = 0)[[3]]
pt4_30 <- probtrans(msf0_30, predt = 0)[[4]]
pt5_30 <- probtrans(msf0_30, predt = 0)[[5]]
pt6_30 <- probtrans(msf0_30, predt = 0)[[6]]
pt7_30 <- probtrans(msf0_30, predt = 0)[[7]]
pt8_30 <- probtrans(msf0_30, predt = 0)[[8]]

plot(x = pt1_30$time, y = pt1_30$pstate1 + pt1_30$pstate2 + pt1_30$pstate3 + pt1_30$pstate4 + pt1_30$pstate8, type = 'l',
     col = "deepskyblue", lwd = 3,
     xlab = "Years", ylab = "Probability", main = "Probability through years", ylim = c(0.00, 1.00))
lines(x = pt1_30$time, y = pt1_30$pstate2 + pt1_30$pstate3 + pt1_30$pstate4 + pt1_30$pstate8, col = "DarkTurquoise", lwd = 3)
lines(x = pt1_30$time, y = pt1_30$pstate3 + pt1_30$pstate4 + pt1_30$pstate8, col = "DeepPink", lwd = 3)
lines(x = pt1_30$time, y = pt1_30$pstate4 + pt1_30$pstate8, col = "RosyBrown", lwd = 3)
lines(x = pt1_30$time, y = pt1_30$pstate8, col = "red", lwd = 3)
legend("topright", c("Health", "IA", "IS", "DM", "Death"),
       col = c("deepskyblue", "DarkTurquoise", "DeepPink", "RosyBrown", "red"),
       lty = c(1,1,1,1,1), lwd = c(3, 3, 3, 3,3))


pt1_mean <- apply(pt1_30[,2:9], 2, mean, na.rm = T)
pt2_mean <- apply(pt2_30[,2:9], 2, mean, na.rm = T)
pt3_mean <- apply(pt3_30[,2:9], 2, mean, na.rm = T)
pt4_mean <- apply(pt4_30[,2:9], 2, mean, na.rm = T)
pt5_mean <- apply(pt5_30[,2:9], 2, mean, na.rm = T)
pt6_mean <- apply(pt6_30[,2:9], 2, mean, na.rm = T)
pt7_mean <- apply(pt7_30[,2:9], 2, mean, na.rm = T)
pt8_mean <- apply(pt8_30[,2:9], 2, mean, na.rm = T)

pt1_links = numeric()
pt2_links = numeric()
pt3_links = numeric()
pt4_links = numeric()
pt5_links = numeric()
pt6_links = numeric()
pt7_links = numeric()

# health -> IA health -> IS health->DM health->Death
pt1_links[c('Health -> IA', 'Health -> IS', 'Health -> DM', 'Health -> Death')] <- pt1_mean[c('pstate2', 'pstate3', 'pstate4', 'pstate8')]

# IA -> IA&IS IA -> IA&DM IA ->Death
pt2_links[c('IA -> IA & IS', 'IA -> IA & DM', 'IA -> Death')] <- pt2_mean[c('pstate5', 'pstate6', 'pstate8')]

# IS -> IA&IS IS -> IS&DM IS -> Death
pt3_links[c('IS -> IA & IS', 'IS -> IS & DM', 'IS -> Death')] <- pt3_mean[c('pstate5', 'pstate7', 'pstate8')]

# DM -> IA&DM DM -> IS&DM DM -> Death
pt4_links[c('DM -> IA & DM', 'DM -> IS & DM', 'DM -> Death')] <- pt4_mean[c('pstate6', 'pstate7', 'pstate8')]

# IA+IS -> Death
pt5_links['IA + IS -> Death'] <- pt5_mean['pstate8']

# IA+DM -> Death
pt6_links['IA + DM -> Death'] <- pt6_mean['pstate8']

# IS+DM -> Death
pt7_links['IS + DM -> Death'] <- pt7_mean['pstate8']

combine_links <- c(pt1_links, pt2_links, pt3_links, pt4_links
                   , pt5_links, pt6_links, pt7_links)

rm(pt1_links, pt2_links, pt3_links, pt4_links, pt5_links, pt6_links, pt7_links, combine_links)



transMat(x = list( c(2, 3), c(1, 3), c() ),
         names = c("Healthy", "Illness", "Death"))