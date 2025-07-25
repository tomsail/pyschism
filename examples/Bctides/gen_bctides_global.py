import os
import pandas as pd
from datetime import datetime, timedelta
from pyschism.forcing.bctides import Tides

def get_earth_tidal_potential(start_date: datetime, rnday: float, constituents='all', database='fes2014'):
    tides = Tides(constituents=constituents, tidal_database=database)
    data = []

    for constituent in tides.get_active_potential_constituents():
        species_type, potential_amp, freq, nodal_factor, greenwich_arg = tides(start_date, rnday, constituent)
        data.append((constituent, species_type, potential_amp, freq, nodal_factor, greenwich_arg))

    return data

        
def write_bctides_in(filename: str, start_date: datetime, rnday: float, cut_off_depth=50.0, const = "all"):
    tidal_data = get_earth_tidal_potential(start_date, rnday, const)
    print(start_date, rnday, const)
    with open(filename, 'w') as f:
        f.write(f"!{start_date.strftime('%Y-%m-%d %H:%M:%S')} UTC\n")
        f.write(f"{len(tidal_data)} {cut_off_depth:.1f} !number of earth tidal potential, cut-off depth for applying tidal potential\n")
        for entry in tidal_data:
            f.write(f"{entry[0]}\n")
            species, amp, freq, nodal, greenwich = entry[1:]
            f.write(f" {species} {amp:.6f} {freq:.8E} {nodal:.5f} {greenwich:.4f}\n")
        f.write(f"{len(tidal_data)} !nbfr\n")

runs = pd.period_range("2021-11-30 0:0:0",periods=40,freq='30D')

if __name__ == '__main__':

  for run in runs:    
    start = run.start_time.to_pydatetime() #datetime(2022, 1, 1)
    rnday = 30
    bctypes = []
    outdir = f'./{run.__add__(timedelta(days = 5)).strftime("%Y%m")}'
    os.makedirs(outdir, exist_ok=True)
    write_bctides_in(f"{outdir}/bctides.in", start, rnday)