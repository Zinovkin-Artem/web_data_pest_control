import streamlit as st


import pandas as pd
import numpy as np

import chek_list
from sql import baza_predpr
from shapka_prevetstvie import shapka

import diagramma_po_barieram as diag


def show_page_1(predpriyatie, bar, nazva_storinki):
    
    
    
    
    val = baza_predpr(predpriyatie)
    
    
    _ = shapka(predpriyatie, nazva_storinki, val[5], val[7], val[2])
   
    if not _: 
        
        return

  

    chek_list.main(_barier = bar, _predpr = predpriyatie,  z_po = val[7])



    diag.diagramma(predpriyatie, bar)



   
