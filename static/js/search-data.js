fetch('/restrictions')
.then(response => response.json())
.then(data => {
    

    listIngred = document.querySelectorAll('#info-product')
    for (let i = 0; i < listIngred.length; i++){
        if (data.includes(listIngred[i].innerHTML)){
            listIngred[i].style.backgroundColor = 'red'
            // document.querySelector('data-bs-toggle');

            // listIngred[i].getAttribute('data-bs-toggle'); 

            // listIngred[i].setAttribute('data-bs-toggle', 'tooltip');
            
        }
    
        
    // let nutrients = document.querySelectorAll('#nutrition')    
    // console.log(nutrients[0].innerHTML)    
    }

});
        



// if( listIngred[i] === 'red') {

//     document.querySelector('data-bs-toggle');

//     listIngred[i].getAttribute('data-bs-toggle'); 

//     listIngred[i].setAttribute('data-bs-toggle', 'tooltip');

// };



// function getData(id) {

const id = document.querySelector('#product-id').value
fetch(`/nutrition-info/${id}`)
.then((response) => response.json())
.then(responseJson => {
    // console.log('hello')
    
    console.log(responseJson)

    const nutrients = responseJson.data.nutrition['nutrients']

    // const data= responseJson.data.nutrition['nutrients'].map((nutri) => ({
    //     x:nutri.name,
    //     y:nutri.amount,
    // }));
   
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



