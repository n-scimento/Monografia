#### Trabalho de Econometria III : Script

### Preliminares 

## Instalação de bibliotecas
install.packages('tidyverse')
install.packages('readxl')
install.packages('zoo')
install.packages('ggplot2')
install.packages('tseries')
install.packages('forecast')
install.packages('dplyr')
install.packages('seasonal')
install.packages('vars')
install.packages('xts')
install.packages("astsa")
install.packages('lmtest')
install.packages('FinTS')
install.packages('urca')

## Imporação de bibliotecas necessárias
library(forecast)
library(zoo)
library(tidyverse)
library(readxl)
library(dplyr)
library(ggplot2)
library(tseries)
library(seasonal)
library(vars)
library(xts)
library(astsa)
library(lmtest)
library(FinTS)
library(urca)

#%%# Parte 1 - Univariada

## Questão 1
# A série não apresenta duplos registros nem erros tipográficos, mas possui outliers.
# Métodos para identificação de outliers: gráfico da série, box-plot e tsoutliers().

# Leitura de dados
df <- read.csv("https://raw.githubusercontent.com/enricoruggieri/econometria/main/dados_trabalho_econometria.csv", row.names = 1, check.names = FALSE)

# Conversão para série temporal
ts.po <- ts(df['Pessoas ocupadas (mil)'], start = c(2012, 3), freq = 12)

# Renomeação de colunas para melhorar a legibilidade
colnames(df) <- c("pop", "pop_trab", "empreg", "desemp", "sal_min", "ipca", "ibc_br", "pmc", "focus", "pib", "usd_brl")


# Verificação de datas duplicadas
if (any(duplicated(rownames(df)))) {
  print("Existem datas duplicadas.")
  datas_duplicadas <- as.Date(rownames(df))[duplicated(rownames(df))]
  print("Datas duplicadas:")
  print(datas_duplicadas)
} else {
  print("Não existem datas duplicadas.")
}

# Identificação de outliers
tsoutliers(ts.po)
plot(ts.po, xlab = "Data", ylab = "Pessoas Ocupadas (mil)", main = "Ocupação - Brasil", col = "#7D9CC0", lty = 1, lwd = 2)
boxplot(ts.po)

# Remoção de outliers
ts.po.cl <- tsclean(ts.po)
ts.po.cl <- na.omit(ts.po.cl)
if (!is.ts(ts.po.cl)) {
  ts.po.cl <- ts(ts.po.cl, start = c(2012, 3), frequency = 12)
}

# Comparação de séries com e sem outliers
boxplot(ts.po.cl)
plot(ts.po.cl, xlab = "Data", ylab = "Pessoas Ocupadas (mil)", main = "Ocupação - Brasil", col = "#7D9CC0", lty = 1, lwd = 2)
lines(ts.po, col = "red", lty = 2, lwd = 2)
legend("bottomright", legend = c("Com Outliers", "Sem Outliers"), col = c("red", "#7D9CC0"), lty = c(1, 2), lwd = c(2, 2))

## Questão 2
# Decomposição da série temporal em componentes
plot(decompose(ts.po.cl, type = 'additive'))
plot(decompose(ts.po.cl, type = 'multiplicative'))

# Análise de autocorrelação e autocorrelação parcial
acf(ts.po.cl, 300)
pacf(ts.po.cl, 300, main = "Pessoas ocupadas")

## Questão 3

# Testes ADF para identificar a presença de raiz unitária na série
adf.drift <- ur.df(ts.po.cl, type = c("trend"), lags = 1, selectlags = "AIC")
print("ACF dos Resíduos")
acf(adf.drift@res, lag.max = 36)
print("ADF da série normal")
summary(ur.df(na.omit(ts.po.cl), type = "trend", lags = 8, selectlags = 'AIC'))
print("ADF da série em primeiras diferenças")
summary(ur.df(diff(na.omit(ts.po.cl)), type = "trend", lags = 8, selectlags = 'AIC'))
print("Plot da Série em primeiras diferenças")
plot(diff(ts.po.cl))
print("ACF e PACF da série em primeiras diferenças")
acf(diff(ts.po.cl, lag = 1), 300, main = 'Pessoas ocupadas, diferença sazonal (n = 4)')
pacf(diff(ts.po.cl, lag = 1), 300, main = 'Pessoas ocupadas, diferença sazonal (n = 4)')

# Testando série dessazonalizada
print("Série Dessazonalizada")
model_dessaz <- seas(ts.po.cl)
df_dessaz <- model_dessaz$data[,"seasonaladj"]
adf.drift <- ur.df(df_dessaz, type = c("trend"), lags = 1, selectlags = "AIC")
print("ACF dos Resíduos")
acf(adf.drift@res, lag.max = 36)
print("ADF da série dessazonalizada")
summary(ur.df(na.omit(df_dessaz), type = "trend", lags = 8, selectlags = 'AIC'))
print("ADF da série dessazonalizada em primeiras diferenças")
summary(ur.df(diff(df_dessaz), type = "trend", lags = 8, selectlags = 'AIC'))
print("ADF da série dessazonalizada em segunda diferenças")
summary(ur.df(diff(diff(df_dessaz)), type = "trend", lags = 8, selectlags = 'AIC'))
print("Plot dos resíduos da série dessazonalizada em segunda diferenças")
plot(ur.df(diff(diff(df_dessaz)), type = "trend", lags = 8, selectlags = 'AIC')@res)

## Questão 4

## Tentativa de encontrar modelos com erros homocedásticos não correlacionados
# Definição de intervalos para parâmetros p, d, q e parâmetros sazonais P, D, Q
p_range <- 0:3
d_range <- 0:3
q_range <- 0:3
P_range <- 0:3
D_range <- 0:3
Q_range <- 0:3

# Inicialização de Data Frame com resultados
results <- data.frame(
  model = character(),
  AIC = numeric(),
  BIC = numeric(),
  LjungBox_pvalue = numeric(),
  JarqueBera_pvalue = numeric(),
  ARCH_pvalue = numeric(),
  Erros_homocedasticos_nao_correlacionados = logical(),
  stringsAsFactors = FALSE
)

# Loop para todos os parâmetros de ARIMA/SARIMA 
for (p in p_range) {
  for (d in d_range) {
    for (q in q_range) {
      for (P in P_range) {
        for (D in D_range) {
          for (Q in Q_range) {
            # Fit do modelo
            model <- Arima(diff(ts.po.cl), order = c(p, d, q), seasonal = c(P, D, Q))
            
            # Estatísticas
            AIC <- AIC(model)
            BIC <- BIC(model)
            LjungBox <- Box.test(model$residuals, lag = 12, type = "Ljung-Box")
            JarqueBera <- jarque.bera.test(model$residuals)
            ARCH <- ArchTest(model$residuals)
            
            # Checa se erros são homocedásticos e não autocorrelacionados
            errors_ok <- LjungBox$p.value > 0.10 && ARCH$p.value > 0.10
            
            # Mapeamento no DataFrame
            results <- rbind(results, data.frame(
              model = paste("ARIMA(", p, ",", d, ",", q, ")", "SARIMA(", P, ",", D, ",", Q, ")", sep=""),
              AIC,
              BIC,
              LjungBox_pvalue = LjungBox$p.value,
              JarqueBera_pvalue = JarqueBera$p.value,
              ARCH_pvalue = ARCH$p.value,
              Erros_homocedasticos_nao_correlacionados = errors_ok
            ))
          }
        }
      }
    }
  }
}

# Modelos válidos segundo critério de homocedasticidade e não autocorrelação
valid_models <- results[results$Erros_homocedasticos_nao_correlacionados, ]
print(valid_models) # Não há modelos com erros homocedásticos e não autocorrelacionados, por conta da natureza dos dados (instabilidade em datas mais recentes)

# Dataframe com modelos
View(results)

# Seleção de modelos ARIMA para a série temporal
model <- auto.arima(diff(ts.po.cl), trace = TRUE, stepwise = TRUE, approximation = FALSE, ic = "bic")
model1 <- Arima(diff(ts.po.cl), c(2, 0, 0), seasonal = c(2, 0, 0)) ## Melhor segundo auto.arima
model2 <- Arima(diff(ts.po.cl), c(1, 0, 0), seasonal = c(1, 0, 0))
model3 <- Arima(diff(ts.po.cl), c(2, 0, 2), seasonal = c(2, 0, 1))

# Exibindo detalhes dos modelos
model
model1
model2
model3

## Questão 5
# Testes de Ljung-Box para verificar autocorrelação nos resíduos dos modelos ARIMA
ljung_box_test_model11 <- Box.test(model1$residuals, lag = 4, type = "Ljung-Box")
ljung_box_test_model12 <- Box.test(model1$residuals, lag = 12, type = "Ljung-Box")
ljung_box_test_model13 <- Box.test(model1$residuals, lag = 24, type = "Ljung-Box")

ljung_box_test_model21 <- Box.test(model2$residuals, lag = 4, type = "Ljung-Box")
ljung_box_test2_model22 <- Box.test(model2$residuals, lag = 12, type = "Ljung-Box")
ljung_box_test3_model23 <- Box.test(model2$residuals, lag = 24, type = "Ljung-Box")

ljung_box_test_model31 <- Box.test(model3$residuals, lag = 4, type = "Ljung-Box")
ljung_box_test2_model32 <- Box.test(model3$residuals, lag = 12, type = "Ljung-Box")
ljung_box_test3_model33 <- Box.test(model3$residuals, lag = 24, type = "Ljung-Box")

# Exibição dos resultados dos testes de Ljung-Box
ljung_box_test_model11
ljung_box_test_model12
ljung_box_test_model13

ljung_box_test_model21
ljung_box_test2_model22
ljung_box_test3_model23

ljung_box_test_model31
ljung_box_test2_model32
ljung_box_test3_model33

# Análise gráfica dos resíduos
acf(model1$residuals)
acf(model2$residuals)
acf(model3$residuals)

# Teste de Jarque-Bera para normalidade dos resíduos
jarque.bera.test(model1$residuals)
jarque.bera.test(model2$residuals)
jarque.bera.test(model3$residuals)

# Gráficos dos resíduos
plot(model1$residuals)
plot(model2$residuals)
plot(model3$residuals)

# Teste ARCH para verificar heterocedasticidade
ArchTest(model1$residuals)
ArchTest(model2$residuals)
ArchTest(model3$residuals)

## Questão 6

# Plots das projeções em horizonte de 24 meses, intervalo de 95%
plot(forecast(model1, h=24, level=95), main="Previsão - Modelo 1")
plot(forecast(model2, h=24, level=95), main="Previsão - Modelo 2")
plot(forecast(model3, h=24, level=95), main="Previsão - Modelo 3")

# Acurácia em treinamento
accuracy(model1)
accuracy(model2)
accuracy(model3)

## Questão 7

# Definindo os dados de treino e teste
train_data <- ts.po.cl[time(ts.po.cl) < c(2019,1)]
test_data <- ts.po.cl[time(ts.po.cl) >= c(2019,1) & time(ts.po.cl) <= c(2020,6)]

# Diferenciando os dados de treino e teste
diff_train_data <- diff(train_data)
diff_test_data <- diff(test_data)

# Modelo 1
model1 <- Arima(diff_train_data, c(2,0,0), seasonal=c(2,0,0))
fc_model1 <- forecast(model1, h=18, level=0.95)
accuracy(fc_model1$mean, diff_test_data)

# Modelo 2
model2 <- Arima(diff_train_data, c(1,0,0), seasonal=c(1,0,0))
fc_model2 <- forecast(model2, h=18, level=0.95)
accuracy(fc_model2$mean, diff_test_data)

# Modelo 3
model3 <- Arima(diff_train_data, c(2,0,2), seasonal=c(2,0,1))
fc_model3 <- forecast(model3, h=18, level=0.95)
accuracy(fc_model3$mean, diff_test_data)

## Questão 8

# Calculando RMSE fora da amostra para cada modelo
rmse_model1 <- accuracy(forecast(model1, h=length(diff_test_data)), diff_test_data)[2, 'RMSE']
rmse_model2 <- accuracy(forecast(model2, h=length(diff_test_data)), diff_test_data)[2, 'RMSE']
rmse_model3 <- accuracy(forecast(model3, h=length(diff_test_data)), diff_test_data)[2, 'RMSE']

# Imprimindo os RMSEs
cat("RMSE do Modelo 1: ", rmse_model1, "\n")
cat("RMSE do Modelo 2: ", rmse_model2, "\n")
cat("RMSE do Modelo 3: ", rmse_model3, "\n")

# Selecionar o modelo com menor RMSE
menor_rmse <- min(rmse_model1, rmse_model2, rmse_model3)
if (menor_rmse == rmse_model1) {
  modelo_selecionado <- model1
} else if (menor_rmse == rmse_model2) {
  modelo_selecionado <- model2
} else {
  modelo_selecionado <- model3
}

# Projeção para 2020 usando o modelo selecionado
projecao_2020 <- forecast(modelo_selecionado, h=12)
dados_reais_2020 <- ts.po.cl[time(ts.po.cl) >= 2020]

# Comparar projetado vs real (considerando a reversão da diferenciação)
comparacao <- data.frame(Real = dados_reais_2020, Projetado = cumsum(projecao_2020$mean) + tail(train_data, n=1))
comparacao$Diferenca <- comparacao$Real - comparacao$Projetado

# Calcular a perda real estimada (usando salário mínimo real)
salario_minimo_real <- df$sal_min[time(ts.po.cl) >= 2020]
comparacao$PerdaEstimada <- comparacao$Diferenca * salario_minimo_real

# Resultado final
perda_total_estimada <- sum(comparacao$PerdaEstimada, na.rm = TRUE)
print(paste("Perda real estimada devido à queda do número de ocupações em 2020: R$", abs(round(perda_total_estimada, 2))))

#%%#  Parte 2 - Multivariada

## Questão 1 - Preparação e Análise de Dados
df <- read.csv("https://raw.githubusercontent.com/enricoruggieri/econometria/main/dados_trabalho_econometria.csv", row.names = 1, check.names = FALSE)
colnames(df) <- c("pop", "pop_trab", "empreg", "desemp", "sal_min", "ipca", "ibc_br", "pmc", "focus", "pib", "usd_brl")
df_ts <- ts(df, frequency = 12, start = c(2012, 3), end = c(2020, 6)) # Transformando em série temporal

# Removendo outliers e aplicando dessazonalização
for (col_name in colnames(df_ts)) {
  df_ts[, col_name] <- tsclean(df_ts[, col_name]) # Limpeza de outliers
  
  for (col_name in colnames(df_ts)) {
    column <- df_ts[, col_name]
    deseasonalized <- seas(column)$data[,"final"] # Removendo sazonalidade
    df_ts[, col_name] <- deseasonalized
  }
  
  plot(df_ts[,"pop"]) # Gráfico da população
  adf.drift <- ur.df(df_ts[, "pop"], type = c("trend"), lags = 1, selectlags = "AIC") # Teste ADF
  acf(adf.drift@res, lag.max = 36) # Autocorrelação
  summary(ur.df(((diff(log(df_ts[, "pop"])))),type="trend",lags=1,selectlags='AIC')) # Resumo do teste ADF
  
  summary(ur.df((diff(log(df_ts[, "pop"]))),type="trend",lags=3,selectlags='AIC')) # Outro teste ADF
  
  summary(ur.df(diff(diff((df_ts[, "pop"]))),type="trend",lags=3,selectlags='AIC')) # Mais um teste ADF
  plot(diff(diff(log(df_ts[, "pop"])))) # Gráfico das diferenças
  df_ts[, "pop"] <- c(NA,diff((df_ts[, "pop"]))) # Diferenciação da série
  plot(df_ts[,'pop']) # Gráfico da série diferenciada
  # Escolha de 1 lag (mais parcimonioso) e I(1)
}

# Criação de variáveis taxa de emprego e desemprego
#df_ts[,"tx_empreg"] <- df_ts[,"empreg"]/df_ts[,"pop_trab"]
#df_ts[,"desemp"] <- df_ts[,"desemp"]/df_ts[,"pop_trab"] # utilizará para montar a taxa de empregados e desempregrados

## Questão 2
# Teste ADF para 'pop_trab'
adf.drift <- ur.df(df_ts[, "pop_trab"], type = c("trend"), lags = 3, selectlags = "AIC") 

# Autocorrelação para 'pop_trab'
acf(adf.drift@res, lag.max = 36) 

# Resumo do teste ADF para 'pop_trab'
summary(ur.df(diff(df_ts[, "pop_trab"]),type="trend",lags=3,selectlags='AIC')) 

# Gráfico das diferenças para 'pop_trab'
plot((diff(df_ts[,"pop_trab"]))) 

# Diferenciação da série 'pop_trab'
df_ts[,"pop_trab"] <- c(NA,diff((df_ts[,"pop_trab"]))) 
# escolha de 3 lags e I(1) para 'pop_trab'
plot(df_ts[,'pop'])
# Escolha de 1 lags(mais parcimonioso) e I(1)


adf.drift <- ur.df(df_ts[, "pop_trab"], type = c("trend"), lags = 3, selectlags = "AIC")

acf(adf.drift@res, lag.max = 36)
summary(ur.df(diff(df_ts[, "pop_trab"]),type="trend",lags=3,selectlags='AIC'))
plot((diff(df_ts[,"pop_trab"])))
df_ts[,"pop_trab"] <- c(NA,diff((df_ts[,"pop_trab"])))
# escolha de 3 lags e I(1)

# Variável empreg

plot(df_ts[,"empreg"])
adf.drift <- ur.df(df_ts[, "empreg"], type = c("drift"), lags =3, selectlags = "AIC")
acf(adf.drift@res, lag.max = 36)
summary(ur.df(diff(diff(log(df_ts[, "empreg"]))),type="drift",lags=2,selectlags='AIC'))
plot(diff(diff((df_ts[, "empreg"]))))
df_ts[,"empreg"] <- c(NA,NA,diff(diff(log(df_ts[,"empreg"]))))


# Variável desemp
plot(df_ts[,"desemp"])
adf.drift <- ur.df(na.omit(df_ts[, "desemp"]), type = c("trend"), lags = 8, selectlags = "AIC")
acf(adf.drift@res, lag.max = 36)
summary(ur.df(diff(diff(na.omit(df_ts[, "desemp"]))),type="trend",lags=8,selectlags='AIC'))
plot(diff(diff(df_ts[,"desemp"])))

df_ts[,"desemp"] <- c(NA,NA,diff(diff(log(df_ts[,"desemp"]))))

# Variável sal_min
plot(df_ts[,"sal_min"])
adf.drift <- ur.df(df_ts[, "sal_min"], type = c("drift"), lags = 5, selectlags = "AIC")
acf(adf.drift@res, lag.max = 36)
summary(ur.df((diff(df_ts[, "sal_min"])),type="drift",lags=5,selectlags='AIC'))
plot((diff(df_ts[,"sal_min"])))

df_ts[,'sal_min'] <- c(NA,diff(log(df_ts[,"sal_min"])))
# escolha de 5 lags e I(1)

# Variável IPCA
plot(df_ts[,"ipca"])
adf.drift <- ur.df(df_ts[, "ipca"], type = c("trend"), lags = 8, selectlags = "AIC")
acf(adf.drift@res, lag.max = 36)
summary(ur.df(((df_ts[, "ipca"])),type="trend",lags=8,selectlags='AIC'))
plot((df_ts[,"ipca"]))
# escolha de 8 lags e I(0) - serie estacionaria com trend

# Variável IBC
plot(df_ts[,"ibc_br"])
adf.drift <- ur.df(df_ts[, "ibc_br"], type = c("drift"), lags = 2, selectlags = "AIC")
acf(adf.drift@res, lag.max = 36)
summary(ur.df((diff(df_ts[, "ibc_br"])),type="drift",lags=2,selectlags='AIC'))
plot((diff(df_ts[,"ibc_br"])))

df_ts[,"ibc_br"] <- c(NA,diff(log(df_ts[,"ibc_br"])))
# escolha de 2 lags e I(1) - serie estacionaria com drift

# Variável pmc
plot(df_ts[,"pmc"])
adf.drift <- ur.df(df_ts[, "pmc"], type = c("drift"), lags = 4, selectlags = "AIC")
acf(adf.drift@res, lag.max = 36)
summary(ur.df((diff(df_ts[, "pmc"])),type="drift",lags=4,selectlags='AIC'))
plot((diff(df_ts[,"pmc"])))

df_ts[,"pmc"] <- c(NA,diff(log(df_ts[,"pmc"])))
# escolha de 4 lags e I(1) - serie estacionaria com drift

# Variável focus
plot(df_ts[,"focus"])
adf.drift <- ur.df(df_ts[, "focus"], type = c("trend"), lags = 2, selectlags = "AIC")
acf(adf.drift@res, lag.max = 36)
summary(ur.df((diff(df_ts[, "focus"])),type="trend",lags=2,selectlags='AIC'))
plot((diff(df_ts[,"focus"])))

df_ts[,"focus"] <- c(NA,diff(log(df_ts[,"focus"])))
# escolha de 2 lags e I(1) - serie estacionaria com trend

# Variável pib
plot(df_ts[,"pib"])
adf.drift <- ur.df(df_ts[, "pib"], type = c("trend"), lags = 2, selectlags = "AIC")
acf(adf.drift@res, lag.max = 36)
summary(ur.df((diff(df_ts[, "pib"])),type="trend",lags=2,selectlags='AIC'))
plot((diff(df_ts[,"pib"])))

df_ts[,"pib"] <- c(NA,diff(log(df_ts[,"pib"])))
# escolha de 2 lags e I(1) - serie estacionaria com trend

# Variável usd_brl
plot(df_ts[,"usd_brl"])
adf.drift <- ur.df(df_ts[, "usd_brl"], type = c("drift"), lags = 5, selectlags = "AIC")
acf(adf.drift@res, lag.max = 36)
summary(ur.df((diff(df_ts[, "usd_brl"])),type="drift",lags=5,selectlags='AIC'))
plot((diff(df_ts[,"usd_brl"])))

df_ts[,"usd_brl"] <- c(NA,diff(log(df_ts[,"usd_brl"])))
#df_ts[,"usd_brl"] <- ifelse(df_ts[,"usd_brl"] > 0, c(NA, diff(log(df_ts[,"usd_brl"]))), NA)
# escolha de 5 lags e I(1) - serie estacionaria com drift


# Teste com cada variável para testar a causalidade de granger
grangertest(empreg ~ usd_brl,data=as.data.frame(df_ts),order=2)
variables_X = c("ipca","focus","pib","usd_brl")

## Questão 3

# Sanitização da série 
df_ts <- df_ts[complete.cases(df_ts), ]
df_ts[is.infinite(df_ts)] <- NA
df_ts <- na.approx(df_ts)

# Seleção com VARselect
var_select <- VARselect(na.omit(df_ts[,c("empreg",variables_X)]), lag.max=12, type='both')
selection <- var_select$selection["SC(n)"]

model <- VAR(na.omit(df_ts[,c("empreg",variables_X)]),type = "both",p=2,season = 12) # p=1 or p=2

## Questão 4

# Estabilidade
roots(model) #Todos o lambdas (inversos das raízes características) são menores do que 1
# em módulo, o que indica a estabilidade

# Heterocedasticidade
arch.test(model,lags.multi = 2) # Podemos rejeitar a H0, então nosso modelo não apresenta heterocedasticidade # Mudo para 1 ou 2, depende do VAR

# Autocorrelação serial
serial.test(model,lags.pt=selection,type='BG') # Podemos rejeitar a H0, então nosso modelo não apresenta autocorrelação seria

# Plots de resíduos (Análise gráfica)
acf(residuals(model)[,1], main="Resíduos da taxa de empregados")
acf(residuals(model)[,2], main="Resíduos IPCA")
acf(residuals(model)[,3], main="Resíduos Expectativas de Inflação")
acf(residuals(model)[,4], main="Resíduos PIB")
acf(residuals(model)[,5], main="Resíduos taxa de câmbio efetiva")
# Podemos aceitar a H0, com 95%, que não temos autocorrelacao

# Testes de normalidade
normality.test(model,) # Rejeita H0 que os residuos são normais
e_empreg_d <- model$varresult$usd_brl$residuals
jarque.bera.test(e_empreg_d)
par(mfrow=c(2,2))                     # Resíduos da equação de produtividade
hist(e_empreg_d , freq=F, ylab='Densidade', xlab='Resíduos', main='Resíduos: Taxa de câmbio efetiva') # Testo para cada variável, resultados no artigo
# Por Jarque Bera rejeitamos a hipótese nula, reiterando a análise gráfica de que há certa assimetria, apesar da semelhança com normal

## Questões 5 e 6

### Função que extrai os dados de IRF() para plotar no ggplot
tsp.var.irf <- function(irf){
  
  if (class(irf) %in% "varirf") {
  } else{
    stop("Only 'varirf' class object from vars::irf()")
  }
  
  
  fortify <- function(data){
    result <- vector(mode = "list",length = 0L)
    for (d in 1:length(data)) {
      result[[length(result)+1]]<- tibble::tibble(imp = names(data)[d],
                                                  lag = 0:{nrow(data[[d]])-1},
                                                  tibble::as_tibble(data[[d]]))
    }
    data <- tidyr::unnest(tibble::tibble(result),cols = result)
    return(data)}
  
  data_irf <- fortify(irf$irf)
  data_lower <- fortify(irf$Lower)
  data_upper <- fortify(irf$Upper)
  suppressMessages(
    plot_data <- tibble::add_column(data_irf,type = "mean") %>%
      dplyr::full_join(tibble::add_column(data_lower,type = "lower")) %>%
      dplyr::full_join(tibble::add_column(data_upper,type = "upper")) %>%
      tidyr::pivot_longer(cols = -c(imp,lag,type)) %>%
      dplyr::mutate(imp = paste(imp),
                    name = paste(name)))
  
  plot <- ggplot2::ggplot(plot_data) +
    ggplot2::geom_line(ggplot2::aes(x = lag,value,
                                    lty = type),show.legend = F) +
    ggplot2::facet_grid(cols = ggplot2::vars(imp),
                        rows = ggplot2::vars(name),
                        scales = "free") +
    ggplot2::scale_linetype_manual(values = c("lower"=2,
                                              "upper"=2,
                                              "mean"=1)) +
    ggplot2::geom_hline(yintercept = 0,lty = 1) +
    ggplot2::scale_x_continuous(labels = as.integer) +
    ggplot2::labs(x="", y="") +
    ggplot2::theme_bw() +
    #ggplot2::theme(panel.spacing = unit(1, "lines")) +
    ggplot2::theme(strip.text.y = element_text(size = 6.5))+
    ggplot2::scale_color_manual(values = c(lower="red",
                                           upper="red",
                                           mean="black"))
  return(plot)
}

# IRF, 'empreg' como impulso
irf_diff_destx_emprego <- irf(model,
                              impulse = "empreg",
                              ortho = T, boot = T, n.ahead = 24,cumulative = T)

# Variância
tsp.var.irf(irf_diff_destx_emprego)

# Plot de IRF
plot(irf(model,impulse = "empreg",response="usd_brl",cumulative = T,ortho = T, boot = T,,n.ahead=24))

# Decomposição da variância, muda de acordo com modelo testado
fevd(model,n.ahead=24)$empreg*100 # Decomposição da variância, muda de acordo com modelo testado

# Teste insample
accuracy(model$varresult[[1]]) 

# Criando o datafacurame para salvar o forecast
mse_results <- data.frame(Time = integer(), MSE = numeric()) # Insample

# Teste / Out samplee
ows_predict <- length(df_ts[time(df_ts)<"2019-01-01","empreg"])
p=min(var_select$selection['SC(n)'])
train_data <- df_ts[1:82, c("empreg",variables_X)]
model <- VAR(ts(na.omit(train_data),frequency = 12), p = p)
fc_model <- predict(model, n.ahead = 18, ci = 0.95)
fc_prod_d.train <- fc_model$fcst[[1]][,"fcst"]
prod_d.test <- tail(df_ts[,'empreg'],18)
accuracy(fc_prod_d.train,prod_d.test) # Out of sample

for (col_name in colnames(df_ts)) {
  if (col_name != "ipca"){
    column <- df_ts[,col_name]
    print(col_name)
    # Perform ADF test on the original data (in levels)
    adf_levels <- adf.test(na.omit(column))
    if (adf_levels$p.value > 0.05) {
      # Test  first difference
      column_diff1 <-  diff(na.omit(column))
      adf_levels <- adf.test(column_diff1)
      df_ts[,col_name] <- c(NA, column_diff1)
      print(paste("Variable:", col_name, "Test first difference", adf_levels$p.value))
    }
    if (adf_levels$p.value > 0.05) {
      column_diff2 <-  diff(na.omit(log(column)))
      adf_levels <- adf.test(column_diff2)
      df_ts[,col_name] <- c(NA, column_diff2)
      print(paste("Variable:", col_name, "Test difference log", adf_levels$p.value))
    }
    if (adf_levels$p.value > 0.05) {
      column_diff3 <-  diff(diff(na.omit(log(column))))
      adf_levels <- adf.test(column_diff3)
      df_ts[,col_name] <- c(NA,NA, column_diff3)
      print(paste("Variable:", col_name, "Test second difference", adf_levels$p.value))
    }
  }
}

## Verificção de correlações
# Seleção das 5 séries mais correlacionadas com o y de interesse
# Seleciono a coluna "população ocupada" da matriz de correlação
cor_df <- cbind(df_ts[,"pop_trab"],stats::lag(df_ts[ , !(colnames(df_ts) == "pop_trab")]))
colnames(cor_df) <- c("pop_trab","pop","empreg","desemp","sal_min","ipca","ibc_br","pmc","focus","pib","usd_brl")

cor_matrix <- cor(na.omit(cor_df))
cor_matrix
# Seleciono a coluna "população ocupada" da matriz de correlação
cor_with_pop_trab <- cor_matrix[,"pop_trab"]

cor_with_pop_trab <-cor_with_pop_trab[-which(names(cor_with_pop_trab) == "pop_trab")]

top_3_correlations <- names(head(sort(abs(cor_with_pop_trab), decreasing = TRUE), 5))

print(top_3_correlations)

## Top 2 correlações

top_2_correlations <- names(head(sort(abs(cor_with_pop_trab), decreasing = TRUE), 2))

print(top_2_correlations)

# os Xs foram selecionados com base na matriz de correlação
var_select <- VARselect(na.omit(df_ts[,c("pop_trab",top_2_correlations)]),)
var_select$selection

model <- VAR(na.omit(df_ts[,c("pop_trab",top_2_correlations)]),p=min(var_select$selection['SC(n)']))

summary(model)

ts <- c(df_ts[,"sal_min"])
adf_result <- ur.df(na.omit(ts), type = "trend", lags = 4)
adf_result

# Teste de estabilidade
roots(model)
# todos acabam ficando dentro do circulo unitário, modelo é estável

# Teste de heterocedasticidade
arch.test(model) # Podemos rejeitar a H0, então nosso modelo não apresenta heterocedasticidade

# Teste de autocorrelação
serial.test(model) # Podemos aceitar a H0, com 95%, que não temos autocorrelacao

#teste de normalidade
normality.test(model) # Rejeito a H0 que os residuos são normais
plot(serial.test(model))
#Olhando o grafico e o teste tem diferenças

# Criando o dataframe para salvar o forecast
mse_results <- data.frame(Time = integer(), MSE = numeric())
p=min(var_select$selection['SC(n)'])

rows_predict <- length(df_ts[time(df_ts)<"2019-01-01","pop_trab"])

for (i in (rows_predict-1):(nrow(df_ts))) {
  # Subconjunto do dataframe para treinamento
  train_data <- df_ts[1:i, c("pop_trab", "pmc", "usd_brl", "ipca")]
  # Sanitização da série 
  train_data <- train_data[complete.cases(train_data), ]
  train_data[is.infinite(train_data)] <- NA
  train_data <- na.approx(train_data)
  
  # Ajuste do modelo VAR
  model <- VAR(ts(train_data,frequency = 12), p = p)
  
  # Faça previsões de múltiplos passos
  forecast <- predict(model, n.ahead = 1)
  
  # Avalie o desempenho da previsão (por exemplo, usando o erro quadrático médio)
  actual_values <- df_ts[i + 1, c("pop_trab", "pmc", "usd_brl", "ipca")]
  mse <- mean((forecast$fcst$pop_trab[,'fcst'] - actual_values["pop_trab"])^2)
  
  cat("MSE at time", i + 1, ":", mse, "\n")
  mse_results <- rbind(mse_results, data.frame(Time = i + 1, Forecast = forecast$fcst$pop_trab[,'fcst']))
  
}
df_final <- cbind(mse_results,df_ts[rows_predict:nrow(df_ts),"pop_trab"])

# Retornar para escala original(diff,SA)
#df_final <- (df_final*dp)+mean_ocupacao

View(df_final)
write.xlsx(df_final,"out_of_sample.xlsx")
