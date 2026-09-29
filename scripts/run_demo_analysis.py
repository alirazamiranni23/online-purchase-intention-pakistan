from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
BASE=Path(__file__).resolve().parents[1]
DATA=BASE/'data/purchase_intention_data_demo.csv'
FIG=BASE/'figures'
ANA=BASE/'analysis'
NUMERIC=['perceived_risk','payment_trust','delivery_reliability','product_information','convenience','digital_interaction','perceived_value','purchase_intention']
df=pd.read_csv(DATA)
for c in NUMERIC: df[c]=pd.to_numeric(df[c],errors='coerce')
complete=df.dropna(subset=NUMERIC).copy()
corr=complete[NUMERIC].corr(method='spearman')
model=smf.ols('purchase_intention ~ perceived_risk + payment_trust + delivery_reliability',data=complete).fit(cov_type='HC3')
summary={'rows_total':int(len(df)),'complete_cases':int(len(complete)),'r_squared':float(model.rsquared),'coefficients':{k:float(model.params[k]) for k in ['perceived_risk','payment_trust','delivery_reliability']},'p_values':{k:float(model.pvalues[k]) for k in ['perceived_risk','payment_trust','delivery_reliability']}}
(ANA/'demo_results.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
