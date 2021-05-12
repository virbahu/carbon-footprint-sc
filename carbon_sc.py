import numpy as np
EMISSION_FACTORS={"truck_kg_per_tkm":0.062,"ocean_kg_per_tkm":0.008,"air_kg_per_tkm":0.602,
                  "rail_kg_per_tkm":0.022,"electricity_kg_per_kwh":0.42,"gas_kg_per_m3":2.0}
def product_footprint(stages):
    total=0; breakdown={}
    for stage in stages:
        co2=0
        if "transport" in stage:
            t=stage["transport"]; co2+=t["weight_t"]*t["distance_km"]*EMISSION_FACTORS[f"{t['mode']}_kg_per_tkm"]
        if "energy" in stage:
            e=stage["energy"]; co2+=e.get("electricity_kwh",0)*EMISSION_FACTORS["electricity_kg_per_kwh"]
            co2+=e.get("gas_m3",0)*EMISSION_FACTORS["gas_kg_per_m3"]
        if "process" in stage: co2+=stage["process"]
        breakdown[stage["name"]]=round(co2,2); total+=co2
    return {"total_kg_co2":round(total,2),"breakdown":breakdown,"per_unit":round(total/stages[0].get("units",1),3)}
if __name__=="__main__":
    stages=[{"name":"Raw Material","units":1000,"transport":{"weight_t":2,"distance_km":5000,"mode":"ocean"},"energy":{"electricity_kwh":500}},
            {"name":"Manufacturing","energy":{"electricity_kwh":2000,"gas_m3":100},"process":50},
            {"name":"Distribution","transport":{"weight_t":1.5,"distance_km":800,"mode":"truck"}}]
    print(product_footprint(stages))
