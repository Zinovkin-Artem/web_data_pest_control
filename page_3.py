import streamlit as st


import pandas as pd
import numpy as np

import chek_list
from sql import baza_predpr, dannie_iz_grizuni_na_territorii 
from shapka_prevetstvie import shapka
import diagramma_po_barieram as diag


def show_page_3(predpriyatie, bar, nazva_storinki):


    val = baza_predpr(predpriyatie)
    
    
    
    _ = shapka(predpriyatie, nazva_storinki, val[4], val[9], val[2])

    if not _: 
        
        return
    
   

    diag.diagramma(predpriyatie, bar, val[9], flag=False)
    chek_list.main(_barier = bar, _predpr = predpriyatie,  z_po = val[9])
    
    