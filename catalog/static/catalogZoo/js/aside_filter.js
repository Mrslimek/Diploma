document.addEventListener("DOMContentLoaded", function() {
    let radioButtons = document.querySelectorAll('input[name="type"]');

    radioButtons.forEach(function(radioButton) {
        radioButton.addEventListener('click', function() {
            let id = this.getAttribute('data-id');
            myFunction(this.value, id);
        });
    });
});

function myFunction(value, id) {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Проверяем, начинается ли этот cookie с нужного имени
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    const csrftoken = getCookie('csrftoken');
    
    
    fetch('http://127.0.0.1:8000/api/filtered_products/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'product_type': id
        })
    })
    .then(response => {
        if (response.ok) {
            console.log('Success');
            return response.json()
        } else {
            console.log('Не получилось')} 
            console.log(id);
        })
    .then(data => {
        renderProducts(data);
    })

    function renderProducts(products) {
        const container = document.querySelector('.product__list-wrap .products__list'); // Указываем контейнер
        container.innerHTML = ''; // Очищаем контейнер перед добавлением новых элементов
    
        products.forEach(product => {
            // Создаем HTML элементы
            const productItem = document.createElement('li');
            productItem.classList.add('products__list-item');
    
            const productArticle = document.createElement('article');
            productArticle.classList.add('products___item');
    
            const productImgDiv = document.createElement('div');
            productImgDiv.classList.add('products___item-img');
            const productImg = document.createElement('img');
            productImg.src = `${product.productimage_set[0].image}`;

            productImg.alt = 'item';
            productImgDiv.appendChild(productImg);
    
            const productTitle = document.createElement('a');
            productTitle.href = `/card_product/${product.id}`;
            productTitle.classList.add('products___item-title');
            productTitle.textContent = product.title;
    
            const productPrice = document.createElement('p');
            productPrice.classList.add('products___item-price');
            productPrice.textContent = `${product.price} BYN`;
    
            // Добавляем элементы в DOM
            productArticle.appendChild(productImgDiv);
            productArticle.appendChild(productTitle);
            productArticle.appendChild(productPrice);
            productItem.appendChild(productArticle);
            container.appendChild(productItem);
        });
    }
    
}
