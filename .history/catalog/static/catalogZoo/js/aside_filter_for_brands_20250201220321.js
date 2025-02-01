// Выпадающий список 'Сортировать по'. Изначально был в файле select.js. Для удобства перенесен сюда
const select = document.querySelector(".catalog__sort-select");
const selectList = document.querySelector(".catalog__sort-select-list");
const selectListItem = document.querySelectorAll(
    ".catalog__sort-select-list-item"
);
const catalogSelectActive = document.querySelector(
    ".catalog__sort-select-active"
);

//EventListener для 'выпадания списка' выше
select.addEventListener("click", () => {
    selectList.classList.toggle("catalog__sort-select-list-active");
});

//EventListener для момента, когда полностью загружен DOM
document.addEventListener("DOMContentLoaded", function () {
    
    localStorage.clear(); //TODO: Сделать так, чтобы при обновлении страницы стандартным способ сбрасывались и кнопки

    const brandCheckboxes = document.querySelectorAll("input[class='brand__type-list-item-hdie']");

    /*Обновляет localStorage
     * Если brandIds нет в localStorage, то создает пустой массив и push-ит в него значение и добавляет в localStorage
     * Если ключ НЕ brandIds, то создает в localStorage переданое значение, также удаляет, если checkbox был unchecked
     */
    function updateLocalStorage(key, value, add) {
        if (key === "brand-ids") {
            let currentArray = JSON.parse(localStorage.getItem(key)) || [];
            if (!Array.isArray(currentArray)) {
                currentArray = [];
            }
            if (add) {
                if (!currentArray.includes(value) && value !== null) {
                    currentArray.push(value);
                }
            } else {
                currentArray = currentArray.filter((item) => item !== value);
            }
            localStorage.setItem(key, JSON.stringify(currentArray));
        } else {
            if (add) {
                localStorage.setItem(key, value);
            } else {
                localStorage.removeItem(key);
            }
        }
    }

    // Просто получаем данные из localStorage
    function getLocalStorageData() {
        return {
            brandIds: JSON.parse(localStorage.getItem("brand-ids")) || [],
            promotion: JSON.parse(localStorage.getItem("promotion")),
            orderByData: localStorage.getItem("orderByData"),
            pageNumber: localStorage.getItem("pageNumber"),
        };
    }

    // Добавляет выбранное значение в localStorage и вызывает getLocalStorageData, вызывает функцию для fetch запроса
    // Не вызывает UpdateLocalStorage, потому что я посчитал, что сбрасывать этот фильтр не нужно
    selectListItem.forEach((item) => {
        item.addEventListener("click", () => {
            // Выбраный пункт становится активным
            catalogSelectActive.innerText = item.innerText;
            let orderByData = item.getAttribute("orderByData");
            localStorage.setItem("orderByData", orderByData);
            let localStorageData = getLocalStorageData();
            filterProducts(
                this.value,
                localStorageData.brandIds.map((id) => parseInt(id, 10)),
                localStorageData.promotion,
                localStorageData.orderByData,
                localStorage.pageNumber
            );
        });
    });

    const promotionCheckbox = document.querySelector("input[class='promotional__item-input-hide']");
          promotionCheckbox.addEventListener("change", function() {
            const promotion = this.getAttribute("promotion");
            updateLocalStorage("promotion", promotion, promotionCheckbox.checked);

            const localStorageData = getLocalStorageData();

            filterProducts(
                this.value,
                localStorageData.brandIds.map((id) => parseInt(id, 10)),
                localStorageData.promotion,
                localStorageData.orderByData,
                localStorage.pageNumber
            );
          });

    // Для каждого чекбокса (чекбоксы это brandIds и promotion) вызывает функцию, вызывает UpdateLocalStorage,
    // вызывает функцию для fetch запроса
    brandCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            const brandId = this.getAttribute("brand-id");

            updateLocalStorage("brand-ids", brandId, checkbox.checked);

            const localStorageData = getLocalStorageData();

            filterProducts(
                this.value,
                localStorageData.brandIds.map((id) => parseInt(id, 10)),
                localStorageData.promotion,
                localStorageData.orderByData,
                localStorage.pageNumber
            );
        });
    });
});

// Функция для fetch запроса
function filterProducts(
    value,
    brandIds,
    promotion,
    orderByData,
    pageNumber
) {
    // Функция для получения куки файла, но испольется только для получения csrf-токена
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Получение csrf-а
    const csrftoken = getCookie("csrftoken");

    // Функция для создания json-а на основе полученых из localStorage данных
    function getBodyDataForFilters(
        brandIds,
        promotion,
        orderByData,
        pageNumber
    ) {
        let bodyData = {};

        let rawObject = {
            brand: brandIds,
            promotion: promotion,
            order_by: orderByData,
            page_number: pageNumber,
        };

        for (let key in rawObject) {
            if (rawObject[key]) {
                bodyData[key] = rawObject[key];
            }
        }

        return JSON.stringify(bodyData);
    }

    //Получение json-a для fetch запроса
    const bodyData = getBodyDataForFilters(
        brandIds,
        promotion,
        orderByData,
        pageNumber
    );

    console.log(bodyData);

    fetch("http://127.0.0.1:8000/api/filtered_products/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: bodyData,
    })
        .then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error(
                    `Запрос не получился - статус ${response.status}`
                );
            }
        })
        .then((data) => {
            console.log(data);
            renderProducts(data);
        })
        .catch((error) => {
            console.error("Ошибка:", error);
        });
}

// Функция для рендера карточек после получения данных с api
function renderProducts(data, fetchUrl) {
    const container = document.querySelector(
        ".product__list-wrap .products__list"
    );
    container.innerHTML = "";

    const paginationContainer = document.querySelector(
        ".product__list-wrap .products__pagination"
    );
    paginationContainer.innerHTML = "";

    data.results.forEach((product) => {
        // Создаем HTML элементы
        const productItem = document.createElement("li");
        productItem.classList.add("products__list-item");

        const productArticle = document.createElement("article");
        productArticle.classList.add("products___item");

        const productImgDiv = document.createElement("div");
        productImgDiv.classList.add("products___item-img");
        const productImg = document.createElement("img");
        productImg.src = `${product.productimage_set[0].image}`;
        productImg.alt = "item";
        productImgDiv.appendChild(productImg);

        let productPromotionDiv;
        if (product.promotion_set && product.promotion_set.length > 0) {
            productPromotionDiv = document.createElement("div");
            productPromotionDiv.classList.add("products___item-promotion");
            productPromotionDiv.textContent = "Акция";
        }

        const productWeight = document.createElement("ul");
        productWeight.classList.add("products___item-weight-list");
        if (
            product.productproperties_set &&
            product.productproperties_set.length > 0
        ) {
            product.productproperties_set.forEach((property) => {
                const productWeightItem = document.createElement("li");
                productWeightItem.classList.add(
                    "slider__item-weight-list-item"
                );
                productWeightItem.textContent = `${property.weight} ${product.unit}`;
                productWeight.appendChild(productWeightItem);
            });
        } else {
            const productWeightItem = document.createElement("li");
            productWeightItem.classList.add("slider__item-weight-list-item");
            productWeightItem.textContent = `${product.amount} ${product.unit}`;
            productWeight.appendChild(productWeightItem);
        }

        const productItemPriceBasket = document.createElement("div");
        productItemPriceBasket.classList.add("products___item-price-basket");
        if (product.promotion_set && product.promotion_set.length > 0) {
            const productItemPrice = document.createElement("p");
            productItemPrice.classList.add("products___item-price-promotion");
            productItemPrice.textContent = `${product.price} BYN`;
            const productItemPricePromotion = document.createElement("p");
            productItemPricePromotion.classList.add("products___item-price");

            const promotion = product.promotion_set[0];
            productItemPricePromotion.textContent = `${promotion.discount} BYN`;
            productItemPriceBasket.appendChild(productItemPrice);
            productItemPriceBasket.appendChild(productItemPricePromotion);
        } else {
            const productItemPrice = document.createElement("p");
            productItemPrice.classList.add("products___item-price");
            productItemPrice.textContent = `${product.price} BYN`;
            productItemPriceBasket.appendChild(productItemPrice);
        }

        const productItemBasket = document.createElement("div");
        productItemBasket.classList.add("products___item-basket");
        const productItemBasketPlus = document.createElement("div");
        productItemBasketPlus.classList.add("slider__item-basket-text");
        productItemBasketPlus.textContent = "+";
        const productItemBasketSVG = document.createElement("div");
        productItemBasketSVG.classList.add("slider__item-basket-img");

        const basketSVG = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "svg"
        );
        basketSVG.setAttribute("width", "20");
        basketSVG.setAttribute("height", "20");
        basketSVG.setAttribute("viewBox", "0 0 20 20");
        basketSVG.setAttribute("fill", "none");
        basketSVG.setAttribute("xmlns", "http://www.w3.org/2000/svg");

        const basketPath = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "path"
        );
        basketPath.setAttribute("fill-rule", "evenodd");
        basketPath.setAttribute("clip-rule", "evenodd");
        basketPath.setAttribute(
            "d",
            "M1 1C1 0.447715 1.44932 0 2.00358 0H3.50894C4.34034 0 5.01431 0.671572 5.01431 1.5V2.06055L17.5883 2.96818C18.4651 3.02278 19.1089 3.81081 18.9846 4.67739L18.1194 10.7121C18.0135 11.4511 17.3783 12 16.6292 12H5.01431V14H15.0572C16.72 14 18.068 15.3431 18.068 17C18.068 18.6569 16.72 20 15.0572 20C13.3945 20 12.0465 18.6569 12.0465 17C12.0465 16.6494 12.1069 16.3128 12.2178 16H6.85015C6.9611 16.3128 7.02147 16.6494 7.02147 17C7.02147 18.6569 5.67352 20 4.01073 20C2.34795 20 1 18.6569 1 17C1 15.6938 1.83779 14.5825 3.00716 14.1707V3.00923C3.00711 3.00372 3.00711 2.99821 3.00716 2.99268V2H2.00358C1.44932 2 1 1.55228 1 1ZM5.01431 4.06445V10H16.194L16.9208 4.93051L5.01431 4.06445ZM14.0537 17C14.0537 16.4477 14.503 16 15.0572 16C15.6115 16 16.0608 16.4477 16.0608 17C16.0608 17.5523 15.6115 18 15.0572 18C14.503 18 14.0537 17.5523 14.0537 17ZM3.00716 17C3.00716 16.4477 3.45647 16 4.01073 16C4.56499 16 5.01431 16.4477 5.01431 17C5.01431 17.5523 4.56499 18 4.01073 18C3.45647 18 3.00716 17.5523 3.00716 17Z"
        );
        basketPath.setAttribute("fill", "#5C5F62");

        basketSVG.appendChild(basketPath);
        productItemBasketSVG.appendChild(basketSVG);
        productItemBasket.appendChild(productItemBasketPlus);
        productItemBasket.appendChild(productItemBasketSVG);
        productItemPriceBasket.appendChild(productItemBasket);

        const productTitle = document.createElement("a");

        productTitle.href = `/details/${product.id}`;
        productTitle.classList.add("products___item-title");
        productTitle.textContent = product.title;

        const productBuyButton = document.createElement("button");
        productBuyButton.type = "button";
        productBuyButton.classList.add("products___item-btn");
        productBuyButton.textContent = "Купить в 1 клик";

        productArticle.appendChild(productImgDiv);
        productArticle.appendChild(productTitle);
        if (productPromotionDiv) {
            productArticle.appendChild(productPromotionDiv);
        }
        if (product.productproperties_set) {
            productArticle.appendChild(productWeight);
        } else {
            productArticle.appendChild(productWeight);
        }
        if (product.promotion_set && product.promotion_set > 0) {
            productArticle.appendChild(productItemPriceBasket);
        } else {
            productArticle.appendChild(productItemPriceBasket);
        }
        productArticle.appendChild(productBuyButton);

        productItem.appendChild(productArticle);
        container.appendChild(productItem);
    });

    const productsPrev = document.createElement("div");
    productsPrev.classList.add("products__prev");
    productsPrev.setAttribute("id", "productsPrev");
    productsPrev.setAttribute("pageData", data.previous_page_number || "");

    const productsPrevImg = document.createElement("div");
    productsPrevImg.classList.add("products__prev-img");
    if (data.previous) {
        const productsPrevImgSvg = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "svg"
        );
        productsPrevImgSvg.setAttribute("width", "16.000000");
        productsPrevImgSvg.setAttribute("height", "16.000000");
        productsPrevImgSvg.setAttribute("viewBox", "0 0 16 16");
        productsPrevImgSvg.setAttribute("fill", "none");
        productsPrevImgSvg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
        productsPrevImgSvg.setAttribute(
            "xmlns:xlink",
            "http://www.w3.org/1999/xlink"
        );

        const productsPrevPath = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "path"
        );
        productsPrevPath.setAttribute("fill-rule", "evenodd");
        productsPrevPath.setAttribute(
            "d",
            "M9.6001 12.7998C9.39502 12.7998 9.19043 12.7214 9.03418 12.5654L5.03418 8.56543C4.72168 8.25269 4.72168 7.74707 5.03418 7.43433L9.03418 3.43433C9.34717 3.12158 9.85303 3.12158 10.1655 3.43433C10.4785 3.74707 10.4785 4.25269 10.1655 4.56543L6.73145 8L10.1655 11.4343C10.4785 11.7471 10.4785 12.2527 10.1655 12.5654C10.0098 12.7214 9.80469 12.7998 9.6001 12.7998Z"
        );
        productsPrevPath.setAttribute("fill", "#00A0AC");
        productsPrevPath.setAttribute("fill-opacity", "1.000000");

        productsPrevImgSvg.appendChild(productsPrevPath);
        productsPrevImg.appendChild(productsPrevImgSvg);

        const previousP = document.createElement("p");
        previousP.textContent = "Предыдущая";
        previousP.onclick = () => {
            fetch(data.previous)
            .then(response => response.json())
            .then(data => {
                renderProducts(data)
            }
        )
        };

        productsPrev.appendChild(productsPrevImg);
        productsPrev.appendChild(previousP);
    }

    const productsPaginationList = document.createElement("ul");
    productsPaginationList.classList.add("products__pagination-list");

    let i = 1;

    do {
        const productsPaginationListItem = document.createElement("li");
        productsPaginationListItem.textContent = `${i}`;

        if (data.current_page == i) {

            productsPaginationListItem.classList.add(
                "products__pagination-list-item"
            );
            productsPaginationListItem.classList.add(
                "products__pagination-list-item-active"
            );
        } else {
            productsPaginationListItem.classList.add(
                "products__pagination-list-item"
            );
            productsPaginationListItem.onclick = () => {
                fetch(`fetchUrl`)
            }
        }

        productsPaginationList.appendChild(productsPaginationListItem);
        i++;
    } while (i <= data.total_pages);

    const productsNext = document.createElement("div");
    productsNext.classList.add("products__next");
    productsNext.setAttribute("id", "productsNext");
    productsNext.setAttribute("pageData", data.next_page_number || "");

    const productsNextImg = document.createElement("div");
    productsPrevImg.classList.add("products__prev-img");
    if (data.next) {
        const productsNextImgSvg = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "svg"
        );
        productsNextImgSvg.setAttribute("width", "16.000000");
        productsNextImgSvg.setAttribute("height", "16.000000");
        productsNextImgSvg.setAttribute("viewBox", "0 0 16 16");
        productsNextImgSvg.setAttribute("fill", "none");
        productsNextImgSvg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
        productsNextImgSvg.setAttribute(
            "xmlns:xlink",
            "http://www.w3.org/1999/xlink"
        );

        const productsNextPath = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "path"
        );
        productsNextPath.setAttribute("fill-rule", "evenodd");
        productsNextPath.setAttribute(
            "d",
            "M6.3999 12.7998C6.19482 12.7998 5.99023 12.7214 5.83398 12.5654C5.52148 12.2527 5.52148 11.7471 5.83398 11.4343L9.26855 8L5.83398 4.56543C5.52148 4.25269 5.52148 3.74707 5.83398 3.43433C6.14697 3.12158 6.65283 3.12158 6.96533 3.43433L10.9653 7.43433C11.2783 7.74707 11.2783 8.25269 10.9653 8.56543L6.96533 12.5654C6.80957 12.7214 6.60449 12.7998 6.3999 12.7998Z"
        );
        productsNextPath.setAttribute("fill", "#00A0AC");
        productsNextPath.setAttribute("fill-opacity", "1.000000");

        productsNextImgSvg.appendChild(productsNextPath);
        productsNextImg.appendChild(productsNextImgSvg);

        const nextP = document.createElement("p");
        nextP.textContent = "Следующая";
        nextP.onclick = () => {
            fetch(data.next)
            .then(response => response.json())
            .then(data => {
                renderProducts(data)
            }
        )
        }

        productsNext.appendChild(nextP);
        productsNext.appendChild(productsNextImgSvg);
    }

    paginationContainer.appendChild(productsPrev);
    paginationContainer.appendChild(productsPaginationList);
    paginationContainer.appendChild(productsNext);
}
