import logging
from dataset import Dataset, RunResult

logger = logging.getLogger(__name__)

# Simulation constants follow from original BASIC source.

TEMP_REGIMES = ["Pergelic", "Cryic", "Frigid", "Mesic",
    "Thermic", "Hyperthermic", "Isofrigid", "Isomesic", 
    "Isothermic", "Isohyperthermic"]

ZPE = [135.0, 139.5, 143.7, 147.8, 151.7, 155.4, 158.9, 162.1,
    165.2, 168.0, 170.7, 173.1, 175.3, 177.2, 179.0, 180.5, 181.8,
    182.9, 183.7, 184.3, 184.7, 184.9, 185.0, 185.0]

ZT = [26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0,
    31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5, 36.0, 36.5,
    37.0, 37.5, 38.0]

INZ = [
    [1.04, 1.02, 1.0, 0.97, 0.95, 0.93, 0.92, 0.92, 0.91, 0.91, 0.9, 0.9, 0.89, 0.88, 0.88, 0.87, 0.87, 0.86, 0.85, 0.85, 0.84, 0.83, 0.82, 0.81, 0.81, 0.8, 0.79, 0.77, 0.76, 0.75, 0.74],
    [0.94, 0.93, 0.91, 0.91, 0.9, 0.89, 0.88, 0.88, 0.88, 0.87, 0.87, 0.87, 0.86, 0.86, 0.85, 0.85, 0.85, 0.84, 0.84, 0.84, 0.83, 0.83, 0.83, 0.82, 0.82, 0.81, 0.81, 0.8, 0.8, 0.79, 0.78],
    [1.04, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02],
    [1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.06, 1.07, 1.07, 1.07, 1.08, 1.08, 1.08, 1.09, 1.09, 1.09, 1.1, 1.1, 1.1, 1.11, 1.11, 1.11, 1.12, 1.12, 1.13, 1.13, 1.13, 1.14, 1.14, 1.14, 1.15],
    [1.04, 1.06, 1.08, 1.11, 1.13, 1.15, 1.15, 1.16, 1.16, 1.17, 1.18, 1.18, 1.19, 1.19, 1.2, 1.21, 1.21, 1.22, 1.23, 1.23, 1.24, 1.25, 1.26, 1.26, 1.27, 1.28, 1.29, 1.3, 1.31, 1.32, 1.33],
    [1.01, 1.03, 1.06, 1.08, 1.11, 1.14, 1.15, 1.15, 1.16, 1.16, 1.17, 1.18, 1.19, 1.2, 1.2, 1.21, 1.22, 1.23, 1.24, 1.24, 1.25, 1.26, 1.27, 1.28, 1.29, 1.29, 1.31, 1.32, 1.33, 1.34, 1.36],
    [1.04, 1.06, 1.08, 1.12, 1.14, 1.17, 1.17, 1.18, 1.18, 1.19, 1.2, 1.2, 1.21, 1.22, 1.22, 1.23, 1.24, 1.25, 1.25, 1.26, 1.27, 1.27, 1.28, 1.29, 1.3, 1.31, 1.32, 1.33, 1.34, 1.35, 1.37],
    [1.04, 1.05, 1.07, 1.08, 1.11, 1.12, 1.12, 1.13, 1.13, 1.13, 1.14, 1.14, 1.15, 1.15, 1.16, 1.16, 1.16, 1.17, 1.17, 1.18, 1.18, 1.19, 1.19, 1.2, 1.2, 1.21, 1.22, 1.22, 1.23, 1.24, 1.25],
    [1.01, 1.01, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.05, 1.05, 1.06],
    [1.04, 1.03, 1.02, 1.01, 1.0, 0.99, 0.99, 0.99, 0.98, 0.98, 0.98, 0.98, 0.98, 0.97, 0.97, 0.97, 0.97, 0.97, 0.96, 0.96, 0.96, 0.96, 0.95, 0.95, 0.95, 0.94, 0.94, 0.93, 0.93, 0.93, 0.92],
    [1.01, 0.99, 0.98, 0.95, 0.93, 0.91, 0.91, 0.9, 0.9, 0.9, 0.89, 0.89, 0.88, 0.88, 0.87, 0.86, 0.86, 0.85, 0.84, 0.84, 0.83, 0.82, 0.82, 0.81, 0.8, 0.79, 0.79, 0.78, 0.77, 0.76, 0.76],
    [1.04, 1.02, 0.99, 0.97, 0.94, 0.91, 0.91, 0.9, 0.9, 0.89, 0.88, 0.88, 0.87, 0.86, 0.86, 0.85, 0.84, 0.83, 0.83, 0.82, 0.81, 0.8, 0.79, 0.77, 0.76, 0.75, 0.74, 0.73, 0.72, 0.71, 0.7]
]

RN = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 26.0, 27.0, 28.0, 29.0,
    30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0, 
    40.0, 41.0, 42.0, 43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0]

FS = [
	[1.06, 1.08, 1.12, 1.14, 1.17, 1.2, 1.23, 1.27, 1.28, 1.3, 1.32, 1.34, 1.37],
    [0.95, 0.97, 0.98, 1.0, 1.01, 1.03, 1.04, 1.06, 1.07, 1.08, 1.1, 1.11, 1.12],
    [1.04, 1.05, 1.05, 1.05, 1.05, 1.06, 1.06, 1.07, 1.07, 1.07, 1.07, 1.08, 1.08],
    [1.0, 0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.92, 0.91, 0.9, 0.89],
    [1.02, 1.01, 0.98, 0.96, 0.94, 0.92, 0.89, 0.86, 0.85, 0.83, 0.82, 0.8, 0.77],
    [0.99, 0.96, 0.94, 0.91, 0.88, 0.85, 0.82, 0.78, 0.76, 0.74, 0.72, 0.7, 0.67],
    [1.02, 1.0, 0.97, 0.95, 0.93, 0.9, 0.87, 0.84, 0.82, 0.81, 0.79, 0.76, 0.74],
    [1.03, 1.01, 1.0, 0.99, 0.98, 0.96, 0.94, 0.92, 0.92, 0.91, 0.9, 0.89, 0.88],
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.99, 0.99, 0.99, 0.99],
    [1.05, 1.06, 1.07, 1.08, 1.1, 1.12, 1.13, 1.15, 1.16, 1.17, 1.17, 1.18, 1.19],
    [1.03, 1.05, 1.07, 1.09, 1.11, 1.14, 1.17, 1.2, 1.22, 1.23, 1.25, 1.27, 1.29],
    [1.06, 1.1, 1.12, 1.15, 1.18, 1.21, 1.25, 1.29, 1.31, 1.33, 1.35, 1.37, 1.41]
]

RS = [5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 42.0, 44.0, 46.0, 48.0, 50.0]

FC = 2.5 # Degree offset between soil and air temperature in Celsius.

FCD = 0.66 # Soil-Air Relationship Amplitude

CV = 5.0/9.0

DP = [8, 7, 16, 6, 15, 24, 5, 14, 23, 32, 4, 13, 22, 31, 40, 3, 12, 21, 30,
    39, 48, 2, 11, 20, 29, 38, 47, 56, 1, 10, 19, 28, 37, 46, 55, 64, 9, 18,
    27, 36, 45, 54, 63, 17, 26, 35, 44, 53, 62, 25, 34, 43, 52, 61, 33, 42,
    51, 60, 41, 50, 59, 49, 58, 57, 160]

DR = [1., 1., 1., 1., 1.02, 1.03, 1.05, 1.07, 1.09, 1.11, 1.13, 1.15, 1.17, 1.19, 1.21, 1.23, 1.26,
    1.28, 1.31, 1.34, 1.37, 1.40, 1.43, 1.46, 1.49, 1.53, 1.57, 1.61, 1.65, 1.69, 1.74, 1.78,
    1.84, 1.89, 1.95, 2.01, 2.07, 2.14, 2.22, 2.30, 2.38, 2.47, 2.57, 2.68, 2.80, 2.93, 3.07,
    3.22, 3.39, 3.58, 3.80, 4.03, 4.31, 4.62, 4.98, 5., 5., 5., 5., 5., 5., 5., 5., 5.]

# Lag phases.  21 days is used for when the soil is warming
# up, and 10 days for when the soil is cooling off.
lagPhaseSummer = 21
lagPhaseWinter = 10

# Given float lists precip and evap, and bools only_summer and
# is_n_hemisphere.  Computes running balance, adding each month's
# precip and removing evapotranspiration.  If only_summer, only use
# the summer months for the given hemisphere.
def compute_water_balance(precip, evap, only_summer, is_n_hemisphere):
    running_balance = 0.0
    if only_summer:
        if is_n_hemisphere:
            # Check only months 6, 7, and 8.
            for i in range(6, 9):
                running_balance += precip[i]
                running_balance -= evap[i]
        else:
            for i in [12, 1, 2]:
                running_balance += precip[i]
                running_balance -= evap[i]
    else:
        for i in range(1, 13):
            running_balance += precip[i]
            running_balance -= evap[i]
    return running_balance

# Run the Newhall simulation model given argument dataset, 
# waterholding capacity, fc (optional), and fcd (optional).
def run_simulation(dataset, water_holding_capacity=200, fc=FC, fcd=FCD):
    logger.debug("Running simulation: {}".format(dataset.get("name")))
    # Begin setting up the base values for the model.
    elevation = dataset.get("elevation")

    # The model does a lot of index-1 addressing of these lists.  
    # To compensate, fill the 0th item with a null.
    temperature = [None] + dataset.get("temperature")
    precip = [None] + dataset.get("precipitation")

    # Hack to keep a problematic region of code from running
    # twice for some datasets.  Hack forces the original model
    # behavior, quirks and all.
    hasRunAlready = False

    # Model operates in metric, convert units if needed.
    if not dataset.get("is_metric"):
        # Convert to meters using original model factor, 1ft = 0.3048m.
        elevation *= 0.305
        for i in range(1, 13):
            # Convert F to C, inches to millimeters.
            temperature[i] = 5.0/9.0 * (temperature[i] - 32)
            precip[i] = precip[i] * 25.4

    # Initialize aggregator calendars and var.
    upe = [None] + [0.0] * 12
    mpe = [None] + [0.0] * 12
    mwi = [None] + [0.0] * 12
    swi = 0.0

    # Original Source Line: 405

    # Check temps for months over 0 degrees C.  If so, store MWI value.
    # mwi = (temp/5)**1.514  If not, store zero.
    for i in range(1, 13):
        if temperature[i] > 0:
            mwi_val = (temperature[i] / 5) ** 1.514
            mwi.append(mwi_val)
            swi += mwi_val
        else:
            mwi.append(0)

    # Original Source Line: 425

    a = (0.000000675 * swi * swi * swi) - \
        (0.0000771 * swi * swi) + (0.01792 * swi) + 0.49239

    # Original Source Line: 430

    # Build upe list.
    for i in range(1, 13):
        if temperature[i] > 0:
            if temperature[i] < 26.5:
                a_base = 10 * (temperature[i] / swi)
                upe[i] = 16 * (a_base ** a)
            elif temperature[i] >= 38:
                upe[i] = 185.0
            else:
                for ki in range(1, 25):
                    kl = ki + 1
                    kk = ki
                    if temperature[i] > ZT[ki - 1] and temperature[i] < ZT[kl - 1]:
                        upe[i] = ZPE[kk - 1]
                        break

    # Original Source Line: 495
    if dataset.get("ns_hemisphere").upper() == "N":
        nrow = 0
        for i in range(1, 32):
            if dataset.get("latitude") < RN[i - 1]:
                break
            else:
                nrow += 1

        for i in range(1, 13):
            if upe[i] <= 0:
                continue
            else:
                mpe[i] = upe[i] * INZ[i - 1][nrow - 1]

    else:
        nrow = 0
        for i in range(1, 14):
            if dataset.get("latitude") < RS[i - 1]:
                break
            else:
                nrow += 1

        if nrow > 0:
            for i in range(1, 13):
                if upe[i] <= 0:
                    continue
                elif nrow >= 13 or FS[i - 1][nrow - 1] == FS[i - 1][nrow]:
                    mpe[i] = upe[i] * FS[i - 1][nrow - 1]
                else:
                    cf = ((FS[i - 1][nrow] - FS[i - 1][nrow - 1]) * (((dataset.get("latitude_deg") - \
                        RS[nrow - 1]) * 60) + dataset.get("latitude_min"))) / \
                        ((RS[nrow] - RS[nrow - 1]) * 60)
                    cf += FS[i - 1][nrow - 1]
                    mpe[i] = upe[i] * cf
        else:
            nrow = 1
            for i in range(1, 13):
                if upe[i] <= 0:
                    continue
                else:
                    cf = (FS[i - 1][0] - INZ[i - 1][0]) * (dataset.get("latitude_deg") * 60 + \
                        dataset.get("latitude_min")) / 300
                    cf += INZ[i - 1][0]
                    mpe[i] = upe[i] * cf

    # Original Source Line: 140     
    
    arf = 0
    aev = 0
    for i in range(1, 13):
        arf += precip[i]
        aev += mpe[i]

    # GOSUB 660

    sumt = 0
    for i in range(1, 13):
        sumt += temperature[i]

    tma = sumt / 12 + fc
    at1 = (temperature[6] + temperature[7] + temperature[8]) / 3 + fc
    at2 = (temperature[1] + temperature[2] + temperature[12]) / 3 + fc

    st = 0
    wt = 0
    if dataset.get("ns_hemisphere").upper() == "N":
      st = at1
      wt = at2
    else:
      st = at2
      wt = at1

    dif = abs(at1 - at2)
    cs = dif * (1 - fcd) / 2

    # Original Source Line: 680

    # TEMPERATURE REGIME DETERMINATION

    # The cr[] dictionary holds the criteria used to determine temperature regimes.
    # The reg[] dictionary holds the flags for each regime.  The last-most
    # flag that registers true identifies the temperature regime.

    cr = {                                  # Criteria for regime determination:
        1: tma < 0,                         # Mean annual air temp (MAAT) < 0C.
        2: 0 <= tma and tma < 8,            # 0C <= MAAT <= 8C.
        3: (st - cs) < 15,                  # Summer temp ave minus (summer/winter difference * (1 - SOIL_AIR_REL) * 0.5) < 15C.
        7: (dif * fcd) > 5,                 # Summer/winter difference * SOIL_AIR_REL > 5.  Change to 6?
        8: (tma >= 8) and (tma < 15),       # 8C <= MAAT < 15C.
        9: (tma >= 15) and (tma < 22),      # 15C <= MAAT < 22C.
        10: tma >= 22,                      # 22C <= MAAT.
        11: tma < 8                         # MAAT < 8C.
    }

    reg = {                                 # Temperature regime type:
        1: cr[1],                           # Pergelic
        2: cr[2] and cr[3],                 # Cryic
        3: cr[11] and not cr[3] and cr[7],  # Frigid
        4: cr[8] and cr[7],                 # Mesic
        5: cr[9] and cr[7],                 # Thermic
        6: cr[10] and cr[7],                # Hyperthermic
        7: cr[11] and not cr[7] and \
            not cr[3],                      # Isofrigid
        8: cr[8] and not cr[7],             # Isomesic
        9: cr[9] and not cr[7],             # Isothermic
        10: cr[10] and not cr[7]            # Isohyperthermic
    }

    st -= cs
    wt += cs
    dif = st - wt

    # Original Source Line: 145

    # Set temperature regime.
    trr = ""
    for i in range(1, 11):
        if reg[i]:
            trr = TEMP_REGIMES[i - 1]
    
    # Original Source Line: 50 ("STORVAR5")

    whc = water_holding_capacity
    fsl = whc / 64
    sl = [0.0] * 65

    k = 1
    swst = 0
    swfi = 0

    ntwi = [0.0] * 4
    ntsu = [0.0] * 4
    nsd = [0.0] * 4
    nzd = [0.0] * 4
    nd = [0.0] * 4
    cc = [False] * 4

    cd = [0.0] * 6

    # Original Source Line: 300

    msw = -1
    sib = 0
    sir = 0.0
    x = 0
    swm = False
    max = 0
    icon = 0
    lt5c = 0
    lt8c = 0
    ie = 0
    ib = 1
    prmo = 0
    nccd = 0
    nccm = 0
    id8c = 0
    id5c = 0
    swt = 0
    tc = 0
    np = 0
    np8 = 0
    ncsm = 0
    ncwm = 0
    ncsp = 0
    ncwp = 0

    # Original Source Line: 360

    nbd = [0.0] * 7
    ned = [0.0] * 7
    nbd8 = [0.0] * 7
    ned8 = [0.0] * 7

    iday = [0] * 361

    swp = -1
    gogr = 0

    no_mpe_greater_than_precip = True
    for i in range(1, 13):
        if mpe[i] > precip[i]:
            no_mpe_greater_than_precip = False
            break
    if no_mpe_greater_than_precip:
        cd[5] = -1
        swt = -1

    for i in range(1, 11):
        for im in range(1, 13):
            zsw = 0
            lp = precip[im] / 2
            npe = (lp - mpe[im]) / 2
            if npe <= 0:
                npe = 0 - npe
            else:
                zsw = -1

            for i3 in range(1, 65):
                if zsw == 0:
                    nr = DP[i3 - 1]
                    if sl[nr] <= 0:
                        continue
                    else:
                        rpe = sl[nr] * DR[i3 - 1]
                        if npe <= rpe:
                            sl[nr] = sl[nr] - (npe / DR[i3 - 1])
                            npe = 0
                            break
                        else:
                            sl[nr] = 0
                            npe = npe - rpe
                            continue
                else:
                    if sl[i3] >= fsl:
                        continue
                    else:
                        esl = fsl - sl[i3]
                        if esl >= npe:
                            sl[i3] += npe
                            break
                        else:
                            sl[i3] = fsl
                            npe -= esl
                            continue

            hp = precip[im] / 2
            for i3 in range(1, 65):
                if sl[i3] >= fsl:
                    continue
                else:
                    esl = fsl - sl[i3]
                    if esl >= hp:
                        sl[i3] += hp
                        break
                    else:
                        sl[i3] = fsl
                        hp -= esl
                        continue

            # Original Source Line: 2750

            zsw = 0
            lp = precip[im] / 2
            npe = (lp - mpe[im]) / 2
            if npe <= 0:
                npe = 0 - npe
            else:
                zsw = -1

            # Original Source Line: 2770

            for i3 in range (1, 65):
                if zsw == 0:
                    nr = DP[i3 - 1]
                    if sl[nr] <= 0:
                        continue
                    else:
                        rpe = sl[nr] * DR[i3 - 1]
                        if npe <= rpe:
                            sl[nr] -= npe / DR[i3 - 1]
                            npe = 0
                            break
                        else:
                            sl[nr] = 0
                            npe -= rpe
                            continue
                else:
                    if sl[i3] >= fsl:
                        continue
                    else:
                        esl = fsl - sl[i3]
                        if esl >= npe:
                            sl[i3] = fsl
                            npe = npe - esl
                            continue

            # Continue for next value in im.
            continue

        # Original Source Line: 510

        tmoi = 0
        for it in range(1, 65):
            tmoi += sl[it]

        if abs(tmoi - prmo) < (prmo / 100):
            break
        else:
            prmo = tmoi
            continue

    # Original Source Line: 550
    # Build pc and cc boolean arrays.

    gogr = -1
    cc = [False] * 4
    pc = [False] * 7
    pc[1] = sl[9] <= 0
    pc[2] = sl[17] <= 0
    pc[3] = sl[25] <= 0

    cc[1] = pc[1] and pc[2] and pc[3]
    cc[2] = not cc[1] and (pc[1] or pc[2] or pc[3])

    pc[4] = sl[9] > 0
    pc[5] = sl[17] > 0
    pc[6] = sl[25] > 0

    cc[3] = pc[4] and pc[5] and pc[6]

    for i in range(1, 4):
        if cc[i]:
            k = i
            break

    # Original Source Line: 570 leading into GOSUB 1630
    # Run month loop.

    for im in range(1, 13):
        dmc = [0] * 4
        cc = [False] * 4

        zsw = 0
        dpmc = 0
        pmc = k
        igmc = 0

        lp = precip[im] / 2.0
        npe = (lp - mpe[im]) / 2.0
        cnpe = 0.0
        skipi3Loop = False

        if npe < 0:
            npe *= -1
            cnpe = npe
        elif npe == 0:
            skipi3Loop = True
        else:
            zsw = 01
            cnpe = npe

        # Original Source Line: 1670

        if not skipi3Loop:
            for i3 in range(1, 65):
                if zsw == 0:
                    if npe <= 0:
                        break
                    else:
                        nr = DP[i3 - 1]
                        if sl[nr] <= 0:
                            continue
                        else:
                            rpd = sl[nr] * DR[i3 - 1]
                            if npe <= rpd:
                                sl[nr] -= npe / DR[i3 - 1]
                                npe = 0
                            else:
                                sl[nr] = 0
                                npe -= rpd

                            # Original Source Line: 1750

                            cc = [False] * 4
                            pc = [False] * 7

                            pc[1] = sl[9] <= 0
                            pc[2] = sl[17] <= 0
                            pc[3] = sl[25] <= 0
                            cc[1] = pc[1] and pc[2] and pc[3]
                            cc[2] = not cc[1] and (pc[1] or pc[2] or pc[3])
                            pc[4] = sl[9] > 0
                            pc[5] = sl[17] > 0
                            pc[6] = sl[25] > 0
                            cc[3] = pc[4] and pc[5] and pc[6]

                            for i in range(1, 4):
                                if cc[i]:
                                    k = i
                                    break

                            kk = k
                            k = pmc
                            if kk == pmc:
                                continue

                            if npe <= 0:
                                break

                            rpe = cnpe - npe
                            dmc[k] = int(((15 * rpe) / cnpe) - dpmc)
                            igmc = dmc[k]
                            dpmc = dmc[k] + dpmc
                            dmc[k] = 0

                            ii = 0
                            mm = 0
                            ie += igmc
                            for i in range(ib, ie + 1):
                                iday[i] = k
                                if i > 30:
                                    ii = (i % 30) - 1
                                else:
                                    ii = i

                                # Original Source Line: 1990

                                mm = i / 30
                                if i % 30 == 0:
                                    mm -= 1

                                if ii == -1:
                                    ii = 29

                                if mm < 0:
                                    mm = 0

                            ib = ie + 1
                            nd[k] += igmc
                            pmc = kk
                            k = kk
                            continue

                # Original Source Line: 1680

                else:
                    if npe <= 0:
                        break
                    else:
                        if sl[i3] >= fsl:
                            continue
                        else:
                            esl = fsl - sl[i3]
                            if esl >= npe:
                                sl[i3] += npe
                                npe = 0
                            else:
                                sl[i3] = fsl
                                npe -= esl

                            cc = [False] * 4
                            pc = [False] * 7

                            pc[1] = sl[9] <= 0
                            pc[2] = sl[17] <= 0
                            pc[3] = sl[25] <= 0
                            cc[1] = pc[1] and pc[2] and pc[3]
                            cc[2] = not cc[1] and (pc[1] or pc[2] or pc[3])
                            pc[4] = sl[9] > 0
                            pc[5] = sl[17] > 0
                            pc[6] = sl[25] > 0
                            cc[3] = pc[4] and pc[5] and pc[6]

                            for i in range(1, 4):
                                if cc[i]:
                                    k = i
                                    break

                            kk = k
                            k = pmc
                            if kk == pmc:
                                continue

                            if npe <= 0:
                                break

                            rpe = cnpe - npe
                            dmc[k] = int(((15 * rpe) / cnpe) - dpmc)
                            igmc = dmc[k]
                            dpmc += dmc[k]
                            dmc[k] = 0

                            # Original Source Line: 1820 -> GOSUB 1960

                            ii = 0
                            mm = 0
                            ie += igmc

                            for i in range(ib, ie + 1):
                                iday[i] = k
                                if i > 30:
                                    ii = (i % 30) - 1
                                else:
                                    ii = ib
                                mm = i / 30
                                if i % 30 == 0:
                                    mm -= 1
                                if ii == -1:
                                    ii = 29
                                if mm < 0:
                                    mm = 0

                            ib = ie + 1
                            nd[k] += igmc
                            pmc = kk
                            k = kk
                            continue

        # Original Source Line: 1920
        # End of month loop.

        dmc[k] = 15 - dpmc
        igmc = dmc[k]
        dmc[k] = 0

        ii = 0
        mm = 0
        ie += igmc

        for i in range(ib, ie + 1):
            iday[i] = k
            if i > 30:
                ii = (i % 30) - 1
            else:
                ii = i
            # TODO: Remove 1990 dupes.
            mm = i / 30
            if i % 30 == 0:
                mm -= 1
            if ii == -1:
                ii = 29
            if mm < 0:
                mm = 0

        ib = ie + 1
        nd[k] += igmc

        hp = precip[im] / 2
        for i3 in range(1, 65):
            if sl[i3] >= fsl:
                continue
            else:
                esl = fsl - sl[i3]
                if esl >= hp:
                    sl[i3] += hp
                    break
                else:
                    sl[i3] = fsl
                    hp -= esl
                    continue

        # Original Source Line: 1630 - "Second Half"

        cc = [False] * 4
        pc = [False] * 7

        # TODO: Remove GOSUB 2880 duplications.

        pc[1] = sl[9] <= 0
        pc[2] = sl[17] <= 0
        pc[3] = sl[25] <= 0
        cc[1] = pc[1] and pc[2] and pc[3]
        cc[2] = not cc[1] and (pc[1] or pc[2] or pc[3])
        pc[4] = sl[9] > 0
        pc[5] = sl[17] > 0
        pc[6] = sl[25] > 0
        cc[3] = pc[4] and pc[5] and pc[6]

        for i in range(1, 4):
            if cc[i]:
                k = i
                break

        for i in range(i, 4):
            dmc[i] = 0
            cc[i] = False

        # TODO: Another repeat w/ i3 loop.

        zsw = 0
        dpmc = 0
        pmc = k

        lp = precip[im] / 2
        npe = (lp - mpe[im]) / 2
        cnpe = 0
        skipi3Loop = False

        if npe < 0:
            npe *= -1
            cnpe = npe
        elif npe == 0:
            skipi3Loop = True
        else:
            zsw = -1
            cnpe = npe

        if not skipi3Loop:
            for i3 in range(1, 65):
                if zsw == 0:
                    if npe <= 0:
                        break
                    else:
                        nr = DP[i3 - 1]
                        if sl[nr] <= 0:
                            continue
                        else:
                            rpd = sl[nr] * DR[i3 - 1]
                            if npe <= rpd:
                                sl[nr] -= npe / DR[i3 -1]
                                npe = 0
                            else:
                                sl[nr] = 0
                                npe -= rpd

                            cc = [False] * 4
                            pc = [False] * 7

                            pc[1] = sl[9] <= 0
                            pc[2] = sl[17] <= 0
                            pc[3] = sl[25] <= 0
                            cc[1] = pc[1] and pc[2] and pc[3]
                            cc[2] = not cc[1] and(pc[1] or pc[2] or pc[3])
                            pc[4] = sl[9] > 0
                            pc[5] = sl[17] > 0
                            pc[6] = sl[25] > 0
                            cc[3] = pc[4] and pc[5] and pc[6]

                            for i in range(1, 4):
                                if cc[i]:
                                    k = i
                                    break

                            kk = k
                            k = pmc
                            if kk == pmc:
                                continue
                            if npe <= 0:
                                break

                            rpe = cnpe - npe
                            dmc[k] = int(((15 * rpe) / cnpe) - dpmc)
                            igmc = dmc[k]
                            dpmc += dmc[k]
                            dmc[k] = 0

                            ii = 0
                            mm = 0
                            ie =+ igmc
                            for i in range(ib, ie + 1):
                                iday[i] = k
                                if i > 30:
                                    ii = (i % 30) - 1
                                else:
                                    ii = i
                                mm = i / 30
                                if i % 30 == 0:
                                    mm -= 1
                                if ii == -1:
                                    ii = 29
                                if mm < 0:
                                    mm = 0
                            ib = ie + 1
                            nd[k] += igmc

                            # Original Source Line: 1820 - GOSUB 1960
                            # Java Waypoint: 1115 in SimulationModel
                            # TODO: Many repeated regions, condense.

                            ii = 0
                            mm = 0
                            ie += igmc
                            for i in range(ib, ie + 1):
                                iday[i] = k
                                if i > 30:
                                    ii = (i % 30) - 1
                                else:
                                    ii = i
                                mm = i / 30
                                if i % 30 == 0:
                                    mm -= 1
                                if ii == -1:
                                    ii = 29
                                if mm < 0:
                                    mm = 0
                            ib = ie + 1
                            nd[k] =+ igmc
                            pmc = kk
                            k = kk
                            continue
                else:
                    if npe <= 0:
                        break
                    else:
                        if sl[i3] >= fsl:
                            continue
                        else:
                            esl = fsl - sl[i3]
                            if esl >= npe:
                                sl[i3] += npe
                                npe = 0
                            else:
                                sl[i3] = fsl
                                npe -= esl

                            cc = [False] * 4
                            pc = [False] * 7

                            pc[1] = sl[9] <= 0
                            pc[2] = sl[17] <= 0
                            pc[3] = sl[25] <= 0
                            cc[1] = pc[1] and pc[2] and pc[3]
                            cc[2] = not cc[1] and (pc[1] or pc[2] or pc[3])
                            pc[4] = sl[9] > 0
                            pc[5] = sl[17] > 0
                            pc[6] = sl[25] > 0
                            cc[3] = pc[4] and pc[5] and pc[6]

                            for i in range(1, 4):
                                if cc[i]:
                                    k = i
                                    break

                            kk = k
                            k = pmc
                            if kk == pmc:
                                continue
                            if npe <= 0:
                                break

                            rpe = cnpe - npe
                            dmc[k] = int(((15 * rpe) / cnpe) - dpmc)
                            igmc = dmc[k]
                            dpmc =+ dmc[k]
                            dmc[k] = 0

                            # Java Source: 1241

                            ii = 0
                            mm = 0
                            ie += igmc
                            for i in range(ib, ie + 1):
                                iday[i] = k
                                if i > 30:
                                    ii = (i % 30) - 1
                                else:
                                    ii = i
                                mm = i / 30
                                if (i % 30) == 0:
                                    mm -= 1
                                if ii == -1:
                                    ii = 29
                                if mm < 0:
                                    mm = 0
                            ib = ie + 1
                            nd[k] += igmc
                            pmc = kk
                            k = kk
                            continue

            # Java Source: 1280, end of i3 loop.

            dmc[k] = 15 - dpmc
            igmc = dmc[k]
            dmc[k] = 0

            ii = 0
            mm = 0
            ie += igmc
            for i in range(ib, ie + 1):
                iday[i] = k
                if i > 30:
                    ii = (i % 30) - 1
                else:
                    ii = i
                mm = i / 30
                if (i % 30) == 0:
                    mm -= 1
                if ii == -1:
                    ii = 29
                if mm < 0:
                    mm = 0
            ib = ie + 1
            nd[k] += igmc
            continue

    # Java Source: 1327

    sn = 0
    kj = 0
    ia = 0
    iz = 0
    nj = [0] * 14
    crr = 0.0
    c = [False] * 15
    tempUnderFive = False
    zwt = False

    for i in range(1, 13):
        if temperature[i] < 5:
            tempUnderFive = True
            break

    skipTo890 = False
    t13 = 0.0

    if tempUnderFive:
        t13 = temperature[1]
        for it in range(1, 12):
            if temperature[it] == 5 and temperature[it + 1] == 5:
                temperature[it] = 5.01
        if temperature[12] == 5 and t13 == 5:
            temperature[12] = 5.01
        
        crr = 5
        nj = [0] * 13
        zwt = False
        kj = 1
        ia = 30
        iz = 30

        # TODO: Determine why this exists.
        if crr != 8:
            ia = 36
            iz = 25

        for i in range (1, 13):
            c = [False] * 15

            m0 = i - 1
            m1 = i
            m2 = i + 1
            if m2 > 12:
                m2 -= 12
            if m0 < 1:
                m0 += 12

            c[1] = temperature[m1] < crr
            c[2] = temperature[m2] > crr
            c[3] = temperature[m0] < crr
            c[4] = temperature[m1] == crr
            c[5] = temperature[m2] > crr
            c[6] = temperature[m2] < crr
            c[7] = temperature[m1] > crr
            c[8] = temperature[m0] > crr
            c[9] = c[1] and c[2]
            c[10] = c[3] and c[4] and c[5]
            c[11] = c[9] or c[10]
            c[12] = c[6] and c[7]
            c[13] = c[8] and c[6] and c[4]
            c[14] = c[12] or c[13]

            if c[11]:
                nj[kj] = (m0 * 30) + ia + int((30 * (crr - 
                    temperature[m1]) / (temperature[m2] - temperature[m1])))
                if nj[kj] > 360:
                    nj[kj] -= 360
                kj += 1
                zwt = True
                continue
            elif c[14]:
                nj[kj] = (m0 * 30) + iz + int((30 * (temperature[m1] - 
                    crr)) / (temperature[m1] - temperature[m2]))
                if nj[kj] > 360:
                    nj[kj] -= 360
                    kj += 1
                    zwt = False
                continue
            else:
                continue

        if zwt:
            le = int(kj - 2)
            npro = int(nj[1])
            for i in range(1, le + 1):
                nj[i] = nj[i + 1]
            nj[le + 1] = npro

        # Original Source Line: 2700
        # Java Source Line: 1450

        npj = (kj - 1) / 2
        nbj = [0] * 7
        nej = [0] * 7
        for i in range(1, npj + 1):
            ib = 2 * i - 1
            ie = 2 * ib
            nbj[i] = nj[ib]
            nej[i] = nj[ie]

        for i in range(1, 7):
            nbd[i] = nbj[i]
            ned[i] = nej[i]

        np = npj
        tc = -1
        jb = 0
        ir = 0.0
        jr = 0.0
        je = 0.0

        if np == 0:
            if wt <= 5:
                lt5c = 0
                nbd[1] = -1
                id5c = 0
                for ik in range(1, 4):
                    nsd[ik] = 0
                tc = 0
                skipTo890 = True
        else:
            for i in range(1, np + 1):
                ib = int(nbd[i])
                if nbd[i] < ned[i]:
                    ir = ned[i] - nbd[i] + 1
                    jb = ib
                    jr = ir
                else:
                    ir = 361 - nbd[i] + ned[i]
                    jb = ib
                    jr = ir

                for ij in range(1, 4):
                    nzd[ij] = 0

                je = jb + jr - 1

                for l in range(jb, je + 1):
                    j = l
                    if j > 360:
                        j -= 360
                    ik = iday[j]
                    nzd[ik] += 1

                if not hasRunAlready:
                    for ic in range(1, 4):
                        nsd[ic] += nzd[ic]
                        hasRunAlready = True

                lt5c += ir

            id5c = nbd[1]
            skipTo890 = True

    if not skipTo890:
        tc = 0
        for ic in range(1, 4):
            nsd[ic] = nd[ic]
        lt5c = 360
        id5c = 0

    ncpm = [0] * 4
    tempUnder8C = False
    for ic in range(1, 13):
        if temperature[ic] < 8:
            tempUnder8C = True
            break

    if tempUnder8C:
        t13 = temperature[1]
        for it in range(1, 12):
            if temperature[it] == 8 and temperature[it + 1] == 8:
                temperature[it] = 8.01
        crr = 8
        if temperature[12] == 8 and t13 == 8:
            temperature[12] = 8.01

        nj = [0] * 13
        zwt = False
        kj = 1
        ia = 30
        iz = 30
        # TODO: Bridge this region with other crr-using region.
        if crr != 8:
            ia = 36
            iz = 25

        for i in range(1, 13):
            c = [False] * 15

            m0 = i - 1
            m1 = i
            m2 = i + 1
            if m2 > 12:
                m2 -= 12
            if m0 < 1:
                m0 += 12

            c[1] = temperature[m1] < crr
            c[2] = temperature[m2] > crr
            c[3] = temperature[m0] < crr
            c[4] = temperature[m1] == crr
            c[5] = temperature[m2] > crr
            c[6] = temperature[m2] < crr
            c[7] = temperature[m1] > crr
            c[8] = temperature[m0] > crr
            c[9] = c[1] and c[2]
            c[10] = c[3] and c[4] and c[5]
            c[11] = c[9] or c[10]
            c[12] = c[6] and c[7]
            c[13] = c[8] and c[6] and c[4]
            c[14] = c[12] or c[13]

            if c[11]:
                nj[kj] = (m0 * 30) + ia + int((30 * (crr - 
                    temperature[m1]) / (temperature[m2] - temperature[m1])))
                if nj[kj] > 360:
                    nj[kj] -= 360
                kj += 1
                zwt = True
                continue
            elif c[14]:
                nj[kj] = (m0 * 30) + iz + int(((30 * (temperature[m1] - 
                    crr)) / (temperature[m1] - temperature[m2])))
                if nj[kj] > 360:
                    nj[kj] -= 360
                kj += 1
                zwt = False
                continue
            else:
                continue

        # Original Source Line: 2660

        if zwt:
            le = kj - 2
            npro = nj[1]
            for i in range(1, le + 1):
                nj[i] = nj[i + 1]
            nj[le + 1] = npro

        npj = int((kj - 1) / 2)
        nbj = [0] * 7
        nej = [0] * 7
        for i in range(i, npj + 1):
            ib = 2 * i - 1
            ie = 2 * i
            nbj[i] = nj[ib]
            nej[i] = nj[ie]

        for i in range(1, 7):
            nbd8[i] = nbj[i]
            ned8[i] = nej[i]

        np8 = npj
        tc = -1
        if np8 != 0:
            for i in range(1, np8 + 1):
                ib = int(nbd8[i])
                ir = 0.0
                if nbd8[i] < ned8[i]:
                    ir = ned8[i] - nbd8[i] + 1
                else:
                    ir = 361 - nbd8[i] + ned8[i]

                msw = 0
                sib = ib
                sir = ir
                x = 1
                swm = (msw != 0)

                ns = [0] * 5
                ns[x] = 0
                ifin = 0
                sw = 0
                si = 0
                max = 0
                siz = sib + sir - 1

                # Java Source Line: 1745

                for n in range(sib, siz + 1):
                    n1 = n + 1
                    if n1 > 360:
                        n1 -= 360
                    if n > 360:
                        si = n - 360
                    else:
                        si = n

                    if swm:
                        if iday[si] == x:
                            if iday[si] != iday[n1]:
                                if sw != 0:
                                    ns[x] += 1
                                    if ns[x] > max:
                                        max = ns[x]
                                    ns[x] = 0
                                    sw = 0
                                    continue
                                else:
                                    continue
                            else:
                                ns[x] += 1
                                sw = -1
                                continue
                        continue
                    else:
                        if iday[si] != x:
                            if iday[n1] == x:
                                if sw != 0:
                                    ns[x] += 1
                                    if ns[x] > max:
                                        max = ns[x]
                                    ns[x] = 0
                                    sw = 0
                                    continue
                                else:
                                    continue
                            else:
                                ns[x] += 1
                                sw = -1
                                continue
                        else:
                            continue

                if sw != 0:
                    ifin = ns[x]

                if ifin > max:
                    max = ifin

                icon = max
                if ncpm[2] > icon:
                    continue
                else:
                    ncpm[2] = icon
                    lt8c = int(ir)
                    id8c = int(nbd8[i])
                    continue

            # Major "i" loop complete, BASIC source line 1140.
            sn = -1
    else:
        # BASIC Source Line: 920 -> GOTO 1170
        msw = 0
        tc = -1
        lt8c = 360
        id8c = 0

    sib = 1
    sir = 720
    x = 1
    swm = (msw != 0)

    sib = ib
    sir = 120
    x = 1
    swm = (msw != 0)

    ns = [0] * 5
    ns[x] = 0
    ifin = 0
    sw = 0
    si = 0
    max = 0
    siz = sib + sir - 1

    for n in range(sib, siz + 1):
        n1 = n + 1
        while n1 > 360:
            n1 -= 360
        if n > 360:
            si = n - 360
        else:
            si = n

        if swm:
            if iday[si] == x:
                if iday[si] != iday[n1]:
                    if sw != 0:
                        ns[x] += 1
                        if ns[x] > max:
                            max = ns[x]
                        ns[x] = 0
                        sw = 0
                        continue
                    else:
                        continue
                else:
                    ns[x] += 1
                    sw = -1
                    continue
            else:
                continue
        else:
            if iday[si] != x:
                if iday[n1] == x:
                    if sw != 0:
                        ns[x] += 1
                        if ns[x] > max:
                            max = ns[x]
                        ns[x] = 0
                        sw = 0
                        continue
                    else:
                        continue
                else:
                    ns[x] += 1
                    sw = -1
                    continue
            else:
                continue

    if sw != 0:
        ifin = ns[x]

    if ifin > max:
        max = ifin

    # BASIC Source Line: GOSUB 2160 returns to 1190

    icon = max
    if icon > 360:
        icon = 360
    ncpm[1] = icon
    if sn == 0:
        ncpm[2] = ncpm[1]

    # Testing for Xeric moisture regime criteria.
    # Java source line: 2005

    sn = 0
    msw = -1
    ic = 0

    if dataset.get("ns_hemisphere").upper() == "N":
        ib = 181
        ic = 1
    else:
        ib = 1
        ic = 181

    sib = ib
    sir = 120
    x = 1
    swm = (msw != 0)

    ns = [0] * 5
    ns[x] = 0
    ifin = 0
    sw = 0
    si = 0
    max = 0
    siz = sib + sir - 1

    for n in range(sib, siz + 1):
        n1 = n + 1
        if n1 > 360:
            n1 -= 360
        if n > 360:
            si = n - 360
        else:
            si = n

        if swm:
            if iday[si] == x:
                if iday[si] != iday[n1]:
                    if sw != 0:
                        ns[x] += 1
                        if ns[x] > max:
                            max = ns[x]
                        ns[x] = 0
                        sw = 0
                        continue
                    else:
                        continue
                else:
                    ns[x] += 1
                    sw = -1
                    continue
            else:
                continue
        else:
            if iday[si] != x:
                if iday[n1] == x:
                    if sw != 0:
                        ns[x] += 1
                        if ns[x] > max:
                            max = ns[x]
                        ns[x] = 0
                        sw = 0
                        continue
                    else:
                        continue
                else:
                    ns[x] += 1
                    sw = -1
                    continue
            else:
                continue

    # Java source line: 2122

    if sw != 0:
        ifin = ns[x]
    if ifin > max:
        max = ifin

    nccd = max
    sib = ic
    sir = 120
    x = 3
    swm = (msw != 0)

    ns = [0] * 5
    ns[x] = 0
    sw = 0
    si = 0
    max = 0
    siz = sib + sir - 1

    # Java source: 2150

    for n in range(sib, siz + 1):
        n1 = n + 1
        if n1 > 360:
            n1 -= 360
        if n > 360:
            si = n - 360
        else:
            si = n

        if swm:
            if iday[si] == x:
                if iday[si] != iday[n1]:
                    if sw != 0:
                        ns[x] += 1
                        if ns[x] > max:
                            max = ns[x]
                        ns[x] = 0
                        sw = 0
                        continue
                    else:
                        continue
                else:
                    ns[x] += 1
                    sw = -1
                    continue
            else:
                continue
        else:
            if iday[si] != x:
                if iday[n1] == x:
                    if sw != 0:
                        ns[x] += 1
                        if ns[x] > max:
                            max = ns[x]
                        ns[x] = 0
                        sw = 0
                        continue
                    else:
                        continue
                else:
                    ns[x] += 1
                    sw = -1
                    continue
            else:
                continue

    if sw != 0:
        ifin = ns[x]
    if ifin > max:
        max = ifin

    # Original Source Line: GOSUB 2160 returns to 1290

    nccm = max
    tu = 0
    skipTo1420 = False

    if nd[3] == 360:
        ncsm = 180
        ncwm = 180
        ncsp = 180
        ncwp = 180
        ntsu[3] = 180
        ntwi[3] = 180
        skipTo1420 = True
    elif nd[1] == 360:
        skipTo1420 = True
    elif nd[1] == 0:
        tu = -1
        sib = ib
        x = 3
        swm = True  # swm = tu != 0

        ns = [0] * 5
        ns[x] = 0
        ifin = 0
        sw = 0
        si = 0
        max = 0
        siz = sib + sir - 1

        for n in range(sib, siz + 1):
            n1 = n + 1
            if n1 > 360:
                n1 -= 360
            if n > 360:
                si = n - 360
            else:
                si = n

            if swm:
                if iday[si] == x:
                    if iday[si] != iday[n1]:
                        if sw != 0:
                            ns[x] += 1
                            if ns[x] > max:
                                max = ns[x]
                            ns[x] = 0
                            sw = 0
                            continue
                        else:
                            continue
                    else:
                        ns[x] += 1
                        sw = -1
                        continue
                else:
                    continue
            else:
                if iday[si] != x:
                    if iday[n1] == x:
                        if sw != 0:
                            ns[x] += 1
                            if ns[x] > max:
                                max = ns[x]
                            ns[x] = 0
                            sw = 0
                            continue
                        else:
                            continue
                    else:
                        ns[x] += 1
                        sw = -1
                        continue
                else:
                    continue

        if sw != 0:
            ifin = ns[x]
        if ifin > max:
            max = ifin

        # Original Source Line: Return from GOSUB 2160

        ncsp = max
        sib = ic
        sir = 180
        swm = (tu != 0)

        ns = [0] * 5
        ns[x] = 0
        ifin = 0
        sw = 0
        si = 0
        max = 0
        siz = sib + sir - 1

        # Another n loop.

        for n in range(sib, siz + 1):
            n1 = n + 1
            if n1 > 360:
                n1 -= 360
            if n > 360:
                si = n - 360
            else:
                si = n

            if swm:
                if iday[si] == x:
                    if iday[si] != iday[n1]:
                        if sw != 0:
                            ns[x] += 1
                            if ns[x] > max:
                                max = ns[x]
                            ns[x] = 0
                            sw = 0
                            continue
                        else:
                            continue
                    else:
                        ns[x] += 1
                        sw = -1
                        continue
                else:
                    continue
            else:
                if iday[si] != x:
                    if iday[n1] == x:
                        if sw != 0:
                            ns[x] += 1
                            if ns[x] > max:
                                max = ns[x]
                            ns[x] = 0
                            sw = 0
                            continue
                        else:
                            continue
                    else:
                        ns[x] += 1
                        sw = -1
                        continue
                else:
                    continue

        if sw != 0:
            ifin = ns[x]
        if ifin > max:
            max = ifin

        ncwp = max

    else:
        # Original Source Line: 1330
        tu = 0
        sib = ib
        sir = 180
        x = 1
        swm = False

        ns = [0] * 5
        ns[x] = 0
        ifin = 0
        sw = 0
        si = 0
        max = 0
        siz = sib + sir - 1

        # Another n loop.
        for n in range(sib, siz + 1):
            n1 = n + 1
            if n1 > 360:
                n1 -= 360
            if n > 360:
                si = n - 360
            else:
                si = n

            if swm:
                if iday[si] == x:
                    if iday[si] != iday[n1]:
                        if sw != 0:
                            ns[x] += 1
                            if ns[x] > max:
                                max = ns[x]
                            ns[x] = 0
                            sw = 0
                            continue
                        else:
                            continue
                    else:
                        ns[x] += 1
                        sw = -1
                        continue
                else:
                    continue
            else:
                if iday[si] != x:
                    if iday[n1] == x:
                        if sw != 0:
                            ns[x] += 1
                            if ns[x] > max:
                                max = ns[x]
                            ns[x] = 0
                            sw = 0
                            continue
                        else:
                            continue
                    else:
                        ns[x] += 1
                        sw = -1
                        continue
                else:
                    continue
        # End of n loop.

        if sw != 0:
            ifin = ns[x]

        if ifin > max:
            max = ifin

        ncsm = max
        sib = ic

        # Java Source: 2631

        ns = [0] * 5
        ns[x] = 0
        ifin = 0
        sw = 0
        si = 0
        max = 0
        siz = sib + sir - 1

        # Another n loop.
        for n in range(sib, siz + 1):
            n1 = n + 1
            if n1 > 360:
                n1 -= 360
            if n > 360:
                si = n - 360
            else:
                si = n

            if swm:
                if iday[si] == x:
                    if iday[si] != iday[n1]:
                        if sw != 0:
                            ns[x] += 1
                            if ns[x] > max:
                                max = ns[x]
                            ns[x] = 0
                            sw = 0
                            continue
                        else:
                            continue
                    else:
                        ns[x] += 1
                        sw = -1
                        continue
                else:
                    continue
            else:
                if iday[si] != x:
                    if iday[n1] == x:
                        if sw != 0:
                            ns[x] += 1
                            if ns[x] > max:
                                max = ns[x]
                            ns[x] = 0
                            sw = 0
                            continue
                        else:
                            continue
                    else:
                        ns[x] += 1
                        sw = -1
                        continue
                else:
                    continue
        # End of n loop.

        if sw != 0:
            ifin = ns[x]
        if ifin > max:
            max = ifin
        ncwm = max

    # Original Source Line: 1400

    jb = 0
    jr = 0
    je = 0
    if not skipTo1420:
        jb = ib
        jr = 180
        nzd = [0.0] * 4
        je = jb + jr - 1

        for l in range(jb, je + 1):
            j = l
            if j > 360:
                j -= 360
            ik = iday[j]
            nzd[ik] += 1

        for i in range(1, 4):
            ntsu[i] = nzd[i]
            ntwi[i] = nd[i] + ntsu[i]

    # Actual model calendar is 360 days.
    ntd = [0] * 365

    if not tempUnder8C:
        # Fill calendar with 8's before mutating further,
        # if we have no temperatures under 8 degrees C.
        # Hacked to parallel original model logic.
        ntd = [8] * 365

    if tc != 0 or tu != 0:
        # Calculate and fill calendar.
        kl = "$-58" # Array of calendar values.
        kr = [0.0] * 25
        m = [0] * 25
        kt = 0

        if nbd[1] < 0 and nbd8[1] < 0:
            for i in range(1, 361):
                ntd[i] = kl[1]
        elif nbd[1] == 0 and nbd8[1] < 0:
            for i in range(1, 361):
                ntd[i] = kl[2]
        else:
            if nbd8[1] < 0:
                nbd8[1] = 0
            for i in range(1, 7):
                kr[i] = nbd[i]
                m[i] = 2
            for i in range(7, 13):
                kt = i - 6
                if ned[kt] != 0:
                    kr[i] = ned[kt] + 1
                    if kr[i] > 360:
                        kr[i] = 1
                    m[i] = 1

            for i in range(13, 19):
                kt = i - 12
                kr[i] = nbd8[kt]
                m[i] = 3

            for i in range(19, 25):
                kt = i - 18
                if ned8[kt] != 0:
                    kr[i] = ned8[kt] + 1
                    if kr[i] > 360:
                        kr[i] = 1
                    m[i] = 2

            nt = 23
            stt = 0
            itemp = 0.0
            itm = 0

            # Original Source Line: 3140

            for i in range(1, 24):
                stt = 0

                for j in range(1, nt + 1):
                    if not (kr[j] <= kr[j + 1]):
                        itemp = kr[j]
                        itm = m[j]
                        kr[j] = kr[j + 1]
                        m[j] = m[j + 1]
                        kr[j + 1] = itemp
                        m[j + 1] = itm
                        stt = -1

                if stt == 0:
                    break
                else:
                    nt -= 1

            ima = m[24]
            nul = 0

            for i in range(1, 25):
                if kr[i] == 0:
                    nul += 1

            kk = 0
            for i in range(1, 25):
                kk = i
                ipl = i + nul
                if ipl > 24:
                    break
                else:
                    kr[i] = kr[ipl]
                    m[i] = m[ipl]

            for i in range(kk, 25):
                kr[i] = 0

            if kr[1] != 1:
                ie = int(kr[1] - 1)
                for i in range(1, ie + 1):
                    ntd[i] = kl[ima]

            ns2 = 0
            nn = 24 - nul
            for i in range(1, nn + 1):
                ns2 = m[i]
                ib = int(kr[i])
                ie = int(kr[i + 1] - 1)
                if kr[i + 1] == 0:
                    ie = 360

                for j in range(ib, ie + 1):
                    ntd[j] = kl[ns2]

    # Regime determination time!
    # Original source line: 1430 -> GOSUB 3390

    ans = " "
    div = " "
    q = " "
    if swt != 0:
        ans = "Perudic"
        ncsm = 180
        ncwm = 180
        ncsp = 180
        ncwp = 180
        ntsu[3] = 180
        ntwi[3] = 180
    elif nsd[1] > (lt5c / 2) and ncpm[2] < 90:
        ans = "Aridic"
        if nd[1] == 360:
            q = "Extreme"
        elif ncpm[2] <= 45:
            q = "Typic"
        else:
            q = "Weak"
            div = ans
    elif tma < 22 and dif >= 5 and nccd >= 45 and nccm >= 45:
        ans = "Xeric"
        if nccd > 90:
            q = "Dry"
        else:
            q = "Typic"
        div = ans
    elif (nd[1] + nd[2]) < 90:
        ans = "Udic"
        if (nd[1] + nd[2]) < 30:
            q = "Typic"
            div = ans
        else:
            q = "Dry"
            if div < 5:
                div = "Tropudic"
            else:
                div = "Tempudic"
    elif trr != "Pergelic" and trr != "Cryic":
        ans = "Ustic"
        if div >= 5:
            div = "Tempustic"
            if nccm <= 45:
                q = "Typic"
            elif nccd > 45:
                q = "Xeric"
            else:
                q = "Wet"
        else:
            div = "Tropustic"
            if ncpm[2] < 180:
                q = "Aridic"
            elif ncpm[2] < 270:
                q = "Typic"
            else:
                q = "Udic"
    else:
        ans = "Undefined"
        div = ans

    # Original source line: Return from GOSUB 3390

    # Calculate water balances for year/summer.
    awb = compute_water_balance(precip, mpe, False, 
        dataset.get("ns_hemisphere") == "N")
    swb = compute_water_balance(precip, mpe, True, 
        dataset.get("ns_hemisphere") == "N")

    rr_dict = {
        "annual_rainfall": arf,
        "water_holding_capacity": whc,
        "annual_water_balance": awb,
        "summer_water_balance": swb,
        "mean_potential_evapotranspiration": mpe[1:13],
        "days_dry_after_summer_solstice": nccd,
        "moist_days_after_winter_solstice": nccm,
        "num_cumulative_days_dry": nd[1],
        "num_cumulative_days_moist_dry": nd[2],
        "num_cumulative_days_moist": nd[3],
        "num_cumulative_days_dry_over_5c": nsd[1],
        "num_cumulative_days_moist_dry_over_5c": nsd[2],
        "num_cumulative_days_moist_over_5c": nsd[3],
        "num_consecutive_days_moist_someplaces": ncpm[1],
        "num_consecutive_days_moist_over_8c_someplaces": ncpm[2],
        "temperature_calendar": ntd[1:361],
        "moisture_calendar": iday[1:361],
        "temperature_regime": trr,
        "moisture_regime:": ans,
        "regime_subdivision_1": div,
        "regime_subdivision_2": q
    }

    debug_report = "=" * 20 + "RESULTS" + "=" * 20
    for key in rr_dict:
        debug_report += "\n{} = {}".format(key, rr_dict[key])
    logger.debug(debug_report)

    print nd

    return RunResult(dataset, rr_dict)