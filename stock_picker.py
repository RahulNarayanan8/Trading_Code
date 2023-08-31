
def normalize_metric(metric_value, is_positive):
    min_positive = 0
    max_positive = 100
    min_negative = 0
    max_negative = 100
    if is_positive:
        return (metric_value - min_positive) / (max_positive - min_positive) * 100
    else:
        return (max_negative - metric_value) / (max_negative - min_negative) * 100
def calculate_bullish_score(rg, nim, roe, dte, pe, pb, ps):
    weights = {
        "rg": 0.15,
        "nim": 0.15,
        "roe": 0.15,
        "dte": -0.1,
        "pe": -0.1,
        "pb": -0.1,
        "ps": -0.1,
    }
    normalized_scores = {
        "rg": normalize_metric(rg, True),
        "nim": normalize_metric(nim, True),
        "roe": normalize_metric(roe, True),
        "dte": normalize_metric(dte, False),
        "pe": normalize_metric(pe, False),
        "pb": normalize_metric(pb, False),
        "ps": normalize_metric(ps, False),
    }
    composite_score = sum(normalized_scores[metric] * weights[metric] for metric in weights)
    return composite_score


sp500_stocks = [
    "MMM", "ABT", "ABBV", "ACN", "ADBE", "AMD", "ALK", "ALGN",
    "AMZN", "AEP", "AXP", "AIG", "AMT", "ABC", "AMGN", "ADI", "AAPL",
    "AMAT", "ANET", "AJG", "T", "ADSK", "ADP", "AZO", "AVB", "BKR", "BAC",
    "BAX", "BIIB", "BLK", "BA", "BKNG", "BWA", "BXP", "BSX", "BMY", "BR",
    "BRCM", "BF.B", "CHRW", "COG", "CDNS", "CPB", "COF", "CAH", "KMX", "CCL",
    "CAT", "CBOE", "CBRE", "CBS", "CE", "CELG", "CNC", "CNP", "CTL", "CERN",
    "CF", "SCHW", "CHTR", "CVX", "CMG", "CB", "CI", "CINF", "CTAS", "CSCO",
    "C", "CFG", "CTXS", "CLX", "CME", "CMS", "KO", "CTSH", "CL", "CMCSA",
    "CMA", "CAG", "CXO", "COP", "ED", "STZ", "COO", "COST", "CCI", "CSX",
    "CMI", "CVS", "DHI", "DHR", "DIS", "DLTR", "D", "DOV", "DOW", "DTE", "DUK",
    "DRE", "DD", "DXC", "ETFC", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW", "EA",
    "EMR", "ETR", "EOG", "EQT", "EFX", "EQIX", "EQR", "ESS", "EL", "ETSY",
    "EVRG", "ES", "RE", "EXC", "EXPE", "EXPD", "EXR", "XOM", "FFIV", "FB",
    "FAST", "FRT", "FDX", "FIS", "FITB", "FE", "FRC", "FISV", "FLT", "FLIR",
    "FLS", "FMC", "F", "FTNT", "FTV", "FBHS", "FOXA", "FOX", "BEN", "FCX",
    "GPS", "GRMN", "IT", "GD", "GE", "GIS", "GM", "GPC", "GILD", "GL", "GPN",
    "GS", "GWW", "HAL", "HBI", "HIG", "HAS", "HCA", "PEAK", "HSIC", "HSY",
    "HES", "HPE", "HLT", "HFC", "HOLX", "HD", "HON", "HRL", "HST", "HPQ",
    "HUM", "HBAN", "HII", "IEX", "IDXX", "INFO", "ITW", "ILMN", "INCY", "IR",
    "INTC", "ICE", "IBM", "INCY", "IP", "IPG", "IFF", "INTU", "ISRG", "IVZ",
    "IPGP", "IQV", "IRM", "JKHY", "J", "JBHT", "SJM", "JNJ", "JCI", "JPM", "JNPR",
    "KSU", "K", "KEY", "KEYS", "KMB", "KIM", "KMI", "KLAC", "KHC", "KR", "LB",
    "LHX", "LH", "LRCX", "LW", "LVS", "LEG", "LDOS", "LEN", "LLY", "LNC",
    "LIN", "LYV", "LKQ", "LMT", "L", "LOW", "LUMN", "LYB", "MTB", "MRO", "MPC",
    "MKTX", "MAR", "MMC", "MLM", "MAS", "MA", "MXIM", "MKC", "MCD", "MCK",
    "MDT", "MRK", "MET", "MTD", "MGM", "MCHP", "MU", "MSFT", "MAA", "MHK",
    "TAP", "MDLZ", "MNST", "MCO", "MS", "MOS", "MSI", "MSCI", "MYL", "NDAQ",
    "NOV", "NTAP", "NFLX", "NWL", "NEM", "NWSA", "NWS", "NEE", "NLSN", "NKE",
    "NI", "NSC", "NTRS", "NOC", "NLOK", "NCLH", "NTRS", "NUE", "NVDA", "NVR",
    "NXPI", "ORLY", "OXY", "ODFL", "OMC", "OKE", "ORCL", "OTIS", "PCAR", "PKG",
    "PH", "PAYX", "PYPL", "PNR", "PBCT", "PEP", "PKI", "PRGO", "PFE", "PM",
    "PSX", "PNW", "PXD", "PNC", "PPG", "PPL", "PFG", "PG", "PGR", "PLD", "PRU",
    "PEG", "PSA", "PHM", "PVH", "QRVO", "PWR", "QCOM", "DGX", "RL", "RJF", "RTX",
    "O", "REG", "REGN", "RF", "RSG", "RMD", "RHI", "ROK", "ROL", "ROST", "RCL",
    "SPGI", "CRM", "SLB", "SMG", "SNPS", "SYY", "TMUS", "TTWO", "ALL", "BKT",
    "GS", "HIG", "HSY", "HES", "EL", "HD", "IPG", "SJM", "KHC", "KR", "LMT",
    "LUK", "MAS", "MDT", "MET", "MGM", "MSFT", "MU", "MYL", "NDAQ", "NOV",
    "NTAP", "NFLX", "NWL", "NEM", "NWSA", "NWS", "NEE", "NLSN", "NKE", "NI",
    "NSC", "NTRS", "NOC", "NLOK", "NCLH", "NTRS", "NUE", "NVDA", "NVR", "NXPI",
    "ORLY", "OXY", "ODFL", "OMC", "OKE", "ORCL", "OTIS", "PCAR", "PKG", "PH",
    "PAYX", "PYPL", "PNR", "PBCT", "PEP", "PKI", "PRGO", "PFE", "PM", "PSX",
    "PNW", "PXD", "PNC", "PPG", "PPL", "PFG", "PG", "PGR", "PLD", "PRU", "PEG",
    "PSA", "PHM", "PVH", "QRVO", "PWR", "QCOM", "DGX", "RL", "RJF", "RTX", "O",
    "REG", "REGN", "RF", "RSG", "RMD", "RHI", "ROK", "ROL", "ROST", "RCL",
    "SPGI", "CRM", "SLB", "SMG", "SNPS", "SYY", "TMUS", "TTWO", "USB", "UBER",
    "ULTA", "UNP", "UAL", "UPS", "UNH", "UHS", "UNM", "VFC", "VLO", "VAR", "VTR",
    "VZ", "VRTX", "VIAC", "V", "VNO", "VMC", "WBA", "WMT", "DIS", "WM", "WAT",
    "WEC", "WFC", "WELL", "WDC", "WAB", "WRK", "WY", "WHR", "WMB", "WLTW", "WYNN",
    "XEL", "XRX", "XLNX", "XYL", "YUM", "ZBH", "ZION"
]
composite_scores = []
import yfinance as yf
import time

for stock in sp500_stocks:
    try:
        data = yf.Ticker(stock)
        stock_information = data.info
        revenue_growth = stock_information["revenueGrowth"]
        net_income_margin = stock_information["profitMargins"]
        return_on_equity = stock_information["returnOnEquity"]
        debt_to_equity = stock_information["debtToEquity"]
        pe_ratio = stock_information["trailingPE"]
        pb_ratio = stock_information["priceToBook"]
        ps_ratio = stock_information["priceToSalesTrailing12Months"]
        composite_scores.append(calculate_bullish_score(revenue_growth, net_income_margin, return_on_equity, debt_to_equity, pe_ratio, pb_ratio, ps_ratio))
    except:
        pass
    


ordered_tickers = [x for _,x in sorted(zip(composite_scores,sp500_stocks))]


best_securities_dictionary = {}
for security, score in zip(ordered_tickers, sorted(composite_scores)):
    best_securities_dictionary[security] = score

print(best_securities_dictionary)
