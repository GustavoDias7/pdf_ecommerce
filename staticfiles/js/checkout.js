const { createApp } = Vue;

const { Mask, MaskInput, vMaska } = Maska;
new MaskInput("[data-maska]");
const mask = new Mask({ mask: "#-#" });

const app = createApp({
  delimiters: ["[[", "]]"],
  data() {
    return {
      payment_format: defaultPaymentFormat,
      fields: {
        card_number: "4556 0303 9617 9514",
        card_name: "Fulano da Silva",
        expiry: "02/2024",
        cvv: 123,
        installments: 1,
        cpf: "255.644.170-46",
      },
    };
  },
  methods: {
    active(field = "") {
      return { active: this.fields[field] != "" };
    },
    showPayment(format = "") {
      return format === this.payment_format;
    },
  },
});

app.directive("maska", vMaska);
app.mount("#app");
