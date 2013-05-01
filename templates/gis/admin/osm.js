{% extends "gis/admin/openlayers.js" %}
{% block base_layer %}new OpenLayers.Layer.OSM("OpenStreetMap (Mapnik)");{% endblock %}

{% block extra_layers %}
var parkmap = new OpenLayers.Layer.MAPC("basemap");
var aerial = new OpenLayers.Layer.Bing({
    name: "Bing Aerial",
    key: "An8pfp-PjegjSInpD2JyXw5gMufAZBvZ_q3cbJb-kWiZ1H55gpJbxndbFHPsO_HN",
    type: "Aerial"
});
{% endblock %}
