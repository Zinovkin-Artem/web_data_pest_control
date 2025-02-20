from sql import value_from_db_for_cheklist as griz, value_from_db_grizuni_for_cheklist as griz_terr



def podshet_grizuni_v_dk(znach):
    _dic = {}
    mous_how = 0
    kris_how = 0


    count = 0
    
    for num in znach[0]:
        for i, j in znach[2][count].items():  
            if "M" in  j[0]:
                mous_how += int(j[0].split("-")[1])
            elif "K" in  j[0]:
                kris_how += int(j[0].split("-")[1])
                
            
        _dic[num]= mous_how, kris_how
        count+=1
        mous_how = 0
        kris_how = 0
        
    return _dic

def yes_or_not_grizuni(value_barier, mes, _year):
    data_akt_util = []
    for kay, value in value_barier.items():
        if value[0] > 0 or value[1] > 0:
            data_akt_util.append(f"№{kay}/{mes} від {kay}.{mes}.{_year}р")
        
    return data_akt_util

def grizuni_v_dk(_predpr, _mes, _year):
    bar_1 = griz(_mes, _year, "I - II", _predpr)
    bar_3 = griz(_mes, _year, "III", _predpr)
    

    a = podshet_grizuni_v_dk(bar_1)
    b = podshet_grizuni_v_dk(bar_3)
    

    c = yes_or_not_grizuni(a, _mes, _year)
    d = yes_or_not_grizuni(b, _mes, _year)
    g = c + [x for x in d if x not in c]
    
    return sorted(g)



def griz_na_ter_akt_util(predpr,month, year):
   
   _date_akti = []

   _ = griz_terr( _predpr = predpr, _month = month, _year = year)[0]
   for kay, value in _.items():
        if int(value.split(",")[0].split("-")[1]) > 0 or int(value.split(",")[1].split("-")[1]) > 0:
            _date_akti.append(f"№{kay}/{month} від {kay}.{month}.{year}р")

   return _date_akti

def stroka_dly_zvita(_predpr,_month, _year):
    c = grizuni_v_dk(_predpr,_month, _year)
    d = griz_na_ter_akt_util(_predpr,_month, _year)
    
    g = c + [x for x in d if x not in c]
    g = sorted(g)
    _g = ",; ".join(g)
    return _g
    


    
    

            


    
    






if __name__ == "__main__":
    print(stroka_dly_zvita("ТОВ 'М.В. КАРГО' СРВ",'07',"2024"))