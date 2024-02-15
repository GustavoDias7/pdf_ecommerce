const { createApp } = Vue

createApp({
    delimiters: ["[[", "]]"],
    data() {
        return { 
            modal: {
                menu: false,
                logout: false
            } 
        }
    },
    methods: {
        openModal(name = "") {
            this.modal[name] = true
        },
        closeModal(name = "") {
            this.modal[name] = false
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