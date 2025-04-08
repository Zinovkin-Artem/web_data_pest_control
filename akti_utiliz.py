from sql import value_from_db_for_cheklist as griz, value_from_db_grizuni_for_cheklist as griz_terr
import number_akti_in_zvit as naz
import xlsxwriter


class Akti_utiliz:


    def __init__(self, _predpr, _month, _year):

        self._predpr = _predpr
        self._month = _month
        self._year = _year

    def ubgrate_grizuni_na_ter(self):
        new_dict = {}
        c = griz_terr( _predpr = self._predpr, _month = self._month, _year = self._year)[0]
        for key, value in c.items():
            new_dict[key] = (int (value.split(",")[1].split("-")[1]), int (value.split(",")[0].split("-")[1]))
        return new_dict

    def delem_i_schitaem_grizunov(self, value_1:dict, value_2:dict, value_3:dict):
      
        val = (value_1, value_2, value_3)
        a = []
        razbor_po_datam = []
        final_value = []
        for kay in value_1:
            a.append(kay)

        for i in a:
            for j in val:
                try:
                    razbor_po_datam.append(j[i])
                except:
                    razbor_po_datam.append((0,0))
            final_value.append({i:(razbor_po_datam[0][0]+razbor_po_datam[1][0]+razbor_po_datam[2][0],
                                       razbor_po_datam[0][1]+razbor_po_datam[1][1]+razbor_po_datam[2][1])})
            razbor_po_datam = []
        return final_value

        


            

    def grizuni_vsego(self):
        bar_1 = griz(self._month, self._year, "I - II", self._predpr)
        bar_3 = griz(self._month, self._year, "III", self._predpr)
        

        a = naz.podshet_grizuni_v_dk(bar_1)
        b = naz.podshet_grizuni_v_dk(bar_3)
        c = self.ubgrate_grizuni_na_ter()
       
      
        return self.delem_i_schitaem_grizunov(a, b, c)
        
    

   
        
        
        



if __name__ == "__main__":
    a = Akti_utiliz("ТОВ 'АДМ'",'02',"2025")
    a.grizuni_vsego()


