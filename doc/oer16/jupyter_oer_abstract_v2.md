---
title: 'JupterHub as an OER Platform'
author: ''
date: '30th November 2015'
classoption: [twocolumn,twoside,a4paper]
bibliography: abstract.bib
csl: sage-harvard.xml

---







In order to help students with little or no programming experience to
become comfortable with basic data analysis and visualisation tasks, we
have been developing course content with [IPython](http://ipython.org) [@PER-GRA:2007].  One of the most attractive components of the framework are browser-based 'notebooks' which offer support for rich text, 
executable code blocks and interactive data visualisation. Although the software for running IPython initially required users to download software on their own computers, 
[JupyterHub](https://github.com/jupyter/jupyterhub) [@JupyterHub] allows the notebooks to be made available as a service over the web. As a result, students receive the same learning materials, but can experiment with the materials on an individual basis. All the software for IPython and JupyterHub is open source and actively maintained.


One of the most attractive aspects of Jupyter notebooks is the possibility
of displaying inline data visualisation. We have chosen to address this
area using two relatively new Python libraries, Bokeh and Folium.

[Bokeh](http://bokeh.pydata.org) is a browser-based interactive
visualization library that builds on the success of Javascript-based tools
such as [D3.js](http://d3js.org). It is designed to allow beautiful and
versatile plots to be constructed on the basis of simple commands and aims
to be scalable over big and streaming data sets. Using Bokeh, we have built
sample notebooks which illustrate a variety of visualisations and plot
types, including heatmaps, scatter plots, timeseries and binary trees. 

[Folium](http://folium.readthedocs.org/) [@folium] is a Python interface to
[leaflet.js](http://leafletjs.com), a widely-used interactive Javascript
mapping library and allows us to create attractive map visualizations.  So
far, we have used Folium for plotting geocoded data elements as markers on
a map; and choropleth maps and Voronoi tessellations to visualise
location-related datasets.

We are using [Docker](https://www.docker.com/) [@docker] to power our JupyterHub
service, following [Jessica Hamrick's JupyterHub deployment for
Computational Models of Cognition][hamrick]. However, rather than adopting
an elastic cloud framework, we decided to start with a single server, and
to postpone scaling up issues to later.

Docker allowed us to rapidly prototype the server configuration, and to
keep the configuration hierarchical. We have built two server
configurations. The first is a standard, centralised JupyterHub instance.
Each student has a persistent account with storage, and server instances
will persist. Docker volumes are used to manage user home directories,
allowing for seamless changes to apply to the entire operating system.
These are also used to link to datasets that the students can access at a
shared location inside the container. In addition, we have built a
temporary notebook server which  serves each new visitor a new notebook
instance that is removed after the user terminates their session. 

JuyterHub has an extendable authentication architecture that allows
deployments to override default authentication strategies with custom
Authenticator modules. To support institutional access using a single
sign-on service based on the [CoSign](http://weblogin.org/) [@cosign] system, we are
deploying JupyerHub behind an Apache proxy server, allowing us to use
well-understood Apache CoSign modules. The Apache server provides a
public-facing SSL port, which redirects requests to the JupyterHub server
instance running on a private port on the same virtual machine. 

[hamrick]: https://developer.rackspace.com/blog/deploying-jupyterhub-for-education/
[tmpnb]: tmphhhh://github.com/jupyter/tmpnb 
  
