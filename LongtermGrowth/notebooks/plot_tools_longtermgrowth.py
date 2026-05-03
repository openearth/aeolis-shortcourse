from datetime import datetime, timedelta
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import netCDF4 as nc
import numpy as np


REF_DATE = datetime(1997, 9, 17, 0, 0)
MHW = 2.2  # Mean High Water elevation (m)

# Standard colors for Models A, B, C, D
MODEL_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']


def extract_netcdf(fname):
    """Load cross-shore profile data from an AeoLiS netCDF output file.

    Parameters
    ----------
    fname : str
        Path to netCDF output file

    Returns
    -------
    x : ndarray (nx,)
        Cross-shore coordinates
    zbi : ndarray (nx,)
        Initial bed level
    zbf : ndarray (nx,)
        Final bed level
    zb_all : ndarray (nt, nx)
        Bed level at all output times
    rhoveg_all : ndarray (nt, nx) or None
        Vegetation density at all output times (None if not in file)
    time : ndarray (nt,)
        Time in seconds from reference date
    dates : list of datetime
        Datetime objects for each output step
    """
    ds = nc.Dataset(fname, 'r')
    time = ds['time'][:]
    x = ds['x'][0, :]
    zbi = ds['zb'][0, 0, :]
    zbf = ds['zb'][-1, 0, :]
    zb_all = ds['zb'][:, 0, :]
    rhoveg_all = ds['rhoveg'][:, 0, :] if 'rhoveg' in ds.variables else None
    ds.close()
    dates = [REF_DATE + timedelta(seconds=float(t)) for t in time]
    return x, zbi, zbf, zb_all, rhoveg_all, time, dates


def _add_colorbar(fig, ax, dates):
    """Add a viridis time colorbar with year tick labels."""
    norm = mpl.colors.Normalize(vmin=0, vmax=len(dates) - 1)
    sm = mpl.cm.ScalarMappable(norm=norm, cmap=plt.cm.viridis)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, pad=0.02)
    cbar.set_label('Dates', fontsize=12, fontweight='bold')
    tick_locs = np.linspace(0, len(dates) - 1, min(6, len(dates))).astype(int)
    cbar.set_ticks(tick_locs)
    cbar.set_ticklabels([str(dates[i].year) for i in tick_locs])
    return cbar


def plot_profile_evolution(fname, mhw=MHW):
    """Plot cross-shore bed profile evolution colored by time (viridis).

    Each profile line is colored by the viridis colormap progressing from
    early (dark purple) to late (yellow).

    Parameters
    ----------
    fname : str
        Path to netCDF output file
    mhw : float
        Mean high water elevation (m) shown as a grey dashed reference line
    """
    x, _, _, zb_all, _, time, dates = extract_netcdf(fname)
    colors_arr = plt.cm.viridis(np.linspace(0, 1, len(time)))

    fig, ax = plt.subplots(figsize=(8, 5))
    for i in range(len(time)):
        ax.plot(x, zb_all[i, :], color=colors_arr[i])
    ax.axhline(y=mhw, color='grey', linestyle='--', label='Mean High Water')
    ax.set_ylabel('Elevation (m)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Cross-shore Distance (m)', fontsize=13, fontweight='bold')
    ax.grid()
    ax.legend(loc='upper left')
    _add_colorbar(fig, ax, dates)
    plt.tight_layout()
    return fig, ax


def plot_bed_change(fname):
    """Plot net bed-level change (final minus initial) with shading.

    Blue shading = deposition, red shading = erosion.

    Parameters
    ----------
    fname : str
        Path to netCDF output file
    """
    x, zbi, zbf, _, _, _, _ = extract_netcdf(fname)
    dz = zbf - zbi

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, dz, color='steelblue', linewidth=2)
    ax.axhline(0, color='k', linewidth=0.8, linestyle='--')
    ax.fill_between(x, dz, 0, where=(dz > 0),
                    color='steelblue', alpha=0.3, label='Deposition')
    ax.fill_between(x, dz, 0, where=(dz < 0),
                    color='salmon', alpha=0.5, label='Erosion')
    ax.set_ylabel('Bed-level Change (m)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Cross-shore Distance (m)', fontsize=13, fontweight='bold')
    ax.legend(loc='upper left')
    ax.grid()
    plt.tight_layout()
    return fig, ax


def plot_dune_growth(fname, dune_toe_elevation=4.4):
    """Plot the cross-shore location of the dune toe elevation over time.

    Parameters
    ----------
    fname : str
        Path to netCDF output file
    dune_toe_elevation : float, optional
        Elevation threshold for the dune toe. If None, uses the mean high
        water elevation constant `MHW`.
    """
    x, _, _, zb_all, _, _, dates = extract_netcdf(fname)

    toe_x = np.full(len(dates), np.nan)
    for i in range(len(dates)):
        profile = zb_all[i, :]
        ix = np.where(profile >= dune_toe_elevation)[0]
        if ix.size > 0:
            j = ix[0]
            if j == 0:
                toe_x[i] = x[0]
            else:
                x0, x1 = x[j - 1], x[j]
                z0, z1 = profile[j - 1], profile[j]
                if z1 != z0:
                    toe_x[i] = x0 + (dune_toe_elevation - z0) * (x1 - x0) / (z1 - z0)
                else:
                    toe_x[i] = x1

    years = [(d - dates[0]).days / 365.25 for d in dates]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(years, toe_x, color='steelblue', linewidth=2)
    ax.invert_yaxis()
    ax.set_xlabel('Time (years)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Dune Toe Cross-shore Location (m)', fontsize=13, fontweight='bold')
    ax.grid()
    plt.tight_layout()
    return fig, ax


def plot_vegetation_evolution(fname):
    """Plot vegetation density evolution colored by time (viridis).

    Parameters
    ----------
    fname : str
        Path to netCDF output file
    """
    x, _, _, _, rhoveg_all, time, dates = extract_netcdf(fname)
    if rhoveg_all is None:
        print(f'No vegetation output found in {os.path.basename(fname)}')
        return None, None
    colors_arr = plt.cm.viridis(np.linspace(0, 1, len(time)))

    fig, ax = plt.subplots(figsize=(8, 5))
    for i in range(len(time)):
        ax.plot(x, rhoveg_all[i, :], color=colors_arr[i])
    ax.set_ylabel('Vegetation Density (-)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Cross-shore Distance (m)', fontsize=13, fontweight='bold')
    ax.set_ylim([0, 1])
    ax.grid()
    _add_colorbar(fig, ax, dates)
    plt.tight_layout()
    return fig, ax
