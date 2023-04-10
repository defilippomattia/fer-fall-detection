<script>
	import { onMount } from 'svelte';
	import AlertsCard from './AlertsCard.svelte';
	import HeaderIntro from './HeaderIntro.svelte';
	
	let alerts = [];
  
	async function fetchAlerts() {
	  const response = await fetch('http://localhost:8081/alerts');
	  alerts = await response.json();
	  console.log(alerts.length);
	}
  
  
	onMount(() => {
	  fetchAlerts();
	});
  </script>
  <style>
	.alert-container {
	  display: grid;
	  grid-template-columns: repeat(3, 1fr);
	  gap: 20px;
	}
  </style>
  
  <HeaderIntro />
  
  <div class="alert-container">
	{#each alerts as alert}
	  <AlertsCard data={alert} />
	{/each}
  </div>