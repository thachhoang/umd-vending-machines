/* globals $:false, L:false */
(function() {
    var map = L.map('map').setView([38.9897623, -76.9447152], 16);
    var baseLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);

    $.getJSON("data/buildings_with_machines.json", function(data) {
        var machineLayer = L.geoJson(data, {
            onEachFeature: function(feature, layer) {
                var html = '<strong>' + feature.properties.name + ' (' + feature.properties.building_id + ')</strong>';
                html += '<ul>';
                var locations = feature.properties.locations;
                for (var i = 0; i < locations.length; i++) {
                    var loc = locations[i];
                    html += '<li>' + loc.location + '<ul>';
                    for (var k = 0; k < loc.machines.length; k++) {
                        var m = loc.machines[k];
                        html += '<li>' + m.name + ' (' + m.count + ')</li>';
                    }
                    html += '</ul></li>';
                }
                html += '</ul>';
                html += '<a target="_blank" href="' + feature.properties.url + '">source</a>';
                layer.bindPopup(html, {
                    className: 'pop-up',
                });
            },
        });
        map.addLayer(machineLayer);
    });
}());