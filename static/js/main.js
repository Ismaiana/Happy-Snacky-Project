// AJAX TO HIGHLIGHT RESTRICTIONS IN DATA INFO PRODUCT

fetch('/restrictions')
.then(response => response.json())
.then(data => {

    let hasRestricted = false;
    listIngred = document.querySelectorAll('#info-product')
    for (let i = 0; i < listIngred.length; i++){
        if (data.includes(listIngred[i].innerHTML)){
            listIngred[i].style.backgroundColor = 'red';
            listIngred[i].setAttribute('data-bs-toggle', 'tooltip');
            listIngred[i].setAttribute('data-bs-placement', 'top');
            listIngred[i].setAttribute('title', 'This ingredient is part of your dietary restrictions');
            hasRestricted = true;
            
        } 

      }
      if (hasRestricted) {
        const message = document.getElementById('message');
        message.innerText = 'This product requires your attention.';
        message.style.color = 'red';
      }
      if (!hasRestricted) {
        const message = document.getElementById('message');
        message.innerText = 'According to your dietary restrictions, this product should be safe for you.';
        message.style.color = 'green';
      }
    
    });

 


// JS CHART  

const id = document.querySelector('#product-id').value;

fetch(`/nutrition-info/${id}`)
  .then((response) => response.json())
  .then(responseJson => {
    const nutrients = responseJson.data.nutrition['nutrients'];

    let names = [];
    let amounts = [];

    for (const nutrient of nutrients) {
      names.push(nutrient.name);
      amounts.push(nutrient.amount);
    }

    const colorArray = ['#FF2B2B', '#FF7F2A', '#FFC62B', '#5CB718', '#0072C6', '#8B0A50',  '#654321'];

    new Chart(document.querySelector('#myChart'), {
      type: 'bar',
      data: {
        labels: names,
        datasets: [
          {
            label: 'Amount',
            data: amounts,
            backgroundColor: colorArray,
            borderColor: colorArray,
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              color: 'white',
            },
          },
          x: {
            ticks: {
              color: 'white',
            },
          },
        },
        plugins: {
          legend: {
            labels: {
              color: 'white',
            },
          },
        },
      },
    });
  });

// BOX ALERT WHEN USER CLICK DELETE BUTTON IN SAVED SEARCH 
  function confirmDelete() {
    
          const confirmed = confirm("Are you sure you want to delete this product?");
          if (confirmed) {
              return true;
          }
           else {
              return false;
          };
      };










