import os
import glob
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1 import make_axes_locatable



def plot_topo(ncfile, change=False, figsize=(10,5),time_index_start=0, time_index_end=-1, ax=None):
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
    time_index_stop : int
      Index of last (final) time dimension to plot [default: -1]
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
            ax.legend()


        else:
            p1 = ax.plot(x, zb[time_index_start,:]-zb[time_index_end,:], 'k-', label='Difference')
            ax.title('Elevation difference initial - final profile')
            ax.set_xlabel('Cross-shore distance [m]')
            ax.set_ylabel('Elevation difference [m]')            
        
        
    return ax

def plot_flux(ncfile, cum = True,figsize=(10,5), grid_cell=442, ax=None):
    '''Plot cumulated sediment flux from an AeoLiS result file
    
    Parameters
    ----------
    ncfile : str
      Path to AeoLiS result file
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
    
    with netCDF4.Dataset(ncfile, 'r') as ds:
        
        # get model output
        qs = np.squeeze(ds.variables['qs'][:,:,grid_cell])
        t = ds.variables['time'][:]
        
        #constants
        d = 2650 # Density sediement [kg/m3]
        p = 0.4 # Porosity [-]
        delta_t = t[1]-t[0] # Timestep [s]
        
        # Calculate volumetric flux [m3/m/s]
        volflux=(qs*delta_t)/(d*(1-p))
        cumvol=np.cumsum(volflux)
        
        # create figure
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        
        # plot flux
        if not cum:
            p1 = ax.plot(t/86400, volflux, 'k-', label='Volumetric flux')
            plt.title('Volumetric flux')
            ax.set_xlabel('Time [days]')
            ax.set_ylabel('Volumetric flux [m$^3$/m/s]')
            ax.legend()


        else:
            p1 = ax.plot(t/86400, cumvol, 'k-', label='Cumulative volumetric flux')
            plt.title('Cumulative volumetric flux')
            ax.set_xlabel('Time [days]')
            ax.set_ylabel('Cumulative volumetric flux [m$^3$/m]')
            ax.legend()          
        
        
    return ax

def plot_flux_compare(ncfile_orig, ncfile_new, cum = True,figsize=(10,5),grid_cell=442, ax=None):
    '''Plot cumulated sediment flux from an AeoLiS result file
    
    Parameters
    ----------
    ncfile_orig : str
      Path to AeoLiS result file - simulation without moisture processes
    ncfile_new : str
      Path to AeoLiS result file - simulation with moisture processes      
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
    
    with netCDF4.Dataset(ncfile_orig, 'r') as ds:
        
        # get model output
        qs = np.squeeze(ds.variables['qs'][:,:,grid_cell])
        t = ds.variables['time'][:]
        
    with netCDF4.Dataset(ncfile_new, 'r') as ds:
        
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
            p1 = ax.plot(t/86400, volflux, 'k-', label='Volumetric flux - no moisture')
            p2 = ax.plot(t_new/86400, volflux_new, 'r-', label='Volumetric flux - with moisture')
            plt.title('Volumetric flux')
            ax.set_xlabel('Time [days]')
            ax.set_ylabel('Volumetric flux [m$^3$/m/s]')
            ax.legend()


        else:
            p1 = ax.plot(t/86400, cumvol, 'k-', label='Volumetric flux - no moisture')
            p2 = ax.plot(t_new/86400, cumvol_new, 'r-', label='Volumetric flux - with moisture')
            plt.title('Cumulative volumetric flux')
            ax.set_xlabel('Time [days]')
            ax.set_ylabel('Cumulative volumetric flux [m$^3$/m]')
            ax.legend()          
        
        
    return ax


def plot_moisture_ave(ncfile, figsize=(10,5), ax=None):
    '''Plot average moisture content across profile from an AeoLiS result file
    
    Parameters
    ----------
    ncfile : str
      Path to AeoLiS result file
    figsize : 2-tuple, optional
      Dimensions of resulting figure
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
        moist = np.squeeze(ds.variables['moist'][...])
        moist_ave = np.average(moist,axis=0)

        # create figure
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        
        # plot bed levels and average moisture content
        p1 = plt.plot(x[:], zb[0,:],'k-')
        p2 = plt.scatter(x[:], zb[0,:], c=moist_ave[:], cmap = 'coolwarm_r')
        cbar = plt.colorbar()    
        cbar.set_label('Average moisture content [m$^3$/m$^3$]') 
        plt.title('Average moisture content')
        ax.set_xlabel('Cross-shore distance [m]')
        ax.set_ylabel('Elevation rel MSL [m]')
        plt.grid(True)
        
        
    return ax


def moisture_animation(ncfile, figsize=(10,5), ext='mp4', nframes=168):
    '''Animate the groundwater level and surface moisture content across profile from an AeoLiS result file
    
    Parameters
    ----------
    ncfile : str
      Path to AeoLiS result file
    figsize : 2-tuple, optional
      Dimensions of resulting figure
    ext : str, optional
      Extension of resulting video file [default: mp4]
    nframes : int, optional
      Number of frames to include in video
      
    Returns
    -------
    videofile : str
      Path to video file
      
    '''
    
    fig, ax = plt.subplots(figsize=figsize)

    
    with netCDF4.Dataset(ncfile, 'r') as ds:
        t = ds.variables['time'][:]
        x = np.squeeze(ds.variables['x'][:,:])
        zb = np.squeeze(ds.variables['zb'][...])
        moist = np.squeeze(ds.variables['moist'][...])
        gw =  np.squeeze(ds.variables['gw'][...])
        units = ds.variables['time'].units
        
    def update(i):
        ax.clear()
        p1 = ax.plot(x[:],gw[i,:], 'b-')
        p2 = plt.plot(x[:], zb[i,:],'k-')
        p3 = plt.scatter(x[:], zb[i,:], c=moist[i,:], cmap = 'coolwarm_r', vmin = 0, vmax = 0.4)
        ax.set_xlabel('Cross-shore distance [m]')
        ax.set_ylabel('Elevation rel MSL [m]')
        ax.set_title('Time =' + str(int(t[i]/3600)) + ' h')
        return p1,p2,p3

    
    if nframes is None:
        nframes = zb.shape[0]
    nframes = int(np.minimum(zb.shape[0], nframes))
    
    h = update(0)[2]
    # create colorbar
    cb = fig.colorbar(h)
    cb.set_label('Average moisture content [m$^3$/m$^3$]') 
    
    videofile = '%s.%s' % (os.path.splitext(ncfile)[0], ext)
    anim = FuncAnimation(fig, update, frames=nframes, interval=100)
    anim.save(videofile, dpi=150, writer='ffmpeg')

    return videofile