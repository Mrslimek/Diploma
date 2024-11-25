const sliderItemBasketBtn = document.querySelectorAll('.slider__item-basket');
const headerBottomBasketCount = document.querySelector('.header__bottom-basket > p')



let count = 0;
headerBottomBasketCount.textContent = count

sliderItemBasketBtn.forEach(item => {
    item.addEventListener('click', () => {
        count++
        headerBottomBasketCount.textContent = count
    })
})