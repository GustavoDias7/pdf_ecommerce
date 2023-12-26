const { createApp, onMounted } = Vue

function getInputValue(field = "") {
    return document.querySelector(`input#${field}`)?.value || ""
}

const fields = {
    username: getInputValue("username"),
    email: getInputValue("email"),
    password: getInputValue("password"),
    confirm_password: getInputValue("confirm_password"),
}

createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            fields,
            modal: {
                menu: false,
                logout: false
            },
            passwords: {
                main: false,
                confirm: false
            } 
        }
    },
    methods: {
        togglePassword(name = "") {
            this.passwords[name] = !this.passwords[name]
        },
        openModal(name = "") {
            this.modal[name] = true
        },
        closeModal(name = "") {
            this.modal[name] = false
        },
        active(field = "") {
            return {active: this.fields[field] != ""}
        },
        openLogout() {
            this.closeModal("menu")
            this.modal.logout = true
        },
        closeLogout() {
            this.modal.logout = false
        }
    },
}).mount('#app')