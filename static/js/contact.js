const { createApp, onMounted } = Vue;

function getInputValue(field = "") {
  return document.querySelector(`input#${field}`)?.value || "";
}

const fields = {
  name: getInputValue("name"),
  email: getInputValue("email"),
  subject: getInputValue("subject"),
  message: getInputValue("message"),
};

createApp({
  delimiters: ["[[", "]]"],
  data() {
    return {
      fields,
      modal: {
        menu: false,
        logout: false,
        email: email_modal,
      },
    };
  },
  methods: {
    openModal(name = "") {
      this.modal[name] = true;
    },
    closeModal(name = "") {
      this.modal[name] = false;
    },
    active(field = "") {
      return { active: this.fields[field] != "" };
    },
    openLogout() {
      this.closeModal("menu");
      this.modal.logout = true;
    },
    closeLogout() {
      this.modal.logout = false;
    },
  },
}).mount("#app");
