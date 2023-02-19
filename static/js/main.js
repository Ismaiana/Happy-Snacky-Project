// AJAX TO HIGHLIGHT RESTRICTIONS IN DATA INFO PRODUCT

fetch('/restrictions')
.then(response => response.json())
.then(data => {
    

    listIngred = document.querySelectorAll('#info-product')
    for (let i = 0; i < listIngred.length; i++){
        if (data.includes(listIngred[i].innerHTML)){
            listIngred[i].style.backgroundColor = 'red'
            
        } 
   }

}); 


// JS CHART  

const id = document.querySelector('#product-id').value
fetch(`/nutrition-info/${id}`)
.then((response) => response.json())
.then(responseJson => {
  
    
    console.log(responseJson)

    const nutrients = responseJson.data.nutrition['nutrients']

  
    let names = []
    let amounts = []

    for (const nutrient of nutrients){

        names.push(nutrient.name)
        amounts.push(nutrient.amount)

    }
    new Chart(document.querySelector('#myChart'), {
        
        type: 'bar',
        data: {
          labels: names,
          datasets: [
                        {
              label: 'Amount',
              data: amounts,
            },
          ],
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

