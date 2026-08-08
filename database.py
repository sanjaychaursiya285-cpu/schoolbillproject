import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_connection() -> Client:
    # Direct Supabase credentials setup to avoid secrets configuration errors
    url = "https://hnyvwzvilueputsnhffh.supabase.co"
    key = "sb_publishable_2BADG0X4hmCKHYOPpVGcWg_1Fm66sTI"
    return create_client(url, key)

supabase = init_connection()