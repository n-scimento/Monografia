library('tidyverse')
library('readxl')
library('zoo')
library('ggplot2')
library('tseries')
library('forecast')
library('dplyr')
library('seasonal')
library('vars')
library('xts')
library("astsa")
library('lmtest')
library('FinTS')
library('urca')

df <- read_excel("data/database.xlsx")
df$Date <- as.Date(df$Date, format = "%Y-%m-%d")
df_xts <- xts(df[ , -which(names(df) == "Date")], order.by = df$Date)
# bring down last obs when Null and so I can have all the days

var_data <- df_xts[, c("beta1", "ipca-12", "selic_anual_1y")]
var_data_clean <- na.omit(var_data)

lag_selection <- VARselect(var_data_clean, lag.max = 12, type = "const")
print(lag_selection$selection)

# Como ele está escolhendo a decomposição de Cholesky?
# Como está o índice de tempo usado na série temporal que foi gerada?
# Entender exatamente o que a biblioteca VAR faz e quais parâmetros são possíveis de serem passados'

var_model <- VAR(var_data_clean, p = 2, type = "const")
summary(var_model)

causality(var_model, cause = "ipca-12")
causality(var_model, cause = "selic_anual_1y")
irf_result <- irf(var_model, impulse = c("ipca-12", "selic_anual_1y"), response = "beta1", boot = TRUE)
plot(irf_result)