<script>
    import { onMount } from "svelte";
    import { GeoJSON, LeafletMap, TileLayer, Marker } from 'svelte-leafletjs';

    export let mapOptions, tileUrl, tileLayerOptions, geoJsonOptions;

    let leafletMap;

    let markers = [[45.80008169452325, 15.9712183962411], [45.80123107449718, 15.970728647644895], [45.800879465593674, 15.970843752804337], [45.80087062334588, 15.970965016814612], [45.800192112064636, 15.971336325727407], [45.80018644022197, 15.97151838703408], [45.80012574840065, 15.970922218160537], [45.80142580973816, 15.971272389637122], [45.800178533668394, 15.970987263944926], [45.80060271997437, 15.97150071767695]];

    onMount(() => {
        leafletMap.getMap().fitBounds([[45.80006, 15.97061], [45.80163, 15.97181]]);
    });
</script>
<div class="example" style="width: 900px; height: 500px;">
    <LeafletMap bind:this={leafletMap} options={mapOptions}>
        <TileLayer url={tileUrl} options={tileLayerOptions}/>
            {#each markers as marker}
                {console.log(marker)}
                <Marker latLng={marker}></Marker>
                {console.log("test...")}
            {/each}
        <GeoJSON url="example.geojson" options={geoJsonOptions}/>
    </LeafletMap>
</div>