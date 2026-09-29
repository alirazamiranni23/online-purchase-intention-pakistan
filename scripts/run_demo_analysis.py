from pathlib import Path
import json
import pandas as pd
import statsmodels.formula.api as smf

BASE=Path(__file__).resolve().parents[1]
DATA=BASE/'analysis_outputs/illustrative_250_responses.csv.gz'
OUT=BASE/'analysis_outputs'
NUMERIC=['perceived_risk','payment_trust','delivery_reliability','product_information','convenience','digital_interaction','perceived_value','purchase_intention']

df=pd.read_csv(DATA)
for c in NUMERIC:
    df[c]=pd.to_numeric(df[c],errors='coerce')

complete=df.dropna(subset=NUMERIC).copy()
model=smf.ols('purchase_intention ~ perceived_risk + payment_trust + delivery_reliability + product_information + convenience + digital_interaction + perceived_value',data=complete).fit(cov_type='HC3')

summary={
    'rows_total':int(len(df)),
    'complete_cases':int(len(complete)),
    'r_squared':float(model.rsquared),
    'adjusted_r_squared':float(model.rsquared_adj),
    'coefficients':{k:float(model.params[k]) for k in NUMERIC[:-1]},
    'p_values':{k:float(model.pvalues[k]) for k in NUMERIC[:-1]}
}
(OUT/'analysis_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
