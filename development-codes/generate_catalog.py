import sys
import glob
import xarray as xr
import intake
import click
from framework import src_header
from framework import src_footer
from update import  update_json, make_ancestors, link_to_children, catalog_parent, gen_direct_parent
import os, re
import subprocess as S
@click.command()
@click.argument('file_path_name')
@click.argument('dataset_sub_name')
@click.argument('tags')

def generate_catalog(file_path_name, dataset_sub_name, tags):
    """
    FILE_NAME: If there are more than one file, FILE_NAME is the pattern for the NetCDF files, otherwise, Name of the NetCDF file. e.g.: 'air.mon.mean.nc' 

    DATASET_SUB_NAME: Name of the directory containing the NetCDf data files, e.g.: 'GHCN_CAMS'. If there is subdirectory like monthly, daily, etc., it should also be included and separated by "_".

    TAG: A dataset may need to be catalogued into multiple child catalogs, e.g.: "Atmosphere", "Temperature". Please keep the format consistent

    You can run the script proving three arguments like:

    python3.6 generate_catalog.py "/shared/obs/gridded/CPC-TEMP/tmax.*.nc" CPC-TEMP-tmax gridded,obs,atm,temperature

    """
    #print("Hi There")
    file_path_name = file_path_name.strip('""')
    real_path, fileName = os.path.split(file_path_name)
    path = (os.path.join(os.path.dirname('/shared/land/CCI'), os.readlink(real_path)))
    #print("1 :"+ file_path_name)
    #print("2 :"+ dataset_sub_name)
    #print("3: "+ tags)
    nfiles = len(glob.glob(file_path_name))
    # Set is_combine based on number of files
    if (nfiles > 1):
        is_combine= True
        print("More than one file###")
    else:
        print("one file###")
        is_combine= False

    temp = dataset_sub_name




    if int(is_combine) == True:
        # Read with xarray
        source = xr.open_mfdataset(file_path_name,combine='nested',concat_dim='time',decode_times=False)
        src = source
        # Use intake with xarray kwargs
        source = intake.open_netcdf(file_path_name,concat_dim='time',xarray_kwargs={'combine':'nested','decode_times':False})
        #source = intake.open_netcdf(file_path_name,concat_dim='time',xarray_kwargs={'combine':'nested'})
    else:
        source = intake.open_netcdf(file_path_name, xarray_kwargs={'decode_times':False})
        src = xr.open_dataset(file_path_name, decode_times=False)
        source.discover()
    dataset_sub_name = open(dataset_sub_name.strip('""')+ '.yaml', 'w')
    dataset_sub_name.write(source.yaml())
    dataset_sub_name.close()
    print(str(dataset_sub_name.name) + " was cataloged")


    dataset_sub_name = str(dataset_sub_name.name)[:-5]

    catalog_dir = "https://raw.githubusercontent.com/kpegion/COLA-DATASETS-CATALOG/gh-pages/intake-catalogs/"


            
    open_catalog = catalog_dir + temp +".yaml"

    try:
        title = src.attrs['title']

    except:
        title = dataset_sub_name

    try:
        url = src.attrs['References']
    except:
        url =""
    # Here url roles as the location
    url = real_path
    html_repr =xr.core.formatting_html.dataset_repr(src).replace('\\n', '\n')

    cmd = "ls -lrt --time-style=+%Y-%m-%d " + str(path) + " | tail -n 1"
    ps = S.Popen(cmd,shell=True,stdout=S.PIPE,stderr=S.STDOUT, universal_newlines=True)
    output = ps.communicate()[0]
    res = re.findall(r'\d{4}-\d{2}-\d{2}', output)
    time_stamp = ''.join(res)    
    print(path)
    print("-----------------------------------------")
    ancestors = make_ancestors(real_path, 1)


    ans = gen_direct_parent(real_path)


    #direct_parent = path.split('/')[-1].lower()
    direct_parent = ans[-1]
    # I did this for subx
    #link_to_children(dataset_sub_name, direct_parent)

    #catalog_parent(file_path_name, dataset_sub_name, direct_parent)

    _header = src_header(title, ancestors,  open_catalog, url, tags, open_catalog, time_stamp)

    tags =tags.split(',')
    _footer = src_footer()
    html_src = _header + html_repr + _footer
    #page_name = fileName.replace('*','').replace('..','.').replace('_.nc','')
    page_name = fileName.replace('*','').replace('..','.')
    #page_name = fileName.replace('*','').replace('..','.').replace('.nc','')
    page_name = re.sub(r"_\d{4,8}-\d{4,8}.nc", "", page_name)
    page_name = re.sub(r"\.\d{4,8}-\d{4,8}.nc", "", page_name)
    print(f'page name is {page_name}')
    print(f'direct parent is  {direct_parent}')
    
    link_to_children(page_name, direct_parent)
    html_page = page_name  + ".html"
    with open(html_page , "w", encoding='utf-8') as file:
        file.write(html_src)
    print( html_page + " was created\n")

    #update_json(tags, html_page, dataset_sub_name)

if __name__ == "__main__":
    generate_catalog()

