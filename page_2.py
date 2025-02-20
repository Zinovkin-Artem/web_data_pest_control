import streamlit as st
from sql import baza_predpr
from shapka_prevetstvie import shapka
import diagramma_po_barieram as diag
import chek_list


def show_page_2(predpriyatie, bar, nazva_storinki):

    val = baza_predpr(predpriyatie)
    
    _ = shapka(predpriyatie, nazva_storinki, val[6], val[8], val[2])
   
    if not _: 
        
        return

  

    



    diag.diagramma(predpriyatie, bar, z_po = val[8])
    chek_list.main(_barier = bar, _predpr = predpriyatie,  z_po = val[8])
