<script>
    export let data;
    const isResolved = data.resolved;
    let comment = data.comment;
    function getResolvedClass() {
      if (isResolved) {
        return 'resolved';
      } else {
        return '';
      }
    }
  
    async function handleResolve(event) {
    comment = event.target.parentNode.querySelector('textarea').value;
    const response = await fetch('http://web:6500/alerts', {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        Id: data.Id,
        comment: comment,
        resolved: true
      })
    });
  
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  
    const updatedData = await response.json();
    data = updatedData;
    location.reload();
    }
  
  
  </script>
  
  <div class="card {getResolvedClass()}">
    <div class="card-header">
      <h3 class="card-title {getResolvedClass()}">Alert</h3>
    </div>
    <div class="card-body">
      <div class="card-text">
        <p><strong>Message ID:</strong> {data.Id}</p>
        <p><strong>Source Type:</strong> {data.source_type}</p>
        <p><strong>Source ID:</strong> {data.source_id}</p>
        <p><strong>Longitude:</strong> {data.longitude}</p>
        <p><strong>Latitude:</strong> {data.latitude}</p>
        <p><strong>Timestamp:</strong> {data.timestamp}</p>
        <p><strong>Resolved:</strong> {data.resolved}</p>
  
      </div>
  
      <hr />
  
      <div class="card-controls">
        <textarea value={comment} placeholder="Add comment..."></textarea>
        <button class="resolvebtn {getResolvedClass()}" on:click={handleResolve}>Resolve</button>
      </div>
    </div>
  </div>

  <style>
    .card {
      border-radius: 12px;
      border: 1px solid #f95738;
      box-shadow: 0px 2px 10px rgba(249, 87, 56, 0.2);
      padding: 24px;
      margin-bottom: 24px;
      background-color: #fff;
      max-width: 450px;
    }
  
    .card.resolved {
      border: 1px solid #28a745;
      box-shadow: 0px 2px 10px rgba(75, 56, 249, 0.2);
      opacity: 0.5;
      pointer-events: none;
    }
    .card-header {
      margin-bottom: 16px;
    }
    .card-text p {
      font-size: 16px;
    }
  
    .card-title {
      margin: 0;
      font-size: 28px;
      font-weight: bold;
      -webkit-appearance: none;
      color: #f95738;
    }
  
    .card-title.resolved {
      color: #28a745;
    }
    .card-text {
      margin-bottom: 24px;
    }
    hr {
      border: none;
      border-bottom: 1px solid #e5e5e5;
      margin: 24px 0;
    }
    textarea {
      width: 90%;
      height: 120px;
      padding: 16px;
      border-radius: 12px;
      border: none;
      background-color: #f2f2f2;
      font-size: 16px;
      margin-bottom: 24px;
      resize: none;
      -webkit-appearance: none;
    }
    .resolvebtn {
    padding: 16px 24px;
    border-radius: 12px;
    background-color: #f95738;
    color: #fff;
    border: none;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    margin-top: 24px;
    -webkit-appearance: none;
  }
  
  .resolvebtn.resolved {
    padding: 16px 24px;
    border-radius: 12px;
    background-color: #28a745;
    color: #fff;
    border: none;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    margin-top: 24px;
    -webkit-appearance: none;
  }
  
  </style>
  
  