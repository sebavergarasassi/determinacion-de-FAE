import streamlit as st

st.set_page_config(
    page_title="ERSEPT - Metodología FAE v3.7",
    page_icon="⚡",
    layout="centered"
)

# Estilo terminal / consola técnica
st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: 'Courier New', Courier, monospace;
    }
    .terminal-header {
        color: #58a6ff;
        font-weight: bold;
        border-bottom: 1px solid #30363d;
        padding-bottom: 8px;
        margin-bottom: 16px;
    }
    .dictamen-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 16px;
        margin: 15px 0;
        border-left: 5px solid #238636;
    }
    .memoria-box {
        background-color: #0b0e14;
        border: 1px solid #21262d;
        border-radius: 4px;
        padding: 12px;
        font-size: 0.85rem;
        line-height: 1.45;
        white-space: pre-wrap;
        color: #79c0ff;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h3 class='terminal-header'>⚡ ERSEPT | METODOLOGÍA FAE v3.7</h3>", unsafe_allow_html=True)
st.caption("POLÍTICA: PRIORIDAD ELECTROQUÍMICA (UPS LiFePO4) | GENERADOR SOLO COMO EXCEPCIÓN TÉCNICA")

with st.form("form_fae_v37"):
    # -------------------------------------------------------------------------
    # BLOQUE A: INFORME MÉDICO OFICIAL (SIPROSA)
    # -------------------------------------------------------------------------
    st.markdown("#### [BLOQUE A: Vía Médica y Sanitaria - SIPROSA]")
    p_nom_med = st.number_input("1. Potencia nominal total equipamiento médico (W):", min_value=0.0, value=150.0, step=10.0)
    p_arranque_max = st.number_input("2. Potencia arranque simultánea equipamiento médico (W):", min_value=0.0, value=max(150.0, p_nom_med), step=10.0)
    t_tol_corte = st.number_input("3. Tiempo clínicamente tolerable sin suministro (minutos):", min_value=0.0, value=0.0, step=5.0)
    t_bat_interna = st.number_input("4. Autonomía batería propia equipo crítico (minutos):", min_value=0.0, value=0.0, step=5.0)
    req_transfer_0 = st.radio("5. ¿Requiere conmutación instantánea estricta (0 ms / sin microcortes)?", [1, 0], format_func=lambda x: "1: SÍ" if x == 1 else "0: NO")
    
    req_clima_med = st.radio("6. ¿Climatización ambiental con indicación médica fundada?", [0, 1], format_func=lambda x: "1: SÍ" if x == 1 else "0: NO")
    p_clima = st.number_input("   -> Potencia aire acondicionado (W):", min_value=0.0, value=1200.0, step=50.0) if req_clima_med == 1 else 0.0

    req_refrig_med = st.radio("7. ¿Requiere refrigeración para medicación prescripta?", [0, 1], format_func=lambda x: "1: SÍ" if x == 1 else "0: NO")
    p_refrig = st.number_input("   -> Potencia heladera medicamentos (W):", min_value=0.0, value=150.0, step=10.0) if req_refrig_med == 1 else 0.0

    t_traslado_hosp = st.number_input("8. Tiempo certificado traslado ambulancia a hospital (minutos):", min_value=0.0, value=30.0, step=5.0)

    st.markdown("---")
    # -------------------------------------------------------------------------
    # BLOQUE B: AUDITORÍA DE RED E INSPECCIÓN TÉCNICA (ERSEPT - EDET)
    # -------------------------------------------------------------------------
    st.markdown("#### [BLOQUE B: Vía Técnica y Regulatoria - ERSEPT / EDET]")
    st.markdown("**>> B1. Auditoría Regulatoria de Red en SET / MT**")
    ttik_sem_max = st.number_input("9. TTIK semestre más desfavorable 2 años (minutos acumulados):", min_value=0.0, value=360.0, step=30.0)
    fmik_sem_max = st.number_input("10. FMIK semestre más desfavorable 2 años (cantidad de cortes):", min_value=0, value=4, step=1)
    t_corte_max_2a = st.number_input("11. Duración corte individual más prolongado en 2 años (horas):", min_value=0.0, value=6.0, step=0.5)

    st.markdown("**>> B2. Logística de Contingencia e Inspección Domiciliaria**")
    t_asistencia_edet = st.number_input("12. Tiempo estimado arribo cuadrilla EDET con grupo móvil (minutos):", min_value=0.0, value=120.0, step=15.0)
    camino_anegable = st.radio("13. ¿Camino de acceso con riesgo de anegamiento/intransitabilidad?", [0, 1], format_func=lambda x: "1: SÍ" if x == 1 else "0: NO")
    pat_conforme = st.radio("14. ¿Posee puesta a tierra reglamentaria (PAT <= 10 Ohm)?", [1, 0], format_func=lambda x: "1: SÍ" if x == 1 else "0: NO")
    tablero_conforme = st.radio("15. ¿Tablero con termomagnéticas y disyuntor 30 mA?", [1, 0], format_func=lambda x: "1: SÍ" if x == 1 else "0: NO")
    circuito_indep = st.radio("16. ¿Línea eléctrica con circuito independiente identificado?", [1, 0], format_func=lambda x: "1: SÍ" if x == 1 else "0: NO")

    st.markdown("---")
    # -------------------------------------------------------------------------
    # BLOQUE C: DECLARACIÓN JURADA DEL CURADOR / FAMILIAR A CARGO
    # -------------------------------------------------------------------------
    st.markdown("#### [BLOQUE C: Declaración Jurada Socioambiental - Curador]")
    aislamiento_geo = st.radio("17. ¿Vivienda en zona rural aislada o de difícil acceso?", [0, 1], format_func=lambda x: "1: SÍ" if x == 1 else "0: NO")
    entorno_adecuado = st.radio("18. ¿Posee entorno adecuado para el equipamiento?", [1, 0], format_func=lambda x: "1: SÍ" if x == 1 else "0: NO")
    espacio_ext_apto = st.radio("19. ¿Dispone de patio/espacio exterior abierto y ventilado?", [1, 0], format_func=lambda x: "1: SÍ" if x == 1 else "0: NO")
    disponibilidad_combust = st.radio("20. ¿Condiciones seguras para acopio y reposición de combustible?", [1, 0], format_func=lambda x: "1: SÍ" if x == 1 else "0: NO")
    cuidador_apto_operar = st.radio("21. ¿Cuidador con capacidad psicofísica para operar generador?", [1, 0], format_func=lambda x: "1: SÍ" if x == 1 else "0: NO")

    btn_evaluar = st.form_submit_button("EJECUTAR DICTAMEN TÉCNICO REGULATORIO", use_container_width=True)

if btn_evaluar:
    # -------------------------------------------------------------------------
    # PARÁMETROS TÉCNICOS Y CRITERIOS DE INGENIERÍA
    # -------------------------------------------------------------------------
    FP = 0.80
    DISP_UPS = 0.80
    FACTOR_SOB = 1.0 / DISP_UPS
    DOD = 0.80
    ETA_INV = 0.90

    C_INC_GEN_KWH = 0.35
    MARGEN_COMBUSTIBLE = 1.25
    BIDONES_COMERCIALES = [5.0, 10.0, 20.0, 25.0, 50.0]

    ESCALONES_UPS = [1.0, 2.0, 3.0, 6.0, 10.0]
    ESCALONES_GEN_KW = [3.0, 6.0]
    MODULOS_BATERIA = [2.5, 5.0, 10.0, 15.0, 20.0]

    # 1. Balance de potencia
    p_base = p_nom_med + (p_clima * req_clima_med) + (p_refrig * req_refrig_med)

    inrush_clima = p_clima * 3.0 if req_clima_med else 0.0
    inrush_refrig = p_refrig * 4.0 if req_refrig_med else 0.0
    pico_max = max(p_arranque_max, inrush_clima, inrush_refrig)

    if pico_max == inrush_clima and req_clima_med:
        p_arr_total = pico_max + (p_base - p_clima)
        equipo_pico = "Climatización"
    elif pico_max == inrush_refrig and req_refrig_med:
        p_arr_total = pico_max + (p_base - p_refrig)
        equipo_pico = "Heladera de Medicamentos"
    else:
        p_arr_total = pico_max + (p_base - p_nom_med)
        equipo_pico = "Equipamiento Médico"

    s_termico_continuo = (FACTOR_SOB * p_base) / (1000.0 * FP)
    s_arranque = p_arr_total / (1000.0 * FP)
    s_calc = max(s_termico_continuo, s_arranque)
    s_ups = next((s for s in ESCALONES_UPS if s >= s_calc), ESCALONES_UPS[-1])

    p_gen_termica_req = (FACTOR_SOB * p_base) / 1000.0
    p_gen_arranque_req = p_arr_total / 1000.0
    p_gen_req_kw = max(p_gen_termica_req, p_gen_arranque_req)
    p_gen_comercial_kw = next((g for g in ESCALONES_GEN_KW if g >= p_gen_req_kw), ESCALONES_GEN_KW[-1])

    c_base_gen_hora = 0.60 if p_gen_comercial_kw == 3.0 else 1.00
    q_horario_gen = c_base_gen_hora + (C_INC_GEN_KWH * (p_base / 1000.0))

    # 2. Autonomía objetivo (t_target)
    if fmik_sem_max > 0:
        t_corte_medio_set_horas = (ttik_sem_max / fmik_sem_max) / 60.0
    else:
        t_corte_medio_set_horas = ttik_sem_max / 60.0

    t_asist_h = t_asistencia_edet / 60.0
    t_hosp_h = t_traslado_hosp / 60.0
    t_base = max(t_corte_medio_set_horas, t_corte_max_2a, t_asist_h, t_hosp_h)

    corte_gt_24h = 1 if t_corte_max_2a >= 24.0 else 0
    delta_aneg = 0.35 if camino_anegable else 0.0
    delta_rural = 0.25 if aislamiento_geo else 0.0
    delta_corte24 = 0.20 if corte_gt_24h else 0.0

    k_logistico_calc = 1.0 + delta_aneg + delta_rural + delta_corte24
    k_logistico = min(k_logistico_calc, 1.80)
    t_target = t_base * k_logistico

    # 3. Selección tecnológica
    req_continuidad_inmediata = 1 if (req_transfer_0 == 1 or t_tol_corte < 0.5 or t_bat_interna < 5.0) else 0
    condicion_corte_extremo = 1 if (t_target > 8.0 or ttik_sem_max > 1440.0 or aislamiento_geo == 1) else 0
    factibilidad_generador = 1 if (espacio_ext_apto == 1 and disponibilidad_combust == 1 and cuidador_apto_operar == 1) else 0

    if req_continuidad_inmediata == 1:
        if condicion_corte_extremo == 1 and factibilidad_generador == 1:
            tipo_fae = "3. HÍBRIDO (UPS + GENERADOR)"
            subtipo = "Excepción técnica por contingencia severa y aptitud operativa para combustión."
            pot_gen_instalado = p_gen_comercial_kw
            p_demanda_bateria = p_nom_med + (p_refrig * req_refrig_med)
            t_autonomia_bat = 3.0
            criterio_bat = "Batería puente de 3 horas para soporte vital y medicación hasta puesta en marcha del generador."
            e_calc_bat = (p_demanda_bateria * t_autonomia_bat) / (1000.0 * DOD * ETA_INV)
            e_bat_final = next((e for e in MODULOS_BATERIA if e >= e_calc_bat), 2.5)

            v_comb_neto = q_horario_gen * t_target
            v_comb_margen = v_comb_neto * MARGEN_COMBUSTIBLE
            v_comb_final = next((b for b in BIDONES_COMERCIALES if b >= v_comb_margen), v_comb_margen)

            caracteristicas_fae = [
                f"Equipo 1: UPS On-Line (0 ms) de {s_ups:.1f} kVA.",
                f"Batería UPS: Banco LiFePO4 de {e_bat_final:.1f} kWh / 48V.",
                f"Equipo 2: Grupo Generador de {p_gen_comercial_kw:.1f} kW con Arranque Eléctrico.",
                f"Combustible: Provisión mínima de {v_comb_final:.0f} Litros en bidón homologado (Consumo: {q_horario_gen:.2f} L/h)."
            ]
        else:
            tipo_fae = "1. UPS"
            pot_gen_instalado = 0.0
            v_comb_final = 0.0
            v_comb_neto = 0.0
            t_autonomia_bat = t_target

            if condicion_corte_extremo == 1 and factibilidad_generador == 0:
                subtipo = "Banco Extendido LiFePO4 (Veto por falta de patio, combustible o cuidador no apto)."
                p_demanda_bateria = p_nom_med + (p_refrig * req_refrig_med)
                criterio_bat = "Banco extendido que cubre soporte vital y refrigeración de medicamentos durante el evento completo."
            else:
                subtipo = "Banco Estándar LiFePO4 (Solución silenciosa preferente)."
                p_demanda_bateria = p_base
                criterio_bat = "Banco estándar que cubre la totalidad de la potencia activa base durante el evento completo."

            e_calc_bat = (p_demanda_bateria * t_autonomia_bat) / (1000.0 * DOD * ETA_INV)
            e_bat_final = next((e for e in MODULOS_BATERIA if e >= e_calc_bat), MODULOS_BATERIA[-1])

            caracteristicas_fae = [
                f"Equipo: UPS On-Line (0 ms) de {s_ups:.1f} kVA.",
                f"Batería: Banco LiFePO4 de {e_bat_final:.1f} kWh / 48V."
            ]
    else:
        if condicion_corte_extremo == 1 and factibilidad_generador == 1:
            tipo_fae = "2. GRUPO GENERADOR"
            subtipo = "Excepción técnica por contingencia severa en paciente no crítico a microcortes."
            pot_gen_instalado = p_gen_comercial_kw
            e_bat_final = 0.0
            e_calc_bat = 0.0
            p_demanda_bateria = 0.0
            t_autonomia_bat = 0.0
            criterio_bat = "No aplica (equipamiento térmico exclusivo)."

            v_comb_neto = q_horario_gen * t_target
            v_comb_margen = v_comb_neto * MARGEN_COMBUSTIBLE
            v_comb_final = next((b for b in BIDONES_COMERCIALES if b >= v_comb_margen), v_comb_margen)

            caracteristicas_fae = [
                f"Equipo: Grupo Generador de {p_gen_comercial_kw:.1f} kW con Arranque Eléctrico.",
                f"Combustible: Provisión mínima de {v_comb_final:.0f} Litros en bidón homologado (Consumo: {q_horario_gen:.2f} L/h)."
            ]
        else:
            tipo_fae = "1. UPS"
            subtipo = "Solución electroquímica para contingencias normales."
            pot_gen_instalado = 0.0
            v_comb_final = 0.0
            v_comb_neto = 0.0
            p_demanda_bateria = p_base
            t_autonomia_bat = t_target
            criterio_bat = "Solución silenciosa que cubre la totalidad de la potencia activa durante contingencias normales."
            e_calc_bat = (p_base * t_target) / (1000.0 * DOD * ETA_INV)
            e_bat_final = next((e for e in MODULOS_BATERIA if e >= e_calc_bat), 2.5)

            caracteristicas_fae = [
                f"Equipo: UPS de {s_ups:.1f} kVA.",
                f"Batería: Banco LiFePO4 de {e_bat_final:.1f} kWh / 48V."
            ]

    requiere_adecuacion = (pat_conforme == 0 or tablero_conforme == 0 or circuito_indep == 0)

    # -------------------------------------------------------------------------
    # SALIDA DEL DICTAMEN
    # -------------------------------------------------------------------------
    st.markdown(f"""
    <div class='dictamen-box'>
        <h4 style='color: #2ea043; margin-top: 0;'>DICTAMEN ASIGNADO: {tipo_fae}</h4>
        <p style='color: #8b949e; margin-bottom: 8px;'><b>Fundamento:</b> {subtipo}</p>
        <p style='margin-bottom: 4px;'><b>Configuración técnica obligatoria:</b></p>
        <ul>
            {''.join([f"<li>{c}</li>" for c in caracteristicas_fae])}
        </ul>
    </div>
    """, unsafe_allow_html=True)

    if requiere_adecuacion:
        st.error("⚠️ INSTALACIÓN CONDICIONADA - EDET DEBE EJECUTAR ADECUACIONES PREVIAS:")
        if not pat_conforme:
            st.write("• Hincado de jabalina de PAT reglamentaria y certificación R_pat <= 10 Ohm.")
        if not tablero_conforme:
            st.write("• Instalación de tablero con termomagnética y disyuntor diferencial de 30 mA.")
        if not circuito_indep:
            st.write("• Tendido de circuito eléctrico exclusivo e identificado para soporte vital.")
    else:
        st.success("✓ INSTALACIÓN ELÉCTRICA CONFORME (Apta para energización inmediata)")

    # -------------------------------------------------------------------------
    # MEMORIA TÉCNICA DE CÁLCULO
    # -------------------------------------------------------------------------
    memoria_txt = f"""========================================================================================
MEMORIA DE CÁLCULO Y JUSTIFICACIÓN TÉCNICA DE LOS PARÁMETROS - ERSEPT
========================================================================================

>> 1. JUSTIFICACIÓN DE LA POTENCIA DE LA FAE:
   • Balance Activo Continuo:     P_base = P_med ({p_nom_med:.0f} W) + P_clima ({p_clima:.0f} W) + P_refrig ({p_refrig:.0f} W) = {p_base:.0f} W
   • Transitorio Crítico Máx:     Pico {equipo_pico} = {pico_max:.0f} W  -->  P_arr_total = {p_arr_total:.0f} W
   • Factor de Potencia (FP):     FP = {FP:.2f} (Conversión de Watts a VA para cargas inductivas/electrónicas)
   • Disponibilidad de Potencia:  eta_disp = {DISP_UPS:.2f} (Límite operativo al 80% para evitar sobrecalentamiento, factor 1/0.80 = {FACTOR_SOB:.2f})
   • Criterio Térmico Continuo:   S_termico_continuo = ({p_base:.0f} W * {FACTOR_SOB:.2f}) / ({FP:.2f} * 1000) = {s_termico_continuo:.2f} kVA
   • Criterio de Arranque:        S_arranque = {p_arr_total:.0f} W / ({FP:.2f} * 1000) = {s_arranque:.2f} kVA
   • Potencia Aparente Cálculo:   S_calc = max(S_termico_continuo: {s_termico_continuo:.2f}, S_arranque: {s_arranque:.2f}) = {s_calc:.2f} kVA
"""
    if "UPS" in tipo_fae:
        memoria_txt += f"   ==> SELECCIÓN UPS:             Escalón normalizado comercial asignado = {s_ups:.1f} kVA\n"
    if pot_gen_instalado > 0:
        memoria_txt += f"""   • Potencia Térmica Requerida:  P_gen_req = max(Régimen Continuo: {p_gen_termica_req:.2f} kW, Arranque: {p_gen_arranque_req:.2f} kW) = {p_gen_req_kw:.2f} kW
   ==> SELECCIÓN GENERADOR:       Escalón comercial asignado (3 kW o 6 kW) = {p_gen_comercial_kw:.1f} kW con Arranque Eléctrico\n"""

    memoria_txt += f"""
>> 2. JUSTIFICACIÓN DEL TIEMPO OBJETIVO DE CONTINGENCIA (t_target):
   • Corte Promedio SET:          t_corte_medio = {ttik_sem_max:.0f} min / (max(1, {fmik_sem_max}) * 60) = {t_corte_medio_set_horas:.2f} h
   • Registro Máximo Histórico:   t_corte_max_2a = {t_corte_max_2a:.2f} h (evento singular más prolongado en 2 años)
   • Logística Auxilio EDET:      t_asistencia_edet = {t_asistencia_edet:.0f} min / 60 = {t_asist_h:.2f} h (tiempo de arribo con grupo móvil)
   • Evacuación Sanitaria:        t_traslado_hosp = {t_traslado_hosp:.0f} min / 60 = {t_hosp_h:.2f} h (tiempo de ambulancia certificado por SIPROSA)
   • Base Temporal (t_base):      max({t_corte_medio_set_horas:.2f}h, {t_corte_max_2a:.2f}h, {t_asist_h:.2f}h, {t_hosp_h:.2f}h) = {t_base:.2f} h (gobierna el evento más desfavorable)
   • Ponderadores Aditivos de Riesgo Territorial:
       - Base Neutra (Entorno Urbano): 1.00 (sin sobrecosto de tiempo de viaje)
       - Dificultad de Acceso:         +{delta_aneg*100:.0f}% (camino con riesgo de anegamiento / intransitabilidad por lluvias)
       - Aislamiento Territorial:     +{delta_rural*100:.0f}% (zona rural dispersa respecto a bases operativas)
       - Antecedente Crítico de Red:   +{delta_corte24*100:.0f}% (historial de cortes continuos >= 24h)
   • Suma Acumulada de Factores:  K_acumulado = 1.00 + {delta_aneg:.2f} + {delta_rural:.2f} + {delta_corte24:.2f} = {k_logistico_calc:.2f}
   • Techo Regulatorio Máximo:    K_max = 1.80 (límite técnico-económico que restringe la sobrecarga a un máximo de +80%)
   • Factor Logístico Final:      Klogistico = min(K_acumulado: {k_logistico_calc:.2f}, K_max: 1.80) = {k_logistico:.2f}
   ==> AUTONOMÍA FINAL:           t_target = t_base ({t_base:.2f} h) * Klogistico ({k_logistico:.2f}) = {t_target:.2f} horas de cobertura continua

>> 3. JUSTIFICACIÓN DEL ALMACENAMIENTO (BATERÍAS Y COMBUSTIBLE):
"""
    if e_bat_final > 0:
        memoria_txt += f"""   • Demanda sobre Batería:       P_demanda = {p_demanda_bateria:.0f} W ({criterio_bat})
   • Autonomía de Batería:        t_bat = {t_autonomia_bat:.2f} h
   • Parámetros Electroquímicos:  Profundidad de descarga DoD = {DOD*100:.0f}% | Rendimiento inversor η_inv = {ETA_INV*100:.0f}%
   • Cálculo de Energía:          E_calc = ({p_demanda_bateria:.0f} W * {t_autonomia_bat:.2f} h) / (1000 * {DOD:.2f} * {ETA_INV:.2f}) = {e_calc_bat:.2f} kWh
   ==> SELECCIÓN BATERÍA:         Módulo comercial normalizado LiFePO4 (48V) = {e_bat_final:.1f} kWh\n"""
    else:
        memoria_txt += "   • Banco de Baterías:           No requerido (atención exclusiva por grupo generador).\n"

    if v_comb_final > 0:
        memoria_txt += f"""   • Consumo Base en Vacío:       Q_base = {c_base_gen_hora:.2f} L/h (para grupo de {p_gen_comercial_kw:.1f} kW a 3000 RPM sin carga)
   • Consumo Incremental Carga:   c_inc  = {C_INC_GEN_KWH:.2f} L/kWh entregado
   • Consumo Horario Estimado:    Q_horario = {c_base_gen_hora:.2f} + ({C_INC_GEN_KWH:.2f} * {p_base/1000.0:.2f} kW) = {q_horario_gen:.2f} L/h
   • Consumo Neto para {t_target:.2f} h:      V_neto = {q_horario_gen:.2f} L/h * {t_target:.2f} h = {v_comb_neto:.2f} Litros
   • Margen de Seguridad (+25%):  V_con_margen = {v_comb_neto:.2f} L * {MARGEN_COMBUSTIBLE:.2f} = {v_comb_margen:.2f} Litros (fondo de tanque y pérdidas)
   ==> RESERVA OBLIGATORIA NAFTA: Bidón normalizado asignado = {v_comb_final:.0f} Litros\n"""
    else:
        memoria_txt += "   • Reserva de Combustible:      0.0 Litros (Sistema 100% electroquímico limpio, sin motor térmico).\n"

    with st.expander("VER MEMORIA DE CÁLCULO COMPLETA (LOG DE INGENIERÍA)", expanded=True):
        st.markdown(f"<div class='memoria-box'>{memoria_txt}</div>", unsafe_allow_html=True)