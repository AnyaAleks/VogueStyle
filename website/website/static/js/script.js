document.addEventListener('DOMContentLoaded', function () {
    // Add smooth scrolling for anchor links
    const anchors = document.querySelectorAll('a[href^="#"]');
    for (let anchor of anchors) {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    }

    // HOVER effect for service cards :)
    const serviceCards = document.querySelectorAll('.service-card');
    for (let card of serviceCards) {
        card.addEventListener('mouseenter', function () {
            this.style.backgroundColor = '#f8f2ff';
        });
        card.addEventListener('mouseleave', function () {
            this.style.backgroundColor = '#fff';
            // This is to keep featured cards highlighted
            if (this.classList.contains('featured')) {
                this.style.backgroundColor = '#f8f2ff';
            }
        });
    }

    // Fetch services from the API and display them
    fetchServices();

    // Add event listener for the "Sort by Price" button
    const sortByPriceButton = document.getElementById('sort-by-price');
    if (sortByPriceButton) {
        sortByPriceButton.addEventListener('click', function () {
            fetchServicesSortedByPrice();
        });
    }


    // Обработчик загрузки фото
    const photoUpload = document.getElementById('photo-upload');
    if (photoUpload) {
        photoUpload.addEventListener('change', function(e) {
            handlePhotoUpload(e);
        });
    }

    // Обработчик удаления фото
    const deletePhoto = document.getElementById('delete-photo');
    if (deletePhoto) {
        deletePhoto.addEventListener('click', function() {
            handlePhotoDelete();
        });
    }
});


function handlePhotoUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    // Проверка типа файла
    if (!file.type.match('image.*')) {
        alert('Пожалуйста, выберите файл изображения');
        return;
    }

    // Проверка размера файла (например, не более 2MB)
    if (file.size > 2 * 1024 * 1024) {
        alert('Размер файла не должен превышать 2MB');
        return;
    }

    // Создаем превью изображения
    const reader = new FileReader();
    reader.onload = function(e) {
        const previewContainer = document.getElementById('photo-preview');

        // Если это div-плейсхолдер, заменяем его на img
        if (previewContainer.tagName === 'DIV') {
            const img = document.createElement('img');
            img.id = 'photo-preview';
            img.className = 'lk-photo';
            img.src = e.target.result;
            img.alt = 'Фото мастера';

            previewContainer.parentNode.replaceChild(img, previewContainer);
        } else {
            // Если это уже img, просто обновляем src
            previewContainer.src = e.target.result;
        }
    };

    reader.readAsDataURL(file);
}

function handlePhotoDelete() {
    const previewContainer = document.getElementById('photo-preview');

    // Если это img, заменяем его на плейсхолдер
    if (previewContainer.tagName === 'IMG') {
        const placeholder = document.createElement('div');
        placeholder.id = 'photo-preview';
        placeholder.className = 'lk-photo-placeholder';
        placeholder.innerHTML = '<span>Фото не загружено</span>';

        previewContainer.parentNode.replaceChild(placeholder, previewContainer);
    }

    // Сбрасываем значение input file
    const photoUpload = document.getElementById('photo-upload');
    if (photoUpload) {
        photoUpload.value = '';
    }
}

// Function to fetch all services from the API
async function fetchServices() {
    console.error("Start fetch")
    try {
        const response = await fetch('/api/v1/resources/services/all');
        const services = await response.json();

        const servicesContainer = document.getElementById('services');
        if (servicesContainer) {
            servicesContainer.innerHTML = ''; // Clear previous content

            // Loop through the services and create HTML elements
            services.forEach(service => {
                const serviceCard = document.createElement('div');
                serviceCard.className = 'service-card';
                serviceCard.innerHTML = `
                    <h3>${service.name}</h3>
                    <p class="price">Price: $${service.price}</p>
                     <button onclick="showPopUpForRequest()" class="btn">Записаться</button>
                     //onclick=showPopUpForRequest() onclick="showPopUpForRequest();"
//                    <button onclick="bookService('${service.name}')" class="btn">Записаться</button>
                `;
                servicesContainer.appendChild(serviceCard);
            });
        }
    } catch (error) {
        console.error('Error fetching services:', error);
    }
}

// Function to fetch services sorted by price
async function fetchServicesSortedByPrice() {
    try {
        const response = await fetch('/api/v1/resources/prices/sort');
        const services = await response.json();

        const servicesContainer = document.getElementById('services');
        if (servicesContainer) {
            servicesContainer.innerHTML = ''; // Clear previous content

            // Loop through the sorted services and create HTML elements
            services.forEach(service => {
                const serviceCard = document.createElement('div');
                serviceCard.className = 'service-card';
                serviceCard.innerHTML = `
                    <h3>${service.service}</h3>
                    <p class="price">Price: $${service.price}</p>
                    <button onclick="bookService('${service.service}')" class="btn">Записаться</button>
                `;
                servicesContainer.appendChild(serviceCard);
            });
        }
    } catch (error) {
        console.error('Error sorting services:', error);
    }
}
function toggleDetails(masterId) {
    const details = document.getElementById(`details-${masterId}`);
    const button = document.querySelector(`#details-${masterId}`).nextElementSibling;

    details.classList.toggle('expanded');
    button.classList.toggle('active');

    if (details.classList.contains('expanded')) {
        button.querySelector('.btn-text').textContent = 'СВЕРНУТЬ';
    } else {
        button.querySelector('.btn-text').textContent = 'ЧИТАТЬ ПОДРОБНЕЕ';
    }
}

const carousel = document.querySelector('.carousel');
const items = document.querySelectorAll('.carousel-item');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const indicators = document.querySelectorAll('.indicator');

let currentIndex = 0;

function updateCarousel() {
    carousel.style.transform = `translateX(-${currentIndex * 100}%)`;

    indicators.forEach((indicator, index) => {
        indicator.classList.toggle('active', index === currentIndex);
    });
}

prevBtn.addEventListener('click', () => {
    currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
    updateCarousel();
});

nextBtn.addEventListener('click', () => {
    currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
    updateCarousel();
});

indicators.forEach((indicator, index) => {
    indicator.addEventListener('click', () => {
        currentIndex = index;
        updateCarousel();
    });
});

// Обновите вызов в fetchServices
async function fetchServices() {
    console.error("Start fetch")
    try {
        const response = await fetch('/api/v1/resources/services/all');
        const services = await response.json();

        const servicesContainer = document.getElementById('services');
        if (servicesContainer) {
            servicesContainer.innerHTML = ''; // Clear previous content

            // Loop through the services and create HTML elements
            services.forEach(service => {
                const serviceCard = document.createElement('div');
                serviceCard.className = 'service-card';
                serviceCard.innerHTML = `
                    <h3>${service.name}</h3>
                    <p class="price">Price: $${service.price}</p>
                    <button onclick="showPopUpForRequest('${service.name}', ${service.price})" class="btn">Записаться</button>
                `;
                servicesContainer.appendChild(serviceCard);
            });
        }
    } catch (error) {
        console.error('Error fetching services:', error);
    }
}



// Автопрокрутка (по желанию)
// setInterval(() => {
//     currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
//     updateCarousel();
// }, 3000);

// Function to book a service
function bookService(serviceName) {
    alert(`Вы выбрали: ${serviceName}\nЦена: ${price} ₽\nФункция записи будет реализована позже`);
    // Отправка на сервер:
    /*
    fetch('/api/bookings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            service: serviceName,
            date: new Date().toISOString()
        })
    })
    .then(response => response.json())
    .then(data => {
        alert('Бронирование подтверждено!');
    })
    .catch(error => {
        console.error('Ошибка бронирования:', error);
        alert('Произошла ошибка при бронировании');
    });
    */
}

//document.getElementById('delete-photo').addEventListener('click', function() {
//    if (confirm('Удалить фото?')) {
//        fetch('/delete-photo/', {
//            method: 'POST',
//            headers: {
//                'X-CSRFToken': '{{ csrf_token }}',
//                'Content-Type': 'application/json',
//            },
//            body: JSON.stringify({master_id: {{ master.id }}})
//        })
//        .then(response => location.reload())
//    }
//});
//
//document.getElementById('photo-upload').addEventListener('change', function(e) {
//    if (e.target.files.length > 0) {
//        document.querySelector('.lk-form').submit();
//    }
//});

//dialog window--------------------------------------
//function showPopUpForRequest(serviceName, servicePrice) {
//    const popUpElement = document.getElementById("pop-up");
//
//    if (!popUpElement) {
//        console.error("Dialog element not found");
//        return;
//    }
//
//    // Устанавливаем информацию об услуге
//    const nameElement = document.getElementById("popup-service-name");
//    const priceElement = document.getElementById("popup-service-price");
//
//    if (nameElement) nameElement.textContent = serviceName;
//    if (priceElement) priceElement.textContent = servicePrice;
//
//    // Показываем диалоговое окно (лучше использовать showModal())
//    popUpElement.showModal();
//}


// Показ диалога с первой страницей
function showDialog(serviceName, servicePrice) {
    const dialog = document.getElementById('pop-up');
    showFirstPage(serviceName, servicePrice);
    dialog.showModal();
}

function showFirstPage(serviceName, servicePrice) {
    const content = document.getElementById('dialog-content');
    content.innerHTML = `
        <div class="popup-content">
            <h3>Запись на услугу</h3>
            <p>Услуга: <span>${serviceName}</span></p>
            <p>Цена: <span>${servicePrice}</span> ₽</p>
            <div class="popup-buttons">
                <button onclick="showSecondPage('${serviceName}', '${servicePrice}')">Записаться</button>
                <button onclick="document.getElementById('pop-up').close()">Закрыть</button>
            </div>
        </div>
    `;
}

function showSecondPage(serviceName, servicePrice) {
    const content = document.getElementById('dialog-content');
    content.innerHTML = `
        <div class="dialog-container">
            <h3 class="dialog-title">Выберите адрес для услуги: <span>${serviceName}</span></h3>
            <p class="service-price-info">Стоимость: <span>${servicePrice}</span> ₽</p>
            <div class="location-list">
                <div class="location" onclick="handleLocationSelect(this, '${serviceName}', ${servicePrice}, 'Центр города')">
                    <div class="location-name">Салон VogueStyle в Центре города</div>
                    <div class="location-address">ул. Большая Морская 67, Санкт-Петербург</div>
                </div>

                <div class="location" onclick="handleLocationSelect(this, '${serviceName}', ${servicePrice}, 'Московская')">
                    <div class="location-name">Салон VogueStyle на Московской</div>
                    <div class="location-address">Гастелло ул. 15, Санкт-Петербург</div>
                </div>

                <div class="location" onclick="handleLocationSelect(this, '${serviceName}', ${servicePrice}, 'Ленсовета')">
                    <div class="location-name">Салон VogueStyle на Ленсовета</div>
                    <div class="location-address">Ленсовета ул. 14, Санкт-Петербург</div>
                </div>
            </div>
            <div class="popup-buttons">
                <button onclick="showFirstPage('${serviceName}', ${servicePrice})">Назад</button>
            </div>
        </div>
    `;
}

function handleLocationSelect(element, serviceName, servicePrice, locationName) {
    // Удаляем класс selected у всех элементов
    document.querySelectorAll('.location').forEach(loc => {
        loc.classList.remove('selected');
    });

    // Добавляем класс selected к выбранному элементу
    element.classList.add('selected');

    // Сразу переходим на третью страницу с выбранным адресом
    showThirdPage(serviceName, servicePrice, locationName);
}



function showThirdPage(serviceName, servicePrice, locationName) {
    const content = document.getElementById('dialog-content');
    content.innerHTML = `
        <div class="popup-content">
            <h3 class="dialog-title">Выберите услугу: <span id="selected-service-name"></span></h3>
            <div class="service-list-js" id="services-container">
                <!-- Услуги будут добавлены динамически -->
            </div>
            <div class="popup-buttons">
                <button onclick="showSecondPage('${serviceName}', ${servicePrice})">Назад</button>
            </div>
        </div>
    `;

    // Загрузка и отображение услуг
    loadServicesData();
}

function loadServicesData() {
    // Используем предзагруженные данные или делаем запрос
    if (window.servicesData && Array.isArray(window.servicesData)) {
        renderServices(window.servicesData);
    } else {
        console.error('Ошибка: Некорректные данные услуг', window.servicesData);
        document.getElementById('services-container').innerHTML =
            '<div class="error">Не удалось загрузить данные услуг</div>';
    }
}

function renderServices(services) {
    const container = document.getElementById('services-container');
    container.innerHTML = '';

    services.forEach(service => {
        const serviceElement = document.createElement('div');
        serviceElement.className = 'service-js';
        serviceElement.dataset.id = service.id;

        serviceElement.innerHTML = `
            <div class="service-info-js">
                <div class="service-name-js">${service.name}</div>
                <div class="service-price-js">${service.price} rub.</div>
            </div>
        `;

        serviceElement.onclick = () => handleServiceSelect(serviceElement, service.id, service.name, service.price);
        container.appendChild(serviceElement);
    });
}

function handleServiceSelect(element, serviceId, serviceName, servicePrice) {
    // Снимаем выделение со всех услуг
    document.querySelectorAll('.service-js').forEach(s => {
        s.classList.remove('selected');
    });

    // Добавляем выделение выбранной услуге
    element.classList.add('selected');

    // Переходим на следующую страницу с выбранной услугой
    showFourthPagePage(serviceName, servicePrice, serviceId);
}

function showFourthPage(serviceName, servicePrice, locationName) {
    const content = document.getElementById('dialog-content');
    content.innerHTML = `
        <div class="popup-content">
            <h3 class="dialog-title">Выберите мастера: <span id="selected-service-name">${serviceName}</span></h3>
            <p class="service-info">Локация: ${locationName} | Стоимость: ${servicePrice} ₽</p>
            <div class="master-list-js" id="masters-container">
                <!-- Мастера будут добавлены динамически -->
            </div>
            <div class="popup-buttons">
                <button onclick="showThirdPage('${serviceName}', ${servicePrice})">Назад</button>
            </div>
        </div>
    `;

    // Загружаем данные мастеров
    loadMastersData(serviceName, servicePrice, locationName);
}

function loadMastersData(serviceName, servicePrice, locationName) {
    // Здесь должна быть логика загрузки данных мастеров!!!!!!!!

    // Пример с предзагруженными данными:
    if (window.mastersData && Array.isArray(window.mastersData)) {
        renderMasters(window.mastersData, serviceName, servicePrice, locationName);
    } else {
        console.error('Данные мастеров не загружены');
        document.getElementById('masters-container').innerHTML =
            '<div class="error">Не удалось загрузить данные мастеров</div>';
    }
}

function renderMasters(masters, serviceName, servicePrice, locationName) {
    const container = document.getElementById('masters-container');
    container.innerHTML = '';

    masters.forEach(master => {
        const masterElement = document.createElement('div');
        masterElement.className = 'master-js';
        masterElement.dataset.id = master.id;

        // Проверяем наличие фото
        const photoUrl = master.photo ? `https://ania.cleverlive.pro/VogueStyle_MastersPhoto/${master.photo}` : null;
        const initials = master.name.split(' ').map(n => n[0]).join('').toUpperCase();

        masterElement.innerHTML = `
            <div class="master-photo-js" style="${photoUrl ? `background-image: url('${photoUrl}')` : ''}">
                ${!photoUrl ? initials : ''}
            </div>
            <div class="master-info-js">
                <div class="master-name-js">${master.name}</div>
                <div class="master-position-js">${master.job}</div>
            </div>
        `;

        // Обработка ошибки загрузки фото
        const photoEl = masterElement.querySelector('.master-photo-js');
        if (photoUrl) {
            photoEl.onerror = function() {
                this.style.backgroundImage = 'none';
                this.textContent = initials;
            };
        }

        masterElement.onclick = () => handleMasterSelect(masterElement, master.id, serviceName, servicePrice, locationName);
        container.appendChild(masterElement);
    });
}

function handleMasterSelect(element, masterId, serviceName, servicePrice, locationName) {
    // Удаляем класс selected у всех элементов
    document.querySelectorAll('.master-js').forEach(m => {
        m.classList.remove('selected');
    });

    // Добавляем класс selected к выбранному элементу
    element.classList.add('selected');

    // Переходим на следующую страницу с выбранным мастером
    showFifthPage(serviceName, servicePrice, locationName, masterId);
}

function showFifthPage(serviceName, servicePrice, locationName, masterId) {
    const content = document.getElementById('dialog-content');
    content.innerHTML = `
        <div class="popup-content">
            <h3>Подтверждение записи</h3>
            <p>Услуга: ${serviceName}</p>
            <p>Цена: ${servicePrice} ₽</p>
            <p>Адрес: ${location}</p>

            <div class="form-group">
                <label>Выберите дату:</label>
                <input type="date" class="popup-input" id="appointment-date">
            </div>
            <div class="form-group">
                <label>Выберите время:</label>
                <input type="time" class="popup-input" id="appointment-time">
            </div>

            <div class="popup-buttons">
                <button onclick="confirmAppointment('${serviceName}', ${servicePrice}, '${location}')">Подтвердить</button>
                <button onclick="showFourthPage('${serviceName}', ${servicePrice})">Назад</button>
            </div>
        </div>
    `;
}


//Для обработки всех данных из записи на услугу
function confirmAppointment(serviceName, servicePrice, location) {
    const date = document.getElementById('appointment-date').value;
    const time = document.getElementById('appointment-time').value;

    if (!date || !time) {
        alert("Пожалуйста, выберите дату и время!");
        return;
    }

    alert(`Запись подтверждена!\nУслуга: ${serviceName}\nЦена: ${servicePrice} ₽\nАдрес: ${location}\nДата: ${date}\nВремя: ${time}`);
    document.getElementById('pop-up').close();
}


//Для обработки всех данных из ЛК мастера
document.querySelector('save-information').addEventListener('click', function(e) {
    e.preventDefault();

    const form = document.querySelector('.lk-form');
    const formData = new FormData(form);

    let output = "Данные мастера:\n\n";
    const fieldLabels = {
        'last_name': 'Фамилия',
        'first_name': 'Имя',
        'middle_name': 'Отчество',
        'birth_date': 'Дата рождения',
        'address': 'Адрес',
        'email': 'E-mail',
        'phone': 'Телефон',
        'photo': 'Фото'
    };

    for (let [key, value] of formData.entries()) {
        if (key === 'photo' && value instanceof File) {
            output += `${fieldLabels[key] || key}: ${value.name || 'файл выбран'}\n`;
        } else {
            output += `${fieldLabels[key] || key}: ${value || 'не указано'}\n`;
        }
    }

    alert(output);
    // form.submit(); // Раскомментировать для реальной отправки
});