# JupyterHub as an OER Platform

In order to help
students with little or no programming experience to become comfortable
with basic data analysis and visualisation tasks, we have been
experimenting with a framework based on [IPython](http://ipython.org) and
[JupyterHub](https://github.com/jupyter/jupyterhub). This approach has
several attractive features:

* it offers a browser-based 'notebook' with support for rich text, 
executable code blocks and interactive data visualisation;
* it allows students to receive the same learning materials but experiment 
with them on an individual basis within a standardised environment;
* the components are all open source and actively maintained;
* since the platform is made available as a service, students are not 
required to download and install the necessary software; in additions we 
are able to ensure that all required libraries are present, together with 
any customisations that we want to make available.


## Interactive Visualization

One of the most attractive aspects of Jupyter notebooks is possibility of displaying inline data visualisation. We have chosen to address this area of functionality using two relatively new Python libraries, Bokeh and Folium.

[Bokeh](http://bokeh.pydata.org) is browser-based interactive visualization library that builds on the success of Javascript-based tools such as [D3.js](http://d3js.org),
like plots. It is designed to allow beautiful and versatile plots to be constructed on the basis of simple commands and aims to be scalable over big and streaming data sets. 

Using Bokeh, we have built sample notebooks which illustrate a variety of visualisations and plot types, including heatmaps, scatter plots, timeseries and binary trees. Advantages of Bokeh include: excellent integration with IPython; easy-to-use artist tools; access to inline Javascript for adding extra interactivity to plots;  widgets for controlling displays; good support for plot labels and hover tools.

[Folium](http://folium.readthedocs.org/) is a Python interface to [leaflet.js](http://leafletjs.com), a widely-used interactive Javascript mapping library.
This allows us to create attractive map visualizations with simple commands.  So far, we have used Folium for plotting geocoded data elements as markers on a map, together with information that displays on hover; and choropleth maps and Voronoi tessellations to visualise location-related datasets.


## Trial Service

We are using [Docker](https://www.docker.com/) to power a JupyterHub service, due to the success of the [Jessica Hamrick's JupyterHub deployment for
Computational Models of Cognition][hamrick]. However, rather than adopting their elastic cloud framework, we decided to start by running on a single server, and to postpone scaling up issues to later.

Docker allowed us to rapidly prototype the server
configuration, and keeping the configuration hierarchical. In
our server configuration repository, the huge stack of
scientific packages required to run the notebooks is contained in a
Dockerfile, so it's possible for motivated students to run their own
Jupyter instance independently on whatever computer they might like to use.
The same Dockerfile is then reused for the JupyterHub server
configurations. Working in this way, we can easily transfer the server to
new hardware, and build upon the work we've already done.

There are two main server configurations we've been working on. The first
is a centralised JupyterHub instance, in line with the standard
configuration described in the JupyterHub repository. Each student has a
persistent account with storage, and server instances will persist. Docker volumes are used to manage user home directories, allowing for seamless changes to apply to the entire operating system.
These are also used to link to datasets that the students can access at a
shared location inside the container.

In addition, we  also built a temporary notebook server which simply serves each new visitor a new notebook instance, and removes the instance after the user is
finished. 

Potentially, the service could be extended to include programming languages
beyond Python, as Jupyter is now agnostic to the language used in the
kernel. And, thanks to the dockerised development work, we could run
independent systems with different courses; or we are free to develop a
distributed system offering data science in the cloud to the entire
University.

[hamrick]: https://developer.rackspace.com/blog/deploying-jupyterhub-for-education/
[tmpnb]: tmphhhh://github.com/jupyter/tmpnb 

## Building a University-Wide Service

JuyterHub has a extendable authentication architecture that allows
deployments to override default authentication strategies with custom
Authenticator modules.  Authenticators already exist for popular identity
providers such as Github OAuth, Google OAuth and MediaWiki OAuth.  To
support institutional access at our university using a single sign-on
service based on the [CoSign](http://weblogin.org/) system, we are deploying JupyerHub behind an
Apache proxy server, allowing us to use existing Apache CoSign modules that
are well understood and supported by our institution. The Apache server provides a public-facing SSL port, which redirects requests to the JupyterHub server instance running on a private port on the
same virtual machine. 

  
