import streamlit as st



import pandas as pd
import numpy as np
import chek_list

from sql import baza_predpr
from shapka_prevetstvie import shapka

import diagramma_zagalna as diag


def show_page_0(predpriyatie, _bar, nazva_storinki):

    
     
    val = baza_predpr(predpriyatie)

    
    
    kilkist_obl = val[3] + val[4]
    number = f"І- бар'єр: {val[7]}, ІI- бар'єр: { val[8]}, ІII- бар'єр: {val[9]}"
    
    _ = shapka(predpriyatie, nazva_storinki, kilkist_obl, number, val[2])

    if not _: 
        
        return

    _z_po = f"{val[7]},{ val[8]},{val[9]}"

    chek_list.main( _barier = "I - II",  _predpr =  predpriyatie, z_po = _z_po)
    chek_list.main( _barier = "III",  _predpr =  predpriyatie, z_po = _z_po)



    diag.diagramma(predpriyatie)