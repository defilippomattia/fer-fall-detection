<script>
    import Map from './Map.svelte';
	import AlertCard from './AlertCard.svelte';
	import { onMount } from 'svelte';
  import GeneralInfo from './GeneralInfo.svelte';



    // const mapOptions = {
    //     center: [1.250111, 103.830933],
    //     zoom: 13,
    // };
    // const tileUrl = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
    // const tileLayerOptions = {
    //     minZoom: 0,
    //     maxZoom: 20,
    //     maxNativeZoom: 19,
    //     attribution: "© OpenStreetMap contributors",
    // };
    // const geoJsonOptions = {
    //     style: function (geoJsonFeature) {
    //         console.log('style', geoJsonFeature);
    //         return {};
    //     },
    //     onEachFeature: function (feature, layer) {
    //         console.log('onEachFeature', feature, layer);
    //     },
    // };
    let alerts = [];
  
  async function fetchAlerts() {
    const response = await fetch('http://localhost:6500/alerts');
    alerts = await response.json();
    console.log(alerts.length);
  }


  onMount(() => {
    fetchAlerts();
  });
</script>

<GeneralInfo />
<Map/>

<div class="alert-container">
	{#each alerts as alert}
	  <AlertCard data={alert} />
	{/each}
  </div>

    <!-- <style>
	.alert-container {
	  display: grid;
	  grid-template-columns: repeat(3, 1fr);
	  gap: 20px;
	} 
  	</style> -->