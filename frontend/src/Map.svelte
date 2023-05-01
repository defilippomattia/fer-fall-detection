<script>
    import { onMount } from "svelte";
    import { GeoJSON, LeafletMap, TileLayer, Marker } from 'svelte-leafletjs';

    const mapOptions = {
        center: [45.80092107101865, 15.97117949077176],
        zoom: 18,
    };
    const tileUrl = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
    const tileLayerOptions = {
        minZoom: 0,
        maxZoom: 20,
        maxNativeZoom: 19,
        attribution: "© OpenStreetMap contributors",
    };
    const geoJsonOptions = {
        style: function (geoJsonFeature) {
            console.log('style', geoJsonFeature);
            return {};
        },
        onEachFeature: function (feature, layer) {
            console.log('onEachFeature', feature, layer);
        },
    };

    const markerOptions = {
  icon: L.icon({
    iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  })
};

    let leafletMap;

    //let markers = [[45.80008169452325, 15.9712183962411], [45.80123107449718, 15.970728647644895], [45.800879465593674, 15.970843752804337], [45.80087062334588, 15.970965016814612], [45.800192112064636, 15.971336325727407], [45.80018644022197, 15.97151838703408], [45.80012574840065, 15.970922218160537], [45.80142580973816, 15.971272389637122], [45.800178533668394, 15.970987263944926], [45.80060271997437, 15.97150071767695]];
    let markers = [];

    onMount(async () => {
        const response = await fetch('/alertslocations');
        const data = await response.json();
        markers = data;
        leafletMap.getMap().fitBounds([[45.80006, 15.97061], [45.80163, 15.97181]]);
    });
</script>
<div class="alertsmap" style="width: 1200px; height: 500px;">
    <LeafletMap bind:this={leafletMap} options={mapOptions}>
        <TileLayer url={tileUrl} options={tileLayerOptions}/>
            {#each markers as marker}
                {console.log(marker)}
                <Marker latLng={marker} options={markerOptions}></Marker>
                
                {console.log("test...")}
            {/each}
        <GeoJSON url="example.geojson" options={geoJsonOptions}/>
    </LeafletMap>
</div>

<style>
    .alertsmap {
        margin: 0 auto;
    }
</style>
