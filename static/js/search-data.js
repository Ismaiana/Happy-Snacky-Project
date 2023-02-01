document.querySelector('.a btn btn-success').addEventListener('click', () => {

    fetch(`https://api.spoonacular.com/food/products/{id}`)
    .then((response) => response.json())
    .then((result) => {
        const dataSave = result.message;
       
        document.querySelector('#savedsnack')
        .innerHTML(`<div>${dataSave}</div>`)
    });
});