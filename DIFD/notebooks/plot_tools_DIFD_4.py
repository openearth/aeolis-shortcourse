import os
import glob
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1 import make_axes_locatable



def plot_topo_fence(ncfile, change=False, figsize=(10,5),time_index_start=0, time_index_end=-1,sand_fence_loc=412, ax=None):
    '''Plot topography or the erosion/deposition from an AeoLiS result file with sand fence
    
    Parameters
    ----------
    ncfile : str
      Path to AeoLiS result file
    change : bool
      Plot bathymetric change rather than actual bathymetry
    figsize : 2-tuple, optional
      Dimensions of resulting figure
    time_index_start : int
      Index of first (initial) time dimension to plot [default: 0]
    time_index_end : int
      Index of last (final) time dimension to plot [default: -1]
    sand_fence_loc : int
      Grid cell where sand fence is located [default:402]
    ax : matplotlib.axes.SubplotAxis, optional
      Axis used for plotting, if not given a new figure is created
      
    Returns
    -------
    ax : matplotlib.axes.SubplotAxis
      plot axes objects
      
    '''
    
    with netCDF4.Dataset(ncfile, 'r') as ds:
        
        # get spatial dimensions and bed levels
        x = np.squeeze(ds.variables['x'][:,:])
        zb = np.squeeze(ds.variables['zb'][...])

        # create figure
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        
        # plot bed levels and bed level change
        if not change:
            p1 = ax.plot(x, zb[time_index_start,:], 'k-', label='Initial')
            p2 = ax.plot(x, zb[time_index_end,:], 'r-', label = 'Final')
            plt.title(['Initial and final profiles'])
            ax.set_xlabel('Cross-shore distance [m]')
            ax.set_ylabel('Elevation rel MSL [m]')
            plt.axvline(x=sand_fence_loc,color='g',linestyle='dashed')
            ax.legend()


        else:
            p1 = ax.plot(x, zb[time_index_start,:]-zb[time_index_end,:], 'k-', label='Difference')
            ax.title('Elevation difference initial - final profile')
            ax.set_xlabel('Cross-shore distance [m]')
            ax.set_ylabel('Elevation difference [m]')    
            plt.axvline(x=sand_fence_loc,color='g',linestyle='dashed')
        
        
    return ax

def plot_topo_veg(ncfile, change=False, figsize=(10,5),time_index_start=0, time_index_end=-1,veg_start= 402, veg_end=422, ax=None):
    '''Plot topography or the erosion/deposition from an AeoLiS result file
    
    Parameters
    ----------
    ncfile : str
      Path to AeoLiS result file
    change : bool
      Plot bathymetric change rather than actual bathymetry
    figsize : 2-tuple, optional
      Dimensions of resulting figure
    time_index_start : int
      Index of first (initial) time dimension to plot [default: 0]
    time_index_end : int
      Index of last (final) time dimension to plot [default: -1]
    veg_start : int
      Index of start of vegetation [default: 402]
    veg_stop : int
      Index of end of vegetation [default: 422]
    ax : matplotlib.axes.SubplotAxis, optional
      Axis used for plotting, if not given a new figure is created
      
    Returns
    -------
    ax : matplotlib.axes.SubplotAxis
      plot axes objects
      
    '''
    
    with netCDF4.Dataset(ncfile, 'r') as ds:
        
        # get spatial dimensions and bed levels
        x = np.squeeze(ds.variables['x'][:,:])
        zb = np.squeeze(ds.variables['zb'][...])

        # create figure
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        
        # plot bed levels and bed level change
        if not change:
            p1 = ax.plot(x, zb[time_index_start,:], 'k-', label='Initial')
            p2 = ax.plot(x, zb[time_index_end,:], 'r-', label = 'Final')
            plt.title(['Initial and final profiles'])
            ax.set_xlabel('Cross-shore distance [m]')
            ax.set_ylabel('Elevation rel MSL [m]')
            plt.axvline(x=veg_start,color='g',linestyle='dashed')
            plt.axvline(x=veg_end,color='g',linestyle='dashed')
            ax.legend()


        else:
            p1 = ax.plot(x, zb[time_index_start,:]-zb[time_index_end,:], 'k-', label='Difference')
            ax.title('Elevation difference initial - final profile')
            ax.set_xlabel('Cross-shore distance [m]')
            ax.set_ylabel('Elevation difference [m]')
            plt.axvline(x=veg_start,color='g',linestyle='dashed')
            plt.axvline(x=veg_end,color='g',linestyle='dashed')            
        
        
    return ax


def compare_flux(ncfile_fence, ncfile_veg, cum = True,figsize=(10,5),grid_cell=442, ax=None):
    '''Plot cumulated sediment flux from two AeoLiS result files
    
    Parameters
    ----------
    ncfile_fence : str
      Path to AeoLiS result file - simulation with sand fence
    ncfile_veg : str
      Path to AeoLiS result file - simulation with vegetation      
    cum : bool
      Plot cumulative flux
    figsize : 2-tuple, optional
      Dimensions of resulting figure
    grid_cell : int
      Index of gridcell to plot [default: 442; where the dike starts]
    ax : matplotlib.axes.SubplotAxis, optional
      Axis used for plotting, if not given a new figure is created
      
    Returns
    -------
    ax : matplotlib.axes.SubplotAxis
      plot axes objects
      
    '''
    
    with netCDF4.Dataset(ncfile_fence, 'r') as ds:
        
        # get model output
        qs = np.squeeze(ds.variables['qs'][:,:,grid_cell])
        t = ds.variables['time'][:]
        
    with netCDF4.Dataset(ncfile_veg, 'r') as ds:
        
        # get model output
        qs_new = np.squeeze(ds.variables['qs'][:,:,grid_cell])
        t_new = ds.variables['time'][:]
        
        #constants
        d = 2650 # Density sediement [kg/m3]
        p = 0.4 # Porosity [-]
        delta_t = t[1]-t[0] # Timestep [s]
        delta_t_new = t_new[1]-t_new[0]
        
        # Calculate volumetric flux [m3/m/s]
        volflux=(qs*delta_t)/(d*(1-p))
        cumvol=np.cumsum(volflux)
        
        volflux_new=(qs_new*delta_t)/(d*(1-p))
        cumvol_new=np.cumsum(volflux_new)
        
        # create figure
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        
        # plot flux
        if not cum:
            p1 = ax.plot(t/86400, volflux, 'k-', label='Volumetric flux - sand fence')
            p2 = ax.plot(t_new/86400, volflux_new, 'r-', label='Volumetric flux - vegetation')
            plt.title('Volumetric flux')
            ax.set_xlabel('Time [days]')
            ax.set_ylabel('Volumetric flux [m$^3$/m/s]')
            ax.legend()


        else:
            p1 = ax.plot(t/86400, cumvol, 'k-', label='Volumetric flux - sand fence')
            p2 = ax.plot(t_new/86400, cumvol_new, 'r-', label='Volumetric flux - vegetation')
            plt.title('Cumulative volumetric flux')
            ax.set_xlabel('Time [days]')
            ax.set_ylabel('Cumulative volumetric flux [m$^3$/m]')
            ax.legend()          
        
        
    return ax

def compare_topo(ncfile_fence, ncfile_veg,figsize=(10,5), time_step=-1,ax=None):
    '''Plot topographic development from two AeoLiS result files
    
    Parameters
    ----------
    ncfile_fence : str
      Path to AeoLiS result file - simulation with sand fence
    ncfile_veg : str
      Path to AeoLiS result file - simulation with vegetation      
    figsize : 2-tuple, optional
        Dimensions of resulting figure
    time_step : int
      Index of timestep to plot [default: -1; last timestep]
    ax : matplotlib.axes.SubplotAxis, optional
      Axis used for plotting, if not given a new figure is created
      
    Returns
    -------
    ax : matplotlib.axes.SubplotAxis
      plot axes objects
      
    '''
    
    with netCDF4.Dataset(ncfile_fence, 'r') as ds:
        
        # get spatial dimensions and bed levels
        x_fence = np.squeeze(ds.variables['x'][:,:])
        zb_veg = np.squeeze(ds.variables['zb'][...])
        
    with netCDF4.Dataset(ncfile_veg, 'r') as ds:
        
        # get spatial dimensions and bed levels
        x_veg = np.squeeze(ds.variables['x'][:,:])
        zb_veg = np.squeeze(ds.variables['zb'][...])
        
        
        # create figure
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        
        # plot flux
        p1 = ax.plot(x_fence, zb_fence[time_step,:], 'k-', label='Final profile - sand fence')
        p2 = ax.plot(x_veg, zb_veg[time_step,:], 'r-', label='Final profile - vegetation')
        plt.title('Final profile')
        ax.set_xlabel('Cross-shore distance [m]')
        ax.set_ylabel('Elevation rel MSL [m]')
        ax.legend()
        
        
    return ax