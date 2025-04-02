import streamlit as st


import pandas as pd
import numpy as np

import chek_list
from sql import baza_predpr, dannie_iz_grizuni_na_territorii 
from shapka_prevetstvie import shapka

import diagramma_po_barieram as diag


def show_page_1(predpriyatie, bar, nazva_storinki):
    
    
    
    
    val = baza_predpr(predpriyatie)
    
    
    _ = shapka(predpriyatie, nazva_storinki, val[5], val[7], val[2])
   
    if not _: 
        
        return

    diag.diagramma(predpriyatie, bar, val[7])
    chek_list.main(_barier = bar, _predpr = predpriyatie,  z_po = val[7])
   


   
