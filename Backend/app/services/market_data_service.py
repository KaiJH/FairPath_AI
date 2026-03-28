import pandas as pd
import os

class MarketDataService:
    def __init__(self, csv_path="/app/app/dataset/cleaned_jobs_nodescription.csv"):
        self.csv_path = csv_path
        # print(f"檔案完整路徑: {os.path.abspath(__file__)}")
        if os.path.exists(csv_path):
            self.df = pd.read_csv(csv_path)
            self.df['title_lower'] = self.df['title'].fillna('').str.lower()
        else:
            self.df = None
            print(f"Warning: Market data CSV not found at {csv_path}")
            
    def get_market_insights(self, target_job: str):
        print(f"[market] target job: {target_job}")
        if self.df is None or not target_job:
            return None
        
        filtered = self.df[self.df['title_lower'].str.contains(target_job.lower())]
        if filtered.empty:
            print("[market] filtered variable is empty")
            return {
                "total_jobs": 0,
                "visa_distribution": {},
                "require_sponsorship": 0,
                "opt_friendly": 0,
                "cpt_friendly": 0
            }
        
        print(f"[market] filtered: {filtered.head()}")
        
        visa_dist = filtered['visa_pathway'].value_counts().to_dict()
        
        sponsor_mask = filtered['visa_pathway'].str.contains('Sponsorship', case=False, na=False)
        sponsor_companies = filtered[sponsor_mask]['company_name'].nunique()
        
        cpt_mask = filtered['visa_pathway'].str.contains('CPT', case=False, na=False)
        cpt_companies = filtered[cpt_mask]['company_name'].nunique()
        
        opt_mask = filtered['visa_pathway'].str.contains('OPT', case=False, na=False)
        opt_companies = filtered[opt_mask]['company_name'].nunique()
        
        return_value = {
            "total_jobs": len(filtered),
            "visa_distribution": visa_dist,
            "require_sponsorship": sponsor_companies,
            "opt_friendly": opt_companies,
            "cpt_friendly": cpt_companies
        }
        
        print(f"[market] return value: {return_value}")
        
        return return_value
        
market_service = MarketDataService()