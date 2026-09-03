import math

def pedir_num(mensaje, min_val=0.0):
    while True:
        try:
            val = float(input(f"{mensaje}: "))
            if val < min_val:
                print(f"  [Error] Debe ser un número mayor o igual a {min_val}.")
                continue
            return val
        except ValueError:
            print("  [Error] Ingrese un valor numérico válido.")

def pedir_int(mensaje, min_val=0):
    while True:
        try:
            val = int(input(f"{mensaje}: "))
            if val < min_val:
                print(f"  [Error] Debe ser un entero mayor o igual a {min_val}.")
                continue
            return val
        except ValueError:
            print("  [Error] Ingrese un número entero válido.")

def pedir_bool(mensaje):
    while True:
        val = input(f"{mensaje} (1=Sí / 0=No): ").strip()
        if val in ["1", "0"]:
            return int(val)
        print("  [Error] Ingrese 1 para Sí o 0 para No.")

def evaluar_fae_v3_7():
    print("=" * 100)
    print(" METODOLOGÍA FAE v3.7 - ENTE ÚNICO DE CONTROL Y REGULACIÓN (ERSEPT)")
    print(" POLÍTICA DE EQUIPAMIENTO: PRIORIDAD ELECTROQUÍMICA (UPS LiFePO4)")
    print(" DISPOSICIÓN: GRUPO GENERADOR SOLO COMO EXCEPCIÓN TÉCNICA (3.0 kW o 6.0 kW CON ARRANQUE ELÉCTRICO)")
    print("=" * 100)

    # -------------------------------------------------------------------------
    # BLOQUE A: INFORME MÉDICO OFICIAL (SIPROSA)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 100)
    print("[BLOQUE A: Vía Médica y Sanitaria - Certificación Oficial SIPROSA]")
    print("-" * 100)
    p_nom_med = pedir_num("1. Potencia nominal total del equipamiento eléctrico prescripto al electrodependiente (W)", 0)
    p_arranque_max = pedir_num("2. Potencia de arranque simultánea del equipamiento eléctrico prescripto (W)", p_nom_med)
    t_tol_corte = pedir_num("3. Tiempo clínicamente tolerable sin suministro eléctrico (minutos)", 0)
    t_bat_interna = pedir_num("4. Autonomía de batería propia del equipo médico más crítico (minutos)", 0)
    req_transfer_0 = pedir_bool("5. ¿Requiere conmutación instantánea estricta (0 ms / sin microcortes)?")
    
    req_clima_med = pedir_bool("6. ¿Climatización ambiental con indicación médica fundada de SIPROSA?")
    p_clima = pedir_num("   -> Potencia del acondicionador de aire (W)", 0) if req_clima_med else 0.0
    
    req_refrig_med = pedir_bool("7. ¿Requiere refrigeración para medicación prescripta?")
    p_refrig = pedir_num("   -> Potencia de la heladera de medicamentos (W)", 0) if req_refrig_med else 0.0

    t_traslado_hosp = pedir_num("8. Tiempo certificado de traslado en ambulancia al hospital de referencia (minutos)", 0)

    # -------------------------------------------------------------------------
    # BLOQUE B: AUDITORÍA DE RED E INSPECCIÓN TÉCNICA (ERSEPT - EDET)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 100)
    print("[BLOQUE B: Vía Técnica y Regulatoria - ERSEPT / EDET]")
    print("-" * 100)
    print(">> B1. Auditoría Regulatoria de Red en SET / Alimentador MT (ERSEPT)")
    ttik_sem_max = pedir_num("9. TTIK del semestre más desfavorable de los últimos 2 años (tiempo acumulado en MINUTOS)", 0)
    fmik_sem_max = pedir_int("10. FMIK del semestre más desfavorable de los últimos 2 años (CANTIDAD DE CORTES REALES)", 0)
    t_corte_max_2a = pedir_num("11. Duración del corte individual más prolongado en los últimos 2 años (HORAS)", 0)
    print("\n>> B2. Logística de Contingencia e Inspección Domiciliaria (EDET)")
    t_asistencia_edet = pedir_num("12. Tiempo estimado de arribo de cuadrilla EDET con grupo móvil (minutos)", 0)
    camino_anegable = pedir_bool("13. ¿El camino de acceso al inmueble presenta riesgo de anegamiento o intransitabilidad?")
    pat_conforme = pedir_bool("14. ¿Posee puesta a tierra reglamentaria (PAT <= 10 Ohm)?")
    tablero_conforme = pedir_bool("15. ¿Posee tablero con protecciones termomagnéticas y disyuntor diferencial (30 mA)?")
    circuito_indep = pedir_bool("16. ¿Posee línea eléctrica con circuito independiente fácilmente identificable para servicios del electrodependiente?")

    # -------------------------------------------------------------------------
    # BLOQUE C: DECLARACIÓN JURADA DEL CURADOR / FAMILIAR A CARGO
    # -------------------------------------------------------------------------
    print("\n" + "-" * 100)
    print("[BLOQUE C: Declaración Jurada Socioambiental y Operativa - Curador del Paciente]")
    print("-" * 100)
    aislamiento_geo = pedir_bool("17. ¿La vivienda se encuentra en zona rural aislada o de difícil acceso?")
    entorno_adecuado = pedir_bool("18. ¿Posee entorno adecuado para el electrodependiente y su equipamiento?")
    espacio_ext_apto = pedir_bool("19. ¿Dispone de patio/espacio exterior abierto y ventilado para generador?")
    disponibilidad_combust = pedir_bool("20. ¿Existen condiciones seguras en el inmueble para acopio y reposición de combustible?")
    cuidador_apto_operar = pedir_bool("21. ¿El cuidador posee capacidad psicofísica para operar el grupo generador?")

    # -------------------------------------------------------------------------
    # PARÁMETROS TÉCNICOS Y CRITERIOS DE INGENIERÍA
    # -------------------------------------------------------------------------
    FP = 0.80               # Factor de potencia reglamentario
    DISP_UPS = 0.80         # Límite de carga continuo del inversor (80%)
    FACTOR_SOB = 1.0 / DISP_UPS  # 1.25 (factor de mayoración por límite térmico)
    DOD = 0.80              # Profundidad de descarga segura LiFePO4
    ETA_INV = 0.90          # Eficiencia global del inversor/cargador

    # Parámetros del motor térmico según potencia asignada (Línea de Willans)
    C_INC_GEN_KWH = 0.35    # Consumo incremental por kWh útil generado (L/kWh)
    MARGEN_COMBUSTIBLE = 1.25  # Margen de seguridad operativo (+25% por remanente de tanque y pérdidas)
    BIDONES_COMERCIALES = [5.0, 10.0, 20.0, 25.0, 50.0]  # Envases normalizados homologados (Litros)

    ESCALONES_UPS = [1.0, 2.0, 3.0, 6.0, 10.0]        # Escalones comerciales normalizados UPS (kVA)
    ESCALONES_GEN_KW = [3.0, 6.0]                      # Escalones comerciales disponibles generador (kW)
    MODULOS_BATERIA = [2.5, 5.0, 10.0, 15.0, 20.0]    # Módulos LiFePO4 comerciales a 48V (kWh)

    # -------------------------------------------------------------------------
    # 1. CÁLCULO DE POTENCIA ELÉCTRICA (kVA y kW)
    # -------------------------------------------------------------------------
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

    # Cálculo de potencia real requerida para generador térmico (kW útiles)
    p_gen_termica_req = (FACTOR_SOB * p_base) / 1000.0   # kW continuos con margen térmico del 20%
    p_gen_arranque_req = p_arr_total / 1000.0            # kW instantáneos de pico de arranque
    p_gen_req_kw = max(p_gen_termica_req, p_gen_arranque_req)
    
    # Selección de escalón comercial de generador (3 kW o 6 kW)
    p_gen_comercial_kw = next((g for g in ESCALONES_GEN_KW if g >= p_gen_req_kw), ESCALONES_GEN_KW[-1])

    # Consumo en vacío según escalón comercial de motor
    # Motor 3 kW (~210 cc): 0.60 L/h base | Motor 6 kW (~420 cc): 1.00 L/h base
    c_base_gen_hora = 0.60 if p_gen_comercial_kw == 3.0 else 1.00
    q_horario_gen = c_base_gen_hora + (C_INC_GEN_KWH * (p_base / 1000.0))

    # -------------------------------------------------------------------------
    # 2. DETERMINACIÓN DE AUTONOMÍA OBJETIVO (t_target)
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # 3. SELECCIÓN DE ARQUITECTURA TECNOLÓGICA Y ASIGNACIÓN
    # -------------------------------------------------------------------------
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
    # DICTAMEN REGULATORIO FORMAL
    # -------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print(" RESOLUCIÓN Y DICTAMEN TÉCNICO REGULATORIO FAE v3.7 - ERSEPT")
    print("=" * 100)
    print(f"DICTAMEN ASIGNADO:             {tipo_fae}")
    print(f"Fundamento de Asignación:      {subtipo}")
    print("-" * 100)
    print("CARACTERÍSTICAS TÉCNICAS OBLIGATORIAS DE LA FAE:")
    for idx, carac in enumerate(caracteristicas_fae, 1):
        print(f"  [{idx}] {carac}")
    print("-" * 100)
    print("MEMORIA DE CÁLCULO Y JUSTIFICACIÓN TÉCNICA DE LOS PARÁMETROS:")
    
    # 1. Justificación de Potencia
    print("\n>> 1. JUSTIFICACIÓN DE LA POTENCIA DE LA FAE:")
    print(f"   • Balance Activo Continuo:     P_base = P_med ({p_nom_med:.0f} W) + P_clima ({p_clima:.0f} W) + P_refrig ({p_refrig:.0f} W) = {p_base:.0f} W")
    print(f"   • Transitorio Crítico Máx:     Pico {equipo_pico} = {pico_max:.0f} W  -->  P_arr_total = {p_arr_total:.0f} W")
    print(f"   • Factor de Potencia (FP):     FP = {FP:.2f} (Conversión de Watts a VA para cargas inductivas/electrónicas)")
    print(f"   • Disponibilidad de Potencia:  eta_disp = {DISP_UPS:.2f} (Límite operativo al 80% para evitar sobrecalentamiento, factor 1/0.80 = {FACTOR_SOB:.2f})")
    print(f"   • Criterio Térmico Continuo:   S_termico_continuo = ({p_base:.0f} W * {FACTOR_SOB:.2f}) / ({FP:.2f} * 1000) = {s_termico_continuo:.2f} kVA")
    print(f"   • Criterio de Arranque:        S_arranque = {p_arr_total:.0f} W / ({FP:.2f} * 1000) = {s_arranque:.2f} kVA")
    print(f"   • Potencia Aparente Cálculo:   S_calc = max(S_termico_continuo: {s_termico_continuo:.2f}, S_arranque: {s_arranque:.2f}) = {s_calc:.2f} kVA")
    if "UPS" in tipo_fae:
        print(f"   ==> SELECCIÓN UPS:             Escalón normalizado comercial asignado = {s_ups:.1f} kVA")
    if pot_gen_instalado > 0:
        print(f"   • Potencia Térmica Requerida:  P_gen_req = max(Régimen Continuo: {p_gen_termica_req:.2f} kW, Arranque: {p_gen_arranque_req:.2f} kW) = {p_gen_req_kw:.2f} kW")
        print(f"   ==> SELECCIÓN GENERADOR:       Escalón comercial asignado (3 kW o 6 kW) = {p_gen_comercial_kw:.1f} kW con Arranque Eléctrico")

    # 2. Justificación de Autonomía Temporal
    print("\n>> 2. JUSTIFICACIÓN DEL TIEMPO OBJETIVO DE CONTINGENCIA (t_target):")
    print(f"   • Corte Promedio SET:          t_corte_medio = {ttik_sem_max:.0f} min / (max(1, {fmik_sem_max}) * 60) = {t_corte_medio_set_horas:.2f} h")
    print(f"   • Registro Máximo Histórico:   t_corte_max_2a = {t_corte_max_2a:.2f} h (evento singular más prolongado en 2 años)")
    print(f"   • Logística Auxilio EDET:      t_asistencia_edet = {t_asistencia_edet:.0f} min / 60 = {t_asist_h:.2f} h (tiempo de arribo con grupo móvil)")
    print(f"   • Evacuación Sanitaria:        t_traslado_hosp = {t_traslado_hosp:.0f} min / 60 = {t_hosp_h:.2f} h (tiempo de ambulancia certificado por SIPROSA)")
    print(f"   • Base Temporal (t_base):      max({t_corte_medio_set_horas:.2f}h, {t_corte_max_2a:.2f}h, {t_asist_h:.2f}h, {t_hosp_h:.2f}h) = {t_base:.2f} h (gobierna el evento más desfavorable)")
    print(f"   • Ponderadores Aditivos de Riesgo Territorial:")
    print(f"       - Base Neutra (Entorno Urbano): 1.00 (sin sobrecosto de tiempo de viaje)")
    print(f"       - Dificultad de Acceso:        +{delta_aneg*100:.0f}% (camino con riesgo de anegamiento / intransitabilidad por lluvias)")
    print(f"       - Aislamiento Territorial:     +{delta_rural*100:.0f}% (zona rural dispersa respecto a bases operativas)")
    print(f"       - Antecedente Crítico de Red:  +{delta_corte24*100:.0f}% (historial de cortes continuos >= 24h)")
    print(f"   • Suma Acumulada de Factores:  K_acumulado = 1.00 + {delta_aneg:.2f} + {delta_rural:.2f} + {delta_corte24:.2f} = {k_logistico_calc:.2f}")
    print(f"   • Techo Regulatorio Máximo:    K_max = 1.80 (límite técnico-económico que restringe la sobrecarga a un máximo de +80%)")
    print(f"   • Factor Logístico Final:      Klogistico = min(K_acumulado: {k_logistico_calc:.2f}, K_max: 1.80) = {k_logistico:.2f}")
    print(f"   ==> AUTONOMÍA FINAL:           t_target = t_base ({t_base:.2f} h) * Klogistico ({k_logistico:.2f}) = {t_target:.2f} horas de cobertura continua")

    # 3. Justificación de Almacenamiento
    print("\n>> 3. JUSTIFICACIÓN DEL ALMACENAMIENTO (BATERÍAS Y COMBUSTIBLE):")
    if e_bat_final > 0:
        print(f"   • Demanda sobre Batería:       P_demanda = {p_demanda_bateria:.0f} W ({criterio_bat})")
        print(f"   • Autonomía de Batería:        t_bat = {t_autonomia_bat:.2f} h")
        print(f"   • Parámetros Electroquímicos:  Profundidad de descarga DoD = {DOD*100:.0f}% | Rendimiento inversor η_inv = {ETA_INV*100:.0f}%")
        print(f"   • Cálculo de Energía:          E_calc = ({p_demanda_bateria:.0f} W * {t_autonomia_bat:.2f} h) / (1000 * {DOD:.2f} * {ETA_INV:.2f}) = {e_calc_bat:.2f} kWh")
        print(f"   ==> SELECCIÓN BATERÍA:         Módulo comercial normalizado LiFePO4 (48V) = {e_bat_final:.1f} kWh")
    else:
        print("   • Banco de Baterías:           No requerido (atención exclusiva por grupo generador).")

    if v_comb_final > 0:
        print(f"   • Consumo Base en Vacío:       Q_base = {c_base_gen_hora:.2f} L/h (para grupo de {p_gen_comercial_kw:.1f} kW a 3000 RPM sin carga)")
        print(f"   • Consumo Incremental Carga:   c_inc  = {C_INC_GEN_KWH:.2f} L/kWh entregado")
        print(f"   • Consumo Horario Estimado:    Q_horario = {c_base_gen_hora:.2f} + ({C_INC_GEN_KWH:.2f} * {p_base/1000.0:.2f} kW) = {q_horario_gen:.2f} L/h")
        print(f"   • Consumo Neto para {t_target:.2f} h:      V_neto = {q_horario_gen:.2f} L/h * {t_target:.2f} h = {v_comb_neto:.2f} Litros")
        print(f"   • Margen de Seguridad (+25%):  V_con_margen = {v_comb_neto:.2f} L * {MARGEN_COMBUSTIBLE:.2f} = {v_comb_margen:.2f} Litros (fondo de tanque y pérdidas)")
        print(f"   ==> RESERVA OBLIGATORIA NAFTA: Bidón normalizado asignado = {v_comb_final:.0f} Litros")
    else:
        print("   • Reserva de Combustible:      0.0 Litros (Sistema 100% electroquímico limpio, sin motor térmico).")

    print("-" * 100)
    print("AUDITORÍA DE SEGURIDAD ELÉCTRICA INTERNA:")
    if requiere_adecuacion:
        print("  [!] INSTALACIÓN CONDICIONADA - EDET DEBE EJECUTAR ADECUACIONES PREVIAS:")
        if not pat_conforme:
            print("      • Hincado de jabalina de PAT reglamentaria y certificación R_pat <= 10 Ohm.")
        if not tablero_conforme:
            print("      • Instalación de tablero con termomagnética y disyuntor diferencial de 30 mA.")
        if not circuito_indep:
            print("      • Tendido de circuito eléctrico exclusivo e identificado para soporte vital.")
    else:
        print("  [✓] INSTALACIÓN ELÉCTRICA CONFORME (Apta para energización inmediata)")
    print("=" * 100)

if __name__ == "__main__":
    evaluar_fae_v3_7()