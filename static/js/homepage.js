const { createApp } = Vue

createApp({
    delimiters: ["[[", "]]"],
    data() {
        return { 
            modal: {
                menu: false
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
    },
}).mount('#app')