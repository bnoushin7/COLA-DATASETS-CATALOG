import json
import os
import yaml
import pdb



def update_json(tags, html_page, dataset_sub_name):
    if tags is None:
        return
    jp = open("../tags_hrefs.json","r")
    data = json.load(jp)
    for tag in tags:
        addr = "https://kpegion.github.io/COLA-DATASETS-CATALOG/"+ html_page
        if tag in data:
            data[tag].append([dataset_sub_name, addr])
        else:
            data[tag] = [dataset_sub_name, addr]
    jp.close()
    jp = open("../tags_hrefs.json","w")
    json.dump(data,jp)
    jp.close()



def make_ancestors(ancestors, _type):
    #<!-- 1qaz2wsx -->
    
    try:
        ancestors = ancestors.replace("/day/day/","/day/")

    except:
        pass


    try:
        file_path = file_path.replace("/fx/fx/","/fx/")

    except:
        pass
    
    try:
        ancestors = ancestors.replace("/mon/Amon/","/mon/")

    except:
        pass



    try:
        ancestors = ancestors.replace("/mon/OImon/","/mon/")

    except:
        pass




    try:
        ancestors = ancestors.replace("/mon/Lmon/","/mon/")

    except:
        pass





    try:
        ancestors = ancestors.replace("/mon/LImon/","/mon/")

    except:
        pass





    try:
        ancestors = ancestors.replace("/mon/Omon/","/mon/")

    except:
        pass

    try:
        ancestors = ancestors.replace("/Ishii/Ishii/","/Ishii/")

    except:
        pass



    ancestors = ancestors.split('/')

    try:
        ancestors.remove('')
    except:
        pass

    """
    try:
        ancestors = ancestors.replace("/shared/","/reanalysis/")

    except:
        pass
    """

    # This is only made for CCI
    try:
        file_path = file_path.replace("/shared/land/CCI/","/cci/")

    except:
        pass
    # This is only made for CCI
    #try:
    #    file_path = file_path.replace("/shared/land/CCI/","obs/gridded/land/soil_moisture/cci/")

    #except:
    #    pass
    #try:
    #    ancestors.remove('shared')
    #except:
    #    pass

    try:
        ancestors.remove('data')

    except:
        pass

    try:
        ancestors.remove('DATA')

    except:
        pass
    #pdb.set_trace()
    ancestors = list(map(lambda x:x.lower(),ancestors))
    
    ans = []
    my_str = ""
    #print(ancestors)
    if _type:
    
        for i in range(len(ancestors)):
            if len(my_str)>0:
                my_str = my_str + '_'
            my_str = my_str + ancestors[i]
            ans.append(my_str)
        ancestors = ans
        
    res = ""
    for i in range(len(ancestors)):
        if ancestors[i] != "":
            res += "<li><a href="+ ancestors[i]+">"+ ancestors[i]+"</a></li>"
            res += "\n\n"

    return res

def catalog_parent( _path, _dataset_name, direct_parent):

    direct_parent = direct_parent + '.yaml'
    rel_path_direct_parent = "../intake-catalogs/" + direct_parent
    yaml_path = "{{CATALOG_DIR}}/"+ _dataset_name + ".yaml"
    try:
        yaml_path = yaml_path.replace("_*.nc.yaml",".yaml")    
    except:
        pass

    if not os.path.isfile(rel_path_direct_parent):

        dict_file = {
        'description': 'COLDA '+ direct_parent.replace('.yaml','').upper() + ' Data Caalog',
        'sources': {
        _dataset_name: {
            'args': {'path':yaml_path}, 
            'description':'', 
            'driver':'intake.catalog.local.YAMLFileCatalog', 
            'metadata':{}}}}
        with open(rel_path_direct_parent, 'w') as fp:
            yaml.dump(dict_file, fp)
            #todo print(direct_parent + " now created")
        
    else:
        
        with open(rel_path_direct_parent) as fp:
            newdct = yaml.load(fp, Loader=yaml.FullLoader)

        with open(rel_path_direct_parent, 'w') as fp:
            try:
                newdct['sources'][_dataset_name] = { 'args': {'path':yaml_path}, 'description':'', 'driver':'intake.catalog.local.YAMLFileCatalog', 'metadata':{}}
                yaml.dump(newdct, fp)
            #todo print(direct_parenupdated")
            except TypeError as e:
                print(e)



 



def link_to_children(child, dp_name):

    #try:
    #    child2 = child.replace("_.nc","")
    #except:
    #    child2 = child
    child2 = child 
    searchee = "<!--qazwsxxswzaq-->"
    res = """<a href="""+ "\""+ child+ "\""+""" class="list-group-item">
                    <h4>""" +child2+ """</h4>
                    <p class="description"> </p>
                </a> """
    #for MERRA-2 I have replaced shared with reanalysis    
    #dp_name = dp_name.replace('shared','reanalysis') 
    #pdb.set_trace() 


    dp_name = dp_name.replace("/shared/land/CCI/","/cci/")

    file_name = dp_name + ".html"
    print(file_name)
    fp = open('../'+file_name, "r+")
    fin = fp.read()

    if (fin.find(res) == -1): 
        res = res + "\n\n" + searchee
        data = fin.replace(searchee, res)
        fp.seek(0,0)
        fp.write(data)
    fp.close()

def gen_direct_parent(file_path):

    try:
        file_path = file_path.replace("/day/day/","/day/")

    except:
        pass


    try:
        file_path = file_path.replace("/fx/fx/","/fx/")

    except:
        pass
    
    try:
        file_path = file_path.replace("/mon/Amon/","/mon/")

    except:
        pass



    try:
        file_path = file_path.replace("/mon/OImon/","/mon/")

    except:
        pass



    try:
        file_path = file_path.replace("/mon/Lmon/","/mon/")

    except:
        pass


    try:
        file_path = file_path.replace("/mon/LImon/","/mon/")

    except:
        pass

    """
    try:
        ancestors = ancestors.replace("/shared/","/reanalysis/")

    except:
        pass
    
    # This is only made for CCI
    try:
        file_path = file_path.replace("/shared/land/CCI/","obs/gridded/land/soil_moisture/cci/")

    except:
        pass
    """
    # This is only made for CCI
    try:
        file_path = file_path.replace("/shared/land/CCI/","/cci/")

    except:
        pass
    try:
        file_path = file_path.replace("/mon/Omon/","/mon/")

    except:
        pass

    file_path = file_path.rstrip("\r")
    path_array = file_path.split('/')

    try:
        path_array.remove('')
    except:
        pass

    #try:
    #    path_array.remove('shared')
    #except:
    #    pass

    # This is only made for CCI
    """
    try:
        file_path = file_path.replace("/shared/land/CCI/","obs/gridded/land/soil_moisture/cci/")

    except:
        pass
    """
    # This is only made for CCI
    try:
        file_path = file_path.replace("/shared/land/CCI/","/cci/")

    except:
        pass
    try:
        path_array.remove('data')
    except:
        pass

    path_array = list(map(lambda x:x.lower(),path_array))
    

    ans = []
    my_str = ""
    for i in range(len(path_array)):
        if len(my_str)>0:
            my_str = my_str + '_'
        my_str = my_str + path_array[i]
        ans.append(my_str)

    return ans
