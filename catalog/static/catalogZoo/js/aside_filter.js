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
        console.log(data);
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

            let productPromotionDiv; 
            if (product.promotion_set && product.promotion_set.length > 0) {

                productPromotionDiv = document.createElement('div');
                productPromotionDiv.classList.add('products___item-promotion');
                productPromotionDiv.textContent = 'Акция'

            };

            const productWeight = document.createElement('ul');
            productWeight.classList.add('products___item-weight-list');
            if (product.productproperties_set && product.productproperties_set.length > 0) {

                product.productproperties_set.forEach(property => {

                    const productWeightItem = document.createElement('li');
                    productWeightItem.classList.add('slider__item-weight-list-item');
                    productWeightItem.textContent = `${property.weight} ${product.unit}`;
                    productWeight.appendChild(productWeightItem);

                });
            } else {

                productWeightItem = document.createElement('li');
                productWeightItem.classList.add('slider__item-weight-list-item');
                productWeightItem.textContent = `${product.amount} ${product.unit}`;
                productWeight.appendChild(productWeightItem);

            };

            const productItemPriceBasket = document.createElement('div');
            productItemPriceBasket.classList.add('products___item-price-basket');
            if (product.promotion_set && product.promotion_set > 0) {

                const productItemPrice = document.createElement('p');
                productItemPrice.classList.add('products___item-price-promotion');
                productItemPrice.textContent = `${product.price} BYN`;
                const productItemPricePromotion = document.createElement('p');
                productItemPricePromotion.classList.add('products___item-price');
                productItemPricePromotion.textContent = `${product.price} BYN`;
                productItemPriceBasket.appendChild(productItemPrice);
                productItemPriceBasket.appendChild(productItemPricePromotion);

            } else {

                const productItemPrice = document.createElement('p');
                productItemPrice.classList.add('products___item-price');
                productItemPrice.textContent = `${product.price} BYN`;
                productItemPriceBasket.appendChild(productItemPrice);

            };

            const productItemBasket = document.createElement('div');
            productItemBasket.classList.add('products___item-basket');
            const productItemBasketPlus = document.createElement('div');
            productItemBasketPlus.classList.add("slider__item-basket-text");
            productItemBasketPlus.textContent = '+';
            const productItemBasketSVG = document.createElement('div');
            productItemBasketSVG.classList.add('slider__item-basket-img'); 

            const basketSVG = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            basketSVG.setAttribute("width", "20");
            basketSVG.setAttribute("height", "20");
            basketSVG.setAttribute("viewBox", "0 0 20 20");
            basketSVG.setAttribute("fill", "none");
            basketSVG.setAttribute("xmlns", "http://www.w3.org/2000/svg");

            const basketPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
            basketPath.setAttribute("fill-rule", "evenodd");
            basketPath.setAttribute("clip-rule", "evenodd");
            basketPath.setAttribute("d", "M1 1C1 0.447715 1.44932 0 2.00358 0H3.50894C4.34034 0 5.01431 0.671572 5.01431 1.5V2.06055L17.5883 2.96818C18.4651 3.02278 19.1089 3.81081 18.9846 4.67739L18.1194 10.7121C18.0135 11.4511 17.3783 12 16.6292 12H5.01431V14H15.0572C16.72 14 18.068 15.3431 18.068 17C18.068 18.6569 16.72 20 15.0572 20C13.3945 20 12.0465 18.6569 12.0465 17C12.0465 16.6494 12.1069 16.3128 12.2178 16H6.85015C6.9611 16.3128 7.02147 16.6494 7.02147 17C7.02147 18.6569 5.67352 20 4.01073 20C2.34795 20 1 18.6569 1 17C1 15.6938 1.83779 14.5825 3.00716 14.1707V3.00923C3.00711 3.00372 3.00711 2.99821 3.00716 2.99268V2H2.00358C1.44932 2 1 1.55228 1 1ZM5.01431 4.06445V10H16.194L16.9208 4.93051L5.01431 4.06445ZM14.0537 17C14.0537 16.4477 14.503 16 15.0572 16C15.6115 16 16.0608 16.4477 16.0608 17C16.0608 17.5523 15.6115 18 15.0572 18C14.503 18 14.0537 17.5523 14.0537 17ZM3.00716 17C3.00716 16.4477 3.45647 16 4.01073 16C4.56499 16 5.01431 16.4477 5.01431 17C5.01431 17.5523 4.56499 18 4.01073 18C3.45647 18 3.00716 17.5523 3.00716 17Z");
            basketPath.setAttribute("fill", "#5C5F62");

            basketSVG.appendChild(basketPath);
            productItemBasketSVG.appendChild(basketSVG);
            productItemBasket.appendChild(productItemBasketPlus);
            productItemBasket.appendChild(productItemBasketSVG);
            productItemPriceBasket.appendChild(productItemBasket)

    
            const productTitle = document.createElement('a');
            productTitle.href = `/card_product/${product.id}`;
            productTitle.classList.add('products___item-title');
            productTitle.textContent = product.title;

            // TODO: Кнопка класса products___item-btn, добавить в фильтру
    
            // Добавляем элементы в DOM
            productArticle.appendChild(productImgDiv);
            productArticle.appendChild(productTitle);
            if (productPromotionDiv) {

                productArticle.appendChild(productPromotionDiv);

            };
            if (product.productproperties_set) {
                
                productArticle.appendChild(productWeight);

            } else {

                productArticle.appendChild(productWeight)

            };
            if (product.promotion_set && product.promotion_set > 0) {
             
                productArticle.appendChild(productItemPriceBasket)

            } else {

                productArticle.appendChild(productItemPriceBasket)

            };

            productItem.appendChild(productArticle);
            container.appendChild(productItem);

        });
    }
    
}
