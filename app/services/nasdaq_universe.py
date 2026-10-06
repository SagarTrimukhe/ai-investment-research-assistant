"""
NASDAQ Universe Catalog for Investment Research Assistant.
Contains 260+ prominent NASDAQ and US growth equities across Tech, Semiconductors,
Cloud/SaaS, Healthcare/Biotech, E-Commerce, Fintech, and Industrials.
"""

from typing import Dict, List, Optional
import re

NASDAQ_UNIVERSE: Dict[str, dict] = {
    # -------------------------------------------------------------
    # Mega-Cap Tech & Market Leaders
    # -------------------------------------------------------------
    "AAPL": {"name": "Apple Inc.", "sector": "Technology", "industry": "Consumer Electronics", "aliases": ["APPLE", "AAPL"]},
    "MSFT": {"name": "Microsoft Corporation", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["MICROSOFT", "MSFT"]},
    "NVDA": {"name": "NVIDIA Corporation", "sector": "Technology", "industry": "Semiconductors", "aliases": ["NVIDIA", "NVDA"]},
    "AMZN": {"name": "Amazon.com Inc.", "sector": "Consumer Cyclical", "industry": "Internet Retail", "aliases": ["AMAZON", "AMZN"]},
    "GOOGL": {"name": "Alphabet Inc. (Class A)", "sector": "Communication Services", "industry": "Internet Content & Information", "aliases": ["GOOGLE", "ALPHABET", "GOOGL"]},
    "GOOG": {"name": "Alphabet Inc. (Class C)", "sector": "Communication Services", "industry": "Internet Content & Information", "aliases": ["GOOGLE", "GOOG"]},
    "META": {"name": "Meta Platforms Inc.", "sector": "Communication Services", "industry": "Internet Content & Information", "aliases": ["META", "FACEBOOK"]},
    "TSLA": {"name": "Tesla Inc.", "sector": "Consumer Cyclical", "industry": "Auto Manufacturers", "aliases": ["TESLA", "TSLA"]},
    "AVGO": {"name": "Broadcom Inc.", "sector": "Technology", "industry": "Semiconductors", "aliases": ["BROADCOM", "AVGO"]},
    "ASML": {"name": "ASML Holding N.V.", "sector": "Technology", "industry": "Semiconductor Equipment", "aliases": ["ASML"]},

    # -------------------------------------------------------------
    # Semiconductors & Chip Equipment
    # -------------------------------------------------------------
    "AMD": {"name": "Advanced Micro Devices Inc.", "sector": "Technology", "industry": "Semiconductors", "aliases": ["AMD"]},
    "INTC": {"name": "Intel Corporation", "sector": "Technology", "industry": "Semiconductors", "aliases": ["INTEL", "INTC"]},
    "QCOM": {"name": "QUALCOMM Inc.", "sector": "Technology", "industry": "Semiconductors", "aliases": ["QUALCOMM", "QCOM"]},
    "AMAT": {"name": "Applied Materials Inc.", "sector": "Technology", "industry": "Semiconductor Equipment", "aliases": ["APPLIED MATERIALS", "AMAT"]},
    "TXN": {"name": "Texas Instruments Inc.", "sector": "Technology", "industry": "Semiconductors", "aliases": ["TEXAS INSTRUMENTS", "TXN"]},
    "LRCX": {"name": "Lam Research Corporation", "sector": "Technology", "industry": "Semiconductor Equipment", "aliases": ["LAM RESEARCH", "LRCX"]},
    "ADI": {"name": "Analog Devices Inc.", "sector": "Technology", "industry": "Semiconductors", "aliases": ["ANALOG DEVICES", "ADI"]},
    "KLAC": {"name": "KLA Corporation", "sector": "Technology", "industry": "Semiconductor Equipment", "aliases": ["KLA", "KLAC"]},
    "MRVL": {"name": "Marvell Technology Inc.", "sector": "Technology", "industry": "Semiconductors", "aliases": ["MARVELL", "MRVL"]},
    "NXPI": {"name": "NXP Semiconductors N.V.", "sector": "Technology", "industry": "Semiconductors", "aliases": ["NXP", "NXPI"]},
    "MCHP": {"name": "Microchip Technology Inc.", "sector": "Technology", "industry": "Semiconductors", "aliases": ["MICROCHIP", "MCHP"]},
    "ON": {"name": "ON Semiconductor Corp.", "sector": "Technology", "industry": "Semiconductors", "aliases": ["ON SEMICONDUCTOR", "ON"]},
    "MPWR": {"name": "Monolithic Power Systems", "sector": "Technology", "industry": "Semiconductors", "aliases": ["MONOLITHIC POWER", "MPWR"]},
    "ARM": {"name": "Arm Holdings plc", "sector": "Technology", "industry": "Semiconductors", "aliases": ["ARM HOLDINGS", "ARM"]},
    "SWKS": {"name": "Skyworks Solutions Inc.", "sector": "Technology", "industry": "Semiconductors", "aliases": ["SKYWORKS", "SWKS"]},
    "QRVO": {"name": "Qorvo Inc.", "sector": "Technology", "industry": "Semiconductors", "aliases": ["QORVO", "QRVO"]},
    "WDC": {"name": "Western Digital Corp.", "sector": "Technology", "industry": "Data Storage", "aliases": ["WESTERN DIGITAL", "WDC"]},
    "MU": {"name": "Micron Technology Inc.", "sector": "Technology", "industry": "Semiconductors", "aliases": ["MICRON", "MU"]},
    "SMCI": {"name": "Super Micro Computer Inc.", "sector": "Technology", "industry": "Computer Hardware", "aliases": ["SUPER MICRO", "SMCI"]},
    "TER": {"name": "Teradyne Inc.", "sector": "Technology", "industry": "Semiconductor Equipment", "aliases": ["TERADYNE", "TER"]},
    "MTSI": {"name": "MACOM Technology Solutions", "sector": "Technology", "industry": "Semiconductors", "aliases": ["MACOM", "MTSI"]},
    "LSCC": {"name": "Lattice Semiconductor", "sector": "Technology", "industry": "Semiconductors", "aliases": ["LATTICE", "LSCC"]},
    "CRUS": {"name": "Cirrus Logic Inc.", "sector": "Technology", "industry": "Semiconductors", "aliases": ["CIRRUS LOGIC", "CRUS"]},
    "DIOD": {"name": "Diodes Incorporated", "sector": "Technology", "industry": "Semiconductors", "aliases": ["DIODES", "DIOD"]},
    "POWI": {"name": "Power Integrations Inc.", "sector": "Technology", "industry": "Semiconductors", "aliases": ["POWER INTEGRATIONS", "POWI"]},
    "SLAB": {"name": "Silicon Laboratories Inc.", "sector": "Technology", "industry": "Semiconductors", "aliases": ["SILICON LABS", "SLAB"]},
    "RMBS": {"name": "Rambus Inc.", "sector": "Technology", "industry": "Semiconductors", "aliases": ["RAMBUS", "RMBS"]},
    "OLED": {"name": "Universal Display Corp.", "sector": "Technology", "industry": "Semiconductors", "aliases": ["UNIVERSAL DISPLAY", "OLED"]},
    "ACLS": {"name": "Axcelis Technologies Inc.", "sector": "Technology", "industry": "Semiconductor Equipment", "aliases": ["AXCELIS", "ACLS"]},

    # -------------------------------------------------------------
    # Enterprise Software, Cloud, AI & Cybersecurity
    # -------------------------------------------------------------
    "ADBE": {"name": "Adobe Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["ADOBE", "ADBE"]},
    "CRM": {"name": "Salesforce Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["SALESFORCE", "CRM"]},
    "INTU": {"name": "Intuit Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["INTUIT", "INTU"]},
    "NOW": {"name": "ServiceNow Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["SERVICENOW", "NOW"]},
    "PANW": {"name": "Palo Alto Networks Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["PALO ALTO", "PANW"]},
    "CRWD": {"name": "CrowdStrike Holdings Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["CROWDSTRIKE", "CRWD"]},
    "FTNT": {"name": "Fortinet Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["FORTINET", "FTNT"]},
    "SNPS": {"name": "Synopsys Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["SYNOPSYS", "SNPS"]},
    "CDNS": {"name": "Cadence Design Systems", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["CADENCE", "CDNS"]},
    "ADSK": {"name": "Autodesk Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["AUTODESK", "ADSK"]},
    "WDAY": {"name": "Workday Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["WORKDAY", "WDAY"]},
    "TEAM": {"name": "Atlassian Corporation", "sector": "Technology", "industry": "Software - Application", "aliases": ["ATLASSIAN", "TEAM"]},
    "DDOG": {"name": "Datadog Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["DATADOG", "DDOG"]},
    "ZS": {"name": "Zscaler Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["ZSCALER", "ZS"]},
    "MDB": {"name": "MongoDB Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["MONGODB", "MDB"]},
    "NET": {"name": "Cloudflare Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["CLOUDFLARE", "NET"]},
    "SNOW": {"name": "Snowflake Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["SNOWFLAKE", "SNOW"]},
    "PLTR": {"name": "Palantir Technologies Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["PALANTIR", "PLTR"]},
    "OKTA": {"name": "Okta Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["OKTA"]},
    "DOCU": {"name": "DocuSign Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["DOCUSIGN", "DOCU"]},
    "HUBS": {"name": "HubSpot Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["HUBSPOT", "HUBS"]},
    "DT": {"name": "Dynatrace Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["DYNATRACE", "DT"]},
    "PATH": {"name": "UiPath Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["UIPATH", "PATH"]},
    "ZM": {"name": "Zoom Video Communications", "sector": "Technology", "industry": "Software - Application", "aliases": ["ZOOM", "ZM"]},
    "DBX": {"name": "Dropbox Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["DROPBOX", "DBX"]},
    "TWLO": {"name": "Twilio Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["TWILIO", "TWLO"]},
    "FSLY": {"name": "Fastly Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["FASTLY", "FSLY"]},
    "BILL": {"name": "BILL Holdings Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["BILL COM", "BILL"]},
    "ESTC": {"name": "Elastic N.V.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["ELASTIC", "ESTC"]},
    "APP": {"name": "AppLovin Corporation", "sector": "Technology", "industry": "Software - Application", "aliases": ["APPLOVIN", "APP"]},
    "MANH": {"name": "Manhattan Associates Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["MANHATTAN ASSOCIATES", "MANH"]},
    "PTC": {"name": "PTC Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["PTC"]},
    "GWRE": {"name": "Guidewire Software Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["GUIDEWIRE", "GWRE"]},
    "MNDY": {"name": "monday.com Ltd.", "sector": "Technology", "industry": "Software - Application", "aliases": ["MONDAY", "MNDY"]},
    "CFLT": {"name": "Confluent Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["CONFLUENT", "CFLT"]},
    "GTLB": {"name": "GitLab Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["GITLAB", "GTLB"]},
    "SHOP": {"name": "Shopify Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["SHOPIFY", "SHOP"]},
    "GEN": {"name": "Gen Digital Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["GEN DIGITAL", "NORTON", "GEN"]},
    "CYBR": {"name": "CyberArk Software Ltd.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["CYBERARK", "CYBR"]},
    "TENB": {"name": "Tenable Holdings Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["TENABLE", "TENB"]},
    "QLYS": {"name": "Qualys Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["QUALYS", "QLYS"]},
    "VRNS": {"name": "Varonis Systems Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["VARONIS", "VRNS"]},
    "S": {"name": "SentinelOne Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["SENTINELONE"]},

    # -------------------------------------------------------------
    # Internet, E-Commerce, Media & Streaming
    # -------------------------------------------------------------
    "NFLX": {"name": "Netflix Inc.", "sector": "Communication Services", "industry": "Entertainment", "aliases": ["NETFLIX", "NFLX"]},
    "BKNG": {"name": "Booking Holdings Inc.", "sector": "Consumer Cyclical", "industry": "Travel Services", "aliases": ["BOOKING", "BKNG"]},
    "ABNB": {"name": "Airbnb Inc.", "sector": "Consumer Cyclical", "industry": "Travel Services", "aliases": ["AIRBNB", "ABNB"]},
    "DASH": {"name": "DoorDash Inc.", "sector": "Consumer Cyclical", "industry": "Internet Retail", "aliases": ["DOORDASH", "DASH"]},
    "SPOT": {"name": "Spotify Technology S.A.", "sector": "Communication Services", "industry": "Entertainment", "aliases": ["SPOTIFY", "SPOT"]},
    "MELI": {"name": "MercadoLibre Inc.", "sector": "Consumer Cyclical", "industry": "Internet Retail", "aliases": ["MERCADOLIBRE", "MELI"]},
    "SE": {"name": "Sea Limited", "sector": "Consumer Cyclical", "industry": "Internet Retail", "aliases": ["SEA LIMITED", "SHOPEE"]},
    "BABA": {"name": "Alibaba Group Holding", "sector": "Consumer Cyclical", "industry": "Internet Retail", "aliases": ["ALIBABA", "BABA"]},
    "JD": {"name": "JD.com Inc.", "sector": "Consumer Cyclical", "industry": "Internet Retail", "aliases": ["JD COM", "JD"]},
    "PDD": {"name": "PDD Holdings Inc.", "sector": "Consumer Cyclical", "industry": "Internet Retail", "aliases": ["PDD", "PINDUODUO", "TEMU"]},
    "BIDU": {"name": "Baidu Inc.", "sector": "Communication Services", "industry": "Internet Content & Information", "aliases": ["BAIDU", "BIDU"]},
    "EBAY": {"name": "eBay Inc.", "sector": "Consumer Cyclical", "industry": "Internet Retail", "aliases": ["EBAY"]},
    "ETSY": {"name": "Etsy Inc.", "sector": "Consumer Cyclical", "industry": "Internet Retail", "aliases": ["ETSY"]},
    "ROKU": {"name": "Roku Inc.", "sector": "Communication Services", "industry": "Entertainment", "aliases": ["ROKU"]},
    "PINS": {"name": "Pinterest Inc.", "sector": "Communication Services", "industry": "Internet Content & Information", "aliases": ["PINTEREST", "PINS"]},
    "SNAP": {"name": "Snap Inc.", "sector": "Communication Services", "industry": "Internet Content & Information", "aliases": ["SNAPCHAT", "SNAP"]},
    "MTCH": {"name": "Match Group Inc.", "sector": "Communication Services", "industry": "Internet Content & Information", "aliases": ["MATCH GROUP", "TINDER", "MTCH"]},
    "EXPE": {"name": "Expedia Group Inc.", "sector": "Consumer Cyclical", "industry": "Travel Services", "aliases": ["EXPEDIA", "EXPE"]},
    "TRIP": {"name": "TripAdvisor Inc.", "sector": "Consumer Cyclical", "industry": "Travel Services", "aliases": ["TRIPADVISOR", "TRIP"]},
    "ZG": {"name": "Zillow Group Inc.", "sector": "Communication Services", "industry": "Internet Content & Information", "aliases": ["ZILLOW", "ZG"]},
    "BMBL": {"name": "Bumble Inc.", "sector": "Communication Services", "industry": "Internet Content & Information", "aliases": ["BUMBLE", "BMBL"]},
    "CHWY": {"name": "Chewy Inc.", "sector": "Consumer Cyclical", "industry": "Internet Retail", "aliases": ["CHEWY", "CHWY"]},
    "CPNG": {"name": "Coupang Inc.", "sector": "Consumer Cyclical", "industry": "Internet Retail", "aliases": ["COUPANG", "CPNG"]},
    "W": {"name": "Wayfair Inc.", "sector": "Consumer Cyclical", "industry": "Internet Retail", "aliases": ["WAYFAIR"]},

    # -------------------------------------------------------------
    # Hardware, Networking & Systems
    # -------------------------------------------------------------
    "CSCO": {"name": "Cisco Systems Inc.", "sector": "Technology", "industry": "Communications Equipment", "aliases": ["CISCO", "CSCO"]},
    "ANET": {"name": "Arista Networks Inc.", "sector": "Technology", "industry": "Computer Hardware", "aliases": ["ARISTA", "ANET"]},
    "DELL": {"name": "Dell Technologies Inc.", "sector": "Technology", "industry": "Computer Hardware", "aliases": ["DELL"]},
    "HPE": {"name": "Hewlett Packard Enterprise", "sector": "Technology", "industry": "Technology Hardware", "aliases": ["HPE", "HEWLETT PACKARD"]},
    "ZBRA": {"name": "Zebra Technologies Corp.", "sector": "Technology", "industry": "Computer Hardware", "aliases": ["ZEBRA", "ZBRA"]},
    "LOGI": {"name": "Logitech International S.A.", "sector": "Technology", "industry": "Computer Hardware", "aliases": ["LOGITECH", "LOGI"]},
    "FFIV": {"name": "F5 Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["F5", "FFIV"]},
    "JNPR": {"name": "Juniper Networks Inc.", "sector": "Technology", "industry": "Communications Equipment", "aliases": ["JUNIPER", "JNPR"]},
    "NTAP": {"name": "NetApp Inc.", "sector": "Technology", "industry": "Computer Hardware", "aliases": ["NETAPP", "NTAP"]},
    "PSTG": {"name": "Pure Storage Inc.", "sector": "Technology", "industry": "Computer Hardware", "aliases": ["PURE STORAGE", "PSTG"]},
    "CIEN": {"name": "Ciena Corporation", "sector": "Technology", "industry": "Communications Equipment", "aliases": ["CIENA", "CIEN"]},
    "LITE": {"name": "Lumentum Holdings Inc.", "sector": "Technology", "industry": "Communications Equipment", "aliases": ["LUMENTUM", "LITE"]},
    "COHR": {"name": "Coherent Corp.", "sector": "Technology", "industry": "Communications Equipment", "aliases": ["COHERENT", "COHR"]},

    # -------------------------------------------------------------
    # Biotechnology, Pharmaceuticals & Healthcare Tech
    # -------------------------------------------------------------
    "AMGN": {"name": "Amgen Inc.", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["AMGEN", "AMGN"]},
    "VRTX": {"name": "Vertex Pharmaceuticals", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["VERTEX", "VRTX"]},
    "GILD": {"name": "Gilead Sciences Inc.", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["GILEAD", "GILD"]},
    "REGN": {"name": "Regeneron Pharmaceuticals", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["REGENERON", "REGN"]},
    "ISRG": {"name": "Intuitive Surgical Inc.", "sector": "Healthcare", "industry": "Medical Instruments & Supplies", "aliases": ["INTUITIVE SURGICAL", "ISRG"]},
    "BIIB": {"name": "Biogen Inc.", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["BIOGEN", "BIIB"]},
    "MRNA": {"name": "Moderna Inc.", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["MODERNA", "MRNA"]},
    "ILMN": {"name": "Illumina Inc.", "sector": "Healthcare", "industry": "Diagnostics & Research", "aliases": ["ILLUMINA", "ILMN"]},
    "DXCM": {"name": "DexCom Inc.", "sector": "Healthcare", "industry": "Medical Devices", "aliases": ["DEXCOM", "DXCM"]},
    "ALNY": {"name": "Alnylam Pharmaceuticals", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["ALNYLAM", "ALNY"]},
    "BMRN": {"name": "BioMarin Pharmaceutical", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["BIOMARIN", "BMRN"]},
    "EXAS": {"name": "Exact Sciences Corp.", "sector": "Healthcare", "industry": "Diagnostics & Research", "aliases": ["EXACT SCIENCES", "EXAS"]},
    "INCY": {"name": "Incyte Corporation", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["INCYTE", "INCY"]},
    "BGNE": {"name": "BeiGene Ltd.", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["BEIGENE", "BGNE"]},
    "TECH": {"name": "Bio-Techne Corp.", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["BIO-TECHNE", "TECH"]},
    "HOLX": {"name": "Hologic Inc.", "sector": "Healthcare", "industry": "Medical Instruments & Supplies", "aliases": ["HOLOGIC", "HOLX"]},
    "PODD": {"name": "Insulet Corporation", "sector": "Healthcare", "industry": "Medical Devices", "aliases": ["INSULET", "PODD"]},
    "ALGN": {"name": "Align Technology Inc.", "sector": "Healthcare", "industry": "Medical Instruments & Supplies", "aliases": ["ALIGN", "INVISALIGN", "ALGN"]},
    "EW": {"name": "Edwards Lifesciences Corp.", "sector": "Healthcare", "industry": "Medical Devices", "aliases": ["EDWARDS", "EW"]},
    "IDXX": {"name": "IDEXX Laboratories Inc.", "sector": "Healthcare", "industry": "Diagnostics & Research", "aliases": ["IDEXX", "IDXX"]},
    "BDX": {"name": "Becton Dickinson and Co.", "sector": "Healthcare", "industry": "Medical Instruments & Supplies", "aliases": ["BECTON DICKINSON", "BDX"]},
    "QDEL": {"name": "QuidelOrtho Corporation", "sector": "Healthcare", "industry": "Diagnostics & Research", "aliases": ["QUIDEL", "QDEL"]},
    "NTRA": {"name": "Natera Inc.", "sector": "Healthcare", "industry": "Diagnostics & Research", "aliases": ["NATERA", "NTRA"]},
    "CRSP": {"name": "CRISPR Therapeutics AG", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["CRISPR", "CRSP"]},
    "BEAM": {"name": "Beam Therapeutics Inc.", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["BEAM THERAPEUTICS", "BEAM"]},
    "ROIV": {"name": "Roivant Sciences Ltd.", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["ROIVANT", "ROIV"]},
    "ARGX": {"name": "argenx SE", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["ARGENX", "ARGX"]},
    "JAZZ": {"name": "Jazz Pharmaceuticals plc", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["JAZZ"]},
    "UTHR": {"name": "United Therapeutics Corp.", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["UNITED THERAPEUTICS", "UTHR"]},
    "HALO": {"name": "Halozyme Therapeutics Inc.", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["HALOZYME", "HALO"]},
    "SRPT": {"name": "Sarepta Therapeutics Inc.", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["SAREPTA", "SRPT"]},
    "RARE": {"name": "Ultragenyx Pharmaceutical", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["ULTRAGENYX", "RARE"]},
    "BBIO": {"name": "BridgeBio Pharma Inc.", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["BRIDGEBIO", "BBIO"]},
    "PCVX": {"name": "Vaxcyte Inc.", "sector": "Healthcare", "industry": "Biotechnology", "aliases": ["VAXCYTE", "PCVX"]},

    # -------------------------------------------------------------
    # Consumer Brands, Food, Beverages & Retail
    # -------------------------------------------------------------
    "COST": {"name": "Costco Wholesale Corp.", "sector": "Consumer Defensive", "industry": "Discount Stores", "aliases": ["COSTCO", "COST"]},
    "SBUX": {"name": "Starbucks Corporation", "sector": "Consumer Cyclical", "industry": "Restaurants", "aliases": ["STARBUCKS", "SBUX"]},
    "MDLZ": {"name": "Mondelez International", "sector": "Consumer Defensive", "industry": "Confectioners", "aliases": ["MONDELEZ", "MDLZ"]},
    "LULU": {"name": "Lululemon Athletica Inc.", "sector": "Consumer Cyclical", "industry": "Apparel Retail", "aliases": ["LULULEMON", "LULU"]},
    "MNST": {"name": "Monster Beverage Corp.", "sector": "Consumer Defensive", "industry": "Beverages - Non-Alcoholic", "aliases": ["MONSTER", "MNST"]},
    "KDP": {"name": "Keurig Dr Pepper Inc.", "sector": "Consumer Defensive", "industry": "Beverages - Non-Alcoholic", "aliases": ["KEURIG", "DR PEPPER", "KDP"]},
    "PEP": {"name": "PepsiCo Inc.", "sector": "Consumer Defensive", "industry": "Beverages - Non-Alcoholic", "aliases": ["PEPSI", "PEPSICO", "PEP"]},
    "ORLY": {"name": "O'Reilly Automotive Inc.", "sector": "Consumer Cyclical", "industry": "Specialty Retail", "aliases": ["OREILLY", "ORLY"]},
    "AZO": {"name": "AutoZone Inc.", "sector": "Consumer Cyclical", "industry": "Specialty Retail", "aliases": ["AUTOZONE", "AZO"]},
    "ROST": {"name": "Ross Stores Inc.", "sector": "Consumer Cyclical", "industry": "Apparel Retail", "aliases": ["ROSS STORES", "ROST"]},
    "DLTR": {"name": "Dollar Tree Inc.", "sector": "Consumer Defensive", "industry": "Discount Stores", "aliases": ["DOLLAR TREE", "DLTR"]},
    "ULTA": {"name": "Ulta Beauty Inc.", "sector": "Consumer Cyclical", "industry": "Specialty Retail", "aliases": ["ULTA", "ULTA BEAUTY"]},
    "TSCO": {"name": "Tractor Supply Company", "sector": "Consumer Cyclical", "industry": "Specialty Retail", "aliases": ["TRACTOR SUPPLY", "TSCO"]},
    "CELH": {"name": "Celsius Holdings Inc.", "sector": "Consumer Defensive", "industry": "Beverages - Non-Alcoholic", "aliases": ["CELSIUS", "CELH"]},
    "CMG": {"name": "Chipotle Mexican Grill", "sector": "Consumer Cyclical", "industry": "Restaurants", "aliases": ["CHIPOTLE", "CMG"]},
    "WEN": {"name": "The Wendy's Company", "sector": "Consumer Cyclical", "industry": "Restaurants", "aliases": ["WENDYS", "WEN"]},
    "DRI": {"name": "Darden Restaurants Inc.", "sector": "Consumer Cyclical", "industry": "Restaurants", "aliases": ["DARDEN", "OLIVE GARDEN", "DRI"]},
    "DPZ": {"name": "Domino's Pizza Inc.", "sector": "Consumer Cyclical", "industry": "Restaurants", "aliases": ["DOMINOS", "DPZ"]},
    "YUM": {"name": "Yum! Brands Inc.", "sector": "Consumer Cyclical", "industry": "Restaurants", "aliases": ["YUM BRANDS", "KFC", "TACO BELL", "YUM"]},
    "BBY": {"name": "Best Buy Co. Inc.", "sector": "Consumer Cyclical", "industry": "Specialty Retail", "aliases": ["BEST BUY", "BBY"]},
    "WMT": {"name": "Walmart Inc.", "sector": "Consumer Defensive", "industry": "Discount Stores", "aliases": ["WALMART", "WMT"]},
    "TGT": {"name": "Target Corporation", "sector": "Consumer Defensive", "industry": "Discount Stores", "aliases": ["TARGET", "TGT"]},
    "DG": {"name": "Dollar General Corp.", "sector": "Consumer Defensive", "industry": "Discount Stores", "aliases": ["DOLLAR GENERAL", "DG"]},
    "POOL": {"name": "Pool Corporation", "sector": "Consumer Cyclical", "industry": "Specialty Retail", "aliases": ["POOL CORP", "POOL"]},
    "FIVE": {"name": "Five Below Inc.", "sector": "Consumer Cyclical", "industry": "Specialty Retail", "aliases": ["FIVE BELOW", "FIVE"]},
    "HAS": {"name": "Hasbro Inc.", "sector": "Consumer Cyclical", "industry": "Leisure", "aliases": ["HASBRO", "HAS"]},
    "MAT": {"name": "Mattel Inc.", "sector": "Consumer Cyclical", "industry": "Leisure", "aliases": ["MATTEL", "MAT"]},
    "CROX": {"name": "Crocs Inc.", "sector": "Consumer Cyclical", "industry": "Footwear & Accessories", "aliases": ["CROCS", "CROX"]},
    "DECK": {"name": "Deckers Outdoor Corp.", "sector": "Consumer Cyclical", "industry": "Footwear & Accessories", "aliases": ["DECKERS", "UGG", "HOKA", "DECK"]},

    # -------------------------------------------------------------
    # Fintech, Payments, Exchanges & Financial
    # -------------------------------------------------------------
    "PYPL": {"name": "PayPal Holdings Inc.", "sector": "Financial Services", "industry": "Credit Services", "aliases": ["PAYPAL", "PYPL"]},
    "SQ": {"name": "Block Inc.", "sector": "Financial Services", "industry": "Credit Services", "aliases": ["BLOCK", "SQUARE", "SQ"]},
    "COIN": {"name": "Coinbase Global Inc.", "sector": "Financial Services", "industry": "Financial Data & Stock Exchanges", "aliases": ["COINBASE", "COIN"]},
    "HOOD": {"name": "Robinhood Markets Inc.", "sector": "Financial Services", "industry": "Financial Data & Stock Exchanges", "aliases": ["ROBINHOOD", "HOOD"]},
    "SOFI": {"name": "SoFi Technologies Inc.", "sector": "Financial Services", "industry": "Credit Services", "aliases": ["SOFI"]},
    "AFRM": {"name": "Affirm Holdings Inc.", "sector": "Financial Services", "industry": "Credit Services", "aliases": ["AFFIRM", "AFRM"]},
    "FISV": {"name": "Fiserv Inc.", "sector": "Financial Services", "industry": "Information Technology Services", "aliases": ["FISERV", "FISV"]},
    "FIS": {"name": "Fidelity National Information Services", "sector": "Financial Services", "industry": "Information Technology Services", "aliases": ["FIS"]},
    "GPN": {"name": "Global Payments Inc.", "sector": "Financial Services", "industry": "Information Technology Services", "aliases": ["GLOBAL PAYMENTS", "GPN"]},
    "MCO": {"name": "Moody's Corporation", "sector": "Financial Services", "industry": "Financial Data & Stock Exchanges", "aliases": ["MOODYS", "MCO"]},
    "MSCI": {"name": "MSCI Inc.", "sector": "Financial Services", "industry": "Financial Data & Stock Exchanges", "aliases": ["MSCI"]},
    "NDAQ": {"name": "Nasdaq Inc.", "sector": "Financial Services", "industry": "Financial Data & Stock Exchanges", "aliases": ["NASDAQ", "NDAQ"]},
    "CME": {"name": "CME Group Inc.", "sector": "Financial Services", "industry": "Financial Data & Stock Exchanges", "aliases": ["CME", "CHICAGO MERCANTILE"]},
    "ICE": {"name": "Intercontinental Exchange", "sector": "Financial Services", "industry": "Financial Data & Stock Exchanges", "aliases": ["ICE", "NYSE"]},
    "CBOE": {"name": "Cboe Global Markets Inc.", "sector": "Financial Services", "industry": "Financial Data & Stock Exchanges", "aliases": ["CBOE"]},
    "IBKR": {"name": "Interactive Brokers Group", "sector": "Financial Services", "industry": "Capital Markets", "aliases": ["INTERACTIVE BROKERS", "IBKR"]},
    "SEIC": {"name": "SEI Investments Co.", "sector": "Financial Services", "industry": "Asset Management", "aliases": ["SEI", "SEIC"]},
    "UPST": {"name": "Upstart Holdings Inc.", "sector": "Financial Services", "industry": "Credit Services", "aliases": ["UPSTART", "UPST"]},
    "LPLA": {"name": "LPL Financial Holdings", "sector": "Financial Services", "industry": "Capital Markets", "aliases": ["LPL FINANCIAL", "LPLA"]},
    "TOST": {"name": "Toast Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["TOAST", "TOST"]},
    "FICO": {"name": "Fair Isaac Corporation", "sector": "Technology", "industry": "Software - Application", "aliases": ["FAIR ISAAC", "FICO"]},

    # -------------------------------------------------------------
    # Industrials, Logistics, Transportation & Defense
    # -------------------------------------------------------------
    "FDX": {"name": "FedEx Corporation", "sector": "Industrials", "industry": "Integrated Freight & Logistics", "aliases": ["FEDEX", "FDX"]},
    "UPS": {"name": "United Parcel Service", "sector": "Industrials", "industry": "Integrated Freight & Logistics", "aliases": ["UPS"]},
    "ODFL": {"name": "Old Dominion Freight Line", "sector": "Industrials", "industry": "Trucking", "aliases": ["OLD DOMINION", "ODFL"]},
    "EXPD": {"name": "Expeditors International", "sector": "Industrials", "industry": "Integrated Freight & Logistics", "aliases": ["EXPEDITORS", "EXPD"]},
    "JBHT": {"name": "J.B. Hunt Transport Services", "sector": "Industrials", "industry": "Trucking", "aliases": ["JB HUNT", "JBHT"]},
    "CSX": {"name": "CSX Corporation", "sector": "Industrials", "industry": "Railroads", "aliases": ["CSX"]},
    "NSC": {"name": "Norfolk Southern Corp.", "sector": "Industrials", "industry": "Railroads", "aliases": ["NORFOLK SOUTHERN", "NSC"]},
    "UNP": {"name": "Union Pacific Corp.", "sector": "Industrials", "industry": "Railroads", "aliases": ["UNION PACIFIC", "UNP"]},
    "CPRT": {"name": "Copart Inc.", "sector": "Industrials", "industry": "Specialty Business Services", "aliases": ["COPART", "CPRT"]},
    "PCAR": {"name": "PACCAR Inc.", "sector": "Industrials", "industry": "Farm & Heavy Construction Machinery", "aliases": ["PACCAR", "PCAR"]},
    "FAST": {"name": "Fastenal Company", "sector": "Industrials", "industry": "Industrial Distribution", "aliases": ["FASTENAL", "FAST"]},
    "CTAS": {"name": "Cintas Corporation", "sector": "Industrials", "industry": "Specialty Business Services", "aliases": ["CINTAS", "CTAS"]},
    "PAYX": {"name": "Paychex Inc.", "sector": "Industrials", "industry": "Staffing & Employment Services", "aliases": ["PAYCHEX", "PAYX"]},
    "ADP": {"name": "Automatic Data Processing", "sector": "Industrials", "industry": "Staffing & Employment Services", "aliases": ["ADP"]},
    "URI": {"name": "United Rentals Inc.", "sector": "Industrials", "industry": "Rental & Leasing Services", "aliases": ["UNITED RENTALS", "URI"]},
    "BLDR": {"name": "Builders FirstSource Inc.", "sector": "Industrials", "industry": "Building Products & Equipment", "aliases": ["BUILDERS FIRSTSOURCE", "BLDR"]},
    "TT": {"name": "Trane Technologies plc", "sector": "Industrials", "industry": "Building Products & Equipment", "aliases": ["TRANE", "TT"]},
    "CARR": {"name": "Carrier Global Corp.", "sector": "Industrials", "industry": "Building Products & Equipment", "aliases": ["CARRIER", "CARR"]},
    "OTIS": {"name": "Otis Worldwide Corp.", "sector": "Industrials", "industry": "Specialty Industrial Machinery", "aliases": ["OTIS"]},
    "RIVN": {"name": "Rivian Automotive Inc.", "sector": "Consumer Cyclical", "industry": "Auto Manufacturers", "aliases": ["RIVIAN", "RIVN"]},
    "LCID": {"name": "Lucid Group Inc.", "sector": "Consumer Cyclical", "industry": "Auto Manufacturers", "aliases": ["LUCID", "LCID"]},
    "BLNK": {"name": "Blink Charging Co.", "sector": "Consumer Cyclical", "industry": "Specialty Retail", "aliases": ["BLINK CHARGING", "BLNK"]},
    "CHPT": {"name": "ChargePoint Holdings Inc.", "sector": "Consumer Cyclical", "industry": "Specialty Retail", "aliases": ["CHARGEPOINT", "CHPT"]},
    "PLUG": {"name": "Plug Power Inc.", "sector": "Industrials", "industry": "Electrical Equipment & Parts", "aliases": ["PLUG POWER", "PLUG"]},
    "AXON": {"name": "Axon Enterprise Inc.", "sector": "Industrials", "industry": "Aerospace & Defense", "aliases": ["AXON", "TASER"]},
    "HEI": {"name": "HEICO Corporation", "sector": "Industrials", "industry": "Aerospace & Defense", "aliases": ["HEICO", "HEI"]},
    "TDG": {"name": "TransDigm Group Inc.", "sector": "Industrials", "industry": "Aerospace & Defense", "aliases": ["TRANSDIGM", "TDG"]},
    "HII": {"name": "Huntington Ingalls Industries", "sector": "Industrials", "industry": "Aerospace & Defense", "aliases": ["HUNTINGTON INGALLS", "HII"]},

    # -------------------------------------------------------------
    # Telecom, Clean Tech, Energy & Utilities
    # -------------------------------------------------------------
    "CHTR": {"name": "Charter Communications", "sector": "Communication Services", "industry": "Telecom Services", "aliases": ["CHARTER", "SPECTRUM", "CHTR"]},
    "CMCSA": {"name": "Comcast Corporation", "sector": "Communication Services", "industry": "Telecom Services", "aliases": ["COMCAST", "XFINITY", "CMCSA"]},
    "TMUS": {"name": "T-Mobile US Inc.", "sector": "Communication Services", "industry": "Telecom Services", "aliases": ["T-MOBILE", "TMUS"]},
    "FSLR": {"name": "First Solar Inc.", "sector": "Technology", "industry": "Solar", "aliases": ["FIRST SOLAR", "FSLR"]},
    "SEDG": {"name": "SolarEdge Technologies", "sector": "Technology", "industry": "Solar", "aliases": ["SOLAREDGE", "SEDG"]},
    "RUN": {"name": "Sunrun Inc.", "sector": "Technology", "industry": "Solar", "aliases": ["SUNRUN", "RUN"]},
    "CEG": {"name": "Constellation Energy Corp.", "sector": "Utilities", "industry": "Utilities - Diversified", "aliases": ["CONSTELLATION", "CEG"]},
    "VST": {"name": "Vistra Corp.", "sector": "Utilities", "industry": "Utilities - Independent Power Producers", "aliases": ["VISTRA", "VST"]},
    "NEE": {"name": "NextEra Energy Inc.", "sector": "Utilities", "industry": "Utilities - Regulated Electric", "aliases": ["NEXTERA", "NEE"]},
    "SRE": {"name": "Sempra", "sector": "Utilities", "industry": "Utilities - Diversified", "aliases": ["SEMPRA", "SRE"]},
    "AEP": {"name": "American Electric Power", "sector": "Utilities", "industry": "Utilities - Regulated Electric", "aliases": ["AEP"]},
    "XEL": {"name": "Xcel Energy Inc.", "sector": "Utilities", "industry": "Utilities - Regulated Electric", "aliases": ["XCEL", "XEL"]},
    "ED": {"name": "Consolidated Edison Inc.", "sector": "Utilities", "industry": "Utilities - Regulated Electric", "aliases": ["CON ED", "ED"]},
    "ETR": {"name": "Entergy Corporation", "sector": "Utilities", "industry": "Utilities - Regulated Electric", "aliases": ["ENTERGY", "ETR"]},
    "FE": {"name": "FirstEnergy Corp.", "sector": "Utilities", "industry": "Utilities - Regulated Electric", "aliases": ["FIRSTENERGY", "FE"]},
    "WEC": {"name": "WEC Energy Group Inc.", "sector": "Utilities", "industry": "Utilities - Regulated Electric", "aliases": ["WEC ENERGY", "WEC"]},
    "ES": {"name": "Eversource Energy", "sector": "Utilities", "industry": "Utilities - Regulated Electric", "aliases": ["EVERSOURCE", "ES"]},
    "D": {"name": "Dominion Energy Inc.", "sector": "Utilities", "industry": "Utilities - Regulated Electric", "aliases": ["DOMINION", "D"]},
    "EXC": {"name": "Exelon Corporation", "sector": "Utilities", "industry": "Utilities - Regulated Electric", "aliases": ["EXELON", "EXC"]},

    # -------------------------------------------------------------
    # High-Growth Tech & Innovative Digital Platforms
    # -------------------------------------------------------------
    "AKAM": {"name": "Akamai Technologies Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["AKAMAI", "AKAM"]},
    "RNG": {"name": "RingCentral Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["RINGCENTRAL", "RNG"]},
    "SMAR": {"name": "Smartsheet Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["SMARTSHEET", "SMAR"]},
    "ASAN": {"name": "Asana Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["ASANA", "ASAN"]},
    "BOX": {"name": "Box Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["BOX INC", "BOX"]},
    "ZEN": {"name": "Zendesk Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["ZENDESK", "ZEN"]},
    "PAGS": {"name": "PagSeguro Digital Ltd.", "sector": "Financial Services", "industry": "Credit Services", "aliases": ["PAGSEGURO", "PAGS"]},
    "STNE": {"name": "StoneCo Ltd.", "sector": "Financial Services", "industry": "Credit Services", "aliases": ["STONECO", "STNE"]},
    "GLBE": {"name": "Global-e Online Ltd.", "sector": "Consumer Cyclical", "industry": "Internet Retail", "aliases": ["GLOBAL-E", "GLBE"]},
    "KNSL": {"name": "Kinsale Capital Group", "sector": "Financial Services", "industry": "Insurance - Property & Casualty", "aliases": ["KINSALE", "KNSL"]},
    "CRDO": {"name": "Credo Technology Group", "sector": "Technology", "industry": "Semiconductors", "aliases": ["CREDO", "CRDO"]},
    "IOT": {"name": "Samsara Inc.", "sector": "Technology", "industry": "Software - Infrastructure", "aliases": ["SAMSARA", "IOT"]},
    "CAVA": {"name": "CAVA Group Inc.", "sector": "Consumer Cyclical", "industry": "Restaurants", "aliases": ["CAVA"]},
    "DUOL": {"name": "Duolingo Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["DUOLINGO", "DUOL"]},
    "CART": {"name": "Maplebear Inc. (Instacart)", "sector": "Consumer Defensive", "industry": "Grocery Stores", "aliases": ["INSTACART", "CART"]},
    "KVYO": {"name": "Klaviyo Inc.", "sector": "Technology", "industry": "Software - Application", "aliases": ["KLAVIYO", "KVYO"]},
    "BIRK": {"name": "Birkenstock Holding plc", "sector": "Consumer Cyclical", "industry": "Footwear & Accessories", "aliases": ["BIRKENSTOCK", "BIRK"]},

    # -------------------------------------------------------------
    # Global Tech / Major Indian ADRs for continuity
    # -------------------------------------------------------------
    "INFY": {"name": "Infosys Limited", "sector": "Technology", "industry": "Information Technology Services", "aliases": ["INFOSYS", "INFY"]},
    "TCS": {"name": "Tata Consultancy Services", "sector": "Technology", "industry": "Information Technology Services", "aliases": ["TCS", "TATA"]},
    "RELIANCE": {"name": "Reliance Industries Limited", "sector": "Energy", "industry": "Oil & Gas Refining", "aliases": ["RELIANCE"]},
}


def get_nasdaq_universe() -> Dict[str, dict]:
    """Return the entire dictionary of 200+ tracked NASDAQ/growth stocks."""
    return NASDAQ_UNIVERSE


def get_nasdaq_tickers() -> List[str]:
    """Return a sorted list of all supported stock tickers."""
    return sorted(list(NASDAQ_UNIVERSE.keys()))


def get_nasdaq_company_name(ticker: str) -> str:
    """Return company name for ticker, defaulting to ticker itself."""
    info = NASDAQ_UNIVERSE.get(ticker.upper())
    return info["name"] if info else ticker.upper()


def detect_nasdaq_ticker(text: str) -> Optional[str]:
    """
    Robust ticker detection from filename, document header, or query text.
    Handles standard patterns like AAPL_10K.txt, 'Apple Inc', or standalone '$NVDA'.
    """
    if not text:
        return None
    
    clean_text = text.upper()

    # 1. Direct exact filename pattern e.g. NVDA_10K or AAPL_REPORT
    prefix_match = re.search(r"^([A-Z]{1,5})[_\-\s\.]", clean_text)
    if prefix_match:
        cand = prefix_match.group(1)
        if cand in NASDAQ_UNIVERSE:
            return cand

    # 2. Check full aliases and company names (longest match first)
    sorted_tickers = sorted(
        NASDAQ_UNIVERSE.items(),
        key=lambda item: max(len(a) for a in item[1].get("aliases", [item[0]])),
        reverse=True
    )
    for ticker, meta in sorted_tickers:
        for alias in meta.get("aliases", []):
            pattern = r"(?:\b|_)" + re.escape(alias) + r"(?:\b|_)"
            if re.search(pattern, clean_text):
                return ticker

    # 3. Fallback: check isolated words matching 2-5 letter tickers
    words = re.findall(r"\b[A-Z]{2,5}\b", clean_text)
    for word in words:
        if word in NASDAQ_UNIVERSE:
            return word

    return None
