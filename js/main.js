/* globals $:false, L:false */
(function() {
    var map = L.map('map').setView([38.9897623, -76.9447152], 16);
    var baseLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);
}());