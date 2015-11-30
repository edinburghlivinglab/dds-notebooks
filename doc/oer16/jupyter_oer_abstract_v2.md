---
classoption: [twocolumn,twoside,a4paper]
bibliography: abstract.bib
csl: sage-harvard.xml

---

In order to help students with little or no programming experience to
become comfortable with basic data analysis and visualisation tasks, we
have been developing course content with [IPython](http://ipython.org) [@PER-GRA:2007].  IPython notebooks allow the user to work with rich text, 
executable code blocks and interactive data visualisation. Although the first iterations of IPython required users to download software on their own computers, 
[JupyterHub](https://github.com/jupyter/jupyterhub) [@JupyterHub] overcomes that barrier by allowing interactive notebooks to be made available as a service over the web. As a result, a group of students can all receive the same learning materials within a uniform programming environment, but can experiment with, and indeed modify, the materials on an individual basis. All the software for IPython and JupyterHub is open source and actively maintained.

One of the most attractive aspects of IPython notebooks is the possibility
of displaying inline data visualisation and for this we have
adopted two relatively new Python libraries, Bokeh and Folium, both of provide interfaces to interactive Javascript frameworks. 

[Bokeh](http://bokeh.pydata.org) is a
visualization library that builds on the success of tools
such as [D3.js](http://d3js.org). Using Bokeh, we have built
sample notebooks which illustrate a variety of visualisations and plot
types, including heatmaps, scatter plots, timeseries and binary trees. 

[Folium](http://folium.readthedocs.org/) is a Python interface to
[leaflet.js](http://leafletjs.com), a widely-used interactive `
mapping library and allows us to create attractive map visualizations.  So
far, we have used Folium for plotting geocoded data elements as markers on
a map; and choropleth maps and Voronoi tessellations to visualise
location-related datasets.

We are using [Docker](https://www.docker.com/) [@docker] to power our JupyterHub
service, following [Jessica Hamrick's JupyterHub deployment for
Computational Models of Cognition][hamrick]. 
Our initial deployment was on a single server, and after experimenting with various configurations, we are in the process of porting the service to a virtual machine that will be available across the university.

Our basic configuration is a standard, centralised JupyterHub instance.
Each student has a persistent account with storage, and server instances
will persist. Docker volumes are used to manage user home directories,
allowing for seamless changes to apply to the entire operating system.
These are also used to link to datasets that the students can access at a
shared location inside the container. 

JuyterHub has an extendable authentication architecture that allows
deployments to override default authentication strategies with custom
Authenticator modules. To support institutional access using a single
sign-on service based on the [CoSign](http://weblogin.org/) [@cosign] system, we are
deploying JupyerHub behind an Apache proxy server, using
well-understood Apache CoSign modules. 

[hamrick]: https://developer.rackspace.com/blog/deploying-jupyterhub-for-education/
[tmpnb]: tmphhhh://github.com/jupyter/tmpnb 

## References

  
