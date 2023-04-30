<script>
    let alerts = [];
  
    function createAlerts() {
      console.log("creating");
    }
  
    function deleteAlerts() {
      console.log("del");
    }
  </script>
  
  <div class="demo-buttons">
    <button on:click={createAlerts}>Generate 10 Random Alerts</button>
    <button on:click={deleteAlerts}>Delete All Alerts</button>
  </div>
  
  <style>
    .demo-buttons {
      display: flex;
      justify-content: center;
    }
  
    .demo-buttons button:first-child {
      margin-right: 10px;
    }
  </style>
  