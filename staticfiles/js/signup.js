const { createApp, onMounted } = Vue;

function getInputValues(fields = []) {
  const obj = {};
  fields.forEach((f) => {
    obj[f] = document.querySelector(`input#${f}`)?.value || "";
  });
  return obj;
}

const fields = getInputValues([
  "first_name",
  "last_name",
  "email",
  "password",
  "confirm_password",
]);

createApp({
  delimiters: ["[[", "]]"],
  data() {
    return {
      fields,
      modal: {
        menu: false,
        logout: false,
      },
      passwords: {
        main: false,
        confirm: false,
      },
    };
  },
  methods: {
    togglePassword(name = "") {
      this.passwords[name] = !this.passwords[name];
    },
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
