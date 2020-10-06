
let cour = 0

function fetchData() {
    $.ajax({
        url: `?id=${$('.latest_req').text()}`,
        type: 'get',
        success: function (response) {
            console.log(response);
            if (response['data'] === null) {
                return
            }
            $('.latest_req').text(response['latest_request_id']);
            updatePage(response['requests'])
            if (cour + response['requests'].length >= 10) {
                document.title = `(${10}) Requests`
            } else {
                cour += response['requests'].length
                document.title = `(${cour}) Requests`
            }
        }
    });
}

function updatePage(requests) {
    for (const request of requests) {
        let requestCard = `
            <div class="card text-white bg-dark mb-3" style="margin-top: 10px">
                <div class="card-header">
                    Method: ${request['method']},
                    <form action="edit-priority/" method="post">
                      <label for="priority">Priority:</label>
                      <input id="priority" type="number" name="priority" value="${request['priority']}">
                      <input type="hidden" name="id" value="${request['id']}">
                      <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">
                      <input type="submit" value="change">
                    </form>
                </div>
                <div class="card-body">
                    <h5 class="card-title">URL: ${request['url']}</h5>
                    <p class="card-text">Content type: ${request['content_type']},
                        User: ${request['user']}, Encoding: ${request['encoding']}
                    </p>
                    <p class="timestamp">Timestamp: ${strftime('%b. %e, %Y, %l:%M %P.', request['timestamp'])}</p>
                </div>
            </div>`
        $('.col-sm').prepend(requestCard);
        $('.col-sm').children().last().remove();
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {
    setInterval(fetchData, 2000)
    window.onmousemove = function () {
        cour = 0
        document.title = 'Requests'
    }
})

