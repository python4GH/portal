document.body.onload = ()=>{
    let inventoryData = JSON.parse(localStorage.getItem('myInventory'));
    let totalItems = document.querySelector('.ti');
    let stockItems = document.querySelector('.tc');
    let catNames = document.querySelector('.tq');
    let dispData = document.querySelector('#dispData');
    let allData = '';
    let colorData = '';
    let colorContainer = document.querySelector('#descStock');

    totalItems.innerHTML = inventoryData.length;

    inventoryData.forEach(data => {
        const dispItem = `<tr><td><span class="text-offset">${data['name']}</span></td><td class="item-desc">${data['description']}</td><td class="item-cat">${data['category']}</td><td class="item-qty">${data['quantity']}</td></tr>`
        allData += dispItem;
    });

    dispData.innerHTML = allData;

    inventoryData.forEach(descData =>{
        let dispDesc;
        if(descData['quantity'] == 0){
            dispDesc = `<div class="box" style="background-color: red; color: ghostWhite;"><div class="right-side"><div class="number">${descData['name']} : Out of stock</div></div></div>`;
        }else if(( descData['quantity'] > 0 ) && (descData['quantity'] < 21 )){
            dispDesc = `<div class="box" style="background-color: orange; color: ghostWhite;"><div class="right-side"><div class="number">${descData['name']} : Almost out</div></div></div>`;
        }else{
            dispDesc = `<div class="box" style="background-color: green; color: ghostWhite;"><div class="right-side"><div class="number">${descData['name']} : In stock</div></div></div>`; 
        }
        colorData += dispDesc;
    })
    colorContainer.innerHTML = colorData;
  
    let totalCate = [];
    inventoryData.forEach(item => {
        if(!totalCate.includes(item['category'])){
            totalCate.push(item['category']);
        }
    })

    stockItems.innerHTML = totalCate.length;

    let totalQTY = 0;
    inventoryData.forEach(item =>{
        totalQTY += Number(item['quantity']);
    })
    catNames.innerHTML = totalQTY;

}