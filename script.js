// Инициализация переменных
let coins = 0;
let clicks = 0;

// Получаем элементы DOM
const coin = document.getElementById('coin');
const balanceElement = document.getElementById('balance');
const counterElement = document.getElementById('counter');

// Загружаем сохранённые данные
function loadData() {
    const savedCoins = localStorage.getItem('coins');
    const savedClicks = localStorage.getItem('clicks');
    
    if (savedCoins) coins = parseInt(savedCoins);
    if (savedClicks) clicks = parseInt(savedClicks);
    
    updateDisplay();
}

// Сохраняем данные
function saveData() {
    localStorage.setItem('coins', coins);
    localStorage.setItem('clicks', clicks);
}

// Обновляем отображение
function updateDisplay() {
    balanceElement.textContent = Баланс: ${coins} ${getCoinWord(coins)};
    counterElement.textContent = clicks;
}

// Склонение слова "монета"
function getCoinWord(num) {
    if (num % 100 >= 11 && num % 100 <= 19) return 'монет';
    
    switch(num % 10) {
        case 1: return 'монета';
        case 2:
        case 3:
        case 4: return 'монеты';
        default: return 'монет';
    }
}

// Анимация "+1"
function createPlusOne(x, y) {
    const plusOne = document.createElement('div');
    plusOne.className = 'plus-one';
    plusOne.textContent = '+1';
    plusOne.style.left = ${x}px;
    plusOne.style.top = ${y}px;
    document.body.appendChild(plusOne);
    
    setTimeout(() => plusOne.remove(), 1000);
}

// Обработчик клика
coin.addEventListener('click', function(e) {
    coins++;
    clicks++;
    saveData();
    updateDisplay();
    
    // Анимация нажатия
    this.style.transform = 'scale(0.95)';
    setTimeout(() => this.style.transform = 'scale(1)', 100);
    
    // Эффект "+1"
    createPlusOne(e.clientX, e.clientY);
});

// Инициализация
loadData();
