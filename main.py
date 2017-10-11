import HelloAnalytics as HA
import functions as f

def main():
    view_Id = 'xx'
    data_Object = HA.init()
    data_Response = data_Object.get_sessions_30_days_total(view_Id)

    adw = f.sortAdwClicksSessions(data_Response)
    adw_Sessions = adw['adw_Sessions']
    adw_Clicks = adw['adw_Clicks']

    print("AdWords Clicks vs. Sessions for yesterday:")
    print("Sessions: ",adw_Sessions)
    print("Clicks: ",adw_Clicks)

if __name__ == "__main__":
    main()