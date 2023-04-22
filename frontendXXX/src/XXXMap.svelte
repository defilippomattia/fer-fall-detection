<script>
    import { onMount } from "svelte";
    import { GeoJSON, LeafletMap, TileLayer, Marker } from 'svelte-leafletjs';

    export let mapOptions, tileUrl, tileLayerOptions, geoJsonOptions;

    let leafletMap;
    // let markers = [
    //     {lat: 1.255, lng: 103.805},
    //     {lat: 1.248, lng: 103.816},
    //     {lat: 1.240, lng: 103.836},
    //     {lat: 1.232, lng: 103.849},
    // ];
    let markers = [
        [1.255,103.805],
        [1.248,103.816],
        [1.240,103.836],
        [1.232,103.849],
        [45.593016,17.223840],
        [45.89861,16.84889]
    ];

    onMount(() => {
        leafletMap.getMap().fitBounds([[1.266835, 103.796403], [1.232988, 103.854861]]);
    });
</script>
<div class="example" style="width: 900px; height: 500px;">
    <LeafletMap bind:this={leafletMap} options={mapOptions}>
        <TileLayer url={tileUrl} options={tileLayerOptions}/>
            {#each markers as marker}
                {console.log(marker)}
                <Marker latLng={marker}></Marker>
                {console.log("test...")}
                {console.log(marker.lat, marker.lng)}
            {/each}
        <GeoJSON url="example.geojson" options={geoJsonOptions}/>
    </LeafletMap>
</div>