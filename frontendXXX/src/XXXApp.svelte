<script>
	import { onMount } from 'svelte';
	import AlertsCard from './XXXAlertsCard.svelte';
	import HeaderIntro from './XXXHeaderIntro.svelte';
	import Map from './XXXMap.svelte';
	
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
  <!-- <style>
	.alert-container {
	  display: grid;
	  grid-template-columns: repeat(3, 1fr);
	  gap: 20px;
	} 
  	</style>-->

	<Map/>
  
  <HeaderIntro />

 
  
  <div class="alert-container">
	{#each alerts as alert}
	  <AlertsCard data={alert} />
	{/each}
  </div>