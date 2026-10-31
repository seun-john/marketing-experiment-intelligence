import numpy as np
import pandas as pd
def scenario(effect,low,high,audience,email_cost,margin,value,operational=0):
    if not np.isfinite([effect,low,high,audience,email_cost,margin,value,operational]).all() or low>effect or high<effect: raise ValueError('Finite ordered estimates required')
    if min(audience,email_cost,value,operational)<0 or not 0<=margin<=1: raise ValueError('Invalid assumptions')
    cost=audience*email_cost+operational;unit=value*margin
    return pd.DataFrame([dict(scenario=s,incremental_conversions=audience*d,incremental_value=audience*d*value,campaign_cost=cost,net_contribution=audience*d*unit-cost,break_even_effect=cost/(audience*unit) if audience*unit else np.nan) for s,d in [('Conservative (CI lower)',low),('Expected (estimate)',effect),('Optimistic (CI upper)',high)]])
