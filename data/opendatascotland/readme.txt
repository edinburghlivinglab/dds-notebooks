Deprivation: All Councils
=========================

Introduction
------------
This data kit was downloaded from http://simd.opendatascotland.org/releases/2012/councils

OpenDataScotland.org provides a showcase of what can be built on the Linked Open Data APIs available at http://data.opendatascotland.org

This kit provides some data downloads and queries to help you get started with working with the data.


Contents of this kit:
---------------------
/all_councils_deprivation_datakit
  -datakit_readme.txt
  /data
    /json|csv
      - all_councils_deprivation_ranks_2012.csv|json
      (csv/json files of the deprivation ranks for all data zones in 2012 for all deprivation domains)
     - most_deprived_datazones_by_council_(#{domain_name})_2012.csv|json
      (csv/json files showing the proportion of data zones per council in the most deprived 10%)
    /boundaries
      / data_zones_by_council
        (one topojson file per council, with boundaries for each data zone in the council, named according to the GSS code of the council)
      - all_councils_topo.json
        (a topojson file of all the council boundaries for Scotland)
      - all_data_zones_topo.json
        (a topojson file of all the data zone boundaries for Scotland)

Licence Information
-------------------
Data controlled by the Scottish Government is released under the Open Government Licence.
https://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/

Geographic boundaries and postcodes come courtesy of Ordnance Survey, under the The OS OpenData Licence.
http://www.ordnancesurvey.co.uk/docs/licences/os-opendata-licence.pdf

All Councils Deprivation Ranks
-----------------------------
The SPARQL query to generate the all_councils_deprivation_ranks_2012.csv|json file is:
PREFIX stats: <http://statistics.data.gov.uk/id/statistical-geography/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX simd: <http://data.opendatascotland.org/def/simd/>
PREFIX cube: <http://purl.org/linked-data/cube#>
PREFIX stats_dim: <http://data.opendatascotland.org/def/statistical-dimensions/>
PREFIX year: <http://reference.data.gov.uk/id/year/>

SELECT DISTINCT
?dz_label
?overall_rank
?income_deprivation_rank
?employment_deprivation_rank
?health_deprivation_rank
?education_deprivation_rank
?access_deprivation_rank
?housing_deprivation_rank
?crime_deprivation_rank

WHERE {

  GRAPH <http://data.opendatascotland.org/graph/simd/rank> {
    ?overall_rank_observation stats_dim:refArea ?dz .
    ?overall_rank_observation stats_dim:refPeriod year:2012 .
    ?overall_rank_observation simd:rank ?overall_rank .
  }

  GRAPH <http://data.opendatascotland.org/graph/simd/income-rank> {
    ?income_rank_observation stats_dim:refArea ?dz .
    ?income_rank_observation stats_dim:refPeriod year:2012 .
    ?income_rank_observation simd:incomeRank ?income_deprivation_rank .
  }

  GRAPH <http://data.opendatascotland.org/graph/simd/employment-rank> {
    ?employment_rank_observation stats_dim:refArea ?dz .
    ?employment_rank_observation stats_dim:refPeriod year:2012 .
    ?employment_rank_observation simd:employmentRank ?employment_deprivation_rank .
  }

  GRAPH <http://data.opendatascotland.org/graph/simd/health-rank> {
    ?health_rank_observation stats_dim:refArea ?dz .
    ?health_rank_observation stats_dim:refPeriod year:2012 .
    ?health_rank_observation simd:healthRank ?health_deprivation_rank .
  }

  GRAPH <http://data.opendatascotland.org/graph/simd/education-rank> {
    ?education_rank_observation stats_dim:refArea ?dz .
    ?education_rank_observation stats_dim:refPeriod year:2012 .
    ?education_rank_observation simd:educationRank ?education_deprivation_rank .
  }

  GRAPH <http://data.opendatascotland.org/graph/simd/geographic-access-rank> {
    ?access_rank_observation stats_dim:refArea ?dz .
    ?access_rank_observation stats_dim:refPeriod year:2012 .
    ?access_rank_observation simd:geographicAccessRank ?access_deprivation_rank .
  }

  GRAPH <http://data.opendatascotland.org/graph/simd/housing-rank> {
    ?housing_rank_observation stats_dim:refArea ?dz .
    ?housing_rank_observation stats_dim:refPeriod year:2012 .
    ?housing_rank_observation simd:housingRank ?housing_deprivation_rank .
  }

  GRAPH <http://data.opendatascotland.org/graph/simd/crime-rank> {
    ?crime_rank_observation stats_dim:refArea ?dz .
    ?crime_rank_observation stats_dim:refPeriod year:2012 .
    ?crime_rank_observation simd:crimeRank ?crime_deprivation_rank .
  }

 {
   SELECT ?dz ?dz_label WHERE
   {
      ?dz a <http://data.opendatascotland.org/def/geography/DataZone> .
      ?dz rdfs:label ?dz_label .
    }
  }
}

Try running/editing it here:
http://data.opendatascotland.org/sparql?query=PREFIX+stats%3A+%3Chttp%3A%2F%2Fstatistics.data.gov.uk%2Fid%2Fstatistical-geography%2F%3E%0APREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0APREFIX+simd%3A+%3Chttp%3A%2F%2Fdata.opendatascotland.org%2Fdef%2Fsimd%2F%3E%0APREFIX+cube%3A+%3Chttp%3A%2F%2Fpurl.org%2Flinked-data%2Fcube%23%3E%0APREFIX+stats_dim%3A+%3Chttp%3A%2F%2Fdata.opendatascotland.org%2Fdef%2Fstatistical-dimensions%2F%3E%0APREFIX+year%3A+%3Chttp%3A%2F%2Freference.data.gov.uk%2Fid%2Fyear%2F%3E%0A%0ASELECT+DISTINCT%0A%3Fdz_label%0A%3Foverall_rank%0A%3Fincome_deprivation_rank%0A%3Femployment_deprivation_rank%0A%3Fhealth_deprivation_rank%0A%3Feducation_deprivation_rank%0A%3Faccess_deprivation_rank%0A%3Fhousing_deprivation_rank%0A%3Fcrime_deprivation_rank%0A%0AWHERE+%7B%0A%0A++GRAPH+%3Chttp%3A%2F%2Fdata.opendatascotland.org%2Fgraph%2Fsimd%2Frank%3E+%7B%0A++++%3Foverall_rank_observation+stats_dim%3ArefArea+%3Fdz+.%0A++++%3Foverall_rank_observation+stats_dim%3ArefPeriod+year%3A2012+.%0A++++%3Foverall_rank_observation+simd%3Arank+%3Foverall_rank+.%0A++%7D%0A%0A++GRAPH+%3Chttp%3A%2F%2Fdata.opendatascotland.org%2Fgraph%2Fsimd%2Fincome-rank%3E+%7B%0A++++%3Fincome_rank_observation+stats_dim%3ArefArea+%3Fdz+.%0A++++%3Fincome_rank_observation+stats_dim%3ArefPeriod+year%3A2012+.%0A++++%3Fincome_rank_observation+simd%3AincomeRank+%3Fincome_deprivation_rank+.%0A++%7D%0A%0A++GRAPH+%3Chttp%3A%2F%2Fdata.opendatascotland.org%2Fgraph%2Fsimd%2Femployment-rank%3E+%7B%0A++++%3Femployment_rank_observation+stats_dim%3ArefArea+%3Fdz+.%0A++++%3Femployment_rank_observation+stats_dim%3ArefPeriod+year%3A2012+.%0A++++%3Femployment_rank_observation+simd%3AemploymentRank+%3Femployment_deprivation_rank+.%0A++%7D%0A%0A++GRAPH+%3Chttp%3A%2F%2Fdata.opendatascotland.org%2Fgraph%2Fsimd%2Fhealth-rank%3E+%7B%0A++++%3Fhealth_rank_observation+stats_dim%3ArefArea+%3Fdz+.%0A++++%3Fhealth_rank_observation+stats_dim%3ArefPeriod+year%3A2012+.%0A++++%3Fhealth_rank_observation+simd%3AhealthRank+%3Fhealth_deprivation_rank+.%0A++%7D%0A%0A++GRAPH+%3Chttp%3A%2F%2Fdata.opendatascotland.org%2Fgraph%2Fsimd%2Feducation-rank%3E+%7B%0A++++%3Feducation_rank_observation+stats_dim%3ArefArea+%3Fdz+.%0A++++%3Feducation_rank_observation+stats_dim%3ArefPeriod+year%3A2012+.%0A++++%3Feducation_rank_observation+simd%3AeducationRank+%3Feducation_deprivation_rank+.%0A++%7D%0A%0A++GRAPH+%3Chttp%3A%2F%2Fdata.opendatascotland.org%2Fgraph%2Fsimd%2Fgeographic-access-rank%3E+%7B%0A++++%3Faccess_rank_observation+stats_dim%3ArefArea+%3Fdz+.%0A++++%3Faccess_rank_observation+stats_dim%3ArefPeriod+year%3A2012+.%0A++++%3Faccess_rank_observation+simd%3AgeographicAccessRank+%3Faccess_deprivation_rank+.%0A++%7D%0A%0A++GRAPH+%3Chttp%3A%2F%2Fdata.opendatascotland.org%2Fgraph%2Fsimd%2Fhousing-rank%3E+%7B%0A++++%3Fhousing_rank_observation+stats_dim%3ArefArea+%3Fdz+.%0A++++%3Fhousing_rank_observation+stats_dim%3ArefPeriod+year%3A2012+.%0A++++%3Fhousing_rank_observation+simd%3AhousingRank+%3Fhousing_deprivation_rank+.%0A++%7D%0A%0A++GRAPH+%3Chttp%3A%2F%2Fdata.opendatascotland.org%2Fgraph%2Fsimd%2Fcrime-rank%3E+%7B%0A++++%3Fcrime_rank_observation+stats_dim%3ArefArea+%3Fdz+.%0A++++%3Fcrime_rank_observation+stats_dim%3ArefPeriod+year%3A2012+.%0A++++%3Fcrime_rank_observation+simd%3AcrimeRank+%3Fcrime_deprivation_rank+.%0A++%7D%0A%0A+%7B%0A+++SELECT+%3Fdz+%3Fdz_label+WHERE%0A+++%7B%0A++++++%3Fdz+a+%3Chttp%3A%2F%2Fdata.opendatascotland.org%2Fdef%2Fgeography%2FDataZone%3E+.%0A++++++%3Fdz+rdfs%3Alabel+%3Fdz_label+.%0A++++%7D%0A++%7D%0A%7D

Most Deprived Datazones by Council
----------------------------------
You can experiment with the SPARQL for generating the proportions of most deprived data zones per council here:

http://data.opendatascotland.org/sparql?filter=%3Frank+%3C%3D+650.5&query=SELECT%0D%0A++++++++%3Flabel%0D%0A++++++++%3Fdep_count%0D%0A++++++++%3Ftotal_count%0D%0A++++++++%28%28%3Fdep_count+%2F+%3Ftotal_count%29+as+%3Fprop%29%0D%0A++++++++%3Fcouncil%0D%0A%0D%0A++++++WHERE+%7B%0D%0A%0D%0A++++++++%3Fcouncil+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23label%3E+%3Flabel+.%0D%0A%0D%0A++++++++%7B%0D%0A++++++++++SELECT+%28count%28%3Fdz%29+as+%3Fdep_count%29+%3Fcouncil+WHERE+%7B%0D%0A++++++++++++%3Fcouncil+a+%3Chttp%3A%2F%2Fdata.opendatascotland.org%2Fdef%2Fgeography%2FCouncilArea%3E+.%0D%0A%0D%0A++++++++++++OPTIONAL+%7B%0D%0A++++++++++++++GRAPH+%3C%25%7Bsimd_domain_graph%7D%3E+%7B%0D%0A+++++++++++++++%3Fobs+%3Chttp%3A%2F%2Fdata.opendatascotland.org%2Fdef%2Fstatistical-dimensions%2FrefArea%3E+%3Fdz+.%0D%0A+++++++++++++++%3Fobs+%3Chttp%3A%2F%2Fpurl.org%2Flinked-data%2Fcube%23dataSet%3E+%3C%25%7Bsimd_domain_dataset%7D%3E+.%0D%0A+++++++++++++++%3Fobs+%3C%25%7Bsimd_domain_rank_predicate%7D%3E+%3Frank+.%0D%0A+++++++++++++++%3Fobs+%3Chttp%3A%2F%2Fdata.opendatascotland.org%2Fdef%2Fstatistical-dimensions%2FrefPeriod%3E+%3C%25%7Bsimd_release_uri%7D%3E+.%0D%0A++++++++++++++%7D%0D%0A++++++++++++++%3Fdz+%3Chttp%3A%2F%2Fdata.ordnancesurvey.co.uk%2Fontology%2Fadmingeo%2FinDistrict%3E+%3Fcouncil+.%0D%0A++++++++++++++FILTER+%28%25%7Bfilter%7D%29+.%0D%0A++++++++++++%7D%0D%0A++++++++++%7D%0D%0A%0D%0A++++++++++GROUP+BY+%3Fcouncil%0D%0A++++++++++ORDER+BY+DESC%28%3Fdep_count%29%0D%0A++++++++%7D%0D%0A%0D%0A++++++++%7B%0D%0A++++++++++SELECT+%28count%28%3Fdz1%29+as+%3Ftotal_count%29+%3Fcouncil+WHERE+%7B%0D%0A++++++++++++%3Fdz1+%3Chttp%3A%2F%2Fdata.ordnancesurvey.co.uk%2Fontology%2Fadmingeo%2FinDistrict%3E+%3Fcouncil+.%0D%0A++++++++++%7D%0D%0A++++++++++GROUP+BY+%3Fcouncil%0D%0A++++++++%7D%0D%0A++++++%7D%0D%0A++++++ORDER+BY+DESC%28%3Fprop%29&simd_domain_dataset=http%3A%2F%2Fdata.opendatascotland.org%2Fdata%2Fsimd%2Frank&simd_domain_graph=http%3A%2F%2Fdata.opendatascotland.org%2Fgraph%2Fsimd%2Frank&simd_domain_rank_predicate=http%3A%2F%2Fdata.opendatascotland.org%2Fdef%2Fsimd%2Frank&simd_release_uri=http%3A%2F%2Freference.data.gov.uk%2Fid%2Fyear%2F2012

Try experimenting with the form fields to produce tables for different percentiles and deprivation domains.

Further Reading
---------------

Developer documentation for the OpenDataScotland Linked Data site can be found here
http://data.opendatascotland.org/docs

For details of all available data kits, and locations of online boundary files
http://data.opendatascotland.org/datakits

Using TopoJSON
http://github.com/mbostock/topojson

For a tutorial with more details on how to access the data published via OpenDataScotland, please see the Schools tutorial section
http://schools.opendatascotland.org
