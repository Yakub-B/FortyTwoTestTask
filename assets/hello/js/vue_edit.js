let app = new Vue ({
    delimiters: ["[[", "]]"],
    el: '#app',
    data: {
        name: document.querySelector("input[id=id_name]").value,
        last_name: document.querySelector("input[id=id_last_name]").value,
        email: document.querySelector("input[id=id_email]").value,
        birthday_date: document.querySelector("input[id=id_birthday_date]").value,
        jabber: document.querySelector("input[id=id_jabber]").value,
        skype: document.querySelector("input[id=id_skype]").value,
        bio: document.querySelector("TextArea[id=id_bio]").textContent,
        other_contacts: document.querySelector("TextArea[id=id_other_contacts]").textContent,
        csrfmiddlewaretoken: document.querySelector("input[name=csrfmiddlewaretoken]").value,
        success: false,
        errors: [],
        fieldsDisable: false
    },
    methods: {
        processForm(e) {
            let vm = this;
            vm.fieldsDisable = true;
            vm.errors = [];
            vm.success = false
            e.preventDefault();
            let form_data = new FormData();
            data = {
                name: vm.name,
                last_name: vm.last_name,
                email: vm.email,
                birthday_date: vm.birthday_date,
                jabber: vm.jabber,
                skype: vm.skype,
                bio: vm.bio,
                other_contacts: vm.other_contacts,
                csrfmiddlewaretoken: vm.csrfmiddlewaretoken,
            }
            for (const key in data) {
                form_data.append(key, data[key])
            }
            axios.defaults.xsrfCookieName = 'csrftoken'
            axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
            axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
            axios({
                method: 'post',
                url: '',
                data: form_data
            }).then(response => {
                vm.success = response.data['success'];
                for (const field in response.data['errors']) {
                    vm.errors.push({field: field, error: response.data['errors'][field][0]})
                }
            }, error => {
                console.log(error);
            }).finally(() => {
                vm.fieldsDisable = false;
            })
        },
    }
})