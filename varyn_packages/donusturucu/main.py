# Birim Dönüştürücü Kütüphanesi

def celcius_fahrenheit(c):
    return round((float(c) * 9.0 / 5.0) + 32.0, 2)

def fahrenheit_celcius(f):
    return round((float(f) - 32.0) * 5.0 / 9.0, 2)

def celcius_kelvin(c):
    return round(float(c) + 273.15, 2)

def km_mil(km):
    return round(float(km) * 0.621371, 2)

def mil_km(mil):
    return round(float(mil) / 0.621371, 2)

def kg_lbs(kg):
    return round(float(kg) * 2.20462, 2)

def lbs_kg(lbs):
    return round(float(lbs) / 2.20462, 2)

def bayt_donustur(bayt_sayisi, hedef_birim="MB"):
    b = float(bayt_sayisi)
    birim = str(hedef_birim).upper()
    if birim == "KB":
        return round(b / 1024.0, 2)
    elif birim == "MB":
        return round(b / (1024.0 ** 2), 2)
    elif birim == "GB":
        return round(b / (1024.0 ** 3), 2)
    elif birim == "TB":
        return round(b / (1024.0 ** 4), 2)
    return b

def plugin():
    return {
        "celcius_fahrenheit": celcius_fahrenheit,
        "fahrenheit_celcius": fahrenheit_celcius,
        "celcius_kelvin": celcius_kelvin,
        "km_mil": km_mil,
        "mil_km": mil_km,
        "kg_lbs": kg_lbs,
        "lbs_kg": lbs_kg,
        "bayt_donustur": bayt_donustur
    }
