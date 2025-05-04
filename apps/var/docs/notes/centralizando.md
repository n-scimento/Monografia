# Centralizando Códigos

## Citations and VAR goals

> The goal is to find important interrelationship among the variables and not to make short term forecasts
- It might have several no significant coefficients - and be highly colinear
- Variables are added according to relevant economic meaning - Granger test helps wit hit tho
- Number of restrictions: $(n^{2}-n)/2s$
- VAR is a mechanical process

## Dont's
- No need to 'no feedback' since Y affects X and X affects Y on a VAR model
- No need to 'no contemporaneity'
- No differenciation on unity root - the says it, the classes didn't

## Should I?
- COVID dummy?


## Glossary
- **Philips-Perron Test**: useful for non-normal data or data with outliers it tests for unit root, autocorrelation and heteroskedasticity
- **Drift Term**: it's just the constant
- **Unit root**: a unit (or greater than one) parameter; not a problem for VAR (I think)
- **Log**: it stabilizes the variance
- **Box-Jenkins**: the test identifies if the variable affects the dependent variable with lag
- **Errors**: apperently they should be normal
- **SBC** (Schwarz-Bayesian-Criterion): it is used to compare two different models and select betweent the most parsimonious one (probably not so useful to VAR since we are not looking for it)
- **Granger Causality**: testes for how the predicitons of a variable are increased when adding another oneç
