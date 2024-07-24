## 24-06-27

## To-do

-   [ ] Organizar pastas
-   [ ] Instalar Git e fazer backup
-   [ ] Instalar bibliotecas Python
-   [ ] Instalar RStudio

------------------------------------------------------------------------

## 24-06-26

### Ideias

#### Qual o melhor método de interpolação?

-   Subtrai uma série de pontos de uma mesma região da curva de juros de um dado dia
-   Interpole a curva e meça qual interpolação chega mais próximo dos valores subtraídos
    -   Flat Forward
    -   NSS
    -   Spline
    -   Interpolação cúbica
-   Qual o melhor tipo de interpolação para curto-prazo? médio-prazo? longo-prazo?
-   **Base de dados:** 1990-2020
-   Metodologia: caso seja computacionalmente custoso, tentar usar Monte Carlo ou Random Forest

#### Como a curva de juros responde as expectativas de mercado?

1.  Construir base de dados de curva de juros
2.  Construir base de dados de expectativas de mercado através da API do BCB, colocando lag nas variáveis
    -   Expectativas para os próximos 12 meses
        -   Inflação
        -   Câmbio
        -   Juros
        -   Produto
    -   Expectativas para o ano fechado
3.  Estimar parâmetros para as curvas de juros
    -   O que fazer com o parâmetro que defino na mão?
        -   Estimar ótimo
4.  Estimar modelos ARIMA: como escolher o melhor para cada caso?
5.  Estimar IRF

### Drafts

#### Distribuição dos comprados e dos vendidos em contratos futuros (USD, IBOVESPA e DI)

-   Tese de livre docência do professor: para bolsa, comprado em IBOV futuro e vendido em IBVO futuro
-   Replicar para DI

#### DeLosso

Investidor que aluga ações mais acerta do que erra

Temos algo semelhante no investidor que opera a termo para se alavancar?

Vendido na ação; aplicado em renda fixa

Contrário: comprado na ação e dívida na renda fixa (operação a termo) - ele acha que a ação subirá muito; compra a termo, comprando além do que ele pod

Será que da mesma forma que o investidor de aluguel, o cara que faz termo também tem uma informação diferenciada em relação aos demais investidores?

Análise: verificar se as ações mais operadas a termo tem um desempenho futuro diferenciado em relação as outras

-   Baseado no DeLosso
