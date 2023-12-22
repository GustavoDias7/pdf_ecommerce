const { createApp } = Vue

createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            fields: {
                username: "",
                email: "",
                password: "",
                confirm_password: "",
            },
            modal: {
                menu: false
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
        }
    },
}).mount('#app')