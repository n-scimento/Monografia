# VAR References
My goal in the research is to understand the impact of expectations in market moves and my try to forecast it, so, other variables doesn't really matter. The point is, given today focus, how should we position in short, medium and long term. That said, this is not a model, so I don't have to do any backtest or similar - I might do it to present later in work, but, to be fair, given that I'm working only with Brazil, it wouldn't be that useful.

- Inflação
- Juros
- Câmbio
- PIB

## For estimating


### Disagreement in Inflation Forecasts and Inflation Risk Premia in Brazil
- Filename: admin
- Source: http://orcid.org/0000-0003-1094-8551

**Paper muito bom para a análise qualitativa, a revisão de literatura pode ser muito útil**

> We first estimate the impact of inflation uncertainty on the inflation risk premia across different horizons using a VAR approach.

> In particular, we entertain two alternative specifications. The first considers a system with the inflation risk premia at different horizons (3, 6, 9, 12, 24 and 36 months) and dispersion in inflation expectations. The second model contemplates a lower-dimensional VAR in which we summarize the term structure of inflation risk premia by means of empirical proxies for the level, slope and curvature factors.

> We find that, increases in the dispersion of agents’ beliefs about future inflation result in a significantly positive response from longer-term inflation risk premia. Interestingly, such a shock leads mainly to parallel shifts in the term structure of inflation risk premia. We observe no significant effect on the slope and curvature factors.

> **Mariani (2015)** employs a Nelson-Siegel approach to estimate both the nominal and real yield curves and then assess the forecasting ability of the resulting breakeven inflation rates against the Focus Survey. He finds that they entail relatively better forecasting performance at the 6- and 12-month horizons.

> **Caldeira and Furlani (2014)** estimate Svensson’s (1994) model to fit the nominal and real yield curves. They show that the BEIRs predict better realized inflation than VAR models, but not as well as the Top 5 forecasters in the Focus Survey.

#### Reading

- Inflation expectations for 3, 6, 9, 12, 24 and 36 months ahead 

- Akaike, Hannan-Quinn and Schwartz to decide lag (5, 3 and 2) - can I use different lags?

- Test for residual autocorrelations with LM test

- Uses a Cholesky Decomposition

- Granger Casuality Test: non-Gaussian identification strategy in Lanne et al. (2016); 

- Pesaran and Shin's IRFs do not depend on VAR ordering

---

### Análise dos determinantes macroeconômicos da relação entre inflação implícita e prêmio de inflação no Brasil
- Filename: dissertacao_thiago
- Source: http://hdl.handle.net/10438/20369)

**Tem todas as tabelas com os testes no final, ótimo**

> As curvas foram construídas a partir dos valores de mercado dos títulos públicos e metodologia usada pela ANBIMA a partir do modelo de Svensson (1994), a partir da qual foi calculada uma curva de inflações implícitas de onde se obtiveram os prêmios de inflação em relação à mediana das projeções de inflação do relatório de expectativas de mercado do Banco Central do Brasil (Relatório FOCUS) [...] onde foi possível a construção de uma base histórica que seria utilizada para a criação de simulações VAR para se estabelecer as relações das inflações implícitas e prêmios de inflação com as demais variáveis de mercado escolhidas
    - apenas mais um exemplo, não parece utilizar as variáveis de expe tativa

> O modelo VAR (Vector Autoregressive Model) é uma generalização do modelo autoregressivo univariado, permitindo a relação intertemporal entre mais de uma variável, sem prévio conhecimento sobre suas endogeneidades.


> Através dos modelos, analisaremos as respostas geradas pelos impulsos das variáveis taxa Selic, juros nominais, taxa de câmbio e CDS Brasil sobre as inflações implícitas e seus prêmios para cada vértice escolhido, com o objetivo de identificar as variáveis que possuem maior impacto nas precificações das inflações implícitas pelo mercado, para horizontes mais longos e mais curtos.

- Estacionaridade via ADF: precisou colocar em primeira diferente

- Defasagem: de sempre

- **Ordenamento das variáveis**: ordenado pela ordem decrescente de exogeneidade definido pelo teste de Granger; verificar a endogeneidade do modelo utilizado por ele e citar no meu trabalho

---

### Central bank’s perception on inflation and inflation expectations of experts

- File name: montes2015
- Source: doi/10.1108/jes-07-2014-0116

> The empirical analysis uses ordinary least squares, the generalized method of moments and vector-autoregressive through impulse-response analysis [...] The findings suggest that the expectations of financial market experts react according to the content of the information provided by the central bank, i.e., announcements cause deterioration of expectations in times of instability, and reduce inflation expectations when inflation is controlled. 
 
#### Reading

- Variables used: inflation expectations (monthly)

- **ADOPT GENERALIZED IRF**: "The generalized impulse-response function as a manner of eliminating the problem of the ordering of variables in the VAR. The main argument is that the generalized impulse responses are invariant to any re-ordering of the variables in the VAR [...] Thus, aiming at eliminating the known problem in the results caused by the order of variables in the VAR, the generalized impulse-response function is adopted." (p. 1552)

- **SIC (Schwarz Information Criterion)**: used to decide lag order, **1 lag**.

##### General advices
- "inflation expectations are positively affected by [...] expectations (statistical significance was not found in the VAR);" (p.1552)
- ON OLS AND GMM ANALYSIS: "The lags of the variables were determined empirically, following the general-to-specific method, observing the statistical significance of the coefficients and the principle of parsimony (Hendry, 2001)" (p. 1149)
- ON OLS AND GMM ANALYSIS: "Thus, when inflation in the past period increases, inflation expectations also increase." (p. 1149)

---

### Inflação, desemprego e choques cambiais: estimativas VAR par aa economia brasileira
- File name: juliaangst
- Source: https://doi.org/10.22456/2176-5456.57948)

> "[...]e as expectativas foram obtidas do boletim Focus do Banco Central do Brasil"

- Verificar como foi estimado o VAR para as expectativas de inflação!

#### Reading

- "Porém, as simulações consideram inovações ortogonais (ϵt) e não os erros de previsão (υt)" (p. 308)
    - Entender diferença, aparentemente está relacionada ao IRF generalizado
    - "Isso nada mais é do que a fatoração de Cholesky aplicada na matriz de covariância dos erros" (p. 308) ué.
    - "O ordenamento é feito da variável mais exógena para a mais endógena" (p. idem)

- Também usa critério de Schwarz com **uma defasagem** (frequência mensal provavelmente).

- Usa **constante** e **tendência** e **dummies de sazonalidade** - como determinar estes?
    - Tendência: justificada pela trajetória de queda da taxa de desemprego durante grande parte do período.
    - Sazonalidade: justificada economicamente pelos autores - talvez apareçam em expectativas de PIB, mas o tratamento via dummy não parece tão adequado.
    
- **Autocorrelação**: testes Breusch-Godfrey e Portmanteau (p. 310)

- **Normalidade dos erros** (para estimação das IFRs via máxima verossimilhança): Doornik-Hansen e Lutkepohl

##### Resultados
- Choque cambial afeta todas as outras variáveis contemporaneamente, mas apresenta pouca persistência
- Para as outras variáveis o efeito só é estatisticamente significante em alguns momentos

---

### Modelos macro-financeiros com o uso de fatores latentes do tipo Nelson-Siegel
- Filename: LucasAMariani
- Source: https://doi.org/10.11606/D.96.2015.tde-07042015-141933

#### Reading
> Usando o critério de informação de Schwarz vemos que tanto para os modelos completos e como para os restritos sem algumas variáveis endógenas, em geral, o modelo com uma defasagem é es- colhido. Apesar de outros testes indicarem mais defasagens para as variáveis endógenas escolhemos essa especificação pois ela é mais parcimoniosa e deve gerar previsões fora da amostra melhores.

- Fica calculando erro quadrado médio repetidamente para encontrar o modelo mais parcimonioso - o que não é necessariamente o objetivo de um VAR
---

### Inflação implícita e o prêmio pelo risco: uma alternativa aos modelos VAR na previsão para o IPCA
- Filename: Fulraninflacao
- Source: https://doi.org/10.1590/S0101-41612013000400001

É um bom estudo para comparar com meus resultados, mas nenhum VAR é efetivamente estimado. 

> O presente artigo avalia, para o caso brasileiro, se a inflação implícita extraída dos títulos de renda fixa constitui um estimador não viesado da inflação ao consumidor, medida pelo IPCA.

> As previsões realizadas com as BEIRs mostraram maior acurácia que aquelas extraídas dos modelos VAR, porém, menos precisas que as geradas pelos Top5

> o Banco Central do Brasil, assim como grande parte de seus pares internacionais, utiliza em larga escala os modelos VAR para análise e previsão de inflação [...] Além disso, os modelos VAR impõem
poucas restrições à estrutura da economia. Estas escolhas se resumem, basicamente, à escolha das variáveis e das defasagens. Todo o resto é determinado pelo próprio modelo. Esta é uma característica desejável em um tipo de exercício como o proposto nesta seção, pois reduz o grau de subjetividade da análise.

> Os modelos VAR do BCB, basicamente, estão divididos em dois grandes grupos: modelos com fundamentação econômica e modelos puramente estatísticos
---



### What drives inflation expectations in Brazil? An empirical analysis
- Filename: cerisola
- Source: https://doi.org/10.1080/00036840601166892)

- A VEC (a specific VAR for non-stationary but cointegrated variables) is estimated and some procedures are alike 

#### Reading

---

### The credit channel and monetary transmission in Brazil and Chile: a structured VAR approach
- Filename: bcch
- Source: https://hdl.handle.net/20.500.12580/3879

- Discute bastante sobre o uso de VAR, não necessariamente no que preciso, mas me parece bem útil

#### Reading

---

### Vector autoregression model with long-term anchoring
- Filename: infrep
- Source: https://aprendervalor.bcb.gov.br/content/ri/inflationreport/201806/INFREP201806-ri201806b7i.pdf

> This box presents a VAR model that allows the anchoring of its long‑term projection in the expectations of Focus survey, thus incorporating important recent changes in the Brazilian economy."

#### Reading

---

### A Efetividade da Política Monetária sobre as Expectativas de Inflação do Brasil: um estudo após o regime de metas de inflação

- Filename: efetividade
- Source: https://www.portaldeperiodicos.idp.edu.br/redea/article/view/7100

> Modelos VAR são utilizados como ferramenta para esta investigação. Analisou-se a função impulso-resposta das expectativas aos choques na Selic e a decomposição da variância dos erros

---

## For literature review
- qin2010: Rise of VAR modelling approach (https://doi.org/10.1111/j.1467-6419.2010.00637.x)

- Empirical Findings on Inflation Expectations in Brazil: a survey: https://liftchallenge.bcb.gov.br/content/publicacoes/WorkingPaperSeries/wps464.pdf
- INFLATION EXPECTATIONS: A SYSTEMATIC LITERATURE REVIEW AND BIBLIOMETRIC ANALYSIS: https://www.scielo.br/j/rec/a/RCDs47sMMW7tHhh4LMWqcwF/?format=html&lang=en
