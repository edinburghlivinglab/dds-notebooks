from IPython.display import HTML
import os

# Folium allows a link between leaflet and python
# which permits ease of use of tiles in notebook
# http://folium.readthedocs.org/en/latest/
# TODO: using requests contruct API which allows address display on map.
# You can see all the facilities folium allows here https://github.com/python-visualization/folium
# Crazy notebook visualizations from the creator of folium:
#     http://nbviewer.ipython.org/gist/wrobstory/1eb8cb704a52d18b9ee8/Up%20and%20Down%20PyData%202014.ipynb
# There are limitations using folium that do not allow the use of js-customized html maps like the one used 
# in TestMap within this directory. A way around it could be to hack folium (time consuming)
# but I am trying to get in contact with the creator to see how he worked around HTML reloading in notebook
 
def inline_map(map):
    """
    Embeds the HTML source of the map directly into the IPython notebook.
    
    This method will not work if the map depends on any files (json data). Also this uses
    the HTML5 srcdoc attribute, which may not be supported in all browsers.
    """
    map._build_map()
    return HTML('<iframe srcdoc="{srcdoc}" style="width: 100%; height: 510px; border: none"></iframe>'.format(srcdoc=map.HTML.replace('"', '&quot;')))
 
def embed_map(map, path="metadata/map.html"):
    """
    Embeds a linked iframe to the map into the IPython notebook.
    
    Note: this method will not capture the source of the map into the notebook.
    This method should work for all maps (as long as they use relative urls).
    """
    map.create_map(path=path)
    return HTML('<iframe src="files/{path}" style="width: 100%; height: 510px; border: none"></iframe>'.format(path=path))

def embed_cloropleth(map, path="metadata/map.html"):
    """
    Embeds a linked iframe to the map into the IPython notebook.
    
    Note: this method will not capture the source of the map into the notebook.
    This method should work for all maps (as long as they use relative urls).
    """
    map.create_map(path=path)
    os.popen("mv data.json metadata")
    os.popen("mv leaflet-dvf.markers.min.js metadata")
    return HTML('<iframe src="files/{path}" style="width: 100%; height: 510px; border: none"></iframe>'.format(path=path))