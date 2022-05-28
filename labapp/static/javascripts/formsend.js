/*
Реализация AJAX с помощью асинхронного метода fetch. Современный вариант реализации AJAX.
*/

var sendbtn = document.getElementById("sendbtnkurs");    // выбираем DOM-елемент (кнопку)

// Привязываем к элементу обработчик события "click"
sendbtn.addEventListener("click", function (e) {
    /* Инструкция preventDefault позволяет переопределить стандартное поведение браузера,
    если ее убрать, то браузер по-умолчанию обновит страницу после отправки данных формы */
    e.preventDefault();
    // Получаем данные полей формы
    let fname = document.getElementsByName("fname")[0].value;
    let lname = document.getElementsByName("lname")[0].value;
    let email = document.getElementsByName("email")[0].value;
    // Преобразуем полученные данные в JSON
    var formdata = JSON.stringify({ firstname: fname, lastname: lname,email: email});
    
    // Отправляем запрос через fetch (необходимо выставить соответствующий заголовок (headers)!)
    fetch("/api/contactrequest",
    {
        method: "POST",
        body: formdata,
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then( response => {
        // fetch в случае успешной отправки возвращает Promise, содержащий response объект (ответ на запрос)
        // Возвращаем json-объект из response и получаем данные из поля message
        response.json().then(function(data) {
            console.log(data)
            //let statfield = document.getElementById("statusfield");
            //statfield.textContent = data.message;
            //statfield.textContent.bold();
            alert(data.message);
        });
    })
    .catch( error => {
        alert(error);
        console.error('error:', error);
    });

});

var getbtn = document.getElementById("get");



getbtn.addEventListener("click", function (e) {
    fetch("/apii/contactrequest",
        {
            method: "GET",
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(request => {
            request.json().then(function (data) {
                let contactrequests = data['contactrequests'];
                var pages = document.getElementById("statusfield");
                pages.textContent = "";

                for (let ownerId in contactrequests) {
                    pages.innerHTML += `
                    <div class="requestss">
                    <p>` + contactrequests[ownerId]['firstname'] + " " + "("+ contactrequests[ownerId]['createdAt'] + ")" + `</p>
                    </div>
                `;

                };
            });
        })
        .catch(error => {
            alert(error);
            console.error('error:', error);
        });

});
