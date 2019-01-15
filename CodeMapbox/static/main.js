mapboxgl.accessToken = 'pk.eyJ1IjoiY2hlcnJ5MTM1OSIsImEiOiJjam81bTRsbjIwOHZwM3ZvMWxoaXIzNzgxIn0.S75v2qYbBXUTvqIqXFQLfg';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/basic-v9',
    zoom: 4,
    center: [7.6261347, 51.9606649]
});

map.addControl(new mapboxgl.GeolocateControl({
    positionOptions: {
        enableHighAccuracy: true
    },
    trackUserLocation: true
}));

map.on('click', function (e) {
    document.getElementById('info').innerHTML =
        // e.point is the x, y coordinates of the mousemove event relative
        // to the top-left corner of the map
        JSON.stringify(e.point) + '<br />' +
        // e.lngLat is the longitude, latitude geographical position of the event
        JSON.stringify(e.lngLat);
});



