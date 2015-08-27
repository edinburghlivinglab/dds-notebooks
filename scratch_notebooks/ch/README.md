A Leaflet.js map created with Folium and the default D3 threshold scale. See the [Gist](https://gist.github.com/wrobstory/5609830#file-choro_states-py) for the python code to generate the dataframe. The map was generated with the following Python code:

```python
map = folium.Map(location=[48, -102], zoom_start=3)
map.geo_json(geo_path=state_geo, data=state_data,
             columns=['State', 'Unemployment'],
             key_on='feature.id',
             fill_color='YlGn', fill_opacity=0.7, line_opacity=0.2,
             legend_name='Unemployment Rate (%)')
map.create_map(path='us_states.html')
```