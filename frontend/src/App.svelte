<script>
    import Map from './Map.svelte';
	import AlertCard from './AlertCard.svelte';
	import { onMount } from 'svelte';
  import GeneralInfo from './GeneralInfo.svelte';

    let alerts = [];
  
  async function fetchAlerts() {
    //const response = await fetch('http://web:6500/alerts'); //when using docker, maybe not?
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
<br>
<br>

<div class="alert-container">
	{#each alerts as alert}
	  <AlertCard data={alert} />
	{/each}
  </div>

    <style>
        :global(body) {
    font-family: 'Open Sans', sans-serif;
  }
      .alert-container {
        width: 80%;
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
      }
      </style>